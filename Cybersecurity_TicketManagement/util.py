import numpy as np
import pandas as pd
import calendar

def tm_eda(df: pd.DataFrame,silent=True) -> pd.DataFrame:
    """
    1. Fill missing Escalated value with 'No'
    2. Clean up invalid date in Date columns (e.g., "31-02-2021 11:30:57" in Completed Date)
    3. Format Date columns 
    4. Extract Month, Day, Dayofweek from date column
    5. Response Time: time taken to response tickets (diff between Create Date and Picked Date)
    6. TTC: time taken to completion (diff between Create Date and Completed Date)
    7. TTW: time taken to work (diff between Picked Date and Completed Date)
    """

    df['Escalated'] = df.Escalated.fillna('No')

    df['Completed Date']=df['Completed Date'].replace("31-02-2021  11:30:57","2021-03-31 11:30:57")
    df['Completed Date']=pd.to_datetime(df['Completed Date'], format="%Y-%m-%d")

    df['Create_DayOfWeek'] = df['Create Date'].apply(lambda x: x.isoweekday())
    df = get_ymd(df,colname="Create Date")
    df = get_ymd(df,colname="Completed Date")

    df = get_timetaken(df,fromcol="Picked Date",tocol="Create Date",prefix_colname="ResponseTime",silent=silent)
    df = get_timetaken(df,fromcol="Completed Date",tocol="Create Date",prefix_colname="TTC",silent=silent)
    
    return df

def get_timetaken(df:pd.DataFrame, fromcol:str, tocol:str, prefix_colname: str, silent:bool) -> pd.DataFrame:
    """
    calculate time taken fromcol Date and tocol Date in various units
    """

    df[prefix_colname] = df.apply(lambda x: (x[fromcol] - x[tocol]).total_seconds(),axis=1)
    df[prefix_colname+"_day"] = df.apply(lambda x: (x[fromcol] - x[tocol]).days,axis=1)
    df[prefix_colname+"_min"] = df[prefix_colname].apply(lambda x: int(x/60))
    df[prefix_colname+"_hour"] = df[prefix_colname].apply(lambda x: int(x/(60*60)))
    
    invalid_records = df[df[prefix_colname]<0].shape[0]
    if invalid_records >0 :
        df = df[df[prefix_colname]>=0].copy()
        if not silent:
            print("**** There are {} records with invalid Date (negative duration) in {}".format(invalid_records, prefix_colname))
            print("**** These records are removed.")
            print("Number of records in the data (after remove): {}".format(df.shape))
    
    return df

def get_ymd(df: pd.DataFrame, colname:str) -> pd.DataFrame:
    """
    extract month and day of the given colname
    """
    prefixcolname = colname.split()[0]
    df[prefixcolname+"_Year"] = df[colname].dt.year
    df[prefixcolname+"_Month"] = df[colname].dt.month
    df[prefixcolname+"_Day"] = df[colname].dt.day
    return df


def get_gp_breakdown(dtc:pd.DataFrame, colname:str)->pd.DataFrame:
    """
    groupby colname and return percentage and count breakdown
    """
    df = dtc.groupby(colname).size().reset_index(name='Count')
    df['Percent'] = (df['Count']/df['Count'].sum())*100
    return df

def get_state_abbrev(df:pd.DataFrame)->pd.DataFrame:
    us_state_to_abbrev = {
                            "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
                            "California": "CA", "Colorado": "CO", "Connecticut": "CT",
                            "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
                            "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
                            "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
                            "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", 
                            "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
                            "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
                            "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND",
                            "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
                            "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
                            "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
                            "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
                            "District of Columbia": "DC", "American Samoa": "AS", "Guam": "GU", "Northern Mariana Islands": "MP",
                            "Puerto Rico": "PR", "United States Minor Outlying Islands": "UM", "U.S. Virgin Islands": "VI",
                        }
    df1 = df.copy()
    df1['State_Abbrev'] = df1.loc[:,'State'].map(us_state_to_abbrev)
    return df1

def get_monthly_create_ticket_count(df:pd.DataFrame, dfyear:int)->pd.DataFrame:
    tmp = df[(df.Create_Year==dfyear)].groupby(['Create_Year','Create_Month']).size().reset_index(name='Count')
    tmp['Month_abb']= tmp['Create_Month'].apply(lambda x: calendar.month_abbr[x])
    tmp['Month_Year'] = tmp.apply(lambda x: x['Month_abb']+"-"+str(x['Create_Year']),axis=1)
    
    return tmp

def calculate_pc(df:pd.DataFrame,colname:str,td:int):
    total = df.shape[0]
    inTD = df[df[colname]<td].shape[0]
    pc = round((inTD/total)*100,2)
    return pc

def get_top_assignee(df:pd.DataFrame)->str:
    t1 = df.groupby(['Assignee']).size().reset_index(name='Count')
    t2 = df.groupby(['Assignee','Customer Rating']).agg({
    "Ticket No":lambda x:x.count()
    }).reset_index()

    t = pd.merge(t1,t2,how='inner',on='Assignee')
    t['top_rating_pc']=t['Ticket No']/t['Count']
    t= t.sort_values(by="top_rating_pc",ascending=False)
    toppc = t.loc[:,'top_rating_pc'].values[0]
    top_assignee = list(t.loc[t['top_rating_pc']==toppc,'Assignee'].values)
    if len(top_assignee) >1:
        top_ = top_assignee[0]+" & "+str(len(top_assignee)-1)+"+"
    elif len(top_assignee) ==1:
        top_ = top_assignee[0]
    else:
        top_=""
    return top_