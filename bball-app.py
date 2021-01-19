import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


#---Display dict
display_dict = {#'Hall of Famer': 'HOF',
 #'Season': 'Season',
 #'Age': 'Age',
 #'Team': 'Tm',
 #'League': 'Lg',
 #'Position': 'Pos',
 #'Games': 'G',
 #'Games Started': 'GS',
 'Minutes Played': 'MP',
 'Field Goals': 'FG',
 'Field Goal Attempts': 'FGA',
 'Field Goal Percentage': 'FG%',
 '3-pointers made': '3P',
 '3-point Attempts': '3PA',
 '3-point Percentage': '3P%',
 '2-pointers made': '2P',
 '2-point Attempts': '2PA',
 '2-point Percentage': '2P%',
 'Effective Field Goal Percentage': 'eFG%',
 'Free Throws': 'FT',
 'Free Throw Attempts': 'FTA',
 'Free Throw Percentage': 'FT%',
 'Offensive Rebounds': 'ORB',
 'Defensive Rebounds': 'DRB',
 'Total Rebounds': 'TRB',
 'Assists': 'AST',
 'Steals': 'STL',
 'Blocks': 'BLK',
 'Turnovers': 'TOV',
 'Personal Fouls': 'PF',
 'Points': 'PTS'}


#---


#--- Function Gets Composite score for each position based on selected stats for each position.
def get_score(x):
    if x['Pos'] == 'PG':
        return sum(x[pg_stat_columns])
    elif x['Pos'] == 'PF':
        return sum(x[pf_stat_columns])
    elif x['Pos'] == 'C':
        return sum(x[c_stat_columns])
    elif x['Pos'] == 'SG':
        return sum(x[sg_stat_columns])
    elif x['Pos'] == 'SF':
        return sum(x[sf_stat_columns])
    else:
        return -1

st.header('RDream Team Selector')
#st.subheader('Choose your positions:')

st.subheader('Choose desired stats for each position:')

#---DataFrame read in with some null values removed
#df = pd.read_csv(st.file_uploader('File uploader'), index_col=0) #---'./data/final_players.csv'

df = pd.read_csv('./top_players_by_season.csv', index_col=0)
df = df[df['Pos'].isna() == 0]
df = df[df['Pos'].str.contains('Did Not Play') == False]


st.subheader('Point Guard:')
pg_stats = st.multiselect('PG Stats', list(display_dict.keys()))
pg_stat_columns = [display_dict[i] for i in pg_stats]


st.subheader('Shooting Guard:')
sg_stats = st.multiselect('SG Stats', list(display_dict.keys()))
sg_stat_columns = [display_dict[i] for i in sg_stats]

st.subheader('Small Forward:')
sf_stats = st.multiselect('SF Stats', list(display_dict.keys()))
sf_stat_columns = [display_dict[i] for i in sf_stats]

st.subheader('Power Forward:')
pf_stats = st.multiselect('PF Stats', list(display_dict.keys()))
pf_stat_columns = [display_dict[i] for i in pf_stats]

st.subheader('Center:')
c_stats = st.multiselect('C Stats', list(display_dict.keys()))
c_stat_columns = [display_dict[i] for i in c_stats]


#-----------Scaling--------------


#---Columns to be scaled
scale_list = ['G','GS','MP','FG','FGA','FG%','3P','3PA','3P%','2P','2PA','2P%','eFG%','FT','FTA','FT%','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS']
df.dropna(axis=0, subset=scale_list, inplace=True) #--subset=scale_list,
df[scale_list].apply(pd.to_numeric, errors='coerce')

#---Peronal Fouls converted to inversion
df['PF'] = 5 - df['PF']

mms = MinMaxScaler(feature_range=(0, 1))
x = df[scale_list]
x_scaled = mms.fit_transform(x)
df[scale_list] = x_scaled
#---Turnovers converted to negative number
df['TOV'] = np.negative(df['TOV'])

#---Calculates Composite Score
df['composite'] = [get_score(df.iloc[i]) for i in range(len(df))]
#---
df[scale_list] = mms.inverse_transform(df[scale_list])


pg_df = df.loc[df['Pos'] == 'PG'].sort_values('composite', ascending=False).head(10)
pg_df.index = np.arange(1, len(pg_df) + 1)
sf_df = df.loc[df['Pos'] == 'SF'].sort_values('composite', ascending=False).head(10)
sf_df.index = np.arange(1, len(sf_df) + 1)
sg_df = df.loc[df['Pos'] == 'SG'].sort_values('composite', ascending=False).head(10)
sg_df.index = np.arange(1, len(sg_df) + 1)
pf_df = df.loc[df['Pos'] == 'PF'].sort_values('composite', ascending=False).head(10)
pf_df.index = np.arange(1, len(pf_df) + 1)
c_df = df.loc[df['Pos'] == 'C'].sort_values('composite', ascending=False).head(10)
c_df.index = np.arange(1, len(c_df) + 1)



#---------Printing tables of result rankings
st.subheader('Point Guards:')
if len(pg_stat_columns) > 0:
    st.dataframe(pg_df[['name', 'Tm', 'Season', 'Pos'] + pg_stat_columns])

st.subheader('Shooting Guards:')
if len(sg_stat_columns) > 0:
    st.dataframe(sg_df[['name', 'Tm', 'Season', 'Pos'] + sg_stat_columns])

st.subheader('Small Forwards:')
if len(sf_stat_columns) > 0:
    st.dataframe(sf_df[['name', 'Tm', 'Season', 'Pos'] + sf_stat_columns])

st.subheader('Power Forwards:')
if len(pf_stat_columns) > 0:
    st.dataframe(pf_df[['name', 'Tm', 'Season', 'Pos'] + pf_stat_columns])

st.subheader('Centers:')
if len(c_stat_columns) > 0:
    st.dataframe(c_df[['name', 'Tm', 'Season', 'Pos'] + c_stat_columns])
