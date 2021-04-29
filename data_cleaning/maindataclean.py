# Import packages
from datetime import datetime, date
import json
import numpy as np
import pandas as pd
import difflib

# Files
survey_json = "data/SurveyDataMarch3.json"
environmental_json = "data/HistoryEnvironmentalHealthMarch3.json"


def clean_data():
    #Open Files 
    with open(survey_json,encoding="utf8") as file:
        data = json.load(file)
    survey_df = pd.json_normalize(data["results"])

    with open(environmental_json, encoding="utf8") as file:
        data = json.load(file)
    environmental_df = pd.json_normalize(data["results"])

    # Filter Data
    survey_df = survey_df[
        [
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
    ]

    def calculate_age(born):
        if "-" in born:
            mod = born.split("-")
            # born = datetime.strptime(born, "%Y-%m-%d").date()
            today = date.today()
            return int(today.year - int(mod[0]))
        elif "/" in born:
            """
            x = ""
            for s in born.split():
                if s.isdigit():
                    x+=s
            """
            mod = born.split("/")
            today = date.today()
            try:
                return int(today.year - int(mod[2]))
            except:
                return None
        else:
            return None

    # Calculate age column
    #replace on column: 'dob' 
    survey_df = survey_df.replace({np.nan: ""})
    survey_df["age"] = survey_df["dob"].apply(calculate_age)

    survey_df = survey_df.replace({"educationLevel" : { "lessThanprimary\n" : "lessThanprimary"},
                   })

    environmental_df = environmental_df.replace({"conditionoFloorinyourhouse" : { "dirtPoor" : "poor", "cementPoor" : "working","dirtWorking":"working","cementWorking":"good"},
                            "conditionoRoofinyourhouse":{"bad":"poor","normal":"working"},
                            "houseownership":{"owned":"Yes","rented":"No"},
                            "latrineAccess":{"N":"No","Y":"Yes"},
                            "clinicAccess":{"N":"No","Y":"Yes"}})

    # Clean City Names
    def f(x):
        try:
            return difflib.get_close_matches(x["city"], city_names)[0]
        except:
            return ""

    # Cities Identified
    city_names = [
        "tireo",
        "spm",
        "adansi",
        "consuelo",
        "constanza",
        "la romana",
        "ciudad de dios",
        "la vega",
        "santo domingo",
        "asokwa",
        "santiago",
        "santa fe",
        "san pedro de macorís",
        "el seibo",
    ]

    # Make all lowercase
    survey_df["city"] = survey_df["city"].str.lower()

        # sex
    survey_df["sex"] = survey_df["sex"].str.lower()

    # dob and age (some are negative or too big)
    survey_df[pd.to_numeric(survey_df["age"]) < 0] = ""
    survey_df[pd.to_numeric(survey_df["age"]) > 110] = ""

    # Create merged data
    df = pd.merge(
        survey_df,
        environmental_df,
        left_on=["objectId"],
        right_on=["client.objectId"],
        how="right",
    )
    del survey_df
    del environmental_df

    df = df.drop_duplicates(subset=["client.objectId"])
    df = df.drop(columns=["client.objectId", "objectId_y"])
    df = df.rename(columns={"objectId_x": "objectId"})
    df = df.replace({np.nan: ""})

    # Create new columns for latrine or bathroom access
    df.loc[
        (df["latrineAccess"] == "Y") | (df["bathroomAccess"] == "Y"),
        "Latrine or Bathroom Access",
    ] = "Yes"
    df.loc[
        (df["latrineAccess"] == "N") & (df["bathroomAccess"] == "N"),
        "Latrine or Bathroom Access",
    ] = "No"

    # Change numbers to digits without decimals for numerical columns
    # replace for age column
    df["age"] = df["age"].replace("", np.nan)
    df["age"] = df["age"].astype("float").astype("Int64")

    df = df.replace({"educationLevel" : { "lessThanprimary" : "Less Than Primary School", "primary" : "Completed Primary School",
                    "college":"Completed College","highschool":"Completed High School","someHighSchool":"Some High School","someCollege":"Some College"},
                        "waterAccess":{"2-3AWeek":"2-3x A Week","4-6AWeek":"4-6x A Week","1AMonth":"1x A Month","1AWeek":"1x A Week","everyday":"Every day"},
                        "conditionoFloorinyourhouse":{"good":"Good","poor":"Needs Repair","working":"Adequate"},
                        "conditionoRoofinyourhouse":{"working":"Adequate","poor":"Needs Repair"},
                        "stoveType":{"cementStove-Ventilation":"Yes - Cement Stove","openfire-noVentilation":"No - Open Fire"},
                        "houseMaterial":{"block":"Block","wood":"Wood","partBlock_partWood":"Mix with Block and Wood","zinc":"Zinc","brick":"Brick",
                    "other":"Other","clay":"Clay"},
                        "electricityAccess":{"sometimes":"Sometimes","always":"Always","never":"Never"},
                        "foodSecurity":{"not_sure":"Uncertain","N":"No","Y":"Yes"},
                        "govAssistance":{"aprendiendo":"Learning","solidaridad":"Solidarity","other":"Other","no_assistance":"No Assistance"}})


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
    rename_columns = [
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

    df = df[df.columns[df.columns.isin(map_columns)]]
    for i in np.arange(len(map_columns)):
        df = df.rename(columns={map_columns[i]: rename_columns[i]})

    # Clean Community Names w scott data
    excel_clean = pd.read_excel(
        "data/Puente Dashboard 2-24-21.xlsx", sheet_name="Environmental Data"
    )

    # Get clean community and clean city names into individual dataframes
    clean_community = excel_clean[
        ["Community (Clean)", "communityname"]
    ].drop_duplicates()
    clean_city = excel_clean[["City (Clean)", "city"]].drop_duplicates()

    # Merge clean names with data in df
    df = pd.merge(
        df,
        clean_community,
        left_on=["Community"],
        right_on=["communityname"],
        how="left",
    )
    df = pd.merge(
        df, clean_city, left_on=["City"], right_on=["city"], how="left"
    )

    df = df.drop(columns=["city", "communityname"])

    # Ensure that data has geographic coordinates
    df = df[df["Latitude"] != ""]

    # Remove outliers for latitude and longitude
    latmin = 17
    latmax = 20
    lonmin = -72
    lonmax = -68

    df = df[df["Latitude"].astype(float) > latmin]
    df = df[df["Latitude"].astype(float) < latmax]
    df = df[df["Longitude"].astype(float) > lonmin]
    df = df[df["Longitude"].astype(float) < lonmax]

    return(df)

