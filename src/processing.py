import os
import pandas as pd
import hydra
from omegaconf import DictConfig, OmegaConf


def main():
    cfg = OmegaConf.load("params.yaml")
    
    dataframe = pd.read_csv(cfg.data.path.raw)
    
    dataframe.to_csv(cfg.data.path.processed, index=False)
    

   
if __name__ == "__main__":
    main()
