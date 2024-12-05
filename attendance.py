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

# If the file is uploaded
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)
    
    # Filter by Date
    st.sidebar.header("Filter by Date")
    start_date = st.sidebar.date_input("Start Date", processed_data['Join_Time'].min())
    end_date = st.sidebar.date_input("End Date", processed_data['Join_Time'].max())
    
    filtered_data = processed_data[(processed_data['Join_Time'] >= pd.Timestamp(start_date)) & 
                                   (processed_data['Join_Time'] <= pd.Timestamp(end_date))]

    if not filtered_data.empty:
        total_students = len(filtered_data)
        full_present_count = len(filtered_data[filtered_data['Attendance_Category'] == 'PRESENT'])
        partially_present_count = len(filtered_data[filtered_data['Attendance_Category'] == 'PARTIALLY PRESENT'])
        absent_count = len(filtered_data[filtered_data['Attendance_Category'] == 'ABSENT'])
        average_duration = filtered_data['Duration (minutes)'].mean()

        st.markdown(f"**Total Students:** {total_students}")
        st.markdown(f"**Present:** {full_present_count}")
        st.markdown(f"**Partially Present:** {partially_present_count}")
        st.markdown(f"**Absent:** {absent_count}")
        st.markdown(f"**Average Attendance Duration:** {average_duration:.2f} minutes")

        # Bar chart for Attendance Trends
        attendance_trend = filtered_data.groupby(filtered_data['Join_Time'].dt.date)['Name'].count()
        st.bar_chart(attendance_trend)

        # Download Button
        csv = filtered_data.to_csv(index=False)
        st.download_button(label="Download Attendance Report", data=csv, file_name="attendance_report.csv", mime="text/csv")

        # Detailed Attendance Data
        st.markdown("### Detailed Attendance Data")
        st.dataframe(filtered_data[['Name', 'Join_Time', 'Leave_Time', 'Duration (minutes)', 'Login_Count', 'Logout_Count', 'Feedback']])
    else:
        st.warning("No data available for the selected date range.")
else:
    st.info("Please upload a CSV file to view the attendance data.")
