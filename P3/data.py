#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSM_FILE = "dataset/vila_velha.osm"
street_type_re = re.compile(r'^\S+', re.IGNORECASE)

expected = ["Aeroporto","Alameda","Área","Avenida","Beco","Campo","Chácara","Colônia","Condomínio","Conjunto","Distrito","Escadaria","Esplanada","Estação","Estrada","Favela","Fazenda","Feira","Jardim","Ladeira","Lago","Lagoa","Largo","Loteamento","Morro","Núcleo","Parque","Passarela","Pátio","Praça","Quadra","Rampa","Recanto","Residencial","Rodovia","Rua","Setor","Sítio","Travessa","Trecho","Trevo","Vale","Vereda","Via","Viaduto","Viela","Vila"]

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit_street_types(osmfile):
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osmfile, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types

st_types = audit_street_types(OSM_FILE)

pprint.pprint(st_types)


# Some street types were fixed using a dict mapping.

mapping = { "Rod": "Rodovia",
            "Rod.": "Rodovia",
            "RODOVIA": "Rodovia",
            "Praca": "Praça",
            "ESTRADA": "Estrada",
            "FAZENDA": "Fazenda"}

print('\nMapping:\n')
pprint.pprint(mapping)

def update_street_type(name, mapping):
    """Fixes the street type (i.e the first word) of a street using a dict mapping. 
    For example, if name == "Rod. BR-101" and mapping == {"Rod" : "Rodovia"}, this function returns "Rodovia BR-101"
    Args:
        name: the street name.
        mapping: the dict mapping used to fix the street types
        
    Returns:
        the street name replacing the street type by its corrected version.
    """
    m = street_type_re.search(name)
    if m:
        t = m.group()
        if t in mapping:
            return street_type_re.sub(mapping[t], name) 
    return name

print('\nResults after fixing the streets:\n')
# validate if the function is working correctly
for st_type, ways in st_types.items():
    for name in ways:
        fixed = update_street_type(name, mapping)
        if name != fixed:
            print("{} => {}".format(name, fixed))


# ### 2. Zip Codes
# Brazilian zip code is called CEP and uses the format 00000-000. Also, acording to [Correios](http://www.correios.com.br/) web site, the range of valid zip codes for Vila Velha is between 29100-001 to 29129-999.

zipcode_re = re.compile(r'^\d{5}\-\d{3}$')
digits_re = re.compile(r'\d+')

def extract_digits(str):
    digits = digits_re.findall(str)
    s = ""
    for d in digits:
        s += d
    
    return int(s)

def is_zipcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit_zipcode(invalid_zipcodes, zipcode):
    m = zipcode_re.search(zipcode)
    if m is None:
        invalid_zipcodes.add(zipcode)     

def audit_zipcode_range(zipcodes_out_of_range, zipcode):
    digits = extract_digits(zipcode)
    if digits < 29101001 or digits > 29129999:
        zipcodes_out_of_range.add(zipcode)

def audit_zipcodes(osmfile):
    invalid_zipcodes = set()
    zipcodes_out_of_range = set()
    for event, elem in ET.iterparse(osmfile, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_zipcode(tag):
                    audit_zipcode(invalid_zipcodes, tag.attrib['v'])
                    audit_zipcode_range(zipcodes_out_of_range, tag.attrib['v'])
    
    return invalid_zipcodes, zipcodes_out_of_range

invalid_zipcodes, zipcodes_out_of_range = audit_zipcodes(OSM_FILE)

print("Zip codes with invalid format:")
pprint.pprint(invalid_zipcodes)
print("\nNumber of zip codes out of range: {}".format(len(zipcodes_out_of_range)))


# The zip codes were standardized to the CEP format and checked if it's within the valid range. For example:

def update_zipcode(zipcode):
    digits = extract_digits(zipcode)
    if digits < 29101001 or digits > 29129999:
        return None
    else:
        fst_part = int(digits / 1000)
        snd_part = round((digits/1000 - fst_part) * 1000)
        return "{}-{}".format(fst_part, snd_part)

# validate if the function is working correctly
for invalid in invalid_zipcodes:
    print("{} => {}".format(invalid, update_zipcode(invalid)))


# ### Reshape Data to JSON
# To be able to import the data into MongoDB, the data had to be reshaped from XML to JSON format. The following rules were applied:
# * process only 2 types of top level tags: "node" and "way"
# * all attributes of "node" and "way" should be turned into regular key/value pairs, except:
#     - attributes in the CREATED array should be added under a key "created"
#     - attributes for latitude and longitude should be added to a "pos" array,
#       for use in geospacial indexing. Make sure the values inside "pos" array are floats
#       and not strings. 
# * if the second level tag "k" value contains problematic characters, it should be ignored
# * if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
# * if the second level tag "k" value does not start with "addr:", but contains ":", you can
#   process it in a way that you feel is best. For example, you might split it into a two-level
#   dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
# * if there is a second ":" that separates the type/direction of a street,
#   the tag should be ignored, for example:
# 
# ```xml
# <tag k="addr:housenumber" v="5158"/>
# <tag k="addr:street" v="North Lincoln Avenue"/>
# <tag k="addr:street:name" v="Lincoln"/>
# <tag k="addr:street:prefix" v="North"/>
# <tag k="addr:street:type" v="Avenue"/>
# <tag k="amenity" v="pharmacy"/>
# ```
# 
# should be turned into:
# 
# ```json
# {...
# "address": {
#     "housenumber": 5158,
#     "street": "North Lincoln Avenue"
# }
# "amenity": "pharmacy",
# ...
# }
# ```
# 
# - for "way" specifically:
# 
#   <nd ref="305896090"/>
#   <nd ref="1719825889"/>
# 
# should be turned into
# ```json
# "node_refs": ["305896090", "1719825889"]
# ```

# In[6]:

import xml.etree.cElementTree as ET
import pprint
import re
import io
import json

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
ADDRESS_TAGS = ["housenumber", "postcode", "street", "city", "place", "state"]

def shape_element(element):
    
    if element.tag == "node" or element.tag == "way" :
        node = {"type" : element.tag}

        # process the attributes
        for k, v in element.attrib.items():
            
            # created
            if k in CREATED:
                if "created" not in node:
                    node["created"] = {}
                node["created"][k] = v
            
            # others
            elif k != "lat" and k != "lon":
                node[k] = v

        # special attribute location
        if element.tag == "node":
            node["pos"] = [float(element.attrib["lat"]), float(element.attrib["lon"])]

        # process the 2nd level tags
        for tag in element.iter("tag"):
            
            k = tag.attrib["k"]
            v = tag.attrib["v"]

            if problemchars.search(k):
                continue

            if is_zipcode(tag):
                v = update_zipcode(v)
            elif is_street_name(tag):
                v = update_street_type(v, mapping)

            # tags that contains ":"
            split = k.split(":")
            if len(split) == 1:
                node[k] = v

            elif len(split) == 2:

                outer = split[0]
                inner = split[1]

                # address
                if outer == "addr":
                    if inner not in ADDRESS_TAGS:
                        continue
                    
                    outer = "address"
                    
                    if outer not in node:
                        node[outer] = {}
                        
                    node[outer][inner] = v
                else:
                    node[outer + "_" + inner] = v                
        
        # process node references
        for nd in element.iter("nd"):
            ref = nd.attrib["ref"]
            if "node_refs" not in node:
                node["node_refs"] = []
            node["node_refs"].append(ref)


        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    with io.open(file_out, "w", encoding="utf-8") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                indent = None
                if pretty:
                    indent = 2

                fo.write(json.dumps(el, indent=indent, ensure_ascii=False)+"\n")


if __name__ == "__main__":
    process_map(OSM_FILE, False)


