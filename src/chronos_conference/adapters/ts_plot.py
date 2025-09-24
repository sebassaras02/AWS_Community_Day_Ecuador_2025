import plotly.express as px
import pandas as pd


def get_plot(df_story: pd.DataFrame, df_pred: pd.DataFrame):
    if pd.api.types.is_datetime64_any_dtype(df_story["datetime"]) is False:
        df_story["datetime"] = pd.to_datetime(df_story["datetime"])

    if pd.api.types.is_datetime64_any_dtype(df_pred["ds"]) is False:
        df_pred["ds"] = pd.to_datetime(df_pred["ds"])

    fig = px.line(df_story, x="datetime", y="value", title="Historical Information")
    fig.add_scatter(
        x=df_pred["ds"], y=df_pred["AWSChronosForecast"], mode="lines", name="Forecast"
    )
    return fig
