import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("weather_tokyo_data.csv")

average_weather = round(df["temperature"].mean(), 2)
print(average_weather)
df["month"] = df["day"].str.split("/").str[0]
average_per_month = df.groupby("month")["temperature"].mean()
print(round(average_per_month, 2))
max_temp = df["temperature"].max()
min_temp = df["temperature"].min()
print(f"The maximum is : {max_temp}")
print(f"The minimum is : {min_temp}")

temperature_trend = df.groupby("month")["temperature"].mean()

plt.figure(figsize=(10,6))
temperature_trend.plot(kind="line", marker="o", color="black")

plt.title("Average temperature by month", fontsize = 16)
plt.xlabel("Month", fontsize = 10)
plt.ylabel("Temperature", fontsize = 10)

plt.grid(axis = "both", linestyle = "--", alpha = 0.7)

plt.show()