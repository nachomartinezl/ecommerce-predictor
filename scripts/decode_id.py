import sys
sys.path.append("/home/app/src/ecommerce-predictor/")
import json

# Store json file
with open("data/products.json") as f:
    products_dicts = json.load(f)

# Create a dictionary that maps ids with names
mapping_dict = {}
for dic in products_dicts:
    for cat in dic["category"]:
        mapping_dict[cat["id"]] = cat["name"]
        
def decode_id(id_or_path: str or list):
    # Return product name if just one id was passed
    if type(id_or_path) == str:
        return mapping_dict[id_or_path]
    
    path = []
    # Return a list of names if a path was passed
    if type(id_or_path) == list:
        for id in id_or_path:
            if id != "":
                path.append(mapping_dict[id])
        return path
    