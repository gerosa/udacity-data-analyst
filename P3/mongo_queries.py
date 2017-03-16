
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pprint
from pymongo import MongoClient

OSM_FILE = "dataset/vila_velha.osm"
json_file = OSM_FILE + '.json' 

print("The OSM file is {:4.2f} MB".format(os.path.getsize(OSM_FILE)/1.0e6)) # convert from bytes to megabytes
print("The JSON file is {:4.2f} MB".format(os.path.getsize(json_file)/1.0e6)) # convert from bytes to megabytes


db_name = 'openstreetmap'

# Connect to MongoDB
client = MongoClient('localhost:27017')
db = client[db_name]

# ### Number of documents
print(db.vv.find().count())


# ### Number of nodes
print(db.vv.find({"type":"node"}).count())


# ### Number of ways
print(db.vv.find({"type":"way"}).count())


# ### Number of unique users
print(len(db.vv.distinct("created.user")))


# ### Top 10 contributing user
top = db.vv.aggregate([
    {"$group" : {"_id" : "$created.user", "count" : {"$sum" : 1}}},
    {"$sort" : {"count": -1}},
    {"$limit" : 10}])

pprint.pprint((list(top)))


# ## Additional Ideas

# ### Top 5 most popular cuisines

top = db.vv.aggregate([
                   {"$match" : {"amenity":"restaurant"}},
                   {"$group" : {"_id" : "$cuisine", "count" : {"$sum" : 1}}},
                   {"$sort" : {"count" : -1}},
                   {"$limit": 5}])
pprint.pprint(list(top))


# ### Improving cuisine information

cuisines = list(db.vv.aggregate([
                   {"$match" : {"amenity":"restaurant"}},
                   {"$group" : {"_id" : "$cuisine", "count" : {"$sum" : 1}}},
                   {"$sort" : {"count" : -1}}]))

total = sum([c["count"] for c in cuisines])

print("\nRestaurants without cuisine defined: {:4.2f}%".format(cuisines[0]['count'] / total * 100))


# As can be observed, more than 40% of the restaurants don't have the cuisine field defined. This is an issue if this dataset would be used, for instance, by a restaurant recommendation app.
# 
# One way to improve the quality of the dataset is to try to infer the cuisine from the restaurant name. For example, if the restaurant has "Natural" on its name, we could infer it's a vegetarian restaurant.

query = {"amenity":"restaurant", "cuisine": {"$exists" : 0}, "name": {"$exists" : 1}}
projection = {"_id" : 0, "name" : 1}
restaurants_without_cuisine = [r["name"] for r in db.vv.find(query, projection)]

name_cuisine_mapping = {
    "Grelhados" : "steak_house",
    "Natural" : "vegetarian",
    "Outback" : "steak_house",
    "Vegetariano" : "vegetarian",
    "Caranguejo" : "seafood",
    "Burger" : "burger",
    "Steakhouse" : "steak_house",
    "Ondas" : "seafood",
    "Mar" : "seafood",
    "Terra": "vegetarian"}
print('Mapping:\n')
pprint.pprint(name_cuisine_mapping)


print('\nCuisines inferred from the restaurant\'s name:\n')
for name in restaurants_without_cuisine:
    for k, v in name_cuisine_mapping.items():
        if k in name:
            print("{} => {}".format(name, v))

