# Step 1
#HOW CODE WORKS
#RUN EACH STEP ONE BY ONE AND SEE OUTPUT AFTER


import requests
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from bs4 import BeautifulSoup




agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

data=requests.get("https://www.spaceweatherlive.com/en/solar-activity/top-50-solar-flares",headers=agent)

#print(data.text)

root = BeautifulSoup(data.content,features="html.parser")

# grabbing the table tag that contains the html table
table = root.find("table",{"class" : "table table-striped table-responsive-md"})

#creating the dataframe of the string using pandas

#convert the table into a dataframe
df = pd.read_html(str(table))[0]


#create a new header
new_header = ["rank","x_class", "date", "region", "start_time", "max_time" ,"end_time" ,"movie"] #grab the first row for the header
#df.columns is the first row in the data frame which is untitled, so we change it to what we want it to be
df.columns=new_header
#setting index from 1 to n instead of 0 to n
df.index = np.arange(1, len(df) + 1)
#print(df)


#print(df.iloc[0])
df


# Step 2

# Drop the last column of the table, since we are not going to use it moving forward.
df["movie"]=df["region"]

del df["region"]
# Use datetime import to combine the date and each of the three time columns into three datetime columns. You will see why this is useful later on. iterrows() should prove useful here.
datetime_str = '09/19/18 13:55:26'



df["start_time"]=  pd.to_datetime(df["date"] +" " + df["start_time"],format='%Y-%m-%d')
df["max_time"]=  pd.to_datetime(df["date"] +" " + df["max_time"],format='%Y-%m-%d')
df["end_time"]=  pd.to_datetime(df["date"] +" " + df["end_time"],format='%Y-%m-%d')


del df["date"]


# renaming everything
new_header = ["rank","x_class", "start_datetime", "max_datetime", "end_datetime", "region"]
df.columns=new_header

#pad a 0 at end of 4 digit region
df['region'] = df['region'].apply(lambda x: '{0:0>4}'.format(x))

regex4='\-+'

df = df.replace(regex4, value = np.nan, regex = True)

df


#Step 3

nasa_url = "https://cdaw.gsfc.nasa.gov/CME_list/radio/waves_type2.html"
r= requests.get(nasa_url,headers=agent)


soup = BeautifulSoup(r.content,features="html.parser")


#print(soup.get_text().split())

pre_tag = soup.find("pre")


# regex to grab start_date start_time etc
regex = r"\d{4}\/\d{2}\/\d{2} \d{2}:\d{2} \d{2}\/\d{2} \d{2}:\d{2}"


#regex to find flare location and flare region
regex2=r"<\/a>\s*[a-zA-Z0-9\.\-\?]+\s*[a-zA-Z0-9\.\-\?]+\s{1}[a-zA-Z0-9\.\-\?]+\s{3}[<|\-]+|\s{3}[a-zA-Z0-9\.\-\?]+\s{3}" \
       r"[a-zA-Z0-9\.\-\?]+\s{1}[a-zA-Z0-9\.\-\?]+\s{1}[a-zA-Z0-9\.\-\?]+\s*[<|\-]" \
       r"|\s+[a-zA-Z0-9\.\-\?]+\s{3}[a-zA-Z0-9\.\-\?]+\s{1}[a-zA-Z0-9\.\-\?]+\s{1}[a-zA-Z0-9\.\-\?]+\s*[<|\-]"

regex3= re.compile(r'(\d{4}/\d{2}/\d{2}\s{1,}\d{2}:\d{2}\s{1,}\d{2}/\d{2}\s{1,}\d{2}:\d{2}\s{1,}[\d\W]{4,}\s{1,}'
                     r'[\d\W]{2,}\s{1,}[A-Za-z\d\w\W]{4,7}\s{1,}[A-Za-z\d\w\W]{2,5}\s{1,}[A-Za-z\w\D\W]{1,4}\s{1,}'
                     r'[0-9\w\W]{2}/[0-9\w\W]{2}\s{1,}[0-9\w\W]{2}:[0-9\w\W]{2}\s{1,}[A-Za-z\d\w\W]{2,4}\s{1,}'
                     r'[A-Za-z\d\w\W]{2,4}\s{1,}[\d\w\W]{3,4}\s{1,}[\w\W]{4})')

grab_soup = soup.get_text()
#\s{3}[a-zA-Z0-9\.\-\?]+\s{3}[a-zA-Z0-9\.\-\?]+\s{1}[a-zA-Z0-9\.\-\?]+\s{1}[a-zA-Z0-9\.\-\?]+\s*[<|\-]

#<\/a>\s*[a-zA-Z0-9\.\-\?]+\s
#print(pre_tag)

match =re.findall(regex,str(pre_tag))

match_2 =re.findall(regex2,str(pre_tag))

match3 = regex3.findall(grab_soup)

#print(match_2)


splitter = []

splitter_two = []

splitter_three = []


for i in match:
    splitter.append(i.split())

for i in match_2:
    splitter_two.append(i.split())
for i in match3:
    splitter_three.append(i.split())






# Forming the columns for my data frame

start_date = []
start_time = []
start_frequency = []
end_frequency= []
end_date = []
end_time =[]
cme_time = []
cpa = []
importance = []
flare_location = []
plot = []

width = []

speed = []


flare_region = []



for i in splitter:
    start_date.append(i[0])
    start_time.append(i[1])
    end_date.append(i[2])
    end_time.append(i[3])


for i in splitter_two:
    flare_location.append(i[1])
    flare_region.append(i[2])

for i in splitter_three:
    start_frequency.append(i[4])
    end_frequency.append(i[5])
    cpa.append(i[11])
    importance.append(i[8])
    cme_time.append(i[10])
    width.append(i[12])
    speed.append(i[13])
    plot.append(i[14])


data = {
            "start_date": start_date,

           "start_time": start_time,

           "end_date": end_date,

           "end_time": end_time,

           "start_frequency": start_frequency,

           "end_frequency":end_frequency,

           "flare_location": flare_location,

            "flare_region": flare_region
}

df2=pd.DataFrame(data)

df2

# Step 4

df2["end_time"].iloc[0]

df2["end_time"] = np.where((df2.end_time == '24:00'),'00:00',df2.end_time)

df2['end_date'] = df2['start_date'].str.split('/').str[0] + "/" + df2['end_date']

df2["end_date"] = pd.to_datetime(df2["end_date"] +" " + df2["end_time"],format='%Y-%m-%d')

df2["end_time"] = df2["start_date"]

df2["start_date"] = pd.to_datetime(df2["start_date"] +" " + df2["start_time"],format='%Y-%m-%d')


df2.rename(columns ={"start_date":"start_datetime"})

df2.rename(columns ={"end_date":"end_datetime"})

#df2["end_date"] = pd.to_datetime(df2["start_date"] +" " + df2["end_time"],format='%Y-%m-%d')

df2["importance"]= importance
df2["cme_datetime"] = cme_time




df2["cme_datetime"] = pd.to_datetime(df2["end_time"] +" " + df2["cme_datetime"], errors='coerce',format='%Y-%m-%d')



regex4="\-+"

df2["cpa"]=cpa

df2= df2.replace(regex4, value = np.nan, regex = True)


df2.replace("Halo",np.nan,inplace=True)
df2['width']=width
df2['speed']=speed


#where ever cpa is null, the new columns value will be true and false otherwise
df2['is_halo'] = np.where(df2.cpa.isnull(), True, False)
df2['plot']=plot
df2['width_lower_bound'] = np.where(df2.width.str.startswith(">"), True, False)




df2.rename(columns = {"start_date":"start_datetime"},inplace=True)


df2.rename(columns = {"end_date":"end_datetime"},inplace=True)



df2.drop('start_time', axis=1, inplace=True)

df2.drop('end_time', axis=1, inplace=True)

df2




# Part 2

#Question 1

'''
since by default the type of the column is "object", we only focus on number 
after X to determine sorting by casting to a float and sorting approiately
'''


topFlares= df2.loc[df2['importance'].str.startswith("X",na=False)].copy()

topFlares['importance'] = topFlares['importance'].astype('str')


topFlares['importance'] = topFlares['importance'].str.split("X").str.get(1)

topFlares['importance']= topFlares['importance'].astype('float64')
topFlares = topFlares.sort_values(by ='importance',ascending = False)

topFlares.index = np.arange(1, len(topFlares) + 1)

topFlares = topFlares.head(50)

topFlares['importance']= "X" + topFlares['importance'].astype('str')


regex4="\-+"

topFlares= topFlares.replace(regex4, value = np.nan, regex = True)

#topFlares now has the top 50 solare flare events for NASA



'''
The data is similar to the top 50 solar flares from SpaceWeatherLive.com but not exact. The lowest flares importance begins at X1.9
for NASA where as its X2.6 for Space Weather Live. 
There are some entries where both data frames rows are equivalent such as X28.0 being the highest classification in both.

Replicating the SpaceWeatherLive data can be efficient enough by having the x_class, and start time to compare against Nasas data set.

Since there arent many descriptive columns like in the NASA dataset, it wont be a very detailed replication.

'''
topFlares


# Question 2

'''
This function compares certain matching entries to determine best matching rows.

x will represent the SpaceWeatherLive dataframe and y will represent NASA's Top 50 Solar Flares.


To insure the best matching row i will consider start date(not time), and x_class.

The reason im only considering these two things is because end dates are not mentioned on spaceweatherlive, only start date.
Time is also not a good measurement because it can vary by several minutes or hours between data entries of the same solar flares from both websites.
Im also considering equivalent X_Class since thats also another important distinguishing feature of a solar flare that wont be different.



'''

def bestMatchingRow(x, y):
    
    df = x.copy()
    
    df2 = y.copy()
    
    
    #parsing the time out and only grabbing the date part
    df['start_datetime'] = df['start_datetime'].astype(str).str.split().str.get(0).astype(str)
    df2['start_datetime'] = df2['start_datetime'].astype(str).str.split().str.get(0).astype(str)



    df2['importance'] = df2['importance'].str.split('X').str[1].astype('float64')

    df['x_class'] = df['x_class'].str.split('X').str[1].str.split('+').str[0].astype('float64')

    #print(df.iloc[0])

    df2['rank']= np.where((df2['importance'].isin(df['x_class'])) & (df2['start_datetime'].isin(df['start_datetime']))
                 ,df['rank'], 'No Rank')

   
    return df2['rank']

topFlares['rank'] = bestMatchingRow(df,topFlares)

topFlares


# Question 3 Analysis 

%matplotlib inLine

topFlareRowTotal= len(topFlares.index)


mean1 = topFlares['is_halo'].mean()
nasaRowTotal = len(df2.index)
top50HaloCME= topFlares['is_halo'].values.sum()
top50Variance = np.var(topFlares['is_halo'])
varianceNasa= np.var(df2['is_halo'])
nasaHaloCME=  df2['is_halo'].values.sum()

df3 = pd.DataFrame({'Halo CME':['Top 50 NASA', 'NASA Halo CME'], 
                    'val':[top50HaloCME, nasaHaloCME]})

'''
This plots out the Halo CMES that are present in the TOP 50 CME subset as well as the entire dataset

There are a total of 44 Halo CMES present in the top 50 solar flares, and a total of 308 Halo CMES present 

in the entire dataset. 88% of the top 50 solare flares are Halo CMES which indicates that the highest class solar flares will

have a higher chance of being Halo CMES.



The mean of NASA HALO CME is 308/518 = .59%
The mean of top 50 solar flares = 44/50 = .88%

Variance(Top 50 Solar Flares) = 0.2410518626734843

Variance(Nasa) = 0.10559999999999999

'''


x = df3.plot.bar(x='Halo CME',y='val',rot=0)

plt.show()
