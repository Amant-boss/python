import pandas as pd

df = pd.read_csv("avgIQpercountry.csv")

print(df.info())

first_rows = df.head()

print(first_rows)

country_data = df["Country"]

print(country_data)

subset = df[["Country" , "Average IQ"]]

print(subset)


filter_df = subset[subset["Average IQ"] > 100]

print(filter_df)

null_mask = df.isnull()

null_count = null_mask.sum()

print("Count of null in each column")
print(null_count)

df.dropna(inplace = True)
print(df.info())


duplicate_count = df.duplicated().sum

print("Count of duplicate rows")
print(duplicate_count)


average_iq_continent = df.froupby("Continent")["Average IQ"].mean()

print(average_iq_continent)


sorted_average_iq_per_continent = average_iq_continent.sort_values(ascending = False)

print(scorted_average_iq_per_continent)