import logging
from pathlib import Path
from typing import List

import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from classification_model import __version__ as _version
from classification_model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config

logger = logging.getLogger(__name__)

# --- Вспомогательные функции (обязательно должны быть в файле) ---


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
    df, source_col="MIS_Status", target_col="target", positive_class="CHGOFF"
):
    df = df.copy()
    df[source_col] = df[source_col].astype(str).str.upper().str.strip()
    df[target_col] = (df[source_col] == positive_class).astype(int)
    return df


def add_city_risk_group(
    df, city_col="City", target_col="target", min_loans=50, n_groups=3, labels=None
):
    if labels is None:
        labels = ["LOW_RISK", "MEDIUM_RISK", "HIGH_RISK"]
    df = df.copy()
    if city_col not in df.columns or target_col not in df.columns:
        if "CityRiskGroup" not in df.columns:
            df["CityRiskGroup"] = "MEDIUM_RISK"
        return df
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
            df = df.merge(
                city_stats[[city_col, "CityRiskGroup"]], on=city_col, how="left"
            )
        df["CityRiskGroup"] = df["CityRiskGroup"].fillna("MEDIUM_RISK")
    except Exception:
        df["CityRiskGroup"] = "MEDIUM_RISK"
    return df


def add_sba_ratio(df, sba_col="SBA_Appv", gr_col="GrAppv", ratio_col="SBA_ratio"):
    df = df.copy()
    df[ratio_col] = df[sba_col] / df[gr_col]
    df[ratio_col] = df[ratio_col].replace([np.inf, -np.inf], np.nan)
    return df


def clean_currency(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = df[col].replace(r"[\$,\s]", "", regex=True)
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


# --- Основные функции ---


def pre_pipeline_preparation(*, dataframe: pd.DataFrame) -> pd.DataFrame:
    data = dataframe.copy()
    is_training = "MIS_Status" in data.columns

    if is_training:
        data = make_target(data)
    else:
        data["target"] = np.nan

    data = group_by_first2_numeric(data, "NAICS")
    if "NewExist" in data.columns:
        data = data.loc[data["NewExist"] != 0.0].copy()
        data["NewExist"] = data["NewExist"].astype("Int64")

    data = add_city_risk_group(data)
    cols_to_clean = ["GrAppv", "SBA_Appv"]
    data = clean_currency(data, cols_to_clean)
    data = add_sba_ratio(data)

    data.drop(
        labels=config.model_config.unused_fields, axis=1, errors="ignore", inplace=True
    )

    if not is_training and "target" in data.columns:
        data.drop(columns=["target"], inplace=True)
    return data


def load_dataset(*, file_name: str) -> pd.DataFrame:
    dataframe = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"), low_memory=False)
    transformed = pre_pipeline_preparation(dataframe=dataframe)
    return transformed


# --- Функции сохранения и загрузки (ИХ НЕ ХВАТАЛО) ---

# def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
#     save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
#     save_path = TRAINED_MODEL_DIR / save_file_name
#     remove_old_pipelines(files_to_keep=[save_file_name])
#     joblib.dump(pipeline_to_persist, save_path)
#     print(f"Pipeline saved at: {save_path}")


def save_pipeline(*, pipeline_to_persist: Pipeline) -> None:
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name
    remove_old_pipelines(files_to_keep=[save_file_name])
    # ВОТ ЗДЕСЬ ДОБАВЛЯЕМ СЖАТИЕ
    joblib.dump(pipeline_to_persist, save_path, compress=3)


def load_pipeline(*, file_name: str) -> Pipeline:
    file_path = TRAINED_MODEL_DIR / file_name
    return joblib.load(filename=file_path)


def remove_old_pipelines(*, files_to_keep: List[str]) -> None:
    do_not_delete = files_to_keep + ["__init__.py"]
    for model_file in TRAINED_MODEL_DIR.iterdir():
        if model_file.name not in do_not_delete:
            model_file.unlink()
