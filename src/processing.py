import os
import pandas as pd
import hydra
from omegaconf import DictConfig, OmegaConf




def load_data(path):
    return pd.read_csv(path)

def process_data(dataframe, columns_to_remove):
    return dataframe.drop(columns=columns_to_remove).reset_index(drop=True)

def save_data(dataframe, path):
    dataframe.to_csv(path, index=False)


def processing():
    cfg = OmegaConf.load("params.yaml")
    
    dataframe = load_data(path=cfg.data.path.raw)

    dataframe_trunc = process_data(dataframe=dataframe, columns_to_remove=cfg.data.processing.columns_to_remove)

    save_data(dataframe=dataframe_trunc, path=cfg.data.path.processed)

   
if __name__ == "__main__":
    processing()
