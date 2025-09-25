# ruff: noqa: F403, F405

import streamlit as st
import pandas as pd

from chronos_conference.domain.inference import get_forecast
from chronos_conference.adapters.filter_ts import filter_ts
from chronos_conference.adapters.model_instance import ChronosForecaster
from chronos_conference.adapters.ts_plot import get_plot
from chronos_conference.settings import *

st.title("AWS Community Day Ecuador 2025")
st.header(
    "Conferencia: Aprendiendo el Lenguaje de las series de tiempo con AWS Chronos Bolt"
)
st.subheader("Ponente: Sebastian Sarasti")

st.write(
    """
Esta aplicación demuestra cómo utilizar AWS Chronos Bolt para la predicción del clima mediante
datos abiertos obtenidos del INAMHI. 
"""
)

df = pd.read_csv("../../../data/historical_simulation_9023624.csv")

col1, col2, col3 = st.columns(3)

with col1:
    min_date = st.date_input("Fecha mínima", value=MIN_PRED_DATE)

with col2:
    max_date = st.date_input("Fecha máxima", value=MAX_PRED_DATE)

with col3:
    n_steps = st.number_input(
        "Número de pasos a predecir",
        min_value=MIN_PRED_DATE_LIMIT,
        max_value=MAX_PRED_DATE_LIMIT,
        value=N_PRED_STEPS,
    )

execution_button = st.button("Ejecutar modelo")

if not execution_button:
    st.stop()

with st.spinner("Filtrando datos..."):
    df_useful = filter_ts(
        df,
        date_col=HISTORICAL_DATE_COLUMN,
        min_date=str(min_date),
        max_date=str(max_date),
    )

model = ChronosForecaster(freq=FREQUENCY)

with st.spinner("Modelo en ejecución..."):
    results = get_forecast(
        df=df_useful,
        date_col=HISTORICAL_DATE_COLUMN,
        target_col=HISTORICAL_TARGET_COLUMN,
        item_col=HISTORICAL_ITEM_COLUMN,
        model_instance=model,
    )

st.success("¡Ejecución completada!")

st.write("Resultados de la ejecución:")

fig = get_plot(df_useful, results)

st.plotly_chart(fig, use_container_width=True)
