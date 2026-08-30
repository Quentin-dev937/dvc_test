import sys
import great_expectations as gx
import pandas as pd
from omegaconf import OmegaConf, DictConfig
import hydra
from pathlib import Path

def validation():
    # 1. Initialisation du contexte
    # CRUCIAL : Il faut pointer vers le dossier où se trouve great_expectations.yml
    context_root_dir = Path("great_expectations")
    
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
        # 2. Récupération de la DataSource, de l'Asset et de la BatchDefinition
        # On utilise les noms que vous aviez dans votre configuration
        ds_name = "titanic_datasource"
        asset_name = "titanic_raw"
        batch_def_name = "titanic.csv"
        suite_name = "titanic_raw_suite"

        # Récupération de la DataSource
        datasource = context.data_sources.get(ds_name)
        if not datasource:
            print(f"❌ DataSource '{ds_name}' introuvable.", flush=True)
            sys.exit(1)

        # Récupération de l'Asset
        asset = datasource.get_asset(asset_name)
        if not asset:
            print(f"❌ Asset '{asset_name}' introuvable.", flush=True)
            sys.exit(1)

        # Récupération de la BatchDefinition
        batch_definition = asset.get_batch_definition(batch_def_name)
        if not batch_definition:
            print(f"❌ BatchDefinition '{batch_def_name}' introuvable.", flush=True)
            sys.exit(1)

        # 3. Récupération de la Suite d'attentes
        suite = context.suites.get(suite_name)
        if not suite:
            print(f"❌ Suite '{suite_name}' introuvable.", flush=True)
            sys.exit(1)

        # 4. Création du Validator et Validation
        # On lie la batch_definition à la suite pour créer un validator
        validator = batch_definition.get_validator(expectation_suite=suite)
        
        print(f"🚀 Lancement de la validation avec la suite '{suite_name}'...", flush=True)
        
        # Exécution de la validation
        results = validator.validate()

        # 5. Gestion du résultat
        if results.success:
            print("✅ SUCCÈS : La validation des données a réussi.", flush=True)
            sys.exit(0)
        else:
            print("❌ ÉCHEC : La validation des données a échoué.", flush=True)
            stats = results.statistics
            print(f"   Tests réussis : {stats['successful_expectations']}/{stats['evaluated_expectations']}", flush=True)
            
            # Afficher les détails des échecs (optionnel mais utile en CI)
            for expectation_result in results.results:
                if not expectation_result["success"]:
                    print(f"   - Échec : {expectation_result['expectation_config']['type']}", flush=True)
            
            # Code de sortie 1 pour faire échouer le pipeline CI
            sys.exit(1)

    except Exception as e:
        print(f"❌ Erreur critique durant la validation : {e}", flush=True)
        # Décommentez la ligne suivante pour voir le détail de l'erreur en local
        # import traceback; traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    validation()