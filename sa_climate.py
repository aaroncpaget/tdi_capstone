import numpy as np
import matplotlib.pyplot as plt
import requests

# Create a climate plots
def show_address_climate(s1):
    s1=str(s1)
    lat_in, lon_in=geocode_latlon(s1)
    if lat_in< 24.5 or lat_in > 49.4 or lon_in < -124.8 or lon_in > -67.1:
        return print("location exceeds limits")

#    load the data and find the indices for the lat and lon from the geotiles
    bin_edges=np.arange(-125,-64,4)
    print(bin_edges)
    fn_list=['nclimgrid_stats_monthly_slim_(-125--121).npz',
         'nclimgrid_stats_monthly_slim_(-121--117).npz',
         'nclimgrid_stats_monthly_slim_(-117--113).npz',
         'nclimgrid_stats_monthly_slim_(-113--109).npz',
         'nclimgrid_stats_monthly_slim_(-109--105).npz',
         'nclimgrid_stats_monthly_slim_(-105--101).npz',
         'nclimgrid_stats_monthly_slim_(-101--97).npz',
         'nclimgrid_stats_monthly_slim_(-97--93).npz',
         'nclimgrid_stats_monthly_slim_(-93--89).npz',
         'nclimgrid_stats_monthly_slim_(-89--85).npz',
         'nclimgrid_stats_monthly_slim_(-85--81).npz',
         'nclimgrid_stats_monthly_slim_(-81--77).npz',
         'nclimgrid_stats_monthly_slim_(-77--73).npz',
         'nclimgrid_stats_monthly_slim_(-73--69).npz',
         'nclimgrid_stats_monthly_slim_(-69--65).npz']
    if (lon_in>=bin_edges[0]) & (lon_in<bin_edges[1]): fn_ind=0
    elif (lon_in>=bin_edges[1]) & (lon_in<bin_edges[2]): fn_ind=1
    elif (lon_in>=bin_edges[2]) & (lon_in<bin_edges[3]): fn_ind=2
    elif (lon_in>=bin_edges[3]) & (lon_in<bin_edges[4]): fn_ind=3
    elif (lon_in>=bin_edges[4]) & (lon_in<bin_edges[5]): fn_ind=4
    elif (lon_in>=bin_edges[5]) & (lon_in<bin_edges[6]): fn_ind=5
    elif (lon_in>=bin_edges[6]) & (lon_in<bin_edges[7]): fn_ind=6
    elif (lon_in>=bin_edges[7]) & (lon_in<bin_edges[8]): fn_ind=7
    elif (lon_in>=bin_edges[8]) & (lon_in<bin_edges[9]): fn_ind=8
    elif (lon_in>=bin_edges[9]) & (lon_in<bin_edges[10]): fn_ind=9
    elif (lon_in>=bin_edges[10]) & (lon_in<bin_edges[11]): fn_ind=10
    elif (lon_in>=bin_edges[11]) & (lon_in<bin_edges[12]): fn_ind=11
    elif (lon_in>=bin_edges[12]) & (lon_in<bin_edges[13]): fn_ind=12
    elif (lon_in>=bin_edges[13]) & (lon_in<bin_edges[14]): fn_ind=13
    elif (lon_in>=bin_edges[14]) & (lon_in<bin_edges[15]): fn_ind=14
    else: return print("location exceeds limits")

    data=np.load(fn_list[fn_ind])
#    data=np.load('nclimgrid_stats_monthly_slim.npz') #file was to big
    lat=data['lat']
    lon=data['lon']

    p_mean=data['p_mean']
    tavg_mean=data['tavg_mean']
    tmin_mean=data['tmin_mean']
    tmax_mean=data['tmax_mean']
    p_mask=data['p_mask']
    indlat=find_nearest_ind(lat,lat_in)
    indlon=find_nearest_ind(lon,lon_in)
#    create the plot for the given location
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    fig1, (ax1,ax2)=plt.subplots(1,2,layout='constrained')
    ax2.bar(months,np.squeeze(p_mean[:,indlat,indlon]*0.0393701))
    ax2.set_title('Average Monthly Precipitation')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Total Precipitation (in)')
    
    ax1.plot(months,np.squeeze(tmax_mean[:,indlat,indlon]*9/5+32),linestyle='-',color='r',label='Average High')
    ax1.plot(months,np.squeeze(tmin_mean[:,indlat,indlon]*9/5+32),linestyle='-',color='b',label='Average Low')
    ax1.plot(months,np.squeeze(tavg_mean[:,indlat,indlon]*9/5+32),linestyle='--',color='k',label='Average Temperature')
    ax1.legend()
    ax1.set_ylim([np.min(np.squeeze(tmin_mean[:,indlat,indlon])*9/5+32)*0.9, 1.2*np.max(np.squeeze(tmax_mean[:,indlat,indlon])*9/5+32)])
    ax1.set_title('Monthly Average Temperatures')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Temperature (°F)')
    for label in ax1.get_xticklabels() + ax2.get_xticklabels():
        label.set_rotation(90)
        label.set_ha('center')
#    plt.show()
    return fig1
    
def find_nearest_ind(array,value):
    array=np.asarray(array)
    idx=(np.abs(array-value)).argmin()
    return idx

def geocode_latlon(address):
    params = { 'format'        :'json', 
              'addressdetails': 1, 
               'q'             : address}
    headers = { 'user-agent'   : 'TDI' }   #  Need to supply a user agent other than the default provided 
                                           #  by requests for the API to accept the query.
    response=requests.get('http://nominatim.openstreetmap.org/search', params=params, headers=headers)
    latval=response.json()[0]['lat']
    lonval=response.json()[0]['lon']
    return [float(latval), float(lonval)]
