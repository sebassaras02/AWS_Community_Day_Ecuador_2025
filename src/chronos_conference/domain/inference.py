import pandas as pd


def get_forecast(
    df: pd.DataFrame,
    date_col: str,
    target_col: str,
    item_col: str,
    model_instance,
    horizon: int = 24,
) -> pd.DataFrame:
    """
    This function is designed to generate forecasts using a pre-trained
    TimeSeriesPredictor model from the AutoGluon library.
    """
    df = df.copy()
    df = df.rename(columns={target_col: "target"})
    model_instance.fit(
        df=df,
        date_col=date_col,
        item_col=item_col,
        target_col=target_col,
    )
    results = model_instance.predict(n_steps=horizon)
    return results
