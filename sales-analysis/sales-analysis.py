import pandas as pd
import os
import matplotlib.pyplot as plt 
import datetime as dt
import calendar as cal
from itertools import combinations
from collections import Counter

graphNo = 2
fig, ax = plt.subplots(2,2)
fig.tight_layout(h_pad=2)
#MERGE ALL DATA INTO A SINGLE FILE
salesFiles=[file for file in os.listdir("Pandas-Data-Science-Tasks-master\SalesAnalysis\Sales_Data")]

totalData = pd.DataFrame()

for file in salesFiles:
    df = pd.read_csv("Pandas-Data-Science-Tasks-master\SalesAnalysis\Sales_Data\\"+file)
    totalData=pd.concat([totalData, df])

totalData.to_csv("total_data.csv", index=False)

#USE UPDATED DATAFRAME
salesData=pd.read_csv("total_data.csv")

#CLEANING DATA
    #remove NaN
nan_df=salesData[salesData.isna().any(axis=1)]
salesData=salesData.dropna(how="any")

    #remove columns with wrong values
salesData=salesData[salesData['Order Date'].str[0:2]!='Or']

#AUGMENT DATA WITH ADDITIONAL COLUMNS
    #adding a month column
salesData["Month"] = salesData["Order Date"].str[0:2]
salesData["Month"] = salesData["Month"].astype('int32')
    #converting columns to apt types
salesData["Price Each"] = salesData["Price Each"].astype('float')
salesData["Quantity Ordered"] = salesData["Quantity Ordered"].astype('int32')
    #adding a sales column
salesData["Sales"] = salesData["Price Each"]*salesData["Quantity Ordered"]

#QUESTION 1: Best month for sales and the sales earned that month:
result1 = salesData.groupby('Month').sum(numeric_only=True)
months = [cal.month_abbr[x] for x in range(1,13)]
plt.subplot(graphNo,2,1)
plt.bar(months, result1['Sales'])
plt.ylabel('Sales in USD')
plt.xlabel('Month')
plt.xticks(months)
plt.title('#1: Sales per Month')

#QUESTION 2: Which city had maximum sales
salesData["City"] = salesData['Purchase Address'].str.extract(',\s([^ ].+),')
result2 = salesData.groupby('City', as_index=False)['Sales'].sum(numeric_only=True)
cities = result2["City"].to_list()
plt.subplot(graphNo,2,2)
plt.bar(cities, result2['Sales'])
plt.ylabel('Sales in USD')
plt.xlabel('City')
plt.xticks(cities, rotation=45, ha='right')
plt.title('#2: Sales per City Annually')


#QUESTION 3: Time to display advertisements to maximise likelihood of customer buying product
salesData['Order Date'] = pd.to_datetime(salesData['Order Date'])
salesData['Hour'] = salesData['Order Date'].dt.hour
result3 = salesData.groupby('Hour', as_index=False)['Quantity Ordered'].sum()
hours = result3['Hour'].to_list()
plt.subplot(graphNo, 2, 3)
plt.xticks=(range(1,25,2))
plt.ylabel('Sales in USD')
plt.xlabel('Hour (24 Hr Clock)')
plt.plot(hours, result3['Quantity Ordered'])
plt.title('#3: Sales at Each Hour of the Day')
plt.grid()
plt.show()

#QUESTION 4: Products most often sold together
df = salesData[salesData['Order ID'].duplicated(keep=False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df=df[['Order ID', 'Grouped']].drop_duplicates()
count = Counter()
for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))
print("\nPRODUCT PAIRS MOST OFTEN SOLD TOGETHER:")
for key, value in count.most_common(10):
    print(key, ':', value)

#QUESTION 5: Highest selling product
productGroup = salesData.groupby('Product', as_index=False)['Quantity Ordered'].sum()
result5 = productGroup.loc[productGroup['Quantity Ordered'].idxmax()]
print('\nHIGHEST SELLING PRODUCT:')
print(result5)
