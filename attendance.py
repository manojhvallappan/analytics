import streamlit as st
import pandas as pd

# File uploader
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    # Load data
    data = pd.read_csv(uploaded_file)
    
    # Display columns to check if 'Join_Time' and 'Leave_Time' exist
    st.write("Columns in the uploaded CSV file:", data.columns)
    
    # Ensure 'Join_Time' and 'Leave_Time' columns exist
    if 'Join_Time' in data.columns and 'Leave_Time' in data.columns:
        # Parse these as datetime
        data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
        data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')

        # Calculate duration in minutes
        data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

        # Filter students based on duration (≥ 120 minutes)
        filtered_data = data[data['Duration_Minutes'] >= 120]

        # Check if students responded to the host (assuming column 'Responded')
        if 'Responded' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['Responded'] == "Yes"]

        # Calculate attendance percentage (assuming a column 'Attendance_Percentage')
        if 'Attendance_Percentage' in filtered_data.columns:
            final_data = filtered_data[filtered_data['Attendance_Percentage'] >= 90]
        else:
            st.error("Attendance percentage column is missing.")
            st.stop()

        # Display final filtered data
        st.write("Students with Attendance > 90%, Duration ≥ 120 mins, and Responded:")
        st.write(final_data)

        # Summary statistics
        st.write("Summary:")
        st.write(final_data.describe())
    else:
        st.error("CSV file is missing required columns: 'Join_Time' and 'Leave_Time'. Please check the CSV file.")
else:
    st.warning("Please upload a CSV file to proceed.")

