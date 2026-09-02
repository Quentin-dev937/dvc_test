import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer, make_column_selector, make_column_transformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.impute import SimpleImputer

import hydra
from omegaconf import DictConfig, OmegaConf

import mlflow
import joblib

THRESHOLD = 0.80

def train():
    cfg = OmegaConf.load("params.yaml")

    remote_server_uri = "sqlite:///mlflow.db"
    mlflow.set_tracking_uri(remote_server_uri)
    mlflow.set_experiment("titanic-mlops-1")

    dataframe = pd.read_csv(cfg.data.path.processed)

    X = dataframe.drop(columns=cfg.training.target_col)
    y = dataframe[cfg.training.target_col]

    num_pipeline = make_pipeline(SimpleImputer(strategy=cfg.training.impute_num_strategy), StandardScaler())
    cat_pipeline = make_pipeline(SimpleImputer(strategy=cfg.training.impute_cat_strategy), OneHotEncoder(handle_unknown="ignore"))

    columns_transformer = make_column_transformer((num_pipeline, make_column_selector(dtype_include=np.number)),
                                                  (cat_pipeline, make_column_selector(dtype_include=object)))

    rfc = RandomForestClassifier(max_depth=cfg.training.max_depth, random_state=cfg.reproductibility.random_state)

    pipeline = make_pipeline(columns_transformer, rfc)

    with mlflow.start_run():

        os.makedirs("models", exist_ok=True)

        rfc_scores = cross_val_score(pipeline, X=X, y=y, scoring=cfg.training.scoring, cv=cfg.training.n_split)
        mlflow.log_param("cv", cfg.training.n_split)
        mlflow.log_param("rfc-max_depth", cfg.training.max_depth)

        rfc_scores_mean = np.mean(rfc_scores)
        mlflow.log_metric("f1-macro-mean", rfc_scores_mean)
        
        pipeline.fit(X, y)
        joblib.dump(pipeline, "models/latest_attempt.pkl")

        if rfc_scores_mean > THRESHOLD:
            print("Promotion avec mlflow", flush=True)
            mlflow.sklearn.log_model(sk_model=pipeline, name="titanic-rfc", input_example=X.iloc[[0]], registered_model_name="titanic-classifier")
            joblib.dump(pipeline, "models/production_model.pkl")
            

        print(f"scoring mean: {rfc_scores}", flush=True)


if __name__ == "__main__":
    train()
