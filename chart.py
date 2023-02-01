from datetime import datetime,date
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob, os
import altair as alt
from io import BytesIO
import matplotlib.dates as mpl_dates


#space function to control layout
def space(num_lines=1):
    for _ in range(num_lines):
        st.write("")

st.set_page_config(layout="wide",page_icon="💰",page_title="How Finance Works")
#add a title
st.title('Financial Analysis')
space(1)
st.image('photo1.jpeg')
st.markdown('##### These 2 charts are used to assess the operating condition of the chosen company ')
space(2)
###############data preparation
DATE_COLUMN = 'Date'
Companies = ['Jiaotong','Xiaomi','Yongan']


#effortless caching: relieve long-running computation in your code for continuously updating
@st.cache
def load_fdata(data):
    data1 = pd.read_excel(open(data, 'rb'),
              sheet_name='Sheet1',index_col='Date')
    data1[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    data2 = pd.read_excel(open(data, 'rb'),
              sheet_name='Sheet2',index_col='Date')
    data2[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data1,data2

def Metrics_Calc(data):
  data['Days Sales Out.']=(data['A/R']/data['Revenue'])*365
  data['Days Inventory Out.']=(data['Inventory']/data['COGS'])*365
  data['Days Payable Out.']=(data['A/P']/data['COGS'])*365
  data['Cash Conversion Cycle']=data['Days Sales Out.']+data['Days Inventory Out.']-data['Days Payable Out.']

space(2)

############## Visualze the data
def Chart(data,title):
  graph = sns.relplot(data=data,kind='line',height=6, aspect=11.7/8.27,linewidth=3)
  plt.title(title,fontsize='xx-large',fontweight='heavy')
  plt.xticks(rotation=45, ha='right')
  plt.axhline(0, ls='--', linewidth=2, color='red')

def Visual_Metrics(data):
  visual_metrics = data[['Days Sales Out.','Days Inventory Out.','Days Payable Out.','Cash Conversion Cycle']]
  return visual_metrics
##########Visualizing stock price
#Load data from csv files
st.header('Economic Returns')
space(1)

mydir = "data"
xlsxfiles = glob.glob(os.path.join(mydir, '*.xlsx'))
df_dict = dict()
for file in xlsxfiles:
    df_dict[file.split('/')[2].split('.')[0]] = load_fdata(file)

s1, s2 = st.columns(2)
option = st.selectbox(
     'Choose one company to visualize',
     Companies)
data = df_dict[option]
Metrics_Calc(data)
with s1:
    Chart(data,option)

with s2:
    Chart(Visual_Metrics(data),option)
