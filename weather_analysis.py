import requests
import pandas as pd
import matplotlib.pyplot as plt

# Your OpenWeather API Key
API_KEY = "918ecd480dc7891ae5901ee553bb6b85"

# 🌍 Ask user for 5 cities
print("Enter 5 city names separated by commas (example: Paris, London, Delhi, Tokyo, Sydney):")
user_input = input().split(",")   # User types cities
selected_cities = [city.strip() for city in user_input][:5]  # Clean and take only 5

# Fetch weather data
weather_data = []
for city in selected_cities:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    
    if response.get("cod") == 200:
        weather_data.append({
            "City": city,
            "Temperature (°C)": response["main"]["temp"],
            "Humidity (%)": response["main"]["humidity"],
            "Condition": response["weather"][0]["main"]
        })
    else:
        print(f"⚠️ Could not fetch data for {city}")

# Convert to DataFrame
df = pd.DataFrame(weather_data)
df.index = df.index + 1

# 🎨 Styled Weather Table
styled_table = df.style.set_table_styles(
    [{'selector': 'th', 'props': [('background-color', '#4CAF50'),
                                  ('color', 'white'),
                                  ('font-size', '12pt'),
                                  ('text-align', 'center')]},
     {'selector': 'td', 'props': [('text-align', 'center'),
                                  ('font-size', '11pt')]}]
).background_gradient(subset=["Temperature (°C)"], cmap="coolwarm") \
 .background_gradient(subset=["Humidity (%)"], cmap="Blues")

display(styled_table)

# 📊 Graph 1 - Temperature
plt.figure(figsize=(10,6))
bars = plt.bar(df["City"], df["Temperature (°C)"], color="skyblue")
plt.title("Temperature in Selected Cities", fontsize=14, fontweight="bold")
plt.ylabel("°C")
plt.xticks(rotation=45)

# Add values on top of bars
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"{bar.get_height():.1f}°C", ha="center", va="bottom", fontsize=9)

plt.tight_layout()
plt.show()

# 📊 Graph 2 - Humidity
plt.figure(figsize=(10,6))
bars = plt.bar(df["City"], df["Humidity (%)"], color="lightgreen")
plt.title("Humidity in Selected Cities", fontsize=14, fontweight="bold")
plt.ylabel("%")
plt.xticks(rotation=45)

# Add values
for bar in bars:
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"{bar.get_height():.0f}%", ha="center", va="bottom", fontsize=9)

plt.tight_layout()
plt.show()

# 📊 Graph 3 - Humidity Share (Pie chart)
plt.figure(figsize=(8,8))
plt.pie(df["Humidity (%)"], labels=df["City"], autopct="%1.1f%%", 
        colors=plt.cm.tab20.colors, startangle=140)
plt.title("Humidity Share Across Cities", fontsize=14, fontweight="bold")
plt.show()


