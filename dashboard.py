import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

# Load the CSV data
data = pd.read_excel("c_previous_application.xlsx")

# Check the data
print(data.head())

# Calculate the number of clients based on the 'SK_ID_PREV' column
noc = data['SK_ID_PREV'].count()  # Count of non-null entries in the 'SK_ID_PREV' column

# Add buttons to the sidebar
page = st.sidebar.radio("KMZ-LOANING SCHEME:", ["Home", "Show Clients", "Show Summary","Train Model", "Download Data"])

# Home Page
if page == "Home":
    # Box for Number of Clients
    with st.container():
        st.markdown(
            """
            <div style='padding: 10px; border: 1px solid #0099ff; border-radius: 5px; background-color: #000000; width: 250px; margin-left: 0; text-align: center;'>
                <h4 style='margin: 0; font-size: 18px;'>Number of Clients</h4>
                <h3 style='margin: 0; font-size: 24px;'>{}</h3>
            </div>
            """.format(noc),
            unsafe_allow_html=True
        )
    
    # Count the values in 'NAME_GOODS_CATEGORY' column
    # Count the values in 'NAME_GOODS_CATEGORY' column
    car_ownership_counts = data['NAME_GOODS_CATEGORY'].value_counts()

    # Create a smaller pie chart with Matplotlib
    fig, ax = plt.subplots(figsize=(5, 5))  # Adjust the size here
    ax.pie(car_ownership_counts, labels=car_ownership_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Style the box with custom HTML
    with st.container():
        st.markdown(
            """
            <div style='padding: 10px; border: 1px solid #000000; border-radius: 5px; background-color: #000000; width: 350px; margin: 0 auto; text-align: center;'>
                <h4 style='margin: 0; font-size: 18px; color: white;'>Goods Category Distribution</h4>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Display the pie chart in Streamlit
        st.pyplot(fig)

    # Example: Approval rates by employment
    fig1 = px.bar(data, x="AMT_GOODS_PRICE", y="NAME_CONTRACT_STATUS", color="NAME_CONTRACT_STATUS")
    fig1.show()

# Show Clients Page
elif page == "Show Clients":
    st.header("Here is the list of clients:")
    st.dataframe(data)  # Display the DataFrame when the button is clicked

# Show Summary Page
elif page == "Show Summary":
    st.header("Summary statistics:")
    st.write(data.describe())  # Display summary statistics

# Download Data Page
elif page == "Download Data":
    # Example functionality for a download button
    st.write("You can download the data from this link.")  # Replace with actual download functionality




# Example: Average Loan Amount by Weekday
#fig = px.line(data, x="WEEKDAY_APPR_PROCESS_START", y="Avg Loan Amount")
#fig.show()

# Example: Auto Approval by Car Ownership
#fig = px.pie(data, names='Car Ownership', values='Approval Count')
#fig.show()
