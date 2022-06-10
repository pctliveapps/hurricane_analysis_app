import pandas as pd
import numpy as np
import time
import geopandas as gpd
import locale

#locale.setlocale( locale.LC_ALL, 'en_CA.UTF-8' )


def load_storm_configurations():


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
	    'states': ["New York", "New Jersey", "Delaware", "Maryland", "Pennsylvania", "Connecticut", "Virginia", "Ohio", "West Virginia"],
	    'storm_center': [40.58370340594471, -74.12008933292537]
	}

	storm_frances = {
	    'name': 'Frances',
	    'year': 2004,
	    'states': ["Florida", "South Carolina", "North Carolina", "Georgia", "Alabama", "Virginia", "Tennessee", "West Virginia"],
	    'storm_center': [32.869893106163026, -84.10818135318395]
	}

	storm_gustav = {
	    'name': 'Gustav',
	    'year': 2008,
	    'states': ["Missouri", "Texas", "Louisiana", "Alabama", "Mississippi", "Arkansas", "Oklahoma"],
	    'storm_center': [32.869893106163026, -84.10818135318395]
	}


	storm_irene = {
	    'name': 'Irene',
	    'year': 2011,
	    'states': ["South Carolina", "North Carolina", "Virginia", "West Virginia", "New York", "New Jersey", "Delaware", "Maryland", "Pennsylvania", "Connecticut", "Massachusetts", "Rhode Island"],
	    'storm_center': [40.58370340594471, -74.12008933292537]
	}

	storms = []
	storms.append( storm_katrina )
	storms.append( storm_michael )
	storms.append( storm_sandy )

	storms.append( storm_frances )
	storms.append( storm_gustav )
	storms.append( storm_irene )


	storm_selector_dict = {}

	#for storm in storms:
	for list_storm_index in range(len(storms)):

		label = storms[list_storm_index]['name'] + ' ' + str(storms[list_storm_index]['year'])

		storm_selector_dict[ list_storm_index ] = label


	return storms, storm_selector_dict




def load_hurricane_data(strMapStormDataCSVFilename, list_of_states_to_load, df_geo):


	# now load the list of extracted hurricane data


	df_hurricane_all_data_counties = pd.read_csv( strMapStormDataCSVFilename ) #"./data/hurricanes/2018_Michael_all_raw_events_counties.csv" )
	df_hurricane_all_data_counties = df_hurricane_all_data_counties.loc[:, ~df_hurricane_all_data_counties.columns.str.contains('^Unnamed')]


	df_hurricane_all_data_counties["fips"] = df_hurricane_all_data_counties["fips"].map(str)
	df_hurricane_all_data_counties["fips"] = df_hurricane_all_data_counties["fips"].str.zfill(5)

	print( df_hurricane_all_data_counties.head() )

	df_geo_storm = df_geo.merge(df_hurricane_all_data_counties, how="left", right_on=["fips"], left_on=["coty_code"])

	df_geo_area_to_render = df_geo_storm[ df_geo_storm["ste_name"].isin( list_of_states_to_load ) ]

	df_geo_area_to_render['storm_dist_formatted'] = df_geo_area_to_render['storm_dist'].map('{:,.2f}'.format)



	return df_geo_area_to_render





def load_fema_damage_data(strFEMADamageData_path, list_of_states_to_load, current_storm, df_geo):


	# now load the fema damage data

	#print(df_geo.info())

	df_fema_damage_data = pd.read_csv( strFEMADamageData_path ) 

	df_fema_damage_data["fips_code"] = df_fema_damage_data["fips_code"].map(str)
	df_fema_damage_data["fips_code"] = df_fema_damage_data["fips_code"].str.zfill(5)



	# current_storm['name'] + ' ' + str( current_storm['year'] )
	only_storm_fema_damage_data = df_fema_damage_data[ (df_fema_damage_data["declarationTitle"] == "HURRICANE " + current_storm['name'].upper()) & (df_fema_damage_data["year"] == current_storm['year']) ]


	df_fema_damage_data_geo = df_geo.merge(only_storm_fema_damage_data, how="left", right_on=["fips_code"], left_on=["coty_code"])

	df_fema_area_to_render = df_fema_damage_data_geo[ df_fema_damage_data_geo["ste_name"].isin( list_of_states_to_load ) ]

	df_fema_area_to_render['totalDamage_Summed_Currency'] = df_fema_area_to_render['totalDamage_Summed'].map('${:,.2f}'.format)
	#.apply(lambda x: "{:,}".format(x['totalDamage_Summed'])) #.map(locale.currency)

	#df_fema_area_to_render.style.format({"totalDamage_Summed_Currency": "{:,.0f}"})


	return df_fema_area_to_render








def load_geo_base_data(strJSON_gdrive_path):



	# load geojson data for county lines
	geojson_online = gpd.read_file(strJSON_gdrive_path)



	geojson_online['coty_code'] = geojson_online['coty_code'].astype(str)
	geojson_online['coty_code'] = geojson_online['coty_code'].str.strip()

	geojson_online['ste_name'] = geojson_online['ste_name'].astype(str)
	geojson_online['ste_name'] = geojson_online['ste_name'].str.strip()

	df_geo = geojson_online[~geojson_online['geometry'].isna()]


	print( geojson_online.head() )




	return df_geo	




