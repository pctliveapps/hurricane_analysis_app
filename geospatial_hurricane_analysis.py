#import streamlit as st
import pandas as pd
import numpy as np
import json

import datetime

import map_builder

#from streamlit_folium import folium_static
import folium
import geopandas as gpd



list_of_states_to_load = ["Virginia", "South Carolina", "North Carolina", "Georgia", "Alabama"] # , "Tennessee"

strJSON_gdrive_path =  "./data/geo/georef-united-states-of-america-county.geojson"


states = {"AL":"Alabama", "AK":"Alaska", "AZ":"Arizona", "AR":"Arkansas", "CA":"California", "CO":"Colorado", "CT":"Connecticut", 
          "DC":"Washington DC", "DE":"Delaware", "FL":"Florida", "GA":"Georgia", "HI":"Hawaii", "ID":"Idaho", "IL":"Illinois", 
          "IN":"Indiana", "IA":"Iowa", "KS":"Kansas", "KY":"Kentucky", "LA":"Louisiana", "ME":"Maine", "MD":"Maryland",
          "MA":"Massachusetts", "MI":"Michigan", "MN":"Minnesota", "MS":"Mississippi", "MO":"Missouri", "MT":"Montana",
          "NE":"Nebraska", "NV":"Nevada", "NH":"New Hampshire", "NJ":"New Jersey", "NM":"New Mexico", "NY":"New York", 
          "NC":"North Carolina", "ND":"North Dakota", "OH":"Ohio", "OK":"Oklahoma", "OR":"Oregon", "PA":"Pennsylvania", 
          "RI":"Rhode Island", "SC":"South Carolina", "SD":"South Dakota", "TN":"Tennessee", "TX":"Texas", "UT":"Utah", "VT":"Vermont",
          "VA":"Virginia", "WA":"Washington", "WV":"West Virginia","WI":"Wisconsin", "WY":"Wyoming"}




print("\n\nTop of Python Script")

# st.set_page_config(layout="wide")

# st.header('Geospatial Hurricane Analysis')

# hurricane_select_col, top_map_col = st.columns([1,2])





print("loading dataframe data...")
# data load
# df_joined_fema_data = pd.read_csv( "./data/snowflake_joined_fema_data.csv")


# load geojson data for county lines
geojson_online = gpd.read_file(strJSON_gdrive_path)



geojson_online['coty_code'] = geojson_online['coty_code'].astype(str)
geojson_online['coty_code'] = geojson_online['coty_code'].str.strip()

geojson_online['ste_name'] = geojson_online['ste_name'].astype(str)
geojson_online['ste_name'] = geojson_online['ste_name'].str.strip()

df_geo = geojson_online[~geojson_online['geometry'].isna()]


print( geojson_online.head() )

# now load the list of extracted hurricane data


df_hurricane_all_data_counties = pd.read_csv( "./data/hurricanes/2018_Michael_all_raw_events_counties.csv" )
df_hurricane_all_data_counties = df_hurricane_all_data_counties.loc[:, ~df_hurricane_all_data_counties.columns.str.contains('^Unnamed')]


df_hurricane_all_data_counties["fips"] = df_hurricane_all_data_counties["fips"].map(str)
df_hurricane_all_data_counties["fips"] = df_hurricane_all_data_counties["fips"].str.zfill(5)

print( df_hurricane_all_data_counties.head() )

df_geo_storm = df_geo.merge(df_hurricane_all_data_counties, how="left", right_on=["fips"], left_on=["coty_code"])

df_geo_area_to_render = df_geo_storm[ df_geo_storm["ste_name"].isin(list_of_states_to_load) ]



map_builder.generate_folium_map(None, df_geo_area_to_render)

