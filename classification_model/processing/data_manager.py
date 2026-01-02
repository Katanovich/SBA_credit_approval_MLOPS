import logging
from pathlib import Path
from typing import Any, List, Optional

import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from classification_model import __version__ as _version
from classification_model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config

logger = logging.getLogger(__name__)


def group_by_first2_numeric(df, col):
    first2 = df[col].astype("Int64").astype(str).str.lstrip("-").str[:2].astype("Int64")

    def mapper(x):
        if pd.isna(x):
            return 81
        if x in {11, 21, 22, 23, 42, 51, 52, 53, 54, 55, 56, 61, 62, 71, 72, 92}:
            return int(x)
        if 31 <= x <= 33:
            return 33
        if 44 <= x <= 45:
            return 45
        if 48 <= x <= 49:
            return 49
        return 81

    df[col] = first2.map(mapper)
    return df


def make_target(
    df: pd.DataFrame,
    source_col: str = "MIS_Status",
    target_col: str = "target",
    positive_class: str = "CHGOFF",
) -> pd.DataFrame:
    df = df.copy()
    df[source_col] = df[source_col].astype(str).str.upper().str.strip()
    df[target_col] = (df[source_col] == positive_class).astype(int)
    return df


def clean_revlinecr(
    df: pd.DataFrame,
    col: str = "RevLineCr",
    valid_values: tuple = ("N", "Y"),
    drop_invalid: bool = True,
) -> pd.DataFrame:
    df = df.copy()
    mapping = {"0": "N", "N": "N", "1": "Y", "T": "Y", "Y": "Y"}
    df[col] = df[col].astype(str).str.upper().str.strip().map(mapping)
    if drop_invalid:
        df = df[df[col].isin(valid_values)]
    return df


def add_city_risk_group(
        df: pd.DataFrame,
        city_col: str = "City",
        target_col: str = "target",
        min_loans: int = 50,
        n_groups: int = 3,
        labels: Optional[List[Any]] = None,
) -> pd.DataFrame:
    if labels is None:
        labels = ["LOW_RISK", "MEDIUM_RISK", "HIGH_RISK"]

    df = df.copy()

    # ЕСЛИ МЫ В API: нет колонки City или нет колонки target (которую создает make_target)
    if city_col not in df.columns or target_col not in df.columns:
        if "CityRiskGroup" not in df.columns:
            df["CityRiskGroup"] = "MEDIUM_RISK"  # Ставим средний риск для новых данных
        return df

    # Логика для ОБУЧЕНИЯ (сработает только если есть таргет и город)
    try:
        city_stats = (
            df.groupby(city_col)
            .agg(TotalLoans=(target_col, "count"), DefaultRate=(target_col, "mean"))
            .reset_index()
        )
        city_stats = city_stats[city_stats["TotalLoans"] >= min_loans]

        if not city_stats.empty:
            city_stats["CityRiskGroup"] = pd.qcut(
                city_stats["DefaultRate"], q=n_groups, labels=labels
            )
            df = df.merge(city_stats[[city_col, "CityRiskGroup"]], on=city_col, how="left")

        # Заполняем пустоты после merge для API
        df["CityRiskGroup"] = df["CityRiskGroup"].fillna("MEDIUM_RISK")
    except Exception:
        df["CityRiskGroup"] = "MEDIUM_RISK"

    return df


def add_sba_ratio(
    df: pd.DataFrame,
    sba_col: str = "SBA_Appv",
    gr_col: str = "GrAppv",
    ratio_col: str = "SBA_ratio",
) -> pd.DataFrame:
    df = df.copy()
    df[ratio_col] = df[sba_col] / df[gr_col]
    df[ratio_col] = df[ratio_col].replace([np.inf, -np.inf], np.nan)
    return df


def clean_currency(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for col in columns:
        if col in df.columns:
            df[col] = df[col].replace(r"[\$,\s]", "", regex=True)
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def pre_pipeline_preparation(*, dataframe: pd.DataFrame) -> pd.DataFrame:
    data = dataframe.copy()

    # ПРОВЕРКА: Делаем таргет только если есть MIS_Status
    if "MIS_Status" in data.columns:
        data = make_target(data)
    else:
        # Создаем временный таргет для API, чтобы add_city_risk_group не падал
        data["target"] = np.nan

    data = group_by_first2_numeric(data, "NAICS")

    # Безопасная фильтрация NewExist
    if "NewExist" in data.columns:
        data = data.loc[data["NewExist"] != 0.0]
        data["NewExist"] = data["NewExist"].astype("Int64")

    data = add_city_risk_group(data)

    cols_to_clean = ["GrAppv", "SBA_Appv"]
    data = clean_currency(data, cols_to_clean)
    data = add_sba_ratio(data)

    # Удаляем лишние поля, ошибки игнорируем (т.к. target/MIS_Status может не быть)
    data.drop(
        labels=config.model_config.unused_fields, axis=1, errors="ignore", inplace=True
    )

    # Удаляем временный таргет, если он был создан для API
    if "target" in data.columns:
        data.drop(columns=["target"], inplace=True)

    return data


def _load_raw_dataset(*, file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(
        Path(f"{DATASET_DIR}/{file_name}"), low_memory=False  # Добавь это здесь
    )
    return dataframe


def load_dataset(*, file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"), low_memory=False)
    transformed = pre_pipeline_preparation(dataframe=dataframe)
    return transformed


def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name
    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)


def load_pipeline(*, file_name: str) -> Pipeline:
    file_path = TRAINED_MODEL_DIR / file_name
    return joblib.load(filename=file_path)


def remove_old_pipelines(*, files_to_keep: List[str]) -> None:
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()
