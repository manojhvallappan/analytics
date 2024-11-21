import streamlit as st
import pandas as pd

# File uploader
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

# Function to calculate duration and filter based on the criteria
def process_attendance_data(data):
    # Rename columns for consistency
    data.rename(columns={
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
        'Recording disclaimer response': 'Responded',
    }, inplace=True)
    
    # Convert 'Join_Time' and 'Leave_Time' to datetime
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')
    
    # Calculate Duration in minutes
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Filter students who have responded with "OK" to the disclaimer and attended for more than 110 minutes
    qualified_data = data[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 110)]

    # Filter students who have responded with "OK" to the disclaimer and attended for 80+ minutes but <= 110 minutes
    potentially_present_data = data[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 80) & (data['Duration_Minutes'] <= 110)]
    
    return qualified_data, potentially_present_data

# If a file is uploaded
if uploaded_file:
    # Read the CSV file into a DataFrame
    data = pd.read_csv(uploaded_file)
    
    # Process attendance data
    qualified_data, potentially_present_data = process_attendance_data(data)

    # Display the filtered data with students who have responded and attended for more than 110 minutes
    st.title("Attendance Report")
    
    # Show success message if there are students who qualify for attendance
    if len(qualified_data) > 0:
        st.success(f"These students qualify for the attendance: {len(qualified_data)}")
        st.write(qualified_data[['Name (original name)', 'Email', 'Duration_Minutes']])
    else:
        st.warning("No students qualify for the attendance based on the given criteria.")
    
    # Show students who are potentially present
    if len(potentially_present_data) > 0:
        st.warning(f"These students are potentially present (80+ minutes): {len(potentially_present_data)}")
        st.write(potentially_present_data[['Name (original name)', 'Email', 'Duration_Minutes']])
    else:
        st.info("No students are potentially present based on the given criteria.")

    # Display the summary statistics (optional)
    st.write("Summary of Attendance Duration (filtered):")
    st.write(f"Qualified students' duration summary:")
    st.write(qualified_data['Duration_Minutes'].describe())
    
    st.write(f"Potentially present students' duration summary:")
    st.write(potentially_present_data['Duration_Minutes'].describe())

else:
    st.warning("Please upload a CSV file to proceed.")




