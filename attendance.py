import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

    # Display pie chart for qualified vs potentially present students
    if len(qualified_data) > 0 or len(potentially_present_data) > 0:
        # Pie chart data
        status_labels = ['Qualified Students', 'Potentially Present Students']
        status_counts = [len(qualified_data), len(potentially_present_data)]

        fig, ax = plt.subplots()
        ax.pie(status_counts, labels=status_labels, autopct='%1.1f%%', startangle=90, colors=['#4CAF50', '#FF9800'])
        ax.axis('equal')  # Equal aspect ratio ensures the pie is circular.
        st.write("### Student Attendance Status")
        st.pyplot(fig)

        # Display bar chart for the distribution of attendance duration
        if len(qualified_data) > 0:
            st.write("### Duration Distribution for Qualified Students (Attendance > 110 minutes)")
            fig, ax = plt.subplots()
            sns.histplot(qualified_data['Duration_Minutes'], bins=10, kde=True, color='#4CAF50', ax=ax)
            ax.set_title("Attendance Duration for Qualified Students")
            ax.set_xlabel("Duration (minutes)")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

        if len(potentially_present_data) > 0:
            st.write("### Duration Distribution for Potentially Present Students (Attendance 80-110 minutes)")
            fig, ax = plt.subplots()
            sns.histplot(potentially_present_data['Duration_Minutes'], bins=10, kde=True, color='#FF9800', ax=ax)
            ax.set_title("Attendance Duration for Potentially Present Students")
            ax.set_xlabel("Duration (minutes)")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

    else:
        st.warning("No students qualify for attendance based on the given criteria.")
else:
    st.warning("Please upload a CSV file to proceed.")


