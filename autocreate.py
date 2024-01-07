
"""
Oliver Bölin
BTH, 2023
More comments are in the jupyter file
"""
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from geopy.geocoders import Nominatim
from sklearn.preprocessing import LabelEncoder
import geopy.geocoders
import pandas as pd
import json
from datetime import datetime
from sklearn.model_selection import GridSearchCV
from geopy.geocoders import Nominatim
import requests
from sklearn.metrics import r2_score
from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import mean_absolute_error
import numpy as np
import joblib


print("Starting step 1/7...")
with open("data/prop.json", encoding="utf-8") as data:
    property_data = json.load(data)

# 1.1 remove for unnecessary data

property_data = [entry for entry in property_data if entry.get("price", 0) != 0]
property_data = [entry for entry in property_data if entry.get("build_year", 0) != 0]
property_data = [entry for entry in property_data if entry.get("price", 0) < 30000000]
property_data = [entry for entry in property_data if entry.get("wanted_price", 0) != 0]
property_data = [entry for entry in property_data if entry.get("county", 0) != 0]

    # note 2 Question is, are we predicting the WANTED PRICE or the FINAL PRICE. 
    # I assume, predicting the final price is much harder than the wanted price, since, wanted price is estimated by brokers and the final price can be completely random based on
    # how many betters, particular interest...
for property_entry in property_data:
    del property_entry["url"]
    del property_entry["broker"]
    del property_entry["price"] 
    del property_entry["association"]
    del property_entry["price_change"]
    del property_entry["street"]
    del property_entry["ownership_type"]
    del property_entry["floor"]
    del property_entry["construction_date"]
    del property_entry["story"]
    del property_entry["housing_form"]
    del property_entry["operating_cost"]


df = pd.DataFrame(property_data)

print("Starting step 2/7...")

#We need to convert the sold_at to a better format, lets train it with just years since sold
df["sold_at"] = pd.to_datetime(df["sold_at"], unit="s")
current_year = datetime.now().year
df["age"] = current_year - df["sold_at"].dt.year #We create a "age" column for the age of the data

df.drop(["sold_at"], axis=1, inplace=True) #Lets remove the old column


df["area"] = df["area"].str.split("/").str[0].str.strip() # cleans some areas that are "sometown1 / sometown2" to just "sometown1"
#Remove län and kommun so it can pair with the population density
strings_to_remove = ['kommun', 'län',]
for string in strings_to_remove:
    df['county'] = df['county'].str.replace(string, '')

#make stockholms -> stockholm
df.loc[df['county'].str.endswith('s'), 'county'] = df['county'].str[:-1]


#Population density can be a important factor for the price of the apartment. We add the population density from
# SCB and pare that with the area of the data.
#population density from https://www.statistikdatabasen.scb.se/
with open("data/population_density_data.json", encoding="utf-8") as data:
    population_density_data = json.load(data)
regions = population_density_data["dimension"]["Region"]["category"]["label"]
densities = population_density_data["value"]
region_density_mapping = dict(zip(regions.values(), densities))
df["county"] = df["county"].str.lower().str.strip()
region_density_mapping = {key.lower().strip(): value for key, value in region_density_mapping.items()}
df["population_density"] = df["county"].map(region_density_mapping)

# for the area and county, we also want to remove some weird strings or convert them. Such as Östra Haninge to östra_haninge
df["area"] = df["area"].str.strip()
df["area"] = df["area"].str.replace(" ", "_").str.split("/").str[0].str.strip().str.lower()
df["area"] = df["area"].str.replace(" ", "_").str.split("-").str[0].str.strip().str.lower()
df["county"] = df["county"].str.strip()
df["county"] = df["county"].str.replace(" ", "_").str.lower().str.strip()
df["county"] = df["county"].str.split("/").str[0].str.strip().str.strip()

#We're only going to look for apartments, rowhouses and villas
allowed_property_types = ["Lägenhet", "Radhus", "Villa"]
df = df[df["property_type"].isin(allowed_property_types)]
df.loc[df['area'].str.endswith('_'), 'area'] = df['area'].str[:-1]

#The data has "Ja" for balcony and "" for no balcony, so lets change it
df["balcony"] = df["balcony"].replace("", "Nej")

#We drop all the missing data
df = df.dropna()
df.dropna(subset=['population_density', 'wanted_price'], inplace=True)

#This effectively removes 100 000 entries into the data
# 1.3 save as CSV
print("Starting step 3/7...")
df.to_csv("prop_modified.csv", index=False, sep=";")
# Select a subset of non-numeric features for encoding

print("Starting step 4/7...")
categorical_features = ["property_type", "county", "area", "balcony"]

# Encode categorical features using LabelEncoder
label_encoder = LabelEncoder()
for feature in categorical_features:

    df[feature] = label_encoder.fit_transform(df[feature])
# Combine numeric and encoded non-numeric features
X = df.drop(columns=["wanted_price"])  # Use all columns except the target variable

y = df["wanted_price"]

# StandardScaler as scaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Starting step 5/7...")

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.1, random_state=66)
print("Starting step 6/7...")

rf_regressor = RandomForestRegressor(random_state=99, n_estimators=41, max_features=63, criterion="friedman_mse")  
rf_regressor.fit(X_train, y_train)

# 5.1 make predictions on the test set
y_pred = rf_regressor.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
#prec = precision_score(y_test, y_pred)
msle = mean_squared_log_error(y_test, y_pred)
mean_price = np.mean(y)

print(f"Mean Absolute Error: {mae}")
print(f"R-squared: {r2}")
residuals = y_test - y_pred
std_deviation = np.std(residuals)
print(f"std: {std_deviation}")
print(f"Mean Price: {mean_price}")
print(f"Mean price gives: {1 - mae/mean_price}")
# It is about 90% correct
print("Starting step 7/7...")
joblib.dump(rf_regressor, 'vm.pkl')

print("Done! You can now run the vm.py file")
