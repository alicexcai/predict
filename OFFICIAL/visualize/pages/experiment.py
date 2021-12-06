import collections
from numpy.core.defchararray import lower
import streamlit as st
import numpy as np
import pandas as pd
import sqlite3
# import utils
import importlib
import os

# TEMPORARY ################################################################################################################
# from .components.params import MetaParams
from doepy import build
import sys
########################################################################################################################


def app():
    st.subheader("Run Experiment")
    # st.markdown("#### Parameter exploration. Data management. Statistical analysis.") 
        
    dirname = st.sidebar.text_input("Enter your data directory path:", os.path.dirname(__file__))
    # dirname = os.path.join(os.path.dirname(__file__), '../data')
    local_files_list = [file for file in os.listdir(dirname) if file.endswith('.py') and not file.startswith('.')] # Ignore hidden files
    
    with st.sidebar.expander("See data in current directory"):
        st.write(local_files_list)
        
    selected_function = st.selectbox('Select Datasets', local_files_list)
    function_file = os.path.join(dirname, selected_function)
    # st.write(selected_function)
        
    uploaded_file = st.file_uploader("Choose a file", type = ['py'])
    with st.expander("See file code "):
        
        st.code(open(function_file).read())
        if uploaded_file is not None:
            uploaded_file_contents = uploaded_file.read().decode("utf-8") 
            st.code(uploaded_file_contents)
        # with uploaded_file as f:
        #     # block = str(f.read())
        #     # st.markdown(str(block))
        #     st.code(f.read())
        
    # with st.echo():
    #     st.write('This code will be printed')
    #     eval(uploaded_file)

    # Code to read a single file 

    # global data
    # if uploaded_file is not None:
    #     if uploaded_file.filename.endswith('.sqlite'):
    #         # data = pd.DataFrame(pd.read_sql_query('SELECT * FROM data', uploaded_file))
    #         conn = sqlite3.connect(uploaded_file)
    #         data = pd.read_sql_query("SELECT * FROM table_name", conn)
    #     try:
    #         data = pd.read_csv(uploaded_file)
    #     except Exception as e:
    #         print(e)
    #         data = pd.read_excel(uploaded_file)
    
    params_tested = build.full_fact(
    {'liquidity': [100.0, 200.0],
    'num_rounds': [60.0, 120.0]}
    )
    params_const = {
        'outcomes': ['Harvard', 'Yale'],
        'agents_list': ['Nerd(1, \'first\', 1000)', 'Nerd(2, \'second\', 1000)', 'Nerd(3, \'third\', 1000)'],
        'mechanism': 'logarithmic',
        'i_shares': {'Harvard': 0.0, 'Yale': 0.0 },
                    }
    # meta_params = MetaParams(
    #     params_tested=['liquidity', 'num_rounds'],
    #     params_const=['outcomes', 'agents_list', 'mechanism', 'i_shares'],
    #     results_primary=['cost', 'probability_Harvard', 'probability_Yale', 'shares_Harvard', 'shares_Yale'],
    #     results_full=['cost', 'probabilities', 'shares', 'p_shares', 'payments']
    # )


    ''' Load the data and save the columns with categories as a dataframe. 
    This section also allows changes in the numerical and categorical columns. '''
    if st.button("Run Exploration"):
        
        # moduleNames = ['sys', 'os', 're', 'unittest', uploaded_file.name] 
        # modules = map(__import__, moduleNames)
        
        st.write("The automatic import of the uploaded / specified file is not working. Feature to be developed.")
        
        # st.write(selected_function[0:-3])
 
        import importlib
        # st.write("successful importlib import")
        # st.write(selected_function[0:-3], type(selected_function[0:-3]))
        mymodule = importlib.import_module(str(selected_function[0:-3]))
        st.write(type(mymodule))
        my_function = getattr(mymodule, 'main')
        
        st.write(type(my_function))
        
        # my_function = getattr(__import__(selected_function[0:-3]), 'main')
        
        # import importlib
        # def import_from(module, name):
        #     module = __import__(module, fromlist=[name])
        #     return getattr(module, name)

        experiment_name = "Test"
        # db = sqlite3.connect("%s.sqlite"%experiment_name)
        # cursor = db.cursor()
        # import_from(selected_function[0:-3], "main")
        
        # eval(f'import {a}')
        # eval(f'{a}.{b}')
        
        my_function(experiment_name, params_tested, params_const, meta_params)
        
        
        # to_run = importlib.import_module(uploaded_file.name)
        # to_run.doe(params_tested, params_const, meta_params)
        st.write("Exploration complete.")
        
        
        # eval(uploaded_file.name)
        
        # to_run = importlib.import_module(uploaded_file.name)
        # to_run(params_tested, params_const, meta_params)
        
        
        # from contextlib import contextmanager, redirect_stdout
        # from io import StringIO
        # from time import sleep

        # @contextmanager
        # def st_capture(output_func):
        #     with StringIO() as stdout, redirect_stdout(stdout):
        #         old_write = stdout.write

        #         def new_write(string):
        #             ret = old_write(string)
        #             output_func(stdout.getvalue())
        #             return ret
                
        #         stdout.write = new_write
        #         yield


        # output = st.empty()
        # with st_capture(output.code):
        #     print("Hello")
        #     eval("python3 doe.py")

        # output = st.empty()
        # with st_capture(output.info):
        #     print("Goodbye")
        
            
            
            
            
            
            
            
        
        # Raw data 
        # st.dataframe(data)
        # data.to_csv('data/main_data.csv', index=False)

        # # Collect the categorical and numerical columns 
        
        # numeric_cols = data.select_dtypes(include=np.number).columns.tolist()
        # categorical_cols = list(set(list(data.columns)) - set(numeric_cols))
        
        # # Save the columns as a dataframe or dictionary
        # columns = []

        # # Iterate through the numerical and categorical columns and save in columns 
        # # columns = utils.genMetaData(data) 
        
        # # Save the columns as a dataframe with categories
        # # Here column_name is the name of the field and the type is whether it's numerical or categorical
        # columns_df = pd.DataFrame(columns, columns = ['column_name', 'type'])
        # columns_df.to_csv('data/metadata/column_type_desc.csv', index = False)

        # # Display columns 
        # st.markdown("**Column Name**-**Type**")
        # for i in range(columns_df.shape[0]):
        #     st.write(f"{i+1}. **{columns_df.iloc[i]['column_name']}** - {columns_df.iloc[i]['type']}")