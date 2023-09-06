import streamlit as st
import folium
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tempfile
from io import BytesIO
import requests
from streamlit_folium import st_folium
import sa_climate
import swm_funct

# requires the following:
# sa_climate.py
# swm_funct.py
# 1950-2022_torn.csv
# 1955-2022_hail.csv
# 1955-2022_wind.csv
# nclimgrid_stats_monthly_slim.npz

# Streamlit app
def main():
    st.set_page_config("Paget Party")
    st.title('Climate and Severe Weather for Your Location')
   
    # Sidebar input for a string
    user_input1 = st.sidebar.text_input('Enter an address:', value='1600 Pennsylvania Avenue NW, Washington, DC 20500')
    user_input4 = st.sidebar.slider('Distance from address in miles:', min_value=5, max_value=100, value=10, step=5, format='%i')
    user_input2 = st.sidebar.number_input('Start Year: (min=1955)', min_value=1955, step=1, value=1996)
    user_input3 = st.sidebar.number_input('End Year: (max=2022)', min_value=user_input2, step=1, value=2022)

    # Display the user input from the sidebar
    st.sidebar.write('Showing:', user_input1)
    st.sidebar.write('Year Range:', user_input2, '-', user_input3)

    # Create Matplotlib-based plot
    climate_plot = sa_climate.show_address_climate(user_input1)
    st.markdown(f"### Climate Plot for {user_input1}")
    st.pyplot(climate_plot)

    # Create Folium map
#    folium_map = severe_weather_map(user_input1,user_input4,user_input2, user_input3)
    folium_map = swm_funct.severe_weather_map(user_input1,user_input4,user_input2, user_input3)
    st.markdown("### Reported Severe Weather Events - Tornado, Hail, Wind")
    st.markdown(f"##### for {user_input4} miles (NESW) from address")
    # call to render Folium map in Streamlit
    st_data = st_folium(folium_map, width=700)
    
    st.markdown(f"###### Climate Data derived from NOAA Monthly U.S. Climate Gridded Dataset (NClimGrid). Available at https://www.ncei.noaa.gov/data/nclimgrid-monthly/access/")
    st.markdown(f"###### Severe Weather Data sourced from the NOAA Storm Prediction Center's Severe Weather Maps, Graphics, and Data Page. Available at https://www.spc.noaa.gov/wcm/")


if __name__ == '__main__':
    main()
