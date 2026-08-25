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

def train():
    cfg = OmegaConf.load("params.yaml")

    dataframe = pd.read_csv(cfg.data.path.processed)

    X = dataframe.drop(columns=cfg.training.target_col)
    y = dataframe[cfg.training.target_col]

    num_pipeline = make_pipeline(SimpleImputer(strategy=cfg.training.impute_num_strategy), StandardScaler())
    cat_pipeline = make_pipeline(SimpleImputer(strategy=cfg.training.impute_cat_strategy), OneHotEncoder(handle_unknown="ignore"))

    columns_transformer = make_column_transformer((num_pipeline, make_column_selector(dtype_include=np.number)),
                                                  (cat_pipeline, make_column_selector(dtype_include=object)))


    rfc = RandomForestClassifier(max_depth=cfg.training.max_depth, random_state=cfg.reproductibility.random_state)

    pipeline = make_pipeline(columns_transformer, rfc)

    rfc_scores = cross_val_score(pipeline, X=X, y=y, scoring=cfg.training.scoring, cv=cfg.training.n_split)


    print(f"Scoring: {rfc_scores}", flush=True)


if __name__ == "__main__":
    train()
