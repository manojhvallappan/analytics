import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to process attendance data and classify based on duration and response
def process_attendance_data(data):
    data.rename(columns={
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
        'Recording disclaimer response': 'Responded',
    }, inplace=True)
    
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')
    
    # Calculate duration in minutes
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Classify attendance based on duration and response
    data['Attendance_Category'] = 'Absent'  # Default category is Absent
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 101) & (data['Duration_Minutes'] <= 120), 'Attendance_Category'] = 'Full Attendance (101–120 mins)'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 70) & (data['Duration_Minutes'] <= 100), 'Attendance_Category'] = 'Partial Attendance (70–100 mins)'

    return data

# Custom styles for a professional look
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
            margin-bottom: 20px;
        }
        .section-title {
            font-size: 20px;
            font-weight: bold;
            margin-top: 30px;
            margin-bottom: 10px;
            color: #F44336; /* Red color for section titles */
        }
        .stat-box {
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            margin: 10px;
            font-size: 16px;
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
        .orange {
            background-color: #FF9800;
        }
        .red {
            background-color: #F44336;
        }
        .card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Display dashboard title
st.markdown('<div class="header">PROFESSIONAL ATTENDANCE DASHBOARD</div>', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    # Read and process the data
    data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)

    # Attendance counts by category
    category_counts = processed_data['Attendance_Category'].value_counts()

    # Overview Section
    st.markdown('<div class="section-title">ATTENDANCE OVERVIEW</div>', unsafe_allow_html=True)
    st.markdown(""" 
        <div style="display: flex; justify-content: space-evenly; margin-bottom: 20px;">
            <div class="stat-box green">Full Attendance (101–120 mins)<br>{}</div>
            <div class="stat-box blue">Partial Attendance (70–100 mins)<br>{}</div>
            <div class="stat-box red">Absent<br>{}</div>
        </div>
    """.format(
        category_counts.get('Full Attendance (101–120 mins)', 0),
        category_counts.get('Partial Attendance (70–100 mins)', 0),
        category_counts.get('Absent', 0),
    ), unsafe_allow_html=True)

    # Pie Chart Section
    st.markdown('<div class="section-title">ATTENDANCE DISTRIBUTION</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = {
        'Full Attendance (101–120 mins)': '#4CAF50',
        'Partial Attendance (70–100 mins)': '#2196F3',
        'Absent': '#F44336'
    }
    ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=[colors[key] for key in category_counts.index])
    ax.axis('equal')
    st.pyplot(fig)

    # Detailed Data Section
    st.markdown('<div class="section-title">DETAILED ATTENDANCE DATA</div>', unsafe_allow_html=True)
    with st.expander("View Full Attendance (101–120 mins)"):
        st.dataframe(processed_data[processed_data['Attendance_Category'] == 'Full Attendance (101–120 mins)'][['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])
    with st.expander("View Partial Attendance (70–100 mins)"):
        st.dataframe(processed_data[processed_data['Attendance_Category'] == 'Partial Attendance (70–100 mins)'][['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])
    with st.expander("View Absent"):
        st.dataframe(processed_data[processed_data['Attendance_Category'] == 'Absent'][['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])

else:
    st.warning("Please upload a CSV file to proceed.")
