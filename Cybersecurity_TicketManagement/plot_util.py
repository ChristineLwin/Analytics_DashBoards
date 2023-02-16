import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import util as ut

rating_color = {'Good (4)':'blue', 'Excellent (5)':'green',
                'Satisfactory (3)':'orange', 'Unsatisfactory (2)':'red'}

def create_donut(df:pd.DataFrame,lbl_col:str, val_col:str,title_text="")->go.Figure:
    if lbl_col=="Customer Rating":
        # rating_color = {'Good (4)':'blue', 'Excellent (5)':'green',
        #         'Satisfactory (3)':'orange', 'Unsatisfactory (2)':'red'}
        fig = go.Figure(data=[go.Pie(labels=df[lbl_col], 
                             values=df[val_col], 
                             hole=.75,
                             textinfo ='label+percent',
                             hoverinfo="label+percent+name",
                             pull=[0, 0, 0, 0.2],
                             marker_colors=df["Customer Rating"].map(rating_color)
                            )])
    else:
        
        fig = go.Figure(data=[go.Pie(labels=df[lbl_col], 
                             values=df[val_col], 
                             hole=.75,
                             textinfo ='label+percent',
                             hoverinfo="label+percent+name",
                            )])

    fig.update_layout(showlegend= False, width=270,height=200,
                    margin=dict(l=88, r=70, t=20, b=20),
                  #title_text=title_text,title_x=0.5,
                  annotations=[dict(text=title_text, x=0.5, y=0.5, font_size=18, showarrow=False)]
                 )
    return fig


def create_monthly_ticket_trend(df:pd.DataFrame,dfyear:int)->go.Figure:
    tmp = ut.get_monthly_create_ticket_count(df,dfyear)
    fig = px.line(tmp, x="Month_Year", y="Count", 
             #template='simple_white', 
             width=700,height=300,
            )
    fig.update_layout(
                margin=dict(l=20, r=50, t=20, b=20), 
                title="Monthly ticket trend",
                title_x=0.25,
                )
    fig.update_xaxes(tickangle=-45)
    return fig

def create_hist(df:pd.DataFrame,colname:str,binsize:int,xtitle:str)->go.Figure:
    fig = px.histogram(df, x=colname, 
                        facet_col='Priority',
                        color='Customer Rating',
                        color_discrete_map = rating_color,
                        template='simple_white',
                        category_orders={"Priority":["High", "Medium", "Low"]},
                        width=750,height=300,
                        facet_col_spacing=0.04,
                        #title="Distribution of response time to ticket",
                    )

    fig.update_traces(xbins=dict( # bins used for histogram
                        start=0,
                        end=30,#df['ResponseTime_day'].max(),
                        size=binsize,
                    ),
    
    )
    fig.for_each_xaxis(lambda x: x.update(title = ''))
    fig.update_layout(
                #title_x=0.25,
                yaxis_title="No. of Tickets",
                bargap=0.05,
                margin=dict(l=0, r=0, t=20, b=0),
                annotations = list(fig.layout.annotations) + 
                [go.layout.Annotation(
                        x=0.5,
                        y=-0.20,
                        font=dict(
                                size=14
                            ),
                        showarrow=False,
                    text=xtitle,
                    #textangle=-90,
                    xref="paper",
                    yref="paper"
                    )
                ]
                )
    
    return fig

def create_box(df:pd.DataFrame,collist:list)->go.Figure:
    
    t1 = df.groupby(collist).size().reset_index(name='Count').copy()
    fig = px.box(t1, x=collist[0], y=collist[1], color=collist[2],
             color_discrete_map={"Yes":'red',"No":'blue'}, 
             height=350,width=700,
             
             )
    fig.update_layout(
                yaxis_title="Time to Completion (Days)",
                margin=dict(l=70, r=0, t=100, b=30), 
                title="Distribution of rating by time to completion",
                title_x=0.25,
                )
    #fig.update_xaxes(tickangle=-45)
    return fig

def create_map(df):
    df = ut.get_state_abbrev(df)
    states_choropleth=px.choropleth(data_frame=df,
                                locations=df.State_Abbrev.value_counts().index,
                                locationmode='USA-states',
                                color=df.State_Abbrev.value_counts().array,
                                color_continuous_scale='reds',
                                scope='usa',
                                basemap_visible=True,
                                title='Tickets Opened by State',
                                labels={'color':'No. of Tickets'},
                                width=800, height=300,
                                )
    states_choropleth.update_layout(
        paper_bgcolor='#ffffff',
        margin=dict(l=100, r=200, t=30, b=30),
        showlegend=False, 
        title_x=0.25)

    return states_choropleth