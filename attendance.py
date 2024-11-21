import streamlit as st
import pandas as pd

# File uploader
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    # Load data
    data = pd.read_csv(uploaded_file)

    # Rename columns to match the expected names
    data.rename(columns={
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
    }, inplace=True)

    # Parse the 'Join_Time' and 'Leave_Time' columns as datetime
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')

    # Calculate duration in minutes
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Filter students based on duration
    filtered_data = data[data['Duration_Minutes'] >= 120]

    # Display filtered data
    st.write("Students with Duration ≥ 120 minutes:")
    st.write(filtered_data)

    # Summary statistics
    st.write("Summary:")
    st.write(filtered_data.describe())

else:
    st.warning("Please upload a CSV file to proceed.")



