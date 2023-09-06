import streamlit as st
import folium
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tempfile
from io import BytesIO
import requests
from streamlit_folium import st_folium## Create a Folium map

def severe_weather_map(address,distance,start_year, end_year):
    latlng = geocode(address)

    d2=distance
    lat,lon=latlng
    latsc=1/69.03
    lonsc=1/(69.03*np.cos(np.deg2rad(lat)))
    if d2<=10: Zoom_Start_val=11
    elif d2<=20: Zoom_Start_val=10
    elif d2<=40: Zoom_Start_val=9
    elif d2<=100: Zoom_Start_val=8
    elif d2<=150: Zoom_Start_val=7
    else: Zoom_Start_val=6

    # base map
    map_ = folium.Map(location=latlng, zoom_start=Zoom_Start_val, prefer_canvas=True)
    folium.Marker(latlng, popup=folium.Popup(location=latlng, parse_html=True)).add_to(map_)
    (folium.CircleMarker(latlng,
                         popup=folium.Popup(location=latlng, parse_html=True),
                         radius=5,
                         color='#3186cc',
                         fill_color='#3186cc')
     .add_to(map_))

    # circle marker at address
    (folium.CircleMarker(latlng,
                         popup=folium.Popup(location=latlng, parse_html=True),
                         radius=5,
                         color='#000000',
                         fill_color='#000000')
     .add_to(map_))


    # ******************** wind **************************
    #print(f'{lat1} N, {lon1} E')
    dfw=pd.read_csv('1955-2022_wind.csv', usecols=['date','yr','slat','slon','mag'])
    dfw[dfw['mag']==-9]=0
    dfw['val_name']=(dfw['yr'].astype(str) + ' Wind Speed: ' +(dfw['mag']*1.15).astype(int).astype(str) +' mph') 
    td2w=dfw[(dfw['slat']>=lat-d2*latsc) & (dfw['slat']<=lat+d2*latsc) & 
             (dfw['slon']>=lon-d2*lonsc) & (dfw['slon']<=lon+d2*lonsc) & (dfw['mag']>=0) &
             (dfw['yr']>=start_year) & (dfw['yr']<=end_year)]

    feature_groupw=folium.FeatureGroup("Wind Events")
    for lata, lnga, namea in zip(td2w['slat'].tolist(), td2w['slon'].tolist(), 
                                 td2w['val_name'].tolist()  ):
        feature_groupw.add_child(folium.CircleMarker(location=[lata,lnga],popup=namea,radius=2,
                         color='#222222',
                         fill_color=False ))
    map_.add_child(feature_groupw)

    # ******************** Hail **************************
    dfh=pd.read_csv('1955-2022_hail.csv', usecols=['date','yr','slat','slon','mag'])
    dfh[dfh['mag']==-9]=0
    dfh['val_name']=(dfh['yr'].astype(str) + ' hail size: ' +dfh['mag'].astype(str) +' in') 
    td2h=dfh[(dfh['slat']>=lat-d2*latsc) & (dfh['slat']<=lat+d2*latsc) & 
             (dfh['slon']>=lon-d2*lonsc) & (dfh['slon']<=lon+d2*lonsc) & (dfh['mag']>=0) &
             (dfh['yr']>=start_year) & (dfh['yr']<=end_year)]

    feature_grouph=folium.FeatureGroup("Hail Events")
    for lata, lnga, namea in zip(td2h['slat'].tolist(), td2h['slon'].tolist(), 
                                 td2h['val_name'].tolist()  ):
        feature_grouph.add_child(folium.CircleMarker(location=[lata,lnga],popup=namea,radius=2,
                         color='#ff4a44',
                         fill_color='#ff4a44' ))
    map_.add_child(feature_grouph)


    # ********************* Tornadoes *********************
    dft=pd.read_csv('1950-2022_torn.csv', usecols=['date','yr','slat','slon','mag'])
    dft[dft['mag']==-9]=0
    dft['val_name']=(dft['yr'].astype(str) + ' EF-' + dft['mag'].astype(str)) 
    td2t=dft[(dft['slat']>=lat-d2*latsc) & (dft['slat']<=lat+d2*latsc) & 
             (dft['slon']>=lon-d2*lonsc) & (dft['slon']<=lon+d2*lonsc) & (dft['mag']>=0) &
             (dft['yr']>=start_year) & (dft['yr']<=end_year)]

    feature_group=folium.FeatureGroup("Tornadoes")
    for lata, lnga, namea in zip(td2t['slat'].tolist(), td2t['slon'].tolist(), 
                                 td2t['val_name'].tolist()  ):
        feature_group.add_child(folium.CircleMarker(location=[lata,lnga],popup=namea,radius=5,
                         color='#3186cc',
                         fill_color='#3186cc',linewidth=.5, opacity=0.6 ))
    map_.add_child(feature_group)

    #******************* add selectible layer legend to map *******************
    folium.LayerControl(collapsed=False).add_to(map_)

    
    
    #show map
    return map_
## geocode gives the lat and lon
def geocode(address):
    params = {'format': 'json', 
              'addressdetails': 1,
              'q': address}
    
    # Need to supply a user agent other than the default provided
    # by requests for the API to accept the query.
    headers = {'user-agent': 'TDI'}   
                                      
    r = requests.get('http://nominatim.openstreetmap.org/search', params=params, headers=headers).json()
    return (float(r[0]['lat']), float(r[0]['lon']))

