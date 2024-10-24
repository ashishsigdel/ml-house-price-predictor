import json
import pickle
import numpy as np
import os

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1
    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    return round(__model.predict([x])[0], 2)

def get_location_names():
    return __locations

def load_saved_artifacts():
    print("Loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model
    
    try:
        # Print current working directory
        print("Current working directory:", os.getcwd())
        
        # Print list of files in artifacts directory
        print("Files in artifacts directory:", os.listdir('./artifacts'))
        
        artifacts_path = os.path.join(os.getcwd(), 'artifacts')
        columns_path = os.path.join(artifacts_path, 'columns.json')
        model_path = os.path.join(artifacts_path, 'house_price_predict_model.pickle')
        
        print(f"Loading columns from: {columns_path}")
        with open(columns_path, 'r') as f:
            __data_columns = json.load(f)['data_columns']
            __locations = __data_columns[3:]
            print(f"Loaded {len(__locations)} locations")
        
        print(f"Loading model from: {model_path}")
        with open(model_path, 'rb') as f:
            __model = pickle.load(f)
        print("Loading saved artifacts...done")
        
    except Exception as e:
        print(f"Error loading artifacts: {str(e)}")
        # Initialize with empty values if loading fails
        __data_columns = []
        __locations = []
        __model = None
        raise e

# Optional: Call load_saved_artifacts when module is imported
try:
    load_saved_artifacts()
except Exception as e:
    print(f"Failed to load artifacts on import: {str(e)}")