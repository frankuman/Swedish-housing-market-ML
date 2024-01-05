
import joblib
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

loaded_model = joblib.load('vm.pkl')
categorical_features = ["property_type", "county", "area", "balcony"]

def run_model(user_input):
    label_encoder = LabelEncoder()
    mae,df,scaler = load_data()
    for feature in categorical_features:
        if feature in user_input:
            all_labels = df[feature].astype(str).append(pd.Series(user_input[feature]).astype(str))
            
            label_encoder.fit(all_labels)
            
            user_input[feature] = label_encoder.transform([user_input[feature]])[0]

    user_df = pd.DataFrame([user_input])



    user_scaled_input = scaler.transform(user_df)
    predicted_price = loaded_model.predict(user_scaled_input)

    print(f"Predicted Price: {predicted_price[0]}")
    def rounder(predicted_price):
        price1 = int(predicted_price[0].round())
        increment = 5000
        rounded_number = round(price1 / increment) * increment
        return rounded_number
    low_price = rounder(predicted_price-mae)
    high_price = rounder(predicted_price+mae)
    print("Recommended price range - Low:", rounder(predicted_price-mae), "- Normal:",rounder(predicted_price), "- High:", rounder(predicted_price+mae))
    return (low_price,rounder(predicted_price),high_price)
def load_data():
    csv_file_path = "data/prop_modified.csv"
    df = pd.read_csv(csv_file_path, sep=";")

    # Encode categorical features using LabelEncoder
    label_encoder = LabelEncoder()
    for feature in categorical_features:
        df[feature] = label_encoder.fit_transform(df[feature])
    print(df.iloc[0])
    # Combine numeric and encoded non-numeric features
    X = df.drop(columns=["wanted_price"]) 
    y = df["wanted_price"]

    # StandardScaler as scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=55)
    y_pred = loaded_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    return(mae,df,scaler)

def main():
    print("Running")
    from frontend import dashboard

    dashboard.app.run(host="127.0.0.1", debug=True)

if __name__ == "__main__":
    main()