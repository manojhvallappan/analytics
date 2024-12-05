import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to process attendance data
def process_attendance_data(data):
    data.rename(columns={
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
        'Name (original name)': 'Name',
        'Recording disclaimer response': 'Responded',
        'Feedback': 'Feedback',
        'Times of Login': 'Login_Count',
        'Times of Logout': 'Logout_Count'
    }, inplace=True)
    
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')
    
    data['Duration (minutes)'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60
    data['Attendance_Category'] = 'ABSENT'
    
    data.loc[(data['Responded'] == 'OK') & (data['Duration (minutes)'] > 100), 'Attendance_Category'] = 'PRESENT'
    data.loc[(data['Responded'] == 'OK') & (data['Duration (minutes)'].between(70, 100)), 'Attendance_Category'] = 'PARTIALLY PRESENT'
    
    return data

# Streamlit App Header
st.title("ZOOM LOG ANALYTICS DASHBOARD")

# File Upload
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)

    st.markdown("### Date Range of Uploaded Data")
    min_date = processed_data['Join_Time'].min()
    max_date = processed_data['Join_Time'].max()
    st.write(f"**Earliest Date:** {min_date}")
    st.write(f"**Latest Date:** {max_date}")

    st.write("### Sample Data:")
    st.write(processed_data[['Name', 'Join_Time', 'Leave_Time']].head(5))

    # Date filtering
    st.sidebar.header("Filter by Date")
    start_date = st.sidebar.date_input("Start Date", min_date.date() if min_date else None)
    end_date = st.sidebar.date_input("End Date", max_date.date() if max_date else None)

    # Filtered data
    if min_date and max_date:
        filtered_data = processed_data[(processed_data['Join_Time'] >= pd.Timestamp(start_date)) & 
                                       (processed_data['Join_Time'] <= pd.Timestamp(end_date))]

        if not filtered_data.empty:
            st.markdown(f"**Total Records for Selected Date Range:** {len(filtered_data)}")
            st.dataframe(filtered_data[['Name', 'Join_Time', 'Leave_Time', 'Duration (minutes)', 'Attendance_Category']])
        else:
            st.warning("No data available for the selected date range.")
    else:
        st.warning("No valid dates available in the uploaded file.")
else:
    st.info("Please upload a CSV file to view the attendance data.")
