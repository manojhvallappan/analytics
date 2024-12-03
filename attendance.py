import streamlit as st
import pandas as pd

def process_attendance_data(data):
    # Check for required columns and handle missing columns
    required_columns = {'Name', 'Join_Time', 'Leave_Time', 'Responded', 'Feedback'}
    missing_columns = required_columns - set(data.columns)
    
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        return pd.DataFrame()  # Return empty DataFrame if columns are missing

    # Convert join and leave times to datetime
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')

    # Calculate attendance duration in minutes
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Categorize attendance
    data['Attendance_Category'] = 'Absent'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 100), 'Attendance_Category'] = 'Full Present (100-120 mins)'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 70) & (data['Duration_Minutes'] < 100), 'Attendance_Category'] = 'Partially Present (70-100 mins)'
    
    return data

# Streamlit UI
st.title("Student Attendance and Feedback Dashboard")
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    try:
        data = pd.read_csv(uploaded_file)
        processed_data = process_attendance_data(data)

        if not processed_data.empty:
            st.subheader("Attendance Overview")
            for category in ["Full Present (100-120 mins)", "Partially Present (70-100 mins)", "Absent"]:
                with st.expander(f"{category}"):
                    filtered_data = processed_data[processed_data['Attendance_Category'] == category]
                    if not filtered_data.empty:
                        st.dataframe(filtered_data[['Name', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Feedback']])
                    else:
                        st.write(f"No students found in the {category} category.")
        else:
            st.warning("Processed data is empty. Please check the uploaded file.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a CSV file to view the attendance report.")
