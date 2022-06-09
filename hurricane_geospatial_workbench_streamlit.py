import streamlit as st
import pandas as pd
import numpy as np
import json

import datetime

from streamlit_folium import folium_static
import folium

import map_builder



print("\n\nTop of Python Script")

st.set_page_config(layout="wide")

st.header('Hurricane Geospatial Analysis Workbench')





import geopandas as gpd


storm_katrina = {
    'name': 'Katrina',
    'year': 2005,
    'states': ["Louisiana", "Alabama", "Mississippi", "Arkansas", "Tennessee", "Kentucky"],
    'storm_center': [32.13176364136887, -91.50372022290216]
}

storm_michael = {
    'name': 'Michael',
    'year': 2018,
    'states': ["Florida", "South Carolina", "North Carolina", "Georgia", "Alabama", "Virginia"],
    'storm_center': [32.869893106163026, -84.10818135318395]
}

storm_sandy = {
    'name': 'Sandy',
    'year': 2012,
    'states': ["New York", "New Jersey", "Delaware", "Maryland", "Pennsylvania", "Connecticut"],
    'storm_center': [40.58370340594471, -74.12008933292537]
}

storms = []
storms.append( storm_katrina )
storms.append( storm_michael )
storms.append( storm_sandy )


storm_selector_dict = {}

#for storm in storms:
for list_storm_index in range(len(storms)):

	label = storms[list_storm_index]['name'] + ' ' + str(storms[list_storm_index]['year'])

	storm_selector_dict[ list_storm_index ] = label


print(storm_selector_dict)


def storm_selector_format_func(option):
	return storm_selector_dict[option]



#list_of_states_to_load = ["Virginia", "South Carolina", "North Carolina", "Georgia", "Alabama"] # , "Tennessee"

strJSON_gdrive_path =  "./data/geo/georef-united-states-of-america-county.geojson"


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


df_hurricane_all_data_counties = pd.read_csv( strMapStormDataCSVFilename ) #"./data/hurricanes/2018_Michael_all_raw_events_counties.csv" )
df_hurricane_all_data_counties = df_hurricane_all_data_counties.loc[:, ~df_hurricane_all_data_counties.columns.str.contains('^Unnamed')]


df_hurricane_all_data_counties["fips"] = df_hurricane_all_data_counties["fips"].map(str)
df_hurricane_all_data_counties["fips"] = df_hurricane_all_data_counties["fips"].str.zfill(5)

print( df_hurricane_all_data_counties.head() )

df_geo_storm = df_geo.merge(df_hurricane_all_data_counties, how="left", right_on=["fips"], left_on=["coty_code"])

df_geo_area_to_render = df_geo_storm[ df_geo_storm["ste_name"].isin( list_of_states_to_load ) ]



m = map_builder.build_streamlit_folium_map(current_storm, None, df_geo_area_to_render)








#m = folium.Map(location=[33.754278, -84.383527], zoom_start=12,tiles='openstreetmap')

print("render map")


    # call to render Folium map in Streamlit
folium_static(m, height=600, width=800)
