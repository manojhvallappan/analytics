import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to process attendance data
def process_attendance_data(data):
    data.rename(columns={
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
        'Name (original name)': 'Name',
        'Recording disclaimer response': 'Responded',
        'Feedback': 'Feedback',
        'Times of Login': 'Login_Count',
        'Times of Logout': 'Logout_Count',
        'Rating': 'Rating'
    }, inplace=True)

    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')

    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Categorize attendance based on duration
    data['Attendance_Category'] = 'ABSENT'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 100), 'Attendance_Category'] = 'PRESENT'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 70) & (data['Duration_Minutes'] <= 100), 'Attendance_Category'] = 'PARTIALLY PRESENT'

    # Poll Participation: Check if 'Poll_Response' exists
    if 'Poll_Response' in data.columns:
        data['Poll_Participated'] = data['Poll_Response'].apply(lambda x: 'YES' if pd.notna(x) else 'NO')
    else:
        data['Poll_Participated'] = 'NO DATA'

    # Feedback Status
    data['Feedback_Submitted'] = data['Feedback'].apply(lambda x: 'YES' if x != '-' else 'NO')

    return data

# Custom CSS for responsive UI
st.markdown("""
    <style>
        body {background-color: #f4f4f4;}
        .header {text-align: center; color: #2c3e50; font-size: 36px; font-weight: bold;}
        .summary-box {display: flex; justify-content: space-between; padding: 20px;}
        .box {background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); text-align: center; width: 23%;}
        .present {background-color: #2ecc71; color: white;}
        .partially-present {background-color: #f39c12; color: white;}
        .absent {background-color: #e74c3c; color: white;}
        .no-feedback {background-color: gray; color: white;}
    </style>
""", unsafe_allow_html=True)

st.title("ZOOM LOG ANALYTICS DASHBOARD")

uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)

    if not processed_data.empty:
        total_students = len(processed_data)
        present_count = len(processed_data[processed_data['Attendance_Category'] == 'PRESENT'])
        partially_present_count = len(processed_data[processed_data['Attendance_Category'] == 'PARTIALLY PRESENT'])
        absent_count = len(processed_data[processed_data['Attendance_Category'] == 'ABSENT'])
        no_feedback_count = len(processed_data[processed_data['Feedback_Submitted'] == 'NO'])

        # Summary Boxes
        st.markdown('<div class="summary-box">', unsafe_allow_html=True)
        st.markdown(f'<div class="box total-students"><strong>TOTAL STUDENTS</strong><br>{total_students}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="box present"><strong>PRESENT</strong><br>{present_count}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="box partially-present"><strong>PARTIALLY PRESENT</strong><br>{partially_present_count}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="box absent"><strong>ABSENT</strong><br>{absent_count}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="box no-feedback"><strong>STUDENTS WITHOUT FEEDBACK</strong><br>{no_feedback_count}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Attendance Distribution Pie Chart
        st.markdown("### ATTENDANCE DISTRIBUTION")
        category_counts = processed_data['Attendance_Category'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=['#e74c3c', '#2ecc71', '#f39c12'])
        ax1.axis('equal')
        st.pyplot(fig1)

        # Detailed Attendance Data
        st.markdown("### DETAILED ATTENDANCE DATA")
        st.dataframe(processed_data[['Name', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Login_Count', 'Logout_Count', 'Poll_Participated', 'Feedback_Submitted']], use_container_width=True)

    else:
        st.warning("No data found after processing. Please check the uploaded file.")
else:
    st.info("Please upload a CSV file.")
