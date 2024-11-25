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

    # Create attendance categories
    data['Attendance_Category'] = 'No Response or < 10 mins'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 100), 'Attendance_Category'] = '> 100 mins'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 50) & (data['Duration_Minutes'] <= 100), 'Attendance_Category'] = '50–100 mins'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 10) & (data['Duration_Minutes'] < 50), 'Attendance_Category'] = '10–50 mins'

    return data

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
        .green {
            background-color: #4CAF50;
        }
        .blue {
            background-color: #2196F3;
        }
        .yellow {
            background-color: #FFC107;
        }
        .red {
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
    processed_data = process_attendance_data(data)

    # Attendance counts by category
    category_counts = processed_data['Attendance_Category'].value_counts()

    # Display stats in a single row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="stat-box green">> 100 mins<br>' + str(category_counts.get('> 100 mins', 0)) + '</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-box blue">50–100 mins<br>' + str(category_counts.get('50–100 mins', 0)) + '</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-box yellow">10–50 mins<br>' + str(category_counts.get('10–50 mins', 0)) + '</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stat-box red">No Response or < 10 mins<br>' + str(category_counts.get('No Response or < 10 mins', 0)) + '</div>', unsafe_allow_html=True)

    # Pie chart
    st.markdown('<div class="subheader">Attendance Status Distribution</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = {
        '> 100 mins': '#4CAF50', 
        '50–100 mins': '#2196F3', 
        '10–50 mins': '#FFC107', 
        'No Response or < 10 mins': '#F44336'
    }
    ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=[colors[key] for key in category_counts.index])
    ax.axis('equal')
    st.pyplot(fig)

    # Display detailed data in columns
    st.markdown('<div class="subheader">Detailed Attendance Data</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**> 100 mins**")
        st.dataframe(processed_data[processed_data['Attendance_Category'] == '> 100 mins'][['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])
        st.markdown("**50–100 mins**")
        st.dataframe(processed_data[processed_data['Attendance_Category'] == '50–100 mins'][['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])
    
    with col2:
        st.markdown("**10–50 mins**")
        st.dataframe(processed_data[processed_data['Attendance_Category'] == '10–50 mins'][['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])
        st.markdown("**No Response or < 10 mins**")
        st.dataframe(processed_data[processed_data['Attendance_Category'] == 'No Response or < 10 mins'][['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])

else:
    st.warning("Please upload a CSV file to proceed.")

   
  

