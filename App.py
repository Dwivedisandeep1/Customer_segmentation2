#!/usr/bin/env python
# coding: utf-8

# In[16]:


import streamlit as st
import pickle
import pandas as pd
from datetime import datetime
import pandas as pd
import numpy as np
import openpyxl
from sklearn.preprocessing import LabelEncoder


# In[17]:


data=pd.read_excel(r'D:\Customer_segmentation/marketing_campaign.xlsx',engine='openpyxl')


# In[18]:


data.rename(columns={'MntWines': 'Wines',
                     'MntFruits': 'Fruits',
                     'MntMeatProducts': 'Meat',
                     'MntFishProducts': 'Fish',
                     'MntSweetProducts': 'Sweet',
                     'MntGoldProds': 'Gold',
                     'NumDealsPurchases': 'Discount_Purchases',
                     'NumWebPurchases': 'Web_Purchases',
                     'NumCatalogPurchases': 'Catalog_Purchases',
                     'NumStorePurchases': 'Store_Purchases'}, inplace=True)


# In[74]:


file = open('Customer_clustering.pkl','rb')
rf = pickle.load(file)
file.close()


le = LabelEncoder()

# In[19]:


data['Total_Accepted'] = data['AcceptedCmp1'] + data['AcceptedCmp2'] + data['AcceptedCmp3'] + data['AcceptedCmp4'] + data['AcceptedCmp5']

data['Day'] = data['Dt_Customer'].apply(lambda x: x.day)
data['Month'] = data['Dt_Customer'].apply(lambda x: x.month)
data['Year'] = data['Dt_Customer'].apply(lambda x: x.year)

data['Total_Products'] = data['Wines'] + data['Fruits'] + data['Meat'] + data['Fish'] + data['Sweet'] + data['Gold']

current_year = datetime.now().year
# Calculate age by subtracting birth year from current year
data['Age'] = current_year - data['Year_Birth']

today = datetime.now()
data['Days Enrolled'] = (today - data['Dt_Customer']).dt.days

data.drop(columns = ['Dt_Customer','Year_Birth','ID'], inplace = True)

data['Marital_Status'].replace(['Married','Together'],'Together',inplace=True)
data['Marital_Status'].replace(['Single','Alone'],'Single',inplace=True)
data['Marital_Status'].replace(['Divorced','Widow'],'Was_married',inplace=True)

data = data.drop(data[data['Marital_Status'].isin(['Absurd', 'YOLO'])].index)

data1 = pd.get_dummies(data, columns=["Marital_Status"])

data1.drop(columns = ['Response', 'Days Enrolled', 'Age', 'Complain'], axis = 1, inplace = True)

data1[['Z_CostContact', 'Z_Revenue']].describe()




data1['total_purchases'] = data1['Discount_Purchases'] + data1['Web_Purchases'] + data1['Catalog_Purchases'] + data1['Store_Purchases']




data1["Children"]=data1["Kidhome"]+data1["Teenhome"]
data1["Is_Parent"] = np.where(data1.Children> 0, 1, 0)

le.fit_transform(['Marital_Status_single','Marital_Status_Together','Marital_Status_Was_married'])
# In[25]:


data1.drop(columns=['Teenhome', 'Kidhome','AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'AcceptedCmp1',
       'AcceptedCmp2',],inplace=True)


# In[26]:


data1.drop(columns=['Z_CostContact', 'Z_Revenue',],inplace=True)


# In[62]:


data1.drop(columns=['Day', 'Month', 'Year'],inplace=True)


# In[63]:
x = data1['Marital_Status_Single']
LE = LabelEncoder()
LE.fit_transform(x)
x = data1['Marital_Status_Was_married']
data1['Marital_Status_Was_married'] = LE.fit_transform(x)
x = data1['Marital_Status_Together']
data1['Marital_Status_Single'] = data1['Marital_Status_Together'] = LE.fit_transform(x)


# In[29]:

data1['Education'] = data1['Education'].map({'Graduation' : 2 ,  'PhD':4  ,  'Master':3 ,  '2n Cycle':1  , 'Basic':0})
Education = st.selectbox('Education' , data1['Education'].sort_values().unique())


