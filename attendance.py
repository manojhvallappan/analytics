import streamlit as st
import pandas as pd

def process_attendance_data(data):
    # Renaming columns to match expected processing names
    data.rename(columns={
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
        'Name (original name)': 'Name',
        'Recording disclaimer response': 'Responded',
        'Feedback': 'Feedback'
    }, inplace=True)

    # Convert join and leave times to datetime
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')

    # Calculate duration in minutes
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Categorize attendance
    data['Attendance_Category'] = 'Absent'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 100), 'Attendance_Category'] = 'Full Present (100+ mins)'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 70) & (data['Duration_Minutes'] <= 100), 'Attendance_Category'] = 'Partially Present (70-100 mins)'
    data.loc[(data['Responded'] != 'OK') | (data['Duration_Minutes'].isna()), 'Attendance_Category'] = 'No Response'

    return data

# Streamlit dashboard setup
st.title("Attendance Dashboard with Feedback")

# File uploader
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)

    if not processed_data.empty:
        st.subheader("Attendance Summary")

        for category in ['Full Present (100+ mins)', 'Partially Present (70-100 mins)', 'No Response']:
            filtered_data = processed_data[processed_data['Attendance_Category'] == category]
            st.markdown(f"### {category} (Total: {len(filtered_data)})")

            if filtered_data.empty:
                st.write(f"No students found in the {category} category.")
            else:
                st.dataframe(filtered_data[['Name', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Feedback']])
    else:
        st.warning("Processed data is empty. Please check the uploaded file.")
else:
    st.info("Please upload a CSV file to view the attendance data.")
