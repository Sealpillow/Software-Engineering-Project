import plotly.express as px
import pandas as pd
import requests

# Make an API call to get the data from the provided URL
url = 'https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3&limit=149326'
data = requests.get(url).json()

# Extract the required data from the response and convert it into a pandas dataframe
data_records = data['result']['records']
df = pd.DataFrame(data_records)

# Clean the data by removing unwanted columns and rows
df = df.drop(columns=['_id', 'block', 'street_name', 'storey_range', 'month'])
df = df[df['town'].notna()]

# Convert the price column to numeric type
df['resale_price'] = pd.to_numeric(df['resale_price'], errors='coerce')

# Create a dummy variable for each unique town
town_dummies = pd.get_dummies(df['town'])

# Merge the dummy variables with the original dataframe
df = pd.concat([df, town_dummies], axis=1)

# Group the data by town and calculate the mean price
df = df.groupby(['flat_type']).mean().reset_index()

# Create the heatmap plot using plotly
fig = px.imshow(df.iloc[:, 1:], x=df.columns[1:], y=['Flat Type'],
                labels=dict(x='Town', y='Flat Type', z='Resale Price'),
                color_continuous_scale=px.colors.sequential.Plasma,
                title='Resale Price by Town and Flat Type Heatmap')
fig.show()