# In[32]:


Income = st.slider('Income', min_value=1730, max_value=113734)


# In[30]:


data1['Recency'].unique()


# In[31]:


Recency = st.slider('Recency', min_value=0, max_value=5)


# In[34]:


Wines = st.number_input('Amount Spent in Wines')


# In[35]:


Fruits = st.number_input('Amount Spent in Fruits')


# In[36]:


Meat = st.number_input('Amount Spent in Meat')


# In[37]:


Fish = st.number_input('Amount Spent in Fish')


# In[38]:


Sweet = st.number_input('Amount Spent in Sweets')


# In[39]:


Gold = st.number_input('Amount Spent in Gold')


# In[40]:


data1['Discount_Purchases'].unique()


# In[41]:


Discount_Purchases = st.selectbox('Discount_Purchases' , data1['Discount_Purchases'].sort_values().unique())


# In[42]:


data1['Web_Purchases'].unique()


# In[43]:


Web_Purchases = st.selectbox('Web_Purchases' , data1['Web_Purchases'].sort_values().unique())


# In[44]:


data1['Catalog_Purchases'].unique()


# In[45]:


Catalog_Purchases = st.selectbox('Catalog_Purchases' , data1['Catalog_Purchases'].sort_values().unique())


# In[46]:


Store_Purchases = st.selectbox('Store_Purchases' , data1['Store_Purchases'].sort_values().unique())


# In[47]:


data1['NumWebVisitsMonth'].unique()


# In[48]:


NumWebVisitsMonth = st.selectbox('NumWebVisitsMonth' , data1['NumWebVisitsMonth'].sort_values().unique())


# In[67]:


data1['Total_Accepted'].unique()


# In[69]:


Total_Accepted = st.selectbox('Total_Accepted' , data1['Total_Accepted'].sort_values().unique())


# In[68]:


Total_Products = st.number_input('Total Products :  Maximum Values 2000',min_value=0,max_value=2000)


# In[71]:


Children = st.selectbox('Children' , data1['Children'].sort_values().unique())


# In[73]:


data1['total_purchases'].max()


# In[ ]:


total_purchases = st.number_input('Total purchases ',min_value=0,max_value=60)
st.write('Total Purchases Min Value:0 , Max Value : 2000 ')


# In[49]:


data1['Is_Parent'].unique()


# In[50]:

Is_Parent1 = {0:'Yes' , 1:'No'}
Is_Parent = st.radio('Is_Parent', [0, 1])


# In[51]:


data1['Marital_Status_Single'].unique()


# In[56]:


data1['Marital_Status_Together'].unique()


# In[57]:


data1['Marital_Status_Was_married'].unique()


# In[53]:


Marital_Status_Single = st.selectbox('Marital_Status_Single',[1,0])


# In[54]:


Marital_Status_Together = st.selectbox('Marital_Status_Together',[1,0])


# In[55]:


Marital_Status_Was_married = st.selectbox('Marital_Status_Was_married',[1,0])


# In[77]:


if st.button('Submit'):
        # if Marital_Status_Single == 'Yes':
        #     Marital_Status_Single == 1
        # else:
        #     Marital_Status_Single == 0
        # if Marital_Status_Together == 'Yes':
        #     Marital_Status_Together == 1
        # else:
        #     Marital_Status_Together == 0 
        # if Marital_Status_Was_married == 'Yes':
        #     Marital_Status_Was_married == 1
        # else:
        #     Marital_Status_Was_married == 0
        query = np.array([Education, Income, Recency, Wines, Fruits, Meat, Fish,
       Sweet, Gold, Discount_Purchases, Web_Purchases,
       Catalog_Purchases, Store_Purchases, NumWebVisitsMonth,
       Total_Accepted, Total_Products,
       Marital_Status_Single, Marital_Status_Together,
       Marital_Status_Was_married, total_purchases, Children,
       Is_Parent])
        query = query.reshape(1, 22)
        features = query
        st.write(features)
        cluster_label = rf.predict(features)
        st.write(f'Belongs to cluster {cluster_label[0]}')

        st.write(cluster_label)    
             





