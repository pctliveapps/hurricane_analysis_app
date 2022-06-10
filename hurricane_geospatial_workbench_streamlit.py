import streamlit as st
import pandas as pd
import numpy as np
import json

import datetime

from streamlit_folium import folium_static
import folium
import geopandas as gpd

import map_builder

import hurricane_data_manager


strFEMADamageData_path = "./data/fema/hurricane_damage_value_per_fips_code.csv"
strJSON_gdrive_path =  "./data/geo/georef-united-states-of-america-county.geojson"

print("\n\nTop of Python Script")

st.set_page_config(layout="wide")

st.header('Hurricane Geospatial Analysis Workbench')


storms, storm_selector_dict = hurricane_data_manager.load_storm_configurations()





print(storm_selector_dict)


def storm_selector_format_func(option):
	return storm_selector_dict[option]



states = {"AL":"Alabama", "AK":"Alaska", "AZ":"Arizona", "AR":"Arkansas", "CA":"California", "CO":"Colorado", "CT":"Connecticut", 
          "DC":"Washington DC", "DE":"Delaware", "FL":"Florida", "GA":"Georgia", "HI":"Hawaii", "ID":"Idaho", "IL":"Illinois", 
          "IN":"Indiana", "IA":"Iowa", "KS":"Kansas", "KY":"Kentucky", "LA":"Louisiana", "ME":"Maine", "MD":"Maryland",
          "MA":"Massachusetts", "MI":"Michigan", "MN":"Minnesota", "MS":"Mississippi", "MO":"Missouri", "MT":"Montana",
          "NE":"Nebraska", "NV":"Nevada", "NH":"New Hampshire", "NJ":"New Jersey", "NM":"New Mexico", "NY":"New York", 
          "NC":"North Carolina", "ND":"North Dakota", "OH":"Ohio", "OK":"Oklahoma", "OR":"Oregon", "PA":"Pennsylvania", 
          "RI":"Rhode Island", "SC":"South Carolina", "SD":"South Dakota", "TN":"Tennessee", "TX":"Texas", "UT":"Utah", "VT":"Vermont",
          "VA":"Virginia", "WA":"Washington", "WV":"West Virginia","WI":"Wisconsin", "WY":"Wyoming"}




with st.sidebar:

	#select_storm_box = st.radio("Choose a Storm to Analyze", ("Katrina (2005)", "Sandy (2012)", "Michael (2018)"))
	selected_storm_option = st.selectbox("Select option", options=list(storm_selector_dict.keys()), format_func=storm_selector_format_func)




print("current storm: " + str(selected_storm_option))



current_storm_index = selected_storm_option

current_storm = storms[ current_storm_index ]

list_of_states_to_load = storms[ current_storm_index ]['states']

strMapStormDataCSVFilename = "./data/hurricanes/" + str( current_storm['year'] ) + "_" + current_storm['name'] + "_all_raw_events_counties.csv"

print("Current Storm: " + current_storm['name'] + ' ' + str( current_storm['year'] ) )




print("\n\nTop of Python Script")





print("loading dataframe data...")
# data load

# TODO: need to look at caching here...

df_geo = hurricane_data_manager.load_geo_base_data(strJSON_gdrive_path)



df_geo_area_to_render = hurricane_data_manager.load_hurricane_data(strMapStormDataCSVFilename, list_of_states_to_load, df_geo)




df_fema_area_to_render = hurricane_data_manager.load_fema_damage_data(strFEMADamageData_path, list_of_states_to_load, current_storm, df_geo)




m = map_builder.build_streamlit_folium_map(current_storm, df_fema_area_to_render, df_geo_area_to_render)








#m = folium.Map(location=[33.754278, -84.383527], zoom_start=12,tiles='openstreetmap')

print("render map")


    # call to render Folium map in Streamlit
folium_static(m, height=600, width=900)
