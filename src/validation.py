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

    try:
        validation_definition = context.validation_definitions.get("titanic_raw_validation_definition")
        print("✅ validation_definition chargé.", flush=True)
    except Exception as e:
        print(f"❌ Erreur lors du chargement validation_definition : {e}", flush=True)
        sys.exit(1)

    try:
        suite = context.suites.get("titanic_raw_suite")
        print("✅ suite chargée.", flush=True)
    except Exception as e:
        print(f"❌ Erreur lors du chargement suite : {e}", flush=True)
        sys.exit(1)

    try:
        df = pd.read_csv(data_raw_path)
        print("✅ df chargée.", flush=True)
    except Exception as e:
        print(f"❌ Erreur lors du chargement du dataframe : {e}", flush=True)
        sys.exit(1)


    batch_parameters_dataframe = {"dataframe": df}
    results = validation_definition.run(batch_parameters=batch_parameters_dataframe)


    print(results["success"], flush=True)



if __name__ == "__main__":
    validation()