import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

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
    
    # Filter students who have not responded or attended for less than 80 minutes
    absent_data = data[~data.index.isin(qualified_data.index) & ~data.index.isin(potentially_present_data.index)]
    
    # Add a column to categorize students as Qualified, Potentially Present, or Absent
    data['Attendance_Status'] = 'Absent'
    data.loc[qualified_data.index, 'Attendance_Status'] = 'Qualified'
    data.loc[potentially_present_data.index, 'Attendance_Status'] = 'Potentially Present'
    
    return data, qualified_data, potentially_present_data, absent_data

# If a file is uploaded
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    # Read the CSV file into a DataFrame
    data = pd.read_csv(uploaded_file)
    
    # Process attendance data
    processed_data, qualified_data, potentially_present_data, absent_data = process_attendance_data(data)

    # Display the filtered data with students who have responded and attended for more than 110 minutes
    st.title("Attendance Report")

    # Display pie chart for qualified, potentially present, and absent students
    if len(processed_data) > 0:
        # Pie chart data
        status_counts = processed_data['Attendance_Status'].value_counts()

        fig, ax = plt.subplots()
        ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF9800', '#F44336'])
        ax.axis('equal')  # Equal aspect ratio ensures the pie is circular.
        st.write("### Student Attendance Status")
        st.pyplot(fig)

        # Show details of Qualified students
        st.write("### Qualified Students (Attended > 110 minutes and Responded OK)")
        st.write(qualified_data)

        # Show details of Potentially Present students
        st.write("### Potentially Present Students (Attended between 80-110 minutes and Responded OK)")
        st.write(potentially_present_data)

        # Show details of Absent students
        st.write("### Absent Students (Did not respond or attended < 80 minutes)")
        st.write(absent_data)

    else:
        st.warning("No students qualify for attendance based on the given criteria.")

    # Add image at the bottom with "Done by" text
    image = Image.open('photoss/mano.jpg')  # Adjusted to use relative path
    st.image(image, use_column_width=True)
    st.markdown("### Done by Manojh Vallappan")

else:
    st.warning("Please upload a CSV file to proceed.")

