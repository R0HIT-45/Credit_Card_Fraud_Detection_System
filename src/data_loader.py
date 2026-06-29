import pandas as pd
def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df

def get_features_and_target(df: pd.DataFrame, target_col: str = "Class"):
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y
