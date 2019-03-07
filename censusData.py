import numpy as np
import pandas as pd
import requests

# urls of detailed & subject tables with example (not used)
url = 'https://api.census.gov/data/2016/acs/acs5/subject?get=NAME,S1902_C01_001E,S2409_C05_006E&for=zip%20code%20tabulation%20area:*'
urlg = 'https://api.census.gov/data/2017/acs/acs5?get=NAME,group(B01001)&for=us:1'

#url fixed variables
urlbeg = 'https://api.census.gov/data/'

urlmid = '/acs/acs5/subject?get=NAME,'
urlmidd = '/acs/acs5?get=NAME,'

urlend = '&for=zip%20code%20tabulation%20area:*'

# reports, while independently stored in list by name
#, are a single string within the call, notice the reports & reports names are in inverse order

reportsf = 'S1902_C01_001E,S2409_C05_006E,S1251_C01_001E,S2301_C01_001E,S1701_C01_001E'
reportsd = 'B01003_001E,B19013_001E,B19301_001E,B25075_001E'
reportnames = ['PopInPoverty','PopEmployed','MarriedPastYr','PercentFemaleEmployed','EstMeanIncAll']
reportnamesd = ['PropVal', 'Per Capita Income','Household Income','Population']

# The looped variable in the calls are the years
years = ['2014', '2015', '2016', '2017']

def loadCensus1():
    # Intialize empty lists to store call urls and json requests of reports by
    #running a for loop appending each url in a string.
    urlsf = [(urlbeg + year + urlmid + reportsf + urlend) for year in years]
    reports1 = [requests.get(url).json() for url in urlsf]
    df_full1 = pd.DataFrame()
    for i, year in enumerate(years):
        df_one = pd.DataFrame([[g[6], g[5], g[4],g[3], g[2], g[1]] for g in reports1[i][1:]],
                                  columns = ['zip'] + reportnames)
        df_one['year'] = years[i]
        df_full1 = df_full1.append(df_one, ignore_index=True).reset_index(drop=True)
    
    df_full1['zip'] = df_full1['zip'].astype('str')
    df_full1['PopInPoverty'] = df_full1['PopInPoverty'].astype('int')
    df_full1['PopEmployed'] = df_full1['PopEmployed'].astype('int')
    df_full1['MarriedPastYr'] = df_full1['MarriedPastYr'].astype('str')
    df_full1['EstMeanIncAll'] = df_full1['EstMeanIncAll'].astype('int')
    df_full1['PercentFemaleEmployed'] = df_full1['PercentFemaleEmployed'].astype(float)
    
    return df_full1

def loadCensus2():
    urlsd = [(urlbeg + year + urlmidd + reportsd + urlend) for year in years]
    reports2 = [requests.get(url).json() for url in urlsd]
    df_full2 = pd.DataFrame()
    for i, year in enumerate(years):
        df_two = pd.DataFrame([[g[5], g[4], g[3], g[2], g[1]] for g in reports2[i][1:]], 
                                  columns = ['zip'] + reportnamesd)
        df_two['year'] = years[i]
        df_full2 = df_full2.append(df_two, ignore_index=True).reset_index(drop=True)
    
    df_full2['zip'] = df_full2['zip'].astype('str')
    df_full2['Per Capita Income'] = df_full2['Per Capita Income'].astype('str')
    df_full2['Household Income'] = df_full2['Household Income'].astype('str')
    df_full2['Population'] = df_full2['Population'].astype('int')
    df_full2['PropVal'] = df_full2['Population'].astype('int')
    
    return df_full2


