import sys
import great_expectations as gx
import pandas as pd
from omegaconf import OmegaConf, DictConfig
import hydra
from pathlib import Path

#@hydra.main(config_path="../conf", config_name="config", version_base=None)
#def validation(cfg: DictConfig):
def validation():

    #data_source = cfg.gx.data_source
    #suite_name = cfg.gx.suite_name
    #asset_name = cfg.gx.asset_name
    #batch_definition_name = cfg.gx.batch_definition_name

    context = gx.get_context()

    batch_definition = context.data_sources.get("titanic_datasource").get_asset("titanic_raw").get_batch_definition("titanic.csv")
    batch = batch_definition.get_batch()
    suite = context.suites.get("titanic_raw_suite")

    results = batch.validate(expect=suite)

    print(results["success"], flush=True)



if __name__ == "__main__":
    validation()