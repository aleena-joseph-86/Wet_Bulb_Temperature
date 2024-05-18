import streamlit as st
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from math import atan, sqrt

# API Key and URL format
API_key = 'a7fd3fa44854968062a3ab33a6c94faf'
base_url = 'https://api.openweathermap.org/data/2.5/weather'

# Function to fetch weather data
def get_weather_data(city_name):
    params = {'q': city_name, 'appid': API_key, 'units': 'metric'}
    response = requests.get(base_url, params=params)
    data = response.json()
    if response.status_code == 200:
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        return temperature, humidity
    else:
        st.error(f"Error fetching data for {city_name}: {data['message']}")
        return None, None

# Function to calculate wet bulb temperature
def calculate_wet_bulb_temperature(T, rh):
    Tw = T * atan(0.152 * sqrt(rh + 8.3136)) + atan(T + rh) - atan(rh - 1.6763) + 0.00391838 * (rh ** 1.5) * atan(0.0231 * rh) - 4.686
    return Tw

# List of initial cities 
initial_cities = ['Chennai', 'Bangalore', 'Hyderabad', 'Kochi', 'Coimbatore','Puducherry','Alappuzha']

# List of all Indian cities 
indian_cities = ["Mumbai","Chennai","Kolkata","Visakhapatnam","Kochi","Puducherry","Kozhikode","Panaji","Mangalore","Bhavnagar","Kakinada",
    "Ratnagiri","Machilipatnam","Port Blair","Diu","Daman","Karaikal","Vasco da Gama","Kollam","Alappuzha","Veraval","Rameswaram","Paradip",
    "Haldia","Kandla","Porbandar","Kochi","Mangalore","Kochi","Mangalore","Delhi","Bengaluru","Hyderabad","Ahmedabad","Pune","Jaipur",
    "Lucknow","Kanpur","Nagpur","Patna","Indore","Bhopal","Ludhiana","Agra","Vadodara","Nashik","Kolkata","Surat","Varanasi","Rajkot",
    "Meerut","Prayagraj","Faridabad","Ghaziabad","Ranchi","Jodhpur","Amritsar","Raipur","Kota","Guwahati","Chandigarh","Thiruvananthapuram",
    "Madurai","Coimbatore","Tiruchirappalli","Hubli-Dharwad","Kozhikode","Bhubaneswar","Salem","Warangal","Guntur","Aurangabad","Vijayawada","Tirupati",
    "Bikaner","Mangalore","Srinagar","Siliguri","Jamshedpur","Ujjain","Noida","Jalandhar","Belagavi","Jammu","Dehradun","Jabalpur","Gwalior","Kollam",
    "Dhanbad","Nanded","Raipur","Nellore","Sangli","Thane","Bhilai","Visakhapatnam","Muzaffarnagar","Srinagar","Navi Mumbai","Bhavnagar",
    "Amravati","Kolhapur","Thoothukudi","Rajahmundry","Gulbarga","Bhatpara","Shimoga","Mangalore","Kottayam","Thrissur","Tirunelveli",
    "Jamnagar","Bikaner","Bharuch","Moradabad","Mysore","Aligarh","Jhansi","Bokaro Steel City","Mangalore","Hospet","Durgapur","Kakinada",
    "Dewas","Sangli-Miraj & Kupwad","Nizamabad","Anantapur","Bilaspur","Chandrapur","Korba","Bhilai Nagar","Mysore","Bhiwandi","Bokaro","Baramati",
    "Akola","Buldana","Wardha","Chittoor","Ambala","Hisar","Panipat","Karnal","Raichur","Anantapur","Karimnagar","Shillong","Khammam","Kadapa","Alwar",
    "Jhunjhunu","Dibrugarh","Sivasagar","Imphal","Aizawl","Kohima","Dimapur","Itanagar","Gangtok","Kavaratti"
]


# Title of the app
st.title('Wet Bulb Temperature Calculator')

# Reference text for risk
st.markdown("""
<hr>
The wet bulb temperature (Tw) is calculated using the formula:<br>
Tw = T * arctan[0.152 * (rh + 8.3136)^(1/2)] + arctan(T + rh%) – arctan(rh – 1.6763) + 0.00391838 *(rh)^(3/2) * arctan(0.0231 * rh) – 4.686<br>
where T is the temperature and rh is the relative humidity
<hr>
Do you want to know the wet bulb temperature in your city?<br>
Then feel free to add your city and know the wet bulb temperature.
""",unsafe_allow_html=True)

# Dropdown menu for adding cities
new_city = st.selectbox('Add a city', indian_cities)   

# Button to add selected city
if st.button('Add City'):
    if new_city and new_city not in initial_cities:
        initial_cities.append(new_city)
        st.success(f'{new_city} added to the list.')

# Fetch weather data and calculate wet bulb temperature
wet_bulb_data = []
for city in initial_cities:
    T, rh = get_weather_data(city)
    if T is not None and rh is not None:
        Tw = calculate_wet_bulb_temperature(T, rh)
        wet_bulb_data.append({'City': city, 'Temperature': T, 'Humidity': rh, 'Wet Bulb Temperature': Tw})

# Display scatter plot with risk intensity
if wet_bulb_data:
    df = pd.DataFrame(wet_bulb_data)

    fig, ax = plt.subplots()

    scatter = ax.scatter(df['Humidity'], df['Temperature'], c=df['Wet Bulb Temperature'], cmap='Oranges', s=df['Wet Bulb Temperature']*20, edgecolors='w', linewidth=1.5)

    ax.set_xlabel('Humidity (%)')
    ax.set_ylabel('Temperature (°C)')

    # Annotate cities
    for i, row in df.iterrows():
        ax.text(row['Humidity'], row['Temperature'], row['City'], size=8, zorder=1, color='k')

    # Create a colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Wet Bulb Temperature (°C)')

    st.pyplot(fig)

# Main function
def main():
    st.title("Wet Bulb Temperature Calculator")

if __name__ == "__main__":
    main()
