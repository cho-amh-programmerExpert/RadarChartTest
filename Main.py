import streamlit as st
import geopandas as gpd
import pandas as pd
import altair as alt
import plotly.express as px
import json

def plot_heatmap_altair(country_name, state_values):
    states = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    country_states = states[states['admin'] == country_name]
    
    if country_states.empty:
        raise ValueError(f"No states/provinces found for country '{country_name}' in the dataset")

    country_states = country_states.set_index('name').join(pd.Series(state_values, name='value'), how='left').reset_index()
    geojson = json.loads(country_states.to_json())

    chart = alt.Chart(alt.Data(values=geojson['features'])).mark_geoshape().encode(
        color='properties.value:Q',
        tooltip=['properties.name:N', 'properties.value:Q']
    ).properties(
        width=800,
        height=600
    ).project(
        type='identity',
        reflectY=True
    )
    
    return chart

def plot_heatmap_plotly(country_name, state_values):
    states = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    country_states = states[states['admin'] == country_name]
    
    if country_states.empty:
        raise ValueError(f"No states/provinces found for country '{country_name}' in the dataset")

    country_states = country_states.set_index('name').join(pd.Series(state_values, name='value'), how='left').reset_index()

    fig = px.choropleth(country_states,
                        geojson=country_states.geometry,
                        locations=country_states.index,
                        color='value',
                        hover_name='name',
                        projection='mercator')
    
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig

# Streamlit interface
st.title("Interactive Heatmap")

country_name = st.text_input("Country Name", "United States of America")
state_values = {
    'California': 10,
    'Texas': 20,
    'New York': 30,
    'Florida': 40
}

chart = plot_heatmap_altair(country_name, state_values)
fig = plot_heatmap_plotly(country_name, state_values)

st.altair_chart(chart)
st.plotly_chart(fig)
