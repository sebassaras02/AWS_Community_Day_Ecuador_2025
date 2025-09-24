from abc import ABC

import pandas as pd
from autogluon.timeseries import TimeSeriesDataFrame, TimeSeriesPredictor


class ForecastingBaseModel(ABC):
    def __init__(self, freq: str, n_jobs: int = 1) -> None:
        self.model = None
        self.freq = freq
        self.n_jobs = n_jobs

    def fit(
        self, df: pd.DataFrame, date_col: str, item_col: str, targe_col: str
    ) -> None:
        pass

    def predict(self, n_steps: int) -> pd.DataFrame:
        pass


class ChronosForecaster(ForecastingBaseModel):
    def __init__(self, freq: str = "H"):
        super().__init__(freq=freq)

    def fit(
        self, df: pd.DataFrame, date_col: str, item_col: str, target_col: str
    ) -> None:
        self.item_id = item_col
        df = df.copy()
        df = df.rename(columns={target_col: "target"})
        self.df = TimeSeriesDataFrame.from_data_frame(
            df,
            id_column=item_col,
            timestamp_column=date_col,
        )

    def predict(self, n_steps):
        self.model = TimeSeriesPredictor(
            prediction_length=n_steps, freq=self.freq, verbosity=0
        ).fit(self.df, presets="bolt_base")
        results = self.model.predict(self.df)
        results = results.to_data_frame().reset_index()
        results = results[["mean", "item_id", "timestamp"]]
        results = results.rename(
            columns={
                "mean": "AWSChronosForecast",
                "item_id": "unique_id",
                "timestamp": "ds",
            }
        )
        return results
