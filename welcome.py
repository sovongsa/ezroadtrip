
import os
from flask import Flask, jsonify,request
from flask import Flask
import requests
import json
import pandas as pd,numpy as np
from sklearn.cluster import DBSCAN
from random import randint
app = Flask(__name__)

@app.route('/myapp')
def WelcomeToMyapp():
    params = {
       "waypoint0":"52.5214,13.4155",
       "waypoint1":"52.4352,13.5053",
        "mode":"fastest;car",
        "alternatives":"4",
        "app_id":"DemoAppId01082013GAL",
        "app_code":"AJKnXv84fjrb0KIHawS0Tg"
    }
    response = requests.get(url="https://route.cit.api.here.com/routing/7.2/calculateroute.json",params=params)
    return response.content


CAT = "camping"
WIDTH=2000
SIZE = 1000
APP_ID=""
APP_CODE=""
@app.route('/apis/places/<startLat>/<startLon>/<desLat>/<desLon>')
def getTopPlaces(startLat,startLon,desLat,desLon):

    url ="https://route.cit.api.here.com/routing/7.2/calculateroute.json"
    params ={
        "waypoint0":"{0},{1}".format(startLat,startLon),
        "waypoint1":"{0},{1}".format(desLat,desLon),
        "mode":"fastest;car;traffic:enabled",
        "app_id": APP_ID,
        "app_code": APP_CODE
    }
    response = json.loads(requests.get(url,params).content)
    position_list =[  maneuver['position'] for maneuver in response['response']['route'][0]['leg'][0]['maneuver']]

    route ="["
    i = 0;
    for position_map in position_list:
        route += "{0},{1}".format(position_map['latitude'],position_map['longitude'])
        if(i<len(position_list)-1):
            route += "|"
            i = i+1
    route +="]"


    url = "https://places.demo.api.here.com/places/v1/browse/by-corridor/"
    params ={
        "route":route+";w={0}".format(WIDTH),
        "cat":CAT,
        "size":SIZE,
        "pretty":True,
        "app_id": APP_ID,
        "app_code": APP_CODE

    }
    response = json.loads(requests.get(url, params=params).content)
    place_list =[]
    for place in response['results']['items']:
        rating,place_id,address = getPlaceRating(place['title'])
        item ={
            "id":place['id'],
            "position":place['position'],
            "title":place['title'],
            "rating":rating,
            "place_id":place_id,
            "address":address,
            "thingstodo":"list all the activies and cost",
            "duration":"People typically spend up to {0} hours here".format(randint(1,13)),
            "fee":"One day Park fee: {0}$".format(randint(10,50))
        }
        place_list.append(item)
    return_cluster_list = getPlacesCluster(place_list)
    final_list =[]
    for cluster in return_cluster_list:
        sort_list = sorted(cluster,key=lambda cluster:cluster['rating'])
        final_list.append(sort_list[0])


    return json.dumps(final_list)

def getPlaceRating(name):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params ={
        "query":name,
        "key":""
    }
    place = json.loads(requests.get(url,params).content)
    place_id= "" if (place['status']=='ZERO_RESULTS' or 'place_id' not in place['results'][0]) else place['results'][0]['place_id']
    rating = 0 if  (place['status']=='ZERO_RESULTS' or 'rating' not in place['results'][0]) else place['results'][0]['rating']
    address= "" if (place['status']=='ZERO_RESULTS' or 'formatted_address' not in place['results'][0]) else place['results'][0]['formatted_address']

    return rating,place_id,address

def getPlacesCluster(place_list):
    df = pd.DataFrame()
    df['lat']= [place['position'][0] for place in place_list]
    df['lng'] =[place['position'][1] for place in place_list]
    coords = df.as_matrix(columns=['lat', 'lng'])

    epsilon = 0.08
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    cluster_labels = db.labels_
    num_clusters = len(set(cluster_labels))
    clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])
    index = 0
    return_cluster_list=[]
    return_cluster=[]
    for cluster in clusters:
        for place in cluster:
            return_cluster.append(place_list[index])
            index = index+1
        return_cluster_list.append(return_cluster)
        return_cluster=[]
    return return_cluster_list

port = os.getenv('PORT', '5555')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
