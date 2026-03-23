import pandas as pd

df = pd.read_csv('avgIQpercountry.csv')

plt.figure(figsize=(10, 6))

plt.scatter(df['Mean years of schooling - 2021'], df['Average IQ'], color='purple', alpha=0.7)

plt.title('Scatter Plot of Mean Years of Schooling vs Average IQ')

plt.xlabel('Mean years of schooling - 2021')
plt.ylabel('Average IQ')

plt.grid(visible=True, linestyle='--', alpha=0.7)

plt.show();