# -*- coding: utf-8 -*-
"""
Created on Wed May 13 15:00:39 2020

@author: Ashok
"""

import os
import pandas as pd
import numpy as np
from statistics import mode
#from geopy.geocoders import Nominatim
#from geopy.distance import geodesic
#import folium 
#from folium.plugins import MarkerCluster
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import re
import fileinput
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly import tools
import plotly.express as px
os.chdir("D:\Dash")


data=pd.read_csv("studentdata_lat_lon.csv")
del data['Unnamed: 0']


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout=html.Div([
        html.Div([
                html.H5(["Select year"]),
                dcc.Dropdown(
                id="year",
                options=[{'label':i,'value':i} for i in data['Year'].unique()],
                value=2015
                ),
                html.H5(["Select class"]),
                dcc.Dropdown(
                id="class",
#                options=[{'label':i,'value':i} for i in data['Class'].unique()],
                value="VI"
                ),
                html.H5(["Select grade"]),
                dcc.Dropdown(
                id="grade",
#                options=[{'label':i,'value':i} for i in data['Grade'].unique()],
                value="A"
                ),
                html.H5(["Select subjects for data table plot"]),
                dcc.Dropdown(
                id="datatable_sub",
                options=[{'label':i,'value':i} for i in data.columns],
                multi=True,
                value=['Year', 'Class', 'Grade', 'StudentName', 'Telugu_PT1(40)','Telugu_PT2(80)', 'Telugu_PT3(100)']
                ),
                html.H5(["Select subjects for Five number summary"]),
                dcc.Dropdown(
                id="sub_summary",
                options=[{'label':i,'value':i} for i in data.columns[4:22]],
                multi=True,
                value=['Telugu_PT1(40)']
                ),
                        
                html.H5(["Select subject for Ternary plot"]),
                dcc.Dropdown(
                id="sub",
                options=[{'label':i,'value':i} for i in ["Telugu","Hindi","English","Maths","Science","Social"]],
                
                value='Telugu'
                ),
                
                html.H5(["Select subjects for Scatter 3D plot"]),
                dcc.Dropdown(
                id="sub3d",
                options=[{'label':i,'value':i} for i in ["Telugu","Hindi","English","Maths","Science","Social"]],
                
                value='Telugu'
                ),
                html.H5(["Select subjects for Distribution plot"]),
                dcc.Dropdown(
                id="sub_dist",
                options=[{'label':i,'value':i} for i in data.columns[4:22]],
                
                value='Telugu_PT1(40)'
                )
                
                
                ],style={'width': '24%',"height":"100%","float":"left",'display': 'inline-block',"position":"fixed","overflow":"scroll"}),
        
                
        html.Div([
                html.H5(["Data table"]),
                dcc.Graph(id="datatable"),
                
                html.H5(["The five number summary of selected subject"]),
                dcc.Graph(id="summary"),
                
                html.H5(["Ternary plot"]),
                dcc.Graph(id="ter_fig"),
                
                html.H5(["Scatter 3D plot"]),
                dcc.Graph(id="scatter_fig"),
                
                
                html.H5(["Distribution plot"]),
                dcc.Graph(id="dist_fig"),
                
                 
                dcc.Graph(id="dist_fig_box"),
#                dcc.Graph(id="pcat_prof_fig"),
#                
#                html.H5(["Parllel coordinates"]),
#                dcc.Graph(id="pcoor_fig"),
#                
#                
#                html.H5(["Grade wise plot with distance"]),
                
                
                
                ],style={'width': '70%','float':'right'}),
    
    
        
        
        ])
@app.callback(
        Output('class','options'),
        [Input("year",'value')])
def class_options(syear):
    return [{'label':i,'value':i} for i in data[data["Year"]==syear]["Class"].unique()]

@app.callback(
        Output('grade','options'),
        [Input("year",'value'),
         Input("class",'value')])
def grade_options(syear,sclass):
    return [{'label':i,'value':i} for i in data[(data["Year"]==syear) & (data["Class"]==sclass)]["Grade"].unique()]
"""
@app.callback(
        Output('student','options'),
        [Input("year",'value'),
         Input("class",'value'),
         Input("grade","value")])
def student_options(syear,sclass,sgrade):
    return [{'label':i,'value':i} for i in data[(data["Year"]==syear) & (data["Class"]==sclass) & (data["Grade"]==sgrade)]["StudentName"].unique()]
"""
@app.callback(
        Output("datatable","figure"),
        [Input("year",'value'),
         Input("class",'value'),
         Input("grade","value"),
         Input("datatable_sub","value")])
def datatable(y,c,g,s):
    data_grade=data[(data["Year"]==y)&(data['Class']==c)&(data['Grade']==g)]
    v=[]
    for i in s:
        v.append(data_grade[i])
        
    fig = go.Figure(data=[go.Table(
    header=dict(values=s,
                fill_color='paleturquoise',
                align='left'),
                
    
    
    cells=dict(values=v,
               fill_color='lavender',
               align='left'))
    ])
    return fig

@app.callback(
        Output("summary","figure"),
        [Input("year",'value'),
         Input("class",'value'),
         Input("grade","value"),
         Input("sub_summary","value")])
def summary(y,c,g,s):
    data_grade=data[(data["Year"]==y)&(data['Class']==c)&(data['Grade']==g)]
    
    fig = go.Figure()
    for i in s:
       fig.add_trace(go.Box(y=data_grade[i],name=i))
    
#    fig=go.Figure(data=go.box(y=data_grade[s[0]]))
    return fig



@app.callback(
        Output('ter_fig','figure'),
        [Input("year",'value'),
         Input("class",'value'),
         Input("grade","value"),
         Input("sub","value")])

def ternary(y,c,g,s):
    data_grade=data[(data["Year"]==y)&(data['Class']==c)&(data['Grade']==g)]
    subs=[]
    for i in data_grade.columns:
        if s in i:
            subs.append(i)
    fig = px.scatter_ternary(data_grade, a=subs[0], b=subs[1], c=subs[2],hover_name="StudentName",color="address",size="Distance(Km)",size_max=15,symbol="address")
#                             hover_name="district", color="winner", size="total", size_max=15,
    
    return fig
    
@app.callback(
        Output('scatter_fig','figure'),
        [Input("year",'value'),
         Input("class",'value'),
         Input("grade","value"),
         Input("sub","value")])

def scatter(y,c,g,s):
    data_grade=data[(data["Year"]==y)&(data['Class']==c)&(data['Grade']==g)]
    subs=[]
    for i in data_grade.columns:
        if s in i:
            subs.append(i)
    fig = px.scatter_3d(data_grade, x=subs[0], y=subs[1], z=subs[2],hover_name="StudentName",color="address",size="Distance(Km)",size_max=25,symbol="address")
#                             hover_name="district", color="winner", size="total", size_max=15,
    
    return fig

@app.callback(
        Output('dist_fig','figure'),
        [Input("year",'value'),
         Input("class",'value'),
         Input("grade","value"),
         Input("sub_dist","value")]) 

def dist(y,c,g,s):
    data_grade=data[(data["Year"]==y)&(data['Class']==c)&(data['Grade']==g)]
    fig=px.histogram(data_grade,x=s,y="Distance(Km)",color="Father's_Education",marginal="rug",hover_data=data_grade.columns[0:5])
    return fig
    
@app.callback(
        Output('dist_fig_box','figure'),
        [Input("year",'value'),
         Input("class",'value'),
         Input("grade","value"),
         Input("sub_dist","value")]) 

def dist_box(y,c,g,s):
    data_grade=data[(data["Year"]==y)&(data['Class']==c)&(data['Grade']==g)]
    data_class=data[(data["Year"]==y)&(data['Class']==c)]
    fig=px.histogram(data_class,x=s,y="Distance(Km)",color="Father's_Education",marginal="box",hover_data=data_grade.columns[0:5])
    return fig   

    
       
if __name__=="__main__":
    app.run_server()


#data_grade=data[(data["Year"]==2015)&(data['Class']=='VI')&(data['Grade']=='A')]
#data_grade.columns
