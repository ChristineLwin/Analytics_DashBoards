import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import util as ut
import plot_util as pltut
pd.set_option('display.max_columns', 25)

df = pd.read_excel("Ticket Details.xlsx")
df1 = ut.tm_eda(df,silent=True)


st.set_page_config(
    page_title = 'Cybersecurity Ticket Management Dashboard',
    page_icon = '✅',
    layout = 'wide'
)


st.title("Cybersecurity Ticket Managment Dashboard")

# creating a single-element container.
placeholder = st.empty()

with placeholder.container():
    cat_filter = st.selectbox("Select Cybersecurity Category", pd.unique(df1['Category']))
    cat_df = df1[df1['Category']==cat_filter]

    kpi1, kpi2,kpi3,kpi4= st.columns(4)
    kpi1.metric(label="Respone within 24 hours ⌛", value=ut.calculate_pc(cat_df,colname="ResponseTime_hour",td=24))
    kpi2.metric(label="Completed within 24 hours 🏆", value= ut.calculate_pc(cat_df,colname="TTC_hour",td=24))
    kpi3.metric(label="Completed within 7 days ✅ ", value= ut.calculate_pc(cat_df,colname="TTC_day",td=7))
    kpi4.metric(label="Top Rating Assignee ⭐", value= ut.get_top_assignee(cat_df))
    

    fig_col1, fig_col2, fig_col3 = st.columns(3)
    with fig_col1:
        #st.markdown("### Ticket Type")
        t1 = ut.get_gp_breakdown(cat_df,colname="Reached via")
        fig1 = pltut.create_donut(t1,"Reached via","Percent","Ticket")
        st.write(fig1)

    with fig_col2:
        #st.markdown("### Priority")
        t2 = ut.get_gp_breakdown(cat_df,colname="Priority")
        fig2 = pltut.create_donut(t2,"Priority","Percent","Priority")
        st.write(fig2)

    with fig_col3:
        #st.markdown("### Customer Rating")
        t3 = ut.get_gp_breakdown(cat_df,colname="Customer Rating")
        fig3 = pltut.create_donut(t3,"Customer Rating","Percent","Rating")
        st.write(fig3)
    
    
    fig_col4, fig_col5 = st.columns(2)

    with fig_col4:
        st.markdown("###### Distribution of response time to ticket")
        intval = st.slider(label="Select Bin Size: # Days",min_value=1,max_value=14, value=1)
        fig4 = pltut.create_hist(cat_df,colname="ResponseTime_day",binsize=intval,xtitle="Response Time(Days)")
        st.write(fig4)

    with fig_col5:
        fig5 = pltut.create_box(cat_df,collist=['Customer Rating','TTC_day','Escalated'])
        st.write(fig5)

    fig_col6, fig_col7 = st.columns(2)
    with fig_col6:
        #st.markdown("#### Monthly Ticket Trend")
        fig6 = pltut.create_monthly_ticket_trend(cat_df,dfyear=2021)
        st.write(fig6)
    
    with fig_col7:
        #st.markdown("#### Tickets Opened by States")
        fig7 = pltut.create_map(cat_df)
        st.write(fig7)