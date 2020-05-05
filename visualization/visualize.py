from folium import plugins, LayerControl, FeatureGroup, Marker
import pandas as pd
import webbrowser
import folium
import json
import sample

#https://morioh.com/p/d896544d6977
#https://www.storybench.org/how-to-build-a-heatmap-in-python/

# should take longitude latitude data
def heatmap(name):
    df = pd.read_csv("sampleCoords.csv")
    with open('nyczip.geojson') as f: nycArea = json.load(f)
    folium.GeoJson(nycArea).add_to(nyMap)
    for i, row in df.iterrows():
        folium.CircleMarker((row.latitude, row.longitude), radius=3, weight=2, color='red', \
                            fill_color='red', fill_opacity=.5)
    nyMap.add_child(plugins.HeatMap(data=df[['latitude', 'longitude']].values, radius=24, blur=10))


# should take zipcode data, black on the map=essentials
def choropleth(map, name, legend, dataset):
    choro = None
    if dataset != None:
        choro = pd.DataFrame()
        choro['zip'] = dataset[0].astype(str)
        choro['essentials'] = dataset[1]        
    else:
        choro = sample.generateSampleZips()  
    cLayer = folium.Choropleth(geo_data='nyczip.geojson', data=choro, columns=['zip', 'essentials'], \
                        key_on='feature.properties.postalCode', fill_color='OrRd', fill_opacity=.7, \
                        legend_name=legend)
    map.add_child(cLayer)
    cLayer.layer_name = name

def show(map):
    LayerControl(collapsed=False).add_to(map)
    map.save('nycLayering.html')
    webbrowser.open('nycLayering.html')
