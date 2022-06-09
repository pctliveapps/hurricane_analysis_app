import pandas as pd
import numpy as np
import time


import folium
import branca


def generate_folium_map(storm_conf, df_fema=None, df_geo_area_to_render=None):

	t0 = time.time()

	print("building folium map...")

	# create the map object

	us_map_geojson = folium.Map(location=[40.7128, -74], zoom_start=6,tiles=None)
	folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(us_map_geojson) # CartoDB positron'




	# build the feature groups

	storm_name = storm_conf['name']
	storm_year = storm_conf['year']


	feature_group_storm_path = folium.FeatureGroup(name=(storm_name + ' ' + str(storm_year) + ' Storm Path'),overlay=True).add_to(us_map_geojson)

	feature_group_storm_distance = folium.FeatureGroup(name=(storm_name + ' ' + str(storm_year) + ' Storm County Distance'),overlay=False).add_to(us_map_geojson)

	feature_group_storm_wind_vmax_sustained = folium.FeatureGroup(name=(storm_name + ' ' + str(storm_year) + ' VMAX Sustained'),overlay=False).add_to(us_map_geojson)
	feature_group_storm_wind_vmax_gusts = folium.FeatureGroup(name=(storm_name + ' ' + str(storm_year) + ' VMAX Gusts'),overlay=False).add_to(us_map_geojson)

	#feature_group_storm_wind_sustained_duration = folium.FeatureGroup(name=(storm_name + ' ' + str(storm_year) + ' Sustained Duration'),overlay=False).add_to(us_map_geojson)
	#feature_group_storm_wind_gust_duration = folium.FeatureGroup(name=(storm_name + ' ' + str(storm_year) + ' Gust Duration'),overlay=False).add_to(us_map_geojson)

	feature_group_storm_flood_exposure = folium.FeatureGroup(name=(storm_name + ' ' + str(storm_year) + ' Flood Exposure'),overlay=False).add_to(us_map_geojson)

	feature_group_fema_damage = folium.FeatureGroup(name=(storm_name + ' ' + str(storm_year) + ' FEMA Damage'),overlay=False).add_to(us_map_geojson)





	# build some layers

	# 1. build the storm distance layer


	storm_distance_colormap = branca.colormap.LinearColormap(colors=['#003302', '#237526', '#ffffff'], index=[10, 50, 175],vmin=0,vmax=400)

	def storm_distance_layer_style_function(feature):
		storm_value = feature["properties"]['storm_dist'] #.isnull()

		if (feature["properties"]['storm_dist'] is None):

			return {
				'fillColor': '#eeeeee', 
				'color':'#000000', 
				'fillOpacity': 0.4, 
				'weight': 0.1
			}
		else:
			# nothing really
			a=0

		float_value = float(storm_value)


		return {
			'fillColor': """{fv}""".format( fv = storm_distance_colormap.rgb_hex_str(float_value) ), 
			'color':'#000000', 
			'fillOpacity': 0.8, 
			'weight': 0.1
		}

	storm_dist_highlight_function = lambda x: {'fillColor': '#000000', 
		'color':'#000000', 
		'fillOpacity': 0.50, 
		'weight': 0.1
		}


	storm_dist_base_layer = folium.features.GeoJson(
		data=df_geo_area_to_render,
		style_function=storm_distance_layer_style_function, 
		control=True,
		highlight_function=storm_dist_highlight_function, 
		smooth_factor=0.1,
		tooltip=folium.features.GeoJsonTooltip(
			fields=['coty_name_long', 'coty_code','storm_dist'],
			aliases=['County: ', 'FIPS: ','Storm Distance: '],
			style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
		)
	)

	feature_group_storm_distance.add_child( storm_dist_base_layer )	

	# 2. build the [ Wind VMAX Sustained ] layer


	storm_vmax_sustained_layer_colormap = branca.colormap.LinearColormap(colors=['#ffffff', '#ff0000', '#630000'], index=[14, 25, 35],vmin=0,vmax=35)

	def storm_vmax_sustained_layer_style_function(feature):
		storm_value = feature["properties"]['vmax_sust'] #.isnull()

	  #print(pre_storm_avg_admissions)

		if (feature["properties"]['vmax_sust'] is None):

			return {
				'fillColor': '#eeeeee', 
				'color':'#000000', 
				'fillOpacity': 0.4, 
				'weight': 0.1
				}
		else:
			# nothing really
			a=0

		float_value = float(storm_value)


		return {
			'fillColor': f'{storm_vmax_sustained_layer_colormap.rgb_hex_str(float_value)}', 
			'color':'#000000', 
			'fillOpacity': 0.8, 
			'weight': 0.1
			}

	storm_vmax_sustained_highlight_function = lambda x: {'fillColor': '#000000', 
		'color':'#000000', 
		'fillOpacity': 0.50, 
		'weight': 0.1}


	storm_vmax_sustained_layer = folium.features.GeoJson(
		data=df_geo_area_to_render,
		style_function=storm_vmax_sustained_layer_style_function, 
		control=True,
		highlight_function=storm_vmax_sustained_highlight_function, 
		smooth_factor=0.1,
		tooltip=folium.features.GeoJsonTooltip(
			fields=['coty_name_long', 'coty_code','vmax_sust'],
			aliases=['County: ', 'FIPS: ','VMAX Sustained: '],
			style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
		)
	)

	feature_group_storm_wind_vmax_sustained.add_child( storm_vmax_sustained_layer )





	# 3. build the [ vmax wind gusts ] layer


	# feature_group_storm_wind_vmax_gusts


	storm_vmax_gusts_layer_colormap = branca.colormap.LinearColormap(colors=['#ffffff', '#ff0000', '#630000'], index=[15, 35, 55],vmin=0,vmax=55)

	def storm_vmax_gusts_layer_style_function(feature):
		storm_value = feature["properties"]['vmax_gust'] #.isnull()

		if (feature["properties"]['vmax_gust'] is None):

			return {
				'fillColor': '#eeeeee', 
				'color':'#000000', 
				'fillOpacity': 0.4, 
				'weight': 0.1
			}
		else:
			# nothing really
			a=0

		float_value = float(storm_value)

		return {
			'fillColor': f'{storm_vmax_gusts_layer_colormap.rgb_hex_str(float_value)}', 
			'color':'#000000', 
			'fillOpacity': 0.8, 
			'weight': 0.1
		}

	storm_vmax_gusts_highlight_function = lambda x: {'fillColor': '#000000', 
		'color':'#000000', 
		'fillOpacity': 0.50, 
		'weight': 0.1}


	storm_vmax_GUSTS_layer = folium.features.GeoJson(
		data=df_geo_area_to_render,
		style_function=storm_vmax_gusts_layer_style_function, 
		control=True,
		highlight_function=storm_vmax_gusts_highlight_function, 
		smooth_factor=0.1,
		tooltip=folium.features.GeoJsonTooltip(
			fields=['coty_name_long', 'coty_code','vmax_gust'],
			aliases=['County: ', 'FIPS: ','VMAX Gusts: '],
			style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
		)
	)

	feature_group_storm_wind_vmax_gusts.add_child( storm_vmax_GUSTS_layer )






	# N. build the [ Flood Exposure ] layer


	storm_flood_layer_colormap = branca.colormap.LinearColormap(colors=['#ffffff', '#0000ff'], index=[0, 1],vmin=0,vmax=1)

	def storm_flood_layer_style_function(feature):
		storm_value = feature["properties"]['flood_exposure'] #.isnull()

		if ((feature["properties"]['flood_exposure'] is None) | (feature["properties"]['flood_exposure'] == False)):

			return {
			'fillColor': '#eeeeee', 
			'color':'#000000', 
			'fillOpacity': 0.4, 
			'weight': 0.1
			}
		else:
			# nothing really
			a=0

		float_value = float(storm_value)

		return {
			'fillColor': f'{storm_flood_layer_colormap.rgb_hex_str(1)}', 
			'color':'#000000', 
			'fillOpacity': 0.4, 
			'weight': 0.1
		}

	storm_flood_highlight_function = lambda x: {'fillColor': '#000000', 
		'color':'#000000', 
		'fillOpacity': 0.50, 
		'weight': 0.1}


	storm_flood_layer = folium.features.GeoJson(
		data=df_geo_area_to_render,
		style_function=storm_flood_layer_style_function, 
		control=True,
		highlight_function=storm_flood_highlight_function, 
		smooth_factor=0.1,
		tooltip=folium.features.GeoJsonTooltip(
			fields=['coty_name_long', 'coty_code','flood_exposure'],
			aliases=['County: ', 'FIPS: ','Flood Exposure: '],
			style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
		)
	)

	feature_group_storm_flood_exposure.add_child( storm_flood_layer )	







	# build the FEMA layers


	# build the feature_group_fema_damage layer


	fema_damage_layer_colormap = branca.colormap.LinearColormap(colors=['#ffffff', '#ff0000', '#630000'], index=[1000, 1000000, 10100500],vmin=0,vmax=10100500)

	def fema_damage_layer_style_function(feature):
		storm_value = feature["properties"]['totalDamage_Summed'] #.isnull()

	  #print(pre_storm_avg_admissions)

		if (feature["properties"]['totalDamage_Summed'] is None):

			return {
				'fillColor': '#eeeeee', 
				'color':'#000000', 
				'fillOpacity': 0.4, 
				'weight': 0.1
				}
		else:
			# nothing really
			a=0

		float_value = float(storm_value)


		return {
			'fillColor': f'{fema_damage_layer_colormap.rgb_hex_str(float_value)}', 
			'color':'#000000', 
			'fillOpacity': 0.8, 
			'weight': 0.1
			}

	fema_damage_highlight_function = lambda x: {'fillColor': '#000000', 
		'color':'#000000', 
		'fillOpacity': 0.50, 
		'weight': 0.1}


	fema_damage_layer = folium.features.GeoJson(
		data=df_fema,
		style_function=fema_damage_layer_style_function, 
		control=True,
		highlight_function=fema_damage_highlight_function, 
		smooth_factor=0.1,
		tooltip=folium.features.GeoJsonTooltip(
			fields=['county', 'fips_code','totalDamage_Summed'],
			aliases=['County: ', 'FIPS: ','FEMA Inspected Damage: '],
			style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
		)
	)

	feature_group_fema_damage.add_child( fema_damage_layer )




	# save the map

	folium.LayerControl().add_to(us_map_geojson)

	strMapFilename = "./maps/test/test_map_" + str(storm_year) + "_" + storm_name + ".html"

	us_map_geojson.save(outfile = strMapFilename)

	print("Saved to disk: " + strMapFilename)

	t1 = time.time()

	total = t1-t0

	print("Map Generation Time: " + str(total))




	return 0



