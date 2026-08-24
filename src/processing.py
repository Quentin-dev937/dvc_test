import os
import pandas as pd

data_raw_path = f"data/raw/titanic.csv"
data_out_path = f"data/processed/titanic.csv"

def main(input_path, output_path):
    
    dataframe = pd.read_csv(input_path)
    
    dataframe.to_csv(output_path, index=False)
    

   
if __name__ == "__main__":
    main(input_path=data_raw_path, output_path=data_out_path)
