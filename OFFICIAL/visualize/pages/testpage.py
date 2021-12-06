import collections
from numpy.core.defchararray import lower
import streamlit as st
import numpy as np
import pandas as pd
import sqlite3
# import utils


def app():
    st.subheader("Run Experiment")
    # st.markdown("#### Parameter exploration. Data management. Statistical analysis.") 

    # Code to read a single file 
    uploaded_file = st.file_uploader("Choose your experiment file", type = ['csv', 'xlsx', 'sqlite', 'db'])
    global data
    if uploaded_file is not None:
        if uploaded_file.filename.endswith('.sqlite'):
            # data = pd.DataFrame(pd.read_sql_query('SELECT * FROM data', uploaded_file))
            conn = sqlite3.connect(uploaded_file)
            data = pd.read_sql_query("SELECT * FROM table_name", conn)
        try:
            data = pd.read_csv(uploaded_file)
        except Exception as e:
            print(e)
            data = pd.read_excel(uploaded_file)


    ''' Load the data and save the columns with categories as a dataframe. 
    This section also allows changes in the numerical and categorical columns. '''
    if st.button("Run Experiment"):
        
        # Raw data 
        st.dataframe(data)
        data.to_csv('data/main_data.csv', index=False)

        # Collect the categorical and numerical columns 
        
        numeric_cols = data.select_dtypes(include=np.number).columns.tolist()
        categorical_cols = list(set(list(data.columns)) - set(numeric_cols))
        
        # Save the columns as a dataframe or dictionary
        columns = []

        # Iterate through the numerical and categorical columns and save in columns 
        # columns = utils.genMetaData(data) 
        
        # Save the columns as a dataframe with categories
        # Here column_name is the name of the field and the type is whether it's numerical or categorical
        columns_df = pd.DataFrame(columns, columns = ['column_name', 'type'])
        columns_df.to_csv('data/metadata/column_type_desc.csv', index = False)

        # Display columns 
        st.markdown("**Column Name**-**Type**")
        for i in range(columns_df.shape[0]):
            st.write(f"{i+1}. **{columns_df.iloc[i]['column_name']}** - {columns_df.iloc[i]['type']}")
        
        st.markdown("""The above are the automated column types detected by the application in the data. 
        In case you wish to change the column types, head over to the **Column Change** section. """)