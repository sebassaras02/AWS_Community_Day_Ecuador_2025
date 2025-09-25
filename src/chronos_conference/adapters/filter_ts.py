import pandas as pd


def filter_ts(
    df: pd.DataFrame, date_col: str, min_date: str, max_date: str
) -> pd.DataFrame:
    df = df.copy()
    if pd.api.types.is_datetime64_any_dtype(df[date_col]) is False:
        df[date_col] = pd.to_datetime(df[date_col])
    return df[(df[date_col] >= min_date) & (df[date_col] <= max_date)]
