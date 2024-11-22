import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to process attendance data
def process_attendance_data(data):
    data.rename(columns={
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
        'Recording disclaimer response': 'Responded',
    }, inplace=True)
    
    # Convert 'Join_Time' and 'Leave_Time' to datetime
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')
    
    # Calculate duration in minutes
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Filter categories
    qualified_data = data[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 110)]
    potentially_present_data = data[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 80) & (data['Duration_Minutes'] <= 110)]
    absent_data = data[~data.index.isin(qualified_data.index) & ~data.index.isin(potentially_present_data.index)]

    # Add attendance status
    data['Attendance_Status'] = 'Absent'
    data.loc[qualified_data.index, 'Attendance_Status'] = 'Qualified'
    data.loc[potentially_present_data.index, 'Attendance_Status'] = 'Potentially Present'

    return data, qualified_data, potentially_present_data, absent_data

# Add custom styles
st.markdown("""
    <style>
        body {
            background-color: #f9f9f9;
        }
        .header {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 30px;
        }
        .subheader {
            color: #333;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .card {
            background-color: #f4f4f4;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        hr {
            border: none;
            border-top: 2px solid #ddd;
            margin: 20px 0;
        }
    </style>
""", unsafe_allow_html=True)

# Display dashboard title
st.markdown('<div class="header">Attendance Dashboard</div>', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    # Read and process the data
    data = pd.read_csv(uploaded_file)
    processed_data, qualified_data, potentially_present_data, absent_data = process_attendance_data(data)

    # Attendance counts
    counts = {
        'Qualified': len(qualified_data),
        'Potentially Present': len(potentially_present_data),
        'Absent': len(absent_data),
    }

    # Display overview
    st.markdown('<div class="subheader">Overview</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card">
        <b>Total Students:</b> {len(processed_data)} <br>
        <b>Qualified Students:</b> {counts['Qualified']} <br>
        <b>Potentially Present Students:</b> {counts['Potentially Present']} <br>
        <b>Absent Students:</b> {counts['Absent']}
    </div>
    """, unsafe_allow_html=True)

    # Pie chart
    st.markdown('<div class="subheader">Attendance Status Distribution</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = {'Qualified': '#4CAF50', 'Potentially Present': '#2196F3', 'Absent': '#F44336'}
    status_counts = processed_data['Attendance_Status'].value_counts()
    ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90, colors=[colors[key] for key in status_counts.index])
    ax.axis('equal')
    st.pyplot(fig)

    # Display detailed data
    st.markdown('<div class="subheader">Student Details</div>', unsafe_allow_html=True)

    # Qualified Students
    if len(qualified_data) > 0:
        st.markdown("**Qualified Students (Attended > 110 mins and Responded OK):**")
        st.dataframe(qualified_data[['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])
    else:
        st.markdown("No students qualified.")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Potentially Present Students
    if len(potentially_present_data) > 0:
        st.markdown("**Potentially Present Students (Attended 80–110 mins and Responded OK):**")
        st.dataframe(potentially_present_data[['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])
    else:
        st.markdown("No potentially present students.")

    st.markdown("<hr>", unsafe_allow_html=True)

    # Absent Students
    if len(absent_data) > 0:
        st.markdown("**Absent Students (Attended < 80 mins or Did Not Respond):**")
        st.dataframe(absent_data[['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])
    else:
        st.markdown("No absent students.")

else:
    st.warning("Please upload a CSV file to proceed.")
