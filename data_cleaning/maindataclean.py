# Import packages
import json
from . import script
import numpy as np
import pandas as pd
import math
import difflib

# Files
survey_json = "data/SurveyDataMarch3.json"
environmental_json = "data/HistoryEnvironmentalHealthMarch3.json"

def clean_data():
    # Open files 
    with open(survey_json, encoding="utf8") as file:
        data = json.load(file)
    survey_df = pd.json_normalize(data["results"])

    with open(environmental_json, encoding="utf8") as file:
        data = json.load(file)
    environmental_df = pd.json_normalize(data["results"])

    # Filter Data
    columns_to_keep = [
            "objectId",
            "fname",
            "lname",
            "nickname",
            "relationship",
            "sex",
            "dob",
            "telephoneNumber",
            "educationLevel",
            "occupation",
            "communityname",
            "city",
            "province",
            "insuranceNumber",
            "insuranceProvider",
            "clinicProvider",
            "cedulaNumber",
            "surveyingUser",
            "surveyingOrganization",
            "latitude",
            "longitude",
            "createdAt",
            "updatedAt",
        ]
    survey_df = script.filter_df(survey_df,columns_to_keep)

    # Create age column
    survey_df = survey_df.replace({np.nan: ""})
    survey_df["age"] = survey_df["dob"].apply(script.calculate_age)

    # Clean Survey adn Environmental Dataframes
    survey_replacements = {"educationLevel" : { "lessThanprimary\n" : "lessThanprimary"}}
    environmental_replacements = {"conditionoFloorinyourhouse" : { "dirtPoor" : "poor", "cementPoor" : "working","dirtWorking":"working","cementWorking":"good"},
                        "conditionoRoofinyourhouse":{"bad":"poor","normal":"working"},
                        "houseownership":{"owned":"Yes","rented":"No"},
                        "bathroomAccess":{"N":"No","Y":"Yes","Yeses":"Yes","Noo":"No"},
                        "latrineAccess":{"N":"No","Y":"Yes","Yeses":"Yes","Noo":"No"},
                        "clinicAccess":{"N":"No","Y":"Yes"}}
    survey_df = script.replace_values(survey_df,survey_replacements)
    environmental_df = script.replace_values(environmental_df,environmental_replacements)

    # Initial data cleaning for survey_df
    survey_df = script.initial_cleaning(survey_df)

    # Merge survey_df and environmental_df
    df = pd.merge(
        survey_df,
        environmental_df,
        left_on=["objectId"],
        right_on=["client.objectId"],
        how="right",
    )

    del survey_df
    del environmental_df

    # Post merge cleaning (removing duplicates, cleaning columns, ...)
    df = script.post_merge_cleaning(df)

    # Replace values for cleaner mapping presentation
    df_replacements = {"educationLevel" : { "lessThanprimary" : "Less Than Primary School", "primary" : "Completed Primary School",
                        "college":"Completed College","highschool":"Completed High School","someHighSchool":"Some High School","someCollege":"Some College"},
                            "waterAccess":{"2-3AWeek":"2-3x A Week","4-6AWeek":"4-6x A Week","1AMonth":"1x A Month","1AWeek":"1x A Week","everyday":"Every day"},
                            "conditionoFloorinyourhouse":{"good":"Good","poor":"Needs Repair","working":"Adequate"},
                            "conditionoRoofinyourhouse":{"working":"Adequate","poor":"Needs Repair"},
                            "stoveType":{"cementStove-Ventilation":"Yes - Cement Stove","openfire-noVentilation":"No - Open Fire"},
                            "houseMaterial":{"block":"Block","wood":"Wood","partBlock_partWood":"Mix with Block and Wood","zinc":"Zinc","brick":"Brick",
                        "other":"Other","clay":"Clay"},
                            "electricityAccess":{"sometimes":"Sometimes","always":"Always","never":"Never"},
                            "foodSecurity":{"not_sure":"Uncertain","N":"No","Y":"Yes"},
                            "govAssistance":{"aprendiendo":"Learning","solidaridad":"Solidarity","other":"Other","no_assistance":"No Assistance"}}

    df = script.replace_values(df,df_replacements)

    # Rename columnn names for mapping. Also Filter out to only include necessary columns
    map_columns = [
        "objectId",
        "educationLevel",
        "latitude",
        "longitude",
        "age",
        "communityname",
        "city",
        "waterAccess",
        "clinicAccess",
        "conditionoFloorinyourhouse",
        "conditionoRoofinyourhouse",
        "stoveType",
        "houseMaterial",
        "electricityAccess",
        "foodSecurity",
        "govAssistance",
        "Latrine or Bathroom Access",
    ]
    rename_columnss = [
        "objectId",
        "Education Level",
        "Latitude",
        "Longitude",
        "Age",
        "Community",
        "City",
        "Water Access",
        "Clinic Access",
        "Floor Condition",
        "Roof Condition",
        "Stove Ventilation",
        "House Material",
        "Electricity Access",
        "Food Security",
        "Government Assistance",
        "Latrine or Bathroom Access",
    ]
    df = script.rename_columns(df,map_columns,rename_columnss)

    # Clean community names with Scott's source of truth community list
    clean_locations = pd.read_excel(
        "data/Puente Dashboard 2-24-21.xlsx", sheet_name="Environmental Data"
    )
    df = script.clean_location_values(df,clean_locations)

    # Remove locations with latititude and longitude outside threshold
    latmin = 17
    latmax = 20
    lonmin = -72
    lonmax = -68
    df = script.geo_clean(df,latmin,latmax,lonmin,lonmax)

    return df