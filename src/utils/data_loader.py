import pandas as pd


def load_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df
