# Import packages 
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np

def open_json(json):
    json = json
    with open(json, encoding="utf8") as file:
        data = json.load(file)
    return pd.json_normalize(data["results"])

def filter_df(df,columns):
    return df[columns]

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

def replace_values(df,replacements):
    return df.replace(replacements)

def initial_cleaning(df):
    # Text to lowercase
    # City
    df["city"] = df["city"].str.lower()

    # sex
    df["sex"] = df["sex"].str.lower()

    # dob and age (some are negative or too big)
    df[pd.to_numeric(df["age"]) < 0] = ""
    df[pd.to_numeric(df["age"]) > 110] = ""
    return df

def post_merge_cleaning(df):
    df = df.drop_duplicates(subset=["client.objectId"])
    df = df.drop(columns=["client.objectId", "objectId_y"])
    df = df.rename(columns={"objectId_x": "objectId"})
    # Create new columns for latrine or bathroom access
    df.loc[
        (df["latrineAccess"] == "Yes") | (df["bathroomAccess"] == "Yes"),
        "Latrine or Bathroom Access",
    ] = "Yes"
    df.loc[
        (df["latrineAccess"] == "No") & (df["bathroomAccess"] == "No"),
        "Latrine or Bathroom Access",
    ] = "No"

    df.loc[
        (df["latrineAccess"] == "") & (df["bathroomAccess"] == ""),
        "Latrine or Bathroom Access",
    ] = ""
    df = df.replace({np.nan: ""})

    # Change numbers to digits without decimals for numerical columns
    # replace for age column
    df["age"] = df["age"].replace("", np.nan)
    df["age"] = df["age"].astype("float").astype("Int64")
    return df 

def rename_columns(df,map_columns,rename_columns):
    df = df[df.columns[df.columns.isin(map_columns)]]
    for i in np.arange(len(map_columns)):
        df = df.rename(columns={map_columns[i]: rename_columns[i]})
    return df

def clean_location_values(df,clean_locations):
    clean_community = clean_locations[
        ["Community (Clean)", "communityname"]
    ].drop_duplicates()
    clean_city = clean_locations[["City (Clean)", "city"]].drop_duplicates()

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

    # Drop non-clean columns and ensure that data is tied to a city and a community. Also rename columns
    df = df.drop(columns=["city", "City","Community","communityname",])
    df = df.rename(columns={"Community (Clean)":"Community", "City (Clean)": "City"})
    df = df[df['Community'].notna()]
    df = df[df['City'].notna()]
    return df 

def geo_clean(df,latmin,latmax,lonmin,lonmax):
    # Ensure that data has geographic coordinates
    df = df[df["Latitude"] != ""]

    #Remove lat and long outliers per community
    def is_outlier(s):
        lower_limit = s.mean() - (s.std() * 2)
        upper_limit = s.mean() + (s.std() * 2)
        return ~s.between(lower_limit, upper_limit)

    df = df[~df.groupby('Community')['Latitude'].apply(is_outlier)]
    df = df[~df.groupby('Community')['Longitude'].apply(is_outlier)]

    # Remove outliers for latitude and longitude for entire country
    df = df[df["Latitude"].astype(float) > latmin]
    df = df[df["Latitude"].astype(float) < latmax]
    df = df[df["Longitude"].astype(float) > lonmin]
    df = df[df["Longitude"].astype(float) < lonmax]
    return df