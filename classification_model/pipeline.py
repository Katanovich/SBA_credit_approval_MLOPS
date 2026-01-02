from feature_engine.encoding import OrdinalEncoder
from feature_engine.imputation import CategoricalImputer, RandomSampleImputer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

from classification_model.config.core import config

xgb = Pipeline(
    [
        # impute categorical variables with string missing
        (
            "categorical_imputation",
            CategoricalImputer(
                imputation_method="missing",
                variables=config.model_config.categorical_vars,
            ),
        ),
        # impute numerical variables with the median
        (
            "random_imputation",
            RandomSampleImputer(
                seed="general",
                variables=config.model_config.numerical_vars,
                random_state=config.model_config.random_state,
            ),
        ),
        (
            "categorical_encoder",
            OrdinalEncoder(
                encoding_method="arbitrary",
                variables=config.model_config.categorical_vars,
            ),
        ),
        (
            "classifier",
            XGBClassifier(
                random_state=config.model_config.random_state,
                n_estimators=config.model_config.n_estimators,
                max_depth=config.model_config.max_depth,
                learning_rate=config.model_config.learning_rate,
                subsample=config.model_config.subsample,
                colsample_bytree=config.model_config.colsample_bytree,
                min_child_weight=config.model_config.min_child_weight,
                reg_alpha=config.model_config.reg_alpha,
                reg_lambda=config.model_config.reg_lambda,
                eval_metric=config.model_config.eval_metric,
                n_jobs=config.model_config.n_jobs,
            ),
        ),
    ]
)
