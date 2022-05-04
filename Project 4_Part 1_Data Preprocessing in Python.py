#!/usr/bin/env python
# coding: utf-8

# Description: This exercise addresses absenteeism at a company during work time. The goal is to predict absenteeism, based on different factors. 

# # Data Preprocessing using pandas

# In[1]:


#importing pandas. Pandas has various tools for handling data in a tabular format (DataFrame).

import pandas as pd

#Declaring the variable that will contain the dataframe. 
#Using pandas' method to read csv file. 

raw_csv_data = pd.read_csv(r"C:\Users\jdela\OneDrive\Documents\Data analyst training\Udemy - BI analyst course\Software integration project\Absenteeism_data.csv")


# In[2]:


#Viewing the data inserted in variable raw_csv_data
raw_csv_data


# In[3]:


#Making a copy of the file. This is the data frame I will be working on as I'm making changes to it. 

df = raw_csv_data.copy()

df


# In[4]:


#Checking for missing values

df.info()


# In[5]:


#dropping columns we don't need for the analysis.

df = df.drop(['ID'], axis = 1)


# In[6]:


#drop the ‘Age’ column from df and assign the newly obtained data set to a new variable, called df_no_age.

df = df.drop(['Age'], axis = 1)


# In[7]:


df_no_age = df

df_no_age


# In[8]:


df['Reason for Absence'].max()


# In[9]:


#pd.unique() - extracts distinct values only

pd.unique(df['Reason for Absence'])


# In[10]:


df['Reason for Absence'].unique()


# In[11]:


len(df['Reason for Absence'].unique())


# In[12]:


sorted(df['Reason for Absence'].unique())


# ### Creating Dummy Variables
# 
# We are using dummy variables to add numeric meaning to the "reason for absence" column. We are turning the values in this column into dummy variables. 

# In[13]:


#for convenience, we'll store the output of this method in a variable

reason_columns = pd.get_dummies(df['Reason for Absence'])


# In[14]:


#Doing some checks to see if we have missing or incorrect values. 
#CHECK 1 across rows. There can only be one reason for absenteeism, thefore the total across axis =1 for column"check" should equal 1. 

reason_columns['check'] = reason_columns.sum(axis=1)
reason_columns


# In[15]:


#CHECK 2 across columns. There can only be one reason for absenteeism, thefore the total across axis =0 should equal 700 for column "check". 


reason_columns['check'].sum(axis=0)


# In[16]:


#CHECK 3
reason_columns['check'].unique()


# In[17]:


#Now that we are satisfied that the data contained in "Reason for Abscence" is correct, we can delete the "check" column.

reason_columns = reason_columns.drop(['check'], axis = 1)

reason_columns


# In[18]:


#Dropping the dummy variable, reason 0, from the data set, to avoid multicollinearity issues. 


# In[19]:


reason_columns = pd.get_dummies(df['Reason for Absence'], drop_first = True)


# In[20]:


reason_columns


# ### Grouping the reasons for absence
# We have 27 reasons for absence, which are potentially too many for our analysis. Therefore we want to group them by characterists they have in common, to help our analysis. 
# 

# In[21]:


#main data frame contains column 'Reason for Absence' with the 27 reasons as values. 
df.columns.values


# In[22]:


#reasons_column contains all 27 reasons as its values. 
reason_columns.columns.values


# In[23]:


#To solve this, we'll drop 'Reason for Absence' from our df. 

df.drop('Reason for Absence', axis=1)


# We want to add the dummy variables to the dataframe; however, this would add 27 columns to our data! Because this would be too much, we'll look to group our dummy variables. 
# To separate the reason_columns we will create 4 groups based on common characteristics (reasons related to sickness, to maternity leave, etc.). We will need to create 4 new dataframes, that will each contain a few reasons for absence. We will use the loc method. 

# In[24]:


#Creating 4 dataframes to store the grouped reasons for absence from our dummy variables.
#We used the .max() method because since we are grouping, we only need to know if an employee falls within this group or not.
reason_type_1 = reason_columns.loc[:,1:14].max(axis=1)
reason_type_2 = reason_columns.loc[:,15:17].max(axis=1)
reason_type_3 = reason_columns.loc[:,18:21].max(axis=1)
reason_type_4 = reason_columns.loc[:,22:28].max(axis=1)


# ### Concatenating Column Values
# We want to add the newly created 4 reason_type dataframes to our main dataframe df. To do this we will use the pd.concat() function.

# In[25]:


df = pd.concat([df, reason_type_1, reason_type_2, reason_type_3, reason_type_4], axis = 1)
df


# #### Renaming the reasons for absence columns. At the moment they are simply called 0, 1, 2 and 3. Not meaningful at all. 

# In[26]:


#Getting the column names of the dataframe as a list

df.columns.values


# In[27]:


#Copying the resulting list and pasting it as the content of a new variable.
#Changing the column names to the desired ones. 

column_names = ['Reason for Absence', 'Date', 'Transportation Expense',
       'Distance to Work', 'Daily Work Load Average', 'Body Mass Index',
       'Education', 'Children', 'Pets', 'Absenteeism Time in Hours', 'Reason_1', 'Reason_2',
       'Reason_3', 'Reason_4']


# In[28]:


#Assigning the newly created variable as the headlines of the df

df.columns = column_names


# In[29]:


#checking if it woked... yes!

df.head()


# #### Reordering columns

# In[30]:


column_names_reordered = ['Reason_1', 'Reason_2',
       'Reason_3', 'Reason_4','Reason for Absence', 'Date', 'Transportation Expense',
       'Distance to Work', 'Daily Work Load Average', 'Body Mass Index',
       'Education', 'Children', 'Pets', 'Absenteeism Time in Hours']


# In[31]:


df = df[column_names_reordered]


# In[32]:


df.head()


# ### Creating checkpoints

# In[33]:


#Creating another copy and will use going forward

df_reason_mod = df.copy()


# ### Reworking DATES

# In[34]:


#Checking the data type of the date column. It is a string.
type(df_reason_mod['Date'][0])


# In[35]:


#converting the strings in Date to datetime format. 

df_reason_mod['Date'] = pd.to_datetime(df_reason_mod['Date'], format = '%d/%m/%Y')


# In[36]:


df_reason_mod['Date']


# In[37]:


#checking data type conversion worked. 
df_reason_mod.info()


# #### Extracting the Month Value
# 
# We want to extract the month value from the date column and store it in a new column. 
# We then will concatenate that column into the df. 

# In[38]:


df_reason_mod['Date'][0].month


# In[39]:


#Creating an empty list

list_months = []
list_months


# We will use .append() to attach the new value obtained from each iteration to the existing content of the designated list. 

# In[40]:


#Creating a for loop to fill in that empty list. This loop will go through all rows in the df. 
#using shape in the for loop.

for i in range(df_reason_mod.shape[0]):
    list_months.append(df_reason_mod['Date'][i].month)
      


# In[41]:


list_months


# In[42]:


#checking it worked. We should have 700 values in the list. 
len(list_months)


# In[43]:


#creating a new column in the df, called "month value"

df_reason_mod['Month Value'] = list_months


# In[44]:


df_reason_mod.head()


# #### Extracting the day of the week (monday to friday)

# In[45]:


#Using the weekday function. 0 is monday ... 6 is sunday. 

df_reason_mod['Date'][0].weekday()


# In[46]:


def date_to_weekday(date_value):
    return date_value.weekday()


# In[47]:


#Creating a new column within the df and applying the newly defined function to extract the day of the week from every row. 
df_reason_mod['Day of the Week'] = df_reason_mod['Date'].apply(date_to_weekday)


# In[48]:


#Droping ‘Date’ column from the df_reason_mod DataFrame.

df_reason_mod.drop('Date', axis=1)


# In[49]:


#Re-ordering the columns in df_reason_mod so that “Month Value” and “Day of the Week” appear exactly where “Date” used to be. That is, between “Reason_4” and “Transportation Expense”.

df_reason_mod.columns.values


# In[50]:


column_names_upd = ['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4', 'Month Value', 'Day of the Week',
       'Reason for Absence', 'Date', 'Transportation Expense',
       'Distance to Work', 'Daily Work Load Average', 'Body Mass Index',
       'Education', 'Children', 'Pets', 'Absenteeism Time in Hours']


# In[51]:


column_names_upd


# In[52]:


df_reason_mod = df_reason_mod[column_names_upd]


# In[53]:


df_reason_mod.head()


# In[54]:


#Creating another checkpoint! 
df_reason_date_mod = df_reason_mod.copy()


# In[55]:


df_reason_date_mod


# ### Modifying the contents of the education column. 
# 
# Making the values in the education column more meaningful.

# In[56]:


#Checking the unique values included in the column. 
#We were told 1 is highschool, 2 undergrad, 3 grad, 4 phd
df_reason_date_mod['Education'].unique()


# In[57]:


#Checking how many records fall within each educational level
df_reason_date_mod['Education'].value_counts()


# As not many employees fall within categories 2, 3, and 4. We'll replace highschool wiht a 0 and the rest with 1. This just so that the data is more meaningful. 
# 
# We'll do this with .map()
# 

# In[58]:


df_reason_date_mod['Education'] = df_reason_date_mod['Education'].map({1:0, 2:1, 3:1, 4:1})


# In[59]:


df_reason_date_mod['Education'].unique()


# In[60]:


df_reason_date_mod['Education'].value_counts()


# ### Final checkpoint!

# In[61]:


df_preprocessed = df_reason_date_mod.copy()
df_preprocessed.head(10)


# In[ ]:




