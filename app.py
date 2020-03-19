from flask import Flask,render_template,request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import six
import googlemaps 
import pandas as pd
pd.options.display.max_columns = 500



app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return closest(processed_text)

@app.route('/')
def closest(address):
    stations=pd.read_csv("stations.csv")
    stations["Station Dist from House"]=2.4
    stations["Station time from House"]=2.3
    stations['Train Time']=stations['Train Time'].astype(float)
    stations['Total Time']="p"
    stations['tt']=2.4
    stations['House Address']="p"
    house = address
    gmaps = googlemaps.Client(key='AIzaSyBG8HCd78PAIOVh0_gB5OAAw3lcZ19Ixtk') 
    for i in range(0,len(stations)):
        try:
            station= stations["Station"][i]
            gott = gmaps.distance_matrix(house,station +  " Station, " + station +  ", NJ"  )['rows'][0]['elements'][0] 
            stations.at[i, 'House Address'] =house
            stations.at[i, 'Station Dist from House'] =round(gott['distance']['value']*0.000621371)
            stations.at[i, 'Station time from House'] =round((gott['duration']['value']/3600)*60,2)
            stations.at[i, 'Total Time']=round(stations.at[i, 'Station time from House']+stations.at[i, 'Train Time'],2)
            stations.at[i, 'tt']=stations.at[i, 'Station time from House']+stations.at[i, 'Train Time']
        except: pass
    return stations.nsmallest(15,'tt').iloc[:,[8,0,1,6,2,5,4,3]].to_html(classes='female')


    

if __name__ == '__main__':
    app.run(debug=True)
