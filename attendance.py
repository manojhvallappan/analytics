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
    }, inplace=True)
    
    # Convert 'Join_Time' and 'Leave_Time' to datetime
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')
    
    # Calculate Duration in minutes
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Filter students with attendance duration greater than or equal to 120 minutes
    filtered_data = data[data['Duration_Minutes'] >= 120]
    
    return filtered_data

# If a file is uploaded
if uploaded_file:
    # Read the CSV file into a DataFrame
    data = pd.read_csv(uploaded_file)
    
    # Check the structure of the file (optional)
    st.write("Columns in the uploaded CSV file:", data.columns)
    st.write("First 5 rows of the data:", data.head())

    # Process attendance data
    filtered_data = process_attendance_data(data)

    # Display the filtered data with students who attended for more than 120 minutes
    st.title("Attendance Report")
    st.write(f"Number of students with attendance > 120 minutes: {len(filtered_data)}")
    
    # Display filtered data in a clickable format
    student_names = filtered_data['Name (original name)'].tolist()
    selected_student = st.selectbox("Select a student to view details", student_names)

    # Fetch the student's data
    student_data = filtered_data[filtered_data['Name (original name)'] == selected_student].iloc[0]

    # Display specific details about the selected student
    st.write(f"### {selected_student}'s Attendance Details")
    st.write(f"**Email:** {student_data['Email']}")
    st.write(f"**Join Time:** {student_data['Join_Time']}")
    st.write(f"**Leave Time:** {student_data['Leave_Time']}")
    st.write(f"**Duration (minutes):** {student_data['Duration_Minutes']}")
    
    # Check if the student qualifies for attendance
    if student_data['Duration_Minutes'] >= 120:
        st.success(f"{selected_student} has earned the attendance.")
    else:
        st.error(f"{selected_student} does not qualify for the attendance.")
    
    # Display summary statistics (optional)
    st.write("Summary of Attendance Duration:")
    st.write(filtered_data['Duration_Minutes'].describe())

else:
    st.warning("Please upload a CSV file to proceed.")



