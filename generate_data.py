import pandas as pd
import numpy as np
import random

# Fix the seed
random.seed(42)
np.random.seed(42)

NUM_ROWS = 4694

weather_options = ["Sunny", "Rainy", "Cloudy", "Windy"]
location_options = ["Hitech City", "Banjara Hills", "Madhapur", "Kukatpally", "Dilsukhnagar"]
day_options = ["Weekday", "Weekend"]

# Always start with empty list
data = []

for _ in range(NUM_ROWS):

    hour = random.randint(0, 23)
    day_type = random.choice(day_options)
    weather = random.choice(weather_options)
    location = random.choice(location_options)
    event = random.choice([0, 1])

    demand = 0

    if 12 <= hour <= 14:
        demand += 3
    elif 19 <= hour <= 21:
        demand += 3
    elif 8 <= hour <= 10:
        demand += 2

    if weather == "Rainy":
        demand += 3
    elif weather == "Cloudy":
        demand += 1

    if day_type == "Weekend":
        demand += 2
    else:
        demand += 1

    if event == 1:
        demand += 3

    if location in ["Hitech City", "Banjara Hills"]:
        demand += 2
    elif location == "Madhapur":
        demand += 1

    demand += random.randint(-1, 2)
    demand = max(0, demand)

    if demand >= 9:
        price_multiplier = round(random.uniform(1.8, 2.5), 2)
    elif demand >= 6:
        price_multiplier = round(random.uniform(1.4, 1.8), 2)
    elif demand >= 3:
        price_multiplier = round(random.uniform(1.1, 1.4), 2)
    else:
        price_multiplier = round(random.uniform(0.9, 1.1), 2)

    data.append([hour, day_type, weather, location, event, demand, price_multiplier])

df = pd.DataFrame(data, columns=[
    "Hour", "Day_Type", "Weather", "Location",
    "Local_Event", "Demand_Score", "Price_Multiplier"
])

df.to_csv("surge_pricing_data.csv", index=False)

print("Dataset created successfully!")
print(df.head(5))
print(f"\nTotal rows: {len(df)}")
print(f"Price Multiplier range: {df['Price_Multiplier'].min()} to {df['Price_Multiplier'].max()}")