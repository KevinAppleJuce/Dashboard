import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="dashboard", page_icon=":bar_chart:", layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
st.title(" :bar_chart: KMZ-LOANING SCHEME")

fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    data = pd.read_csv(fl, encoding='ISO-8859-1') if filename.endswith('.csv') else pd.read_excel(fl)
else:
    os.chdir(r"C:\Users\Grizzly\Documents\CISM623\test")
    data = pd.read_excel("c_previous_application.xlsx")

# Sidebar for filters and buttons
st.sidebar.header("Sidebar")
contracttype = st.sidebar.multiselect("Pick Contract Type", data["NAME_CONTRACT_TYPE"].unique())
loanpurpose = st.sidebar.multiselect("Loan Purpose", data["NAME_CASH_LOAN_PURPOSE"].unique())
repeateornew = st.sidebar.multiselect("Repeate Or New", data["NAME_CLIENT_TYPE"].unique())

# Adding buttons
view_data = st.sidebar.button("View Data")
feedback = st.sidebar.button("Feedback")

# Display dataset if View Data is clicked
if view_data:
    st.subheader("Dataset Preview")
    st.dataframe(data)

# Feedback section
if feedback:
    st.subheader("Feedback")
    feedback_text = st.text_area("Please provide your feedback:")
    
    if st.button("Submit Feedback"):
        if feedback_text:
            st.success("Thank you for your feedback!")
            # Clear the text area
            feedback_text = ""
        else:
            st.warning("Please enter some feedback before submitting.")

# Apply filters
filtered_data = data.copy()

# Filter by contract type
if contracttype:
    filtered_data = filtered_data[filtered_data["NAME_CONTRACT_TYPE"].isin(contracttype)]

# Filter by loan purpose
if loanpurpose:
    filtered_data = filtered_data[filtered_data["NAME_CASH_LOAN_PURPOSE"].isin(loanpurpose)]

# Filter by repeat or new client
if repeateornew:
    filtered_data = filtered_data[filtered_data["NAME_CLIENT_TYPE"].isin(repeateornew)]

# Ensure that the 'NAME_YIELD_GROUP' column is numeric
filtered_data["NAME_YIELD_GROUP"] = pd.to_numeric(filtered_data["NAME_YIELD_GROUP"], errors='coerce')



# Aggregate data for the bar chart
category_data = filtered_data.groupby(by=["NAME_CONTRACT_STATUS"], as_index=False)["AMT_APPLICATION"].sum()

# Column 1: Bar chart
column1, column2 = st.columns((2))
with column1:
    st.subheader("Contract Status by Yield Group")
    fig = px.bar(
        category_data, 
        x="NAME_CONTRACT_STATUS", 
        y="AMT_APPLICATION", 
        text=[f'${x:,.2f}' for x in category_data["AMT_APPLICATION"]], 
        template="seaborn"
    )
    st.plotly_chart(fig, use_container_width=True, height=200)

# Column 2: Pie chart
with column2:
    st.subheader("Distribution of Contract Types")
    contract_type_counts = filtered_data["NAME_CONTRACT_TYPE"].value_counts().reset_index()
    contract_type_counts.columns = ["NAME_CONTRACT_TYPE", "count"]
    
    fig = px.pie(
        contract_type_counts, 
        values="count", 
        names="NAME_CONTRACT_TYPE", 
        hole=0.5
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
