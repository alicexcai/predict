import streamlit as st

# Custom imports 
from multipage import MultiPage
from pages import testpage, visualize, experiment

# Create an instance of the app 
app = MultiPage()
apptitle = 'PARAM'
st.set_page_config(page_title=apptitle, page_icon=":brain:")
st.sidebar.markdown("## Select a page")

# Title of the main page
st.title("PARAM")
app.add_page("Visualize Data", visualize.app)
app.add_page("Run Experiment", experiment.app)

# Add all your applications (pages) here
app.add_page("Experiment 2", testpage.app)
# app.add_page("Experiment", experiment.app)
# app.add_page("Visualize", visualize.app)

# app.add_page("Upload Data", data_upload.app)
# app.add_page("Change Metadata", metadata.app)
# app.add_page("Machine Learning", machine_learning.app)
# app.add_page("Data Analysis",data_visualize.app)
# app.add_page("Y-Parameter Optimization",redundant.app)

# The main app
app.run()