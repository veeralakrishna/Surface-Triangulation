__author__ = "Hari Krishna Veerala"
__credits__ = []
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = ""
__status__ = "Development" # Production/Development


# import packages
import base64
import json
import pickle
import uuid
import re


import streamlit as st
import pandas as pd
import numpy as np



##############################################
#              Streamlit Utilities
##############################################


# Hide the Streamlit header and footer
def hide_header_footer():
    """
    Function to hide header & footer of streamlit app

    """
    hide_streamlit_style = """
                <style>
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Load dataset
@st.cache(allow_output_mutation=True)
def load_data(data_file):
    """
    load_data reads csv files

    Used st.cache decorator to cache data

    Parameters:
    ************************
    data_file:
                fileuploader object

    Returns:
    *********************
    df:
        Pandas dataframe
    """
    # Read csv using pandas
    data = pd.read_csv(data_file)
    # Copy dataframe
    df = data.copy()
    # return dataframe
    return df


@st.cache(allow_output_mutation=True)
def load_excel(data_file):
    """
    load_excel reads the excel file

    *Note: st.cache decorator is used
    Streamlit provides a caching mechanism that allows your app to stay performant
    even when loading data from the web, manipulating large datasets, or performing
    expensive computations. This is done with the @st.cache decorator.*

    Parameters:
    ************************
    data_file:
            object from uploader

    Returns:
    ************************
    xls :
         Dataframe/ dictionary of dataframes(for multiple sheets)

    sheet_names:
                list of sheet names in excel file
    """
    # read excel using pandas
    exls = pd.read_excel(data_file, sheet_name=None)
    # make a copy of df
    xls = exls.copy()
    # extract sheet names to a list
    sheet_names = list(xls.keys())
    # return datframe & sheet names
    return xls, sheet_names


@st.cache
def returnCatNumList(df):
    """
    Function to get numeric columns and object columns from dataframe

    Parameters:
    ****************
    df:
        A dataframe

    Returns:
    *****************
    object_cols(list):
                        Object columns in list

    numeric_cols(list):
                        Numeric columns in list

    """

    # Get object columns
    object_cols = list(df.select_dtypes(exclude=np.number).columns)
    # Get numeric columns
    numeric_cols = list(df.select_dtypes(include=np.number).columns)

    # return object & numeric column
    return object_cols, numeric_cols



# Extracts var from datetime column
def extract_timeline(data, date_col):
    """
    Function to extract year, month, day, day name and month name features

    Parameters:
    ******************
    data    : dataframe

    date_col: pandas datetime column in str

    Returns:
    ****************
    df : dataframe

    """

    df = data.copy()

    df['Year'] = df[date_col].dt.year
    df['Month'] = df[date_col].dt.month
    df['Day'] = df[date_col].dt.day
    df['Day_of_week'] = df[date_col].dt.day_name()
    df['Month_Name'] = df[date_col].dt.month_name()

    return df


def download_button(object_to_download, download_filename, button_text, pickle_it=False):
    """
    Generates a link to download the given object_to_download.
    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    some_txt_output.txt download_link_text (str): Text to display for download
    link.
    button_text (str): Text to display on download button (e.g. 'click here to download file')
    pickle_it (bool): If True, pickle file.
    Returns:
    -------
    (str): the anchor tag to download object_to_download
    Examples:
    --------
    download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
    download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')
    """
    if pickle_it:
        try:
            object_to_download = pickle.dumps(object_to_download)
        except pickle.PicklingError as e:
            st.write(e)
            return None

    else:
        if isinstance(object_to_download, bytes):
            pass

        elif isinstance(object_to_download, pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)

        # Try JSON encode for everything else
        else:
            object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub(r'\d+', '', button_uuid)

    # background-color: rgb(255, 255, 255);
    custom_css = f"""
        <style>
            #{button_id} {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: rgb(180, 177, 186);
                color: rgb(38, 39, 48);
                padding: .25rem .75rem;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(180, 177, 186);
                border-image: initial;
            }}
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = custom_css + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'

    return dl_link

