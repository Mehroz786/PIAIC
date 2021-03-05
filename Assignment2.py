import pandas as pd
import numpy as np
import  re
import matplotlib.pyplot as plt

uri = "Q2_Pandas_Assignments"
fileNames = ['states0.csv','states1.csv','states2.csv','states3.csv','states4.csv','states5.csv','states6.csv','states7.csv','states8.csv','states9.csv']
dataframes = []
for i in range(len(fileNames)):
    url = '\\'.join([uri,fileNames[i]])
    dataframes.append(pd.read_csv(url,index_col=[0]))

# Merging all dataframes into one dataframe
us_census = pd.concat(dataframes,ignore_index=True)
print("Us_census Rows",len(us_census))

# Utility Functions
def to_string(val):
    """Converts the DataType of any Series to String"""
    return val.astype('string')

def col_in_proper_format(str_val):
    """Takes Pandas Series as argument and
        Changes the DataType to float
        return Pandas Series"""
    pat2='[$MF%]'
    # regex1 = re.compile(pat)
    if str_val[0].startswith('$'):
        str_val=to_string(str_val)
        result = str_val.str.split(pat2,expand=True)[1]
        result[result==""]='0' # Assign '0' value to empty string
        return np.round(result.astype('float'),2) # change the dtype to float and round of to two decimal points
    elif str_val[0].endswith('M') or str_val[0].endswith('F'):
        result = str_val.str.split(pat2,expand=True)[0]
        result[result==""]='0' # Assign '0' value to empty string
        result = result.astype('int64')
        result.replace(0,np.nan,inplace=True)
        return result
    elif str_val[0].endswith('%'):
        str_val=to_string(str_val)
        result = str_val.str.split(pat2,expand=True)[0]
        result[result==""]='0' # Assign '0' value to empty string
        return np.round(result.astype('float'),0) # change the dtype to float and round of to two decimal points
def col_splitter(combinedCol,separator):
    combinedCol = to_string(combinedCol)
    men = combinedCol.str.split(separator,expand=True)[0]
    women = combinedCol.str.split(separator,expand=True)[1]
    return men, women

us_census['men_Pop'],us_census['women_Pop'] = col_splitter(us_census.GenderPop,'_')
us_census.men_Pop = col_in_proper_format(us_census.men_Pop)
us_census.women_Pop = col_in_proper_format(us_census.women_Pop)
us_census.women_Pop.fillna(us_census.TotalPop-us_census.men_Pop,inplace=True)

us_census.Income = col_in_proper_format(us_census.Income)
us_census.drop_duplicates(keep ='first',inplace=True)
plt.scatter(us_census.women_Pop,us_census.Income)
plt.show()
print(us_census.columns)
us_census.Hispanic = col_in_proper_format(us_census.Hispanic)
us_census.White = col_in_proper_format(us_census.White)
us_census.Black = col_in_proper_format(us_census.Black)
us_census.Native = col_in_proper_format(us_census.Native)
us_census.Asian = col_in_proper_format(us_census.Asian)
us_census.Pacific = col_in_proper_format(us_census.Pacific)
us_census.Pacific.fillna(method = 'ffill',inplace=True)
histogram_data = [us_census.Hispanic,us_census.White,us_census.Black,us_census.Asian,us_census.Native,us_census.Pacific]
print(us_census.head())
# plt.figure(figsize=(150,100))
plt.title('Histograms of Races')
plt.xlabel('Races')
plt.ylabel('Population in Percentage')
plt.hist(histogram_data,bins=100,label=["Hispanic",'White','Black','Asian','Native','Pacific'],rwidth=.95,histtype='bar')
plt.legend(loc='best') # Positioning the legend
plt.show()