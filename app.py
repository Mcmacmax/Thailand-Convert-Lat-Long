# -*- coding: utf-8 -*-
# import os, sys
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import datetime
from flask import Flask, jsonify, redirect, url_for, request, render_template 

start_datetime = datetime.datetime.now()
print (start_datetime,'execute')



def convert(inputlat,inputlong) :    
    try:
        inputlat = float(inputlat)
        inputlong = float(inputlong)
    except:
        return ("ตรวจสอบ Lat กับ Long")

    d = {'Lat': [inputlat], 'Long': [inputlong]}
    df = pd.DataFrame(data=d)
    
    #---------------------INPUT SHAPE---------------------
    # Importing Thailand ESRI Shapefile 
    th_boundary = gpd.read_file('./SHAPE/TH_tambon_boundary.shp')
    #---------------------Read POINT---------------------
    
    cvm_geo = [Point(xy) for xy in zip(df['Long'],df['Lat'])]
    df = gpd.GeoDataFrame(df, geometry = cvm_geo)
    df.set_crs(epsg=4326, inplace=True)
    df = df.to_crs(epsg=32647)
    #cvm_point.plot()
    
    #--------------------- Spatial Join------------------
    output = gpd.sjoin(df,th_boundary, how = 'inner', op = 'intersects')
    
    #---------------------- print output ------------------
    print(output['p_name_t'])
    if output['p_name_t'].empty :
        return ("lat กับ Long ของท่านไม่อยู่ในขอบเขตประเทศไทย")
    else:
        for x in output.values:
            Province = x[7]
            Aumphoe = x[9]
            Tambon = x[11]
            result = "จังหวัด : "+Province+ " อำเภอ : "+Aumphoe+" ตำบล : "+Tambon
        return (result)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload():
    if request.method == 'POST':
        data1 = request.form['Lat']
        data2 = request.form['Long']
        print(data1 , data2)
        return convert(data1,data2)
    return None

if __name__ == "__main__":
    app.run(debug=False)