def build_streamlit_folium_map(storm_conf, df_fema=None, df_geo_area_to_render=None):

	t0 = time.time()

	print("building folium map...")

	# create the map object

	us_map_geojson = folium.Map(location=storm_conf['storm_center'], zoom_start=6,tiles=None)
	folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(us_map_geojson) # CartoDB positron'




	# build the feature groups

	storm_name = storm_conf['name']
	storm_year = storm_conf['year']


	feature_group_storm_path = folium.FeatureGroup(name=(storm_name + ' ' + str(storm_year) + ' Storm Path'),overlay=True).add_to(us_map_geojson)


	feature_group_storm_wind_vmax_sustained = folium.FeatureGroup(name=(storm_name + ' ' + str(storm_year) + ' VMAX Sustained'),overlay=False).add_to(us_map_geojson)
	feature_group_storm_wind_vmax_gusts = folium.FeatureGroup(name=(storm_name + ' ' + str(storm_year) + ' VMAX Gusts'),overlay=False).add_to(us_map_geojson)


	feature_group_storm_distance = folium.FeatureGroup(name=(storm_name + ' ' + str(storm_year) + ' Storm County Distance'),overlay=False).add_to(us_map_geojson)
	
	#feature_group_storm_wind_sustained_duration = folium.FeatureGroup(name=(storm_name + ' ' + str(storm_year) + ' Sustained Duration'),overlay=False).add_to(us_map_geojson)
	#feature_group_storm_wind_gust_duration = folium.FeatureGroup(name=(storm_name + ' ' + str(storm_year) + ' Gust Duration'),overlay=False).add_to(us_map_geojson)

	feature_group_storm_flood_exposure = folium.FeatureGroup(name=(storm_name + ' ' + str(storm_year) + ' Flood Exposure'),overlay=False).add_to(us_map_geojson)





	# build some layers

	# 1. build the storm distance layer


	storm_distance_colormap = branca.colormap.LinearColormap(colors=['#003302', '#237526', '#ffffff'], index=[10, 50, 175],vmin=0,vmax=400)

	def storm_distance_layer_style_function(feature):
		storm_value = feature["properties"]['storm_dist'] #.isnull()

		if (feature["properties"]['storm_dist'] is None):

			return {
				'fillColor': '#eeeeee', 
				'color':'#000000', 
				'fillOpacity': 0.4, 
				'weight': 0.1
			}
		else:
			# nothing really
			a=0

		float_value = float(storm_value)


		return {
			'fillColor': """{fv}""".format( fv = storm_distance_colormap.rgb_hex_str(float_value) ), 
			'color':'#000000', 
			'fillOpacity': 0.8, 
			'weight': 0.1
		}

	storm_dist_highlight_function = lambda x: {'fillColor': '#000000', 
		'color':'#000000', 
		'fillOpacity': 0.50, 
		'weight': 0.1
		}


	storm_dist_base_layer = folium.features.GeoJson(
		data=df_geo_area_to_render,
		style_function=storm_distance_layer_style_function, 
		control=True,
		highlight_function=storm_dist_highlight_function, 
		smooth_factor=0.1,
		tooltip=folium.features.GeoJsonTooltip(
			fields=['coty_name_long', 'coty_code','storm_dist'],
			aliases=['County: ', 'FIPS: ','Storm Distance: '],
			style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
		)
	)

	feature_group_storm_distance.add_child( storm_dist_base_layer )	

	# 2. build the [ Wind VMAX Sustained ] layer


	storm_vmax_sustained_layer_colormap = branca.colormap.LinearColormap(colors=['#ffffff', '#ff0000', '#630000'], index=[14, 25, 35],vmin=0,vmax=35)

	def storm_vmax_sustained_layer_style_function(feature):
		storm_value = feature["properties"]['vmax_sust'] #.isnull()

	  #print(pre_storm_avg_admissions)

		if (feature["properties"]['vmax_sust'] is None):

			return {
				'fillColor': '#eeeeee', 
				'color':'#000000', 
				'fillOpacity': 0.4, 
				'weight': 0.1
				}
		else:
			# nothing really
			a=0

		float_value = float(storm_value)


		return {
			'fillColor': f'{storm_vmax_sustained_layer_colormap.rgb_hex_str(float_value)}', 
			'color':'#000000', 
			'fillOpacity': 0.8, 
			'weight': 0.1
			}

	storm_vmax_sustained_highlight_function = lambda x: {'fillColor': '#000000', 
		'color':'#000000', 
		'fillOpacity': 0.50, 
		'weight': 0.1}


	storm_vmax_sustained_layer = folium.features.GeoJson(
		data=df_geo_area_to_render,
		style_function=storm_vmax_sustained_layer_style_function, 
		control=True,
		highlight_function=storm_vmax_sustained_highlight_function, 
		smooth_factor=0.1,
		tooltip=folium.features.GeoJsonTooltip(
			fields=['coty_name_long', 'coty_code','vmax_sust'],
			aliases=['County: ', 'FIPS: ','VMAX Sustained: '],
			style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
		)
	)

	feature_group_storm_wind_vmax_sustained.add_child( storm_vmax_sustained_layer )





	# 3. build the [ vmax wind gusts ] layer


	# feature_group_storm_wind_vmax_gusts


	storm_vmax_gusts_layer_colormap = branca.colormap.LinearColormap(colors=['#ffffff', '#ff0000', '#630000'], index=[15, 35, 55],vmin=0,vmax=55)

	def storm_vmax_gusts_layer_style_function(feature):
		storm_value = feature["properties"]['vmax_gust'] #.isnull()

		if (feature["properties"]['vmax_gust'] is None):

			return {
				'fillColor': '#eeeeee', 
				'color':'#000000', 
				'fillOpacity': 0.4, 
				'weight': 0.1
			}
		else:
			# nothing really
			a=0

		float_value = float(storm_value)

		return {
			'fillColor': f'{storm_vmax_gusts_layer_colormap.rgb_hex_str(float_value)}', 
			'color':'#000000', 
			'fillOpacity': 0.8, 
			'weight': 0.1
		}

	storm_vmax_gusts_highlight_function = lambda x: {'fillColor': '#000000', 
		'color':'#000000', 
		'fillOpacity': 0.50, 
		'weight': 0.1}


	storm_vmax_GUSTS_layer = folium.features.GeoJson(
		data=df_geo_area_to_render,
		style_function=storm_vmax_gusts_layer_style_function, 
		control=True,
		highlight_function=storm_vmax_gusts_highlight_function, 
		smooth_factor=0.1,
		tooltip=folium.features.GeoJsonTooltip(
			fields=['coty_name_long', 'coty_code','vmax_gust'],
			aliases=['County: ', 'FIPS: ','VMAX Gusts: '],
			style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
		)
	)

	feature_group_storm_wind_vmax_gusts.add_child( storm_vmax_GUSTS_layer )






	# N. build the [ Flood Exposure ] layer


	storm_flood_layer_colormap = branca.colormap.LinearColormap(colors=['#ffffff', '#0000ff'], index=[0, 1],vmin=0,vmax=1)

	def storm_flood_layer_style_function(feature):
		storm_value = feature["properties"]['flood_exposure'] #.isnull()

		if ((feature["properties"]['flood_exposure'] is None) | (feature["properties"]['flood_exposure'] == False)):

			return {
			'fillColor': '#eeeeee', 
			'color':'#000000', 
			'fillOpacity': 0.4, 
			'weight': 0.1
			}
		else:
			# nothing really
			a=0

		float_value = float(storm_value)

		return {
			'fillColor': f'{storm_flood_layer_colormap.rgb_hex_str(1)}', 
			'color':'#000000', 
			'fillOpacity': 0.4, 
			'weight': 0.1
		}

	storm_flood_highlight_function = lambda x: {'fillColor': '#000000', 
		'color':'#000000', 
		'fillOpacity': 0.50, 
		'weight': 0.1}


	storm_flood_layer = folium.features.GeoJson(
		data=df_geo_area_to_render,
		style_function=storm_flood_layer_style_function, 
		control=True,
		highlight_function=storm_flood_highlight_function, 
		smooth_factor=0.1,
		tooltip=folium.features.GeoJsonTooltip(
			fields=['coty_name_long', 'coty_code','flood_exposure'],
			aliases=['County: ', 'FIPS: ','Flood Exposure: '],
			style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
		)
	)

	feature_group_storm_flood_exposure.add_child( storm_flood_layer )	



	# save the map

	folium.LayerControl().add_to(us_map_geojson)

	#strMapFilename = "./maps/test/test_map_" + str(storm_year) + "_" + storm_name + ".html"

	#us_map_geojson.save(outfile = strMapFilename)

	#print("Saved to disk: " + strMapFilename)

	t1 = time.time()

	total = t1-t0

	print("Map Generation Time: " + str(total))




	return us_map_geojson	