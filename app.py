
__author__ = "Hari Krishna Veerala"
__credits__ = ["", ""]
__license__ = ""
__version__ = "1.0.1"
__maintainer__ = ""
__email__ = "veeralakrishna.com"
__status__ = "Development" # Production/Development


VERSION = "0.2.2"
#---------------------------------------------------------------------------
#                                imports
#---------------------------------------------------------------------------

import os
import json
import numpy as np
import matplotlib.cm as cm

import plotly.graph_objs as go


from pathlib import Path
from functools import reduce
from operator import itemgetter
from plyfile import PlyData, PlyElement

import streamlit as st

from utils import *





#------------------------------------------------------------------------------------------------
#                                page configuration
#------------------------------------------------------------------------------------------------

st.set_page_config(
     page_title="Surface-Triangulation",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://github.com/veeralakrishna/Surface-Triangulation',
         'Report a bug': "https://github.com/veeralakrishna/Surface-Triangulation",
         'About': """# Ply Data Viewer using Plotly Surface Triangulation"""
     }
 )



Path(f"Output").mkdir(parents=True, exist_ok=True)

car_models_list = next(os.walk("data/car_models_json"))[2]
car_models_list = [i.replace(".json", "") for i in car_models_list]


ply_file_list = next(os.walk("data/ply_data"))[2]
ply_file_list = [i.replace(".ply", "") for i in ply_file_list]

# insert None at index 0
car_models_list.insert(0, None)
ply_file_list.insert(0, None)


# -------------------------------------------------------------------------------------------
h1, h2, h3 = st.columns((0.1,0.8, 0.1))

with h1:
    pass
with h2:
    st.markdown("<h1 style='text-align: center;'>Surface-Triangulation</h1>", 
                unsafe_allow_html=True)
    st.markdown(f"""<h5 style='text-align: justify;'>
                Ply Data Viewer
                </h5>""", 
                    unsafe_allow_html=True)
    
with h3:
    pass


# -------------------------------------------------------------------------------------------
m1, m2, m3 = st.columns(3, gap="large")

filename = None
with m1: 
    
    select_data = st.selectbox("Select Sample Data", [None, "JSON(Car Models)", "Ply Files"])
        
    if select_data == "Ply Files":
        with m2:
            filename = st.selectbox("Select Sample Ply File", ply_file_list)
            data_type = ".ply"
    
    elif select_data == "JSON(Car Models)":
        with m3:
            filename = st.selectbox("Select Sample JSON File", car_models_list)
            data_type = ".json"


if filename:
    
    m4, m5 = st.columns([0.2, 0.8], gap="small")
    
    with m4:
        paper_bgcolr_sel = st.selectbox("Select Paper Background", 
                                        paper_bgcolr, 
                                        index=paper_bgcolr.index('peachpuff'))
        width = st.slider("Select Width",
                            min_value=700, 
                        max_value=1400, 
                        value=1000, 
                        step=50) 
        height = st.slider("Select Height",
                        min_value=500, 
                        max_value=1200, 
                        value=600, 
                        step=50) 
        
    with m5: 
        with st.container():
            plotly_Surface_Triangulation(filename, #car_models_list[1],
                                        data_type=data_type,
                                        axis=True,
                                        paper_bgcolor=paper_bgcolr_sel,
                                        width=width,
                                        height=height,
                                        save_html=None
                                        )