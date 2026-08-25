import os
import pandas as pd
import hydra
from omegaconf import DictConfig, OmegaConf


def processing():
    cfg = OmegaConf.load("params.yaml")
    
    dataframe = pd.read_csv(cfg.data.path.raw)
    print("Dataframe shape:", dataframe.shape, flush=True)

    dataframe_trunc = dataframe.drop(columns=cfg.data.processing.columns_to_remove).reset_index(drop=True)
    
    dataframe_trunc.to_csv(cfg.data.path.processed, index=False)
    print("Dataframe processed saved !", flush=True)

   
if __name__ == "__main__":
    processing()
