import streamlit as st
import pandas as pd

from chronos_conference.domain.inference import get_forecast
from chronos_conference.adapters.filter_ts import filter_ts
from chronos_conference.adapters.model_instance import ChronosForecaster
from chronos_conference.adapters.ts_plot import get_plot

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
    min_date = st.date_input("Fecha mínima", value="2022-01-01")

with col2:
    max_date = st.date_input("Fecha máxima", value="2023-06-30")

with col3:
    n_steps = st.number_input(
        "Número de pasos a predecir", min_value=1, max_value=128, value=48
    )

execution_button = st.button("Ejecutar modelo")

if not execution_button:
    st.stop()

with st.spinner("Filtrando datos..."):
    df_useful = filter_ts(
        df, date_col="datetime", min_date=str(min_date), max_date=str(max_date)
    )

model = ChronosForecaster(freq="D")

with st.spinner("Modelo en ejecución..."):
    results = get_forecast(
        df=df_useful,
        date_col="datetime",
        target_col="value",
        item_col="unique_id",
        model_instance=model,
    )

st.success("¡Ejecución completada!")

st.write("Resultados de la ejecución:")

fig = get_plot(df_useful, results)

st.plotly_chart(fig, use_container_width=True)
