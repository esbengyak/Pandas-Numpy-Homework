
# coding: utf-8

# - Our oldest customer group (40+) have the highest average purchase price based on normalized totals
# - The largest portion of customers 20-24 (45% of customers) have the lowest average purchase price based on normalized totals
# - Our most frequently purchased items are the Betrayal,Whisper of Grieving Widows and Arcane Gem, with 11 total purchases each

# In[1]:


import numpy as np
import pandas as pd
import os
players = os.path.join("purchase_data.json")
player_data = pd.read_json(players)
player_data.head()


# In[2]:


unique_players = player_data["SN"].nunique()
unique_players_df = pd.DataFrame({
    'Total Players': [unique_players]})
unique_players_df


# In[3]:


item_count = player_data["Item ID"].nunique()
average_purchase = player_data["Price"].mean()
total_purchases = player_data["Price"].count()
total_revenue = player_data["Price"].sum()

purchase_info = pd.DataFrame({
    'Number of Unique Items': [item_count],
    'Average Price': [average_purchase],
    'Number of Purchases': [total_purchases],
    'Total Revenue': [total_revenue]})

purchase_info ["Average Price"] = purchase_info["Average Price"].map("${:,.2f}".format)
purchase_info ["Total Revenue"] = purchase_info["Total Revenue"].map("${:,.2f}".format)
purchase_info = purchase_info.loc[:, ["Number of Unique Items", "Average Price", "Number of Purchases", "Total Revenue"]]
purchase_info


# In[4]:


player_data_remove_dups = player_data.drop_duplicates('SN')
gender_counts = player_data_remove_dups['Gender'].value_counts()
gender_percent = gender_counts/unique_players*100

gender_demographics = pd.DataFrame(
    {"Total Count": gender_counts, 
    "Percentage of Players": gender_percent})

gender_demographics = gender_demographics.round(2)
gender_demographics


# In[19]:


gender_purch_total = player_data.groupby('Gender').sum()["Price"]
gender_purchase_count = player_data.groupby('Gender').count()["Price"]
gender_purchase_average = player_data.groupby('Gender').mean()["Price"]
normalized_total = gender_purch_total/ gender_demographics["Total Count"]

gender_purchases = pd.DataFrame(
    {'Purchase Count': gender_purchase_count, 
    'Average Purchase Price': gender_purchase_average,
    'Total Purchase Volume': gender_purch_total,
    'Normalized Totals': normalized_total})

gender_purchases ["Average Purchase Price"] = gender_purchases["Average Purchase Price"].map("${:,.2f}".format)
gender_purchases ["Total Purchase Volume"] = gender_purchases["Total Purchase Volume"].map("${:,.2f}".format)
gender_purchases ["Normalized Totals"] = gender_purchases["Normalized Totals"].map("${:,.2f}".format)  
gender_purchases = gender_purchases.loc[:, ["Purchase Count", "Average Purchase Price", "Total Purchase Volume", "Normalized Totals"]]
gender_purchases


# In[7]:


age_remove_dups = player_data.drop_duplicates('SN')
age_bins = [0, 9.99, 14.99, 19.99, 24.99, 29.99, 34.99, 39.99, 99999]
age_groups = ["<10","10-14","15-19", "20-24","25-29","30-34", "35-39", "40+"]
player_data["Age Ranges"] = pd.cut(player_data['Age'],age_bins, labels=age_groups)
age_counts = age_remove_dups['Age Ranges'].value_counts()
age_percentage = age_counts/unique_players *100

age_totals = pd.DataFrame(
    {'Percentage of Players': age_percentage, 
    'Total Count': age_counts})

age_totals = age_totals.round(2)
age_totals = age_totals.sort_index()
age_totals


# In[9]:


age_purch_total = player_data.groupby('Age Ranges').sum()["Price"]
age_purchase_count = player_data.groupby('Age Ranges').count()["Price"]
age_purchase_average = player_data.groupby('Age Ranges').mean()["Price"]
age_normalized_total = age_purch_total/age_totals['Total Count']


age_purchases = pd.DataFrame(
    {'Purchase Count': age_purchase_count, 
    'Average Purchase Price': age_purchase_average,
    'Total Purchase Volume': age_purch_total,
    'Normalized Totals': age_normalized_total})

age_purchases ["Average Purchase Price"] = age_purchases["Average Purchase Price"].map("${:,.2f}".format)
age_purchases ["Total Purchase Volume"] = age_purchases["Total Purchase Volume"].map("${:,.2f}".format)
age_purchases ["Normalized Totals"] = age_purchases["Normalized Totals"].map("${:,.2f}".format)  
age_purchases = age_purchases.loc[:,['Purchase Count', 'Average Purchase Price', 'Total Purchase Volume', 'Normalized Totals']]
age_purchases


# In[10]:


user_purch_total = player_data.groupby('SN').sum()["Price"]
user_purchase_count = player_data.groupby('SN').count()["Price"]
user_purchase_average = player_data.groupby('SN').mean()["Price"]

user_purchases = pd.DataFrame(
    {'Purchase Count': user_purchase_count, 
    'Average Purchase Price': user_purchase_average,
    'Total Purchase Volume': user_purch_total,})

user_purchases ["Average Purchase Price"] = user_purchases["Average Purchase Price"].map("${:,.2f}".format)
user_purchases ["Total Purchase Volume"] = user_purchases["Total Purchase Volume"].map("${:,.2f}".format)
user_purchases.sort_values("Purchase Count", ascending = False).head(5)


# In[26]:


#finished
item_list = player_data.loc[:,['Item ID','Item Name', 'Price']]

item_purch_total = item_list.groupby(['Item ID', 'Item Name']).sum()['Price']
item_purchase_count = item_list.groupby(['Item ID', 'Item Name']).count()['Price']
item_price = item_list.groupby(['Item ID', 'Item Name']).mean()['Price']
item_total_purch_value = item_purchase_count * item_price

item_purchases = pd.DataFrame(
    {'Purchase Count': item_purchase_count, 
     'Total Purchase Value': item_purch_total,
    'Item Price': item_price})

item_purchases ["Item Price"] = item_purchases["Item Price"].map("${:,.2f}".format)

item_purchases = item_purchases.loc[:,["Purchase Count", "Item Price", "Total Purchase Value"]]
item_purchases.columns = [i+' ($)' if i != 'Purchase Count' else i for i in item_purchases.columns]
item_purchases.sort_values("Purchase Count", ascending = False).head(5)


# In[29]:


item_purchases.sort_values('Total Purchase Value ($)', ascending = False).head(5)

