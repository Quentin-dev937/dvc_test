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

    context_root_dir = Path("great_expectations")
    data_raw_path = Path("data/raw/titanic.csv")
    
    if not context_root_dir.exists():
        print(f"❌ Erreur: Le dossier {context_root_dir} n'existe pas.", flush=True)
        sys.exit(1)

    try:
        context = gx.get_context(context_root_dir=str(context_root_dir))
        print("✅ Contexte Great Expectations chargé.", flush=True)
    except Exception as e:
        print(f"❌ Erreur lors du chargement du contexte : {e}", flush=True)
        sys.exit(1)


    batch_definition = context.data_sources.get("titanic_datasource").get_asset("titanic_raw").get_batch_definition("titanic.csv")
    print("✅ batch_definition", batch_definition, flush=True)
    suite = context.suites.get("titanic_raw_suite")

    df = pd.read_csv(data_raw_path)

    batch = batch_definition.get_batch("titanic.csv")

    results = batch.validate(expect=suite)

    print(results["success"], flush=True)



if __name__ == "__main__":
    validation()