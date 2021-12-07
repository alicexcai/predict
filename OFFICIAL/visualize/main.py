import streamlit as st

from multipage import MultiPage
from pages import visualize, experiment

app = MultiPage()
apptitle = 'PARAM'
st.set_page_config(page_title=apptitle, page_icon=":brain:")
st.sidebar.markdown("## Select a page")

st.title("PARAM")
app.add_page("Visualize Data", visualize.app)
app.add_page("Run Experiment", experiment.app)

app.run()