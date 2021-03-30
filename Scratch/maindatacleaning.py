# Import packages
from datetime import datetime, timedelta, date
from . import script
import json
import csv
import numpy as np
import pandas as pd

#Files 
survey_json = "SurveyDataMarch3.json"
environmental_json = "HistoryEnvironmentalHealthMarch3.json"

def clean_api_code():

    #Open Files 
    with open(survey_json,encoding="utf8") as file:
        data = json.load(file)
    survey_df = pd.json_normalize(data['results'])

    with open(environmental_json,encoding="utf8") as file:
        data = json.load(file)
    environmental_df = pd.json_normalize(data['results'])

    # Clean Survey Data 

    survey_df, environmental_df = script.initial_filter(survey_df,environmental_df)
    survey_df, environmental_df = script.clean_values(survey_df,environmental_df)
    survey_df, environmental_df = script.city_matching(survey_df,environmental_df)    #houseownership
    survey_df, environmental_df = script.map_formatting(survey_df,environmental_df)    
    survey_df, environmental_df = script.geo_clean(survey_df,environmental_df)


    return(df)

