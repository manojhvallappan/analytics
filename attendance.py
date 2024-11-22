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
    qualified_data = data[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 101)]
    potentially_present_data = data[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 80) & (data['Duration_Minutes'] <= 101)]
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
            background-color: #f0f8ff;
        }
        .header {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px #888888;
        }
        .subheader {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333333;
        }
        .card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stat-box {
            text-align: center;
            padding: 20px;
            border-radius: 10px;
            margin: 10px;
            font-size: 18px;
            font-weight: bold;
            color: white;
        }
        .qualified {
            background-color: #4CAF50;
        }
        .potential {
            background-color: #2196F3;
        }
        .absent {
            background-color: #F44336;
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

    # Display stats in a single row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="stat-box qualified">Qualified Students<br>' + str(counts['Qualified']) + '</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-box potential">Potentially Present<br>' + str(counts['Potentially Present']) + '</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-box absent">Absent Students<br>' + str(counts['Absent']) + '</div>', unsafe_allow_html=True)

    # Pie chart
    st.markdown('<div class="subheader">Attendance Status Distribution</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = {'Qualified': '#4CAF50', 'Potentially Present': '#2196F3', 'Absent': '#F44336'}  # Green, Blue, Red
    status_counts = processed_data['Attendance_Status'].value_counts()
    ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90, colors=[colors[key] for key in status_counts.index])
    ax.axis('equal')
    st.pyplot(fig)

    # Display detailed data
    st.markdown('<div class="subheader">Student Details</div>', unsafe_allow_html=True)
    with st.expander("Qualified Students (Attended > 101 mins and Responded OK)"):
        st.dataframe(qualified_data[['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])
    with st.expander("Potentially Present Students (Attended 80–101 mins and Responded OK)"):
        st.dataframe(potentially_present_data[['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])
    with st.expander("Absent Students (Attended < 80 mins or Did Not Respond)"):
        st.dataframe(absent_data[['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])

else:
    st.warning("Please upload a CSV file to proceed.")
