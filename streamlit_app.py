import streamlit as st
import requests
import datetime as dt
import pandas as pd
import json
from joblib import load

# loading model
@st.cache(allow_output_mutation=True)
def load_model():
    return load("tuned_model.joblib")

model = load_model()

# hash function to use secret api key
def _hash_st_secrets(secrets) -> int:
	"""
	An st.cache hash_func to hash st.secrets objects. The hash should change
	whenever the underyling secrets object changes.
	"""
	hash_just_the_secrets = hash(json.dumps(st.secrets._secrets))
	return hash_just_the_secrets

# get weather data from OpenWeatherMap
@st.cache(hash_funcs={type(st.secrets): _hash_st_secrets}, ttl=12*3600)
def get_weather_data():
    lat = "44.30"
    lon = "-120.91"
    api_key = st.secrets["api_key"]
    exclude = "current,minutely,hourly,alerts"

    URL = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={api_key}"

    response = requests.get(URL)
    # response.status_code # put in some kind of redirect if fail
    response_json = response.json()

    inputs = {
    "AmbientTemp": [],
    "Pressure": [],
    "month": [],
    "Latitude": [response_json["lat"]]*8,
    "Longitude": [response_json["lon"]]*8,
    "date": []
    }

    for day in response_json["daily"]:
        daily_temp = day["temp"]["day"]
        daily_temp = daily_temp - 273.15 # convert to Celsius
        inputs["AmbientTemp"].append(daily_temp)

        daily_pressure = day["pressure"]
        inputs["Pressure"].append(daily_pressure)

        timestamp = int(day["dt"])
        month = dt.datetime.fromtimestamp(timestamp).month
        inputs["month"].append(month)

        date = dt.datetime.fromtimestamp(timestamp).day
        inputs["date"].append(date)

    inputs_df = pd.DataFrame(inputs)
    inputs_df = inputs_df[["Latitude", "Longitude", "AmbientTemp", "Pressure", "month", "date"]]

    return inputs_df

# make predictions using model
def push_through_model(input, total_panel_wattage=2500):
    predictions = model.predict(input.drop(["date"], axis=1)) # efficiency
    predictions = predictions*total_panel_wattage*5/1000 # kWh, 5 hours of sunlight
    return pd.Series(data=predictions, index=input["date"], name="Energy Output (kWh)")

# drop stuff not needed from inputs
def drop_inputs(df):
    drop_list = ["date"]
    return df.drop(drop_list, axis=1)

# convert final total energy output to something more fun
def convert_energy_to_tesla(energy):
    return energy/340 # 340 Wh/mile for an average Tesla

# should be able to put in acres rather than solar panel area/wattage
def convert_acres_to_wattage(acres):
    watts_per_panel = 450 # https://www.literoflightusa.org/solar-panel-sizes/
    area_per_panel = 20.9 # square feet
    watt_density = watts_per_panel/area_per_panel # W/ft^2
    acres_to_square_feet = acres * 43560 # ft^2
    return acres_to_square_feet*watt_density

def convert_energy_to_dollars(energy):
    dollars = energy*11.73/100 # https://www.eia.gov/state/print.php?sid=OR
    return dollars

st.title("Expected Solar Energy Output at the Property")

inputs_df = get_weather_data()
total_acreage = st.slider("How many acres do you want converted to solar?", 10, 280, 100, 10)
total_panel_wattage = convert_acres_to_wattage(total_acreage)
predictions_df = push_through_model(inputs_df, total_panel_wattage)
total_output = predictions_df.sum()
miles_for_tesla = convert_energy_to_tesla(total_output) # https://www.carshtuff.com/post/how-much-electricity-does-a-tesla-use
dollars_of_energy = convert_energy_to_dollars(total_output)

st.subheader(f"Estimated output next week is *{total_output:,.0f}* kilowatt-hours")
st.markdown(
    f"""
    Enough energy to:
    - Drive an average Tesla **{miles_for_tesla:,.1f} miles**
    - Sell at the average Oregon residential rate for **${dollars_of_energy:,.2f}**
    """
)

st.bar_chart(data=predictions_df)

st.markdown(
    """
    Assumptions:
    - 450 W panels taking up 20.9 square feet each, no space between them
    - 5 hours of sunlight per day
    - Polycrystalline panels
    - Horizontal array
    """
)

st.markdown("Predictions for daily energy output for next week in Watt-Hours")
st.dataframe(predictions_df)

st.markdown("Inputs for the next week (today is the first row):")
st.dataframe(inputs_df)
