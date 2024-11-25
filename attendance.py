import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def process_attendance_data(data):
    data.rename(columns={
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
        'Recording disclaimer response': 'Responded',
    }, inplace=True)
    
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')
    
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    data['Attendance_Category'] = 'No Response'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 100) & (data['Duration_Minutes'] <= 150), 'Attendance_Category'] = '101–150 mins'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 50) & (data['Duration_Minutes'] <= 100), 'Attendance_Category'] = '51–100 mins'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 10) & (data['Duration_Minutes'] <= 50), 'Attendance_Category'] = '11–50 mins'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 0) & (data['Duration_Minutes'] <= 10), 'Attendance_Category'] = '1–10 mins'

    return data

# Add custom styles for a professional look
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

st.markdown('<div class="header">PROFESSIOAL ATTENDANCE DASHBOARD</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
     data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)

    category_counts = processed_data['Attendance_Category'].value_counts()


    st.markdown('<div class="section-title">ATTENDANCE OVERVIEW</div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="display: flex; justify-content: space-evenly; margin-bottom: 20px;">
            <div class="stat-box green">101–150 mins<br>{}</div>
            <div class="stat-box blue">51–100 mins<br>{}</div>
            <div class="stat-box yellow">11–50 mins<br>{}</div>
            <div class="stat-box orange">1–10 mins<br>{}</div>
            <div class="stat-box red">No Response<br>{}</div>
        </div>
    """.format(
        category_counts.get('101–150 mins', 0),
        category_counts.get('51–100 mins', 0),
        category_counts.get('11–50 mins', 0),
        category_counts.get('1–10 mins', 0),
        category_counts.get('No Response', 0),
    ), unsafe_allow_html=True)

    st.markdown('<div class="section-title">ATTENDANCE DISTRIBUTION</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = {
        '101–150 mins': '#4CAF50',
        '51–100 mins': '#2196F3',
        '11–50 mins': '#FFC107',
        '1–10 mins': '#FF9800',
        'No Response': '#F44336'
    }
    ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=[colors[key] for key in category_counts.index])
    ax.axis('equal')
    st.pyplot(fig)

    st.markdown('<div class="section-title">DETAILED ATTENDANCE DATA</div>', unsafe_allow_html=True)
    with st.expander("View 101–150 mins (Qualified Students)"):
        st.dataframe(processed_data[processed_data['Attendance_Category'] == '101–150 mins'][['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])
    with st.expander("View 51–100 mins (Moderately Attended)"):
        st.dataframe(processed_data[processed_data['Attendance_Category'] == '51–100 mins'][['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])
    with st.expander("View 11–50 mins (Short Duration Attendance)"):
        st.dataframe(processed_data[processed_data['Attendance_Category'] == '11–50 mins'][['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])
    with st.expander("View 1–10 mins (Very Short Attendance)"):
        st.dataframe(processed_data[processed_data['Attendance_Category'] == '1–10 mins'][['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])
    with st.expander("View No Response"):
        st.dataframe(processed_data[processed_data['Attendance_Category'] == 'No Response'][['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Responded']])

else:
    st.warning("Please upload a CSV file to proceed.")


   
