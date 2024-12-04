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

    data['Attendance_Category'] = 'ABSENT'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 100), 'Attendance_Category'] = 'PRESENT'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 70) & (data['Duration_Minutes'] <= 100), 'Attendance_Category'] = 'PARTIALLY PRESENT'

    return data

# Custom CSS for dashboard design
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f8f9fa;
        }
        .main-container {
            display: flex;
            flex-direction: column;
            padding: 20px;
        }
        .title {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
        }
        .summary-row {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
        }
        .summary-box {
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            text-align: center;
            width: 18%;
        }
        .summary-value {
            font-size: 24px;
            font-weight: bold;
            margin-top: 10px;
        }
        .chart-container, .detailed-data {
            margin-top: 20px;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Main Title
st.markdown('<div class="title">ZOOM LOG ANALYTICS DASHBOARD</div>', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)

    if not processed_data.empty:
        # Summary Section
        st.markdown('<div class="summary-row">', unsafe_allow_html=True)
        
        total_students = len(processed_data)
        full_present_count = len(processed_data[processed_data['Attendance_Category'] == 'PRESENT'])
        partially_present_count = len(processed_data[processed_data['Attendance_Category'] == 'PARTIALLY PRESENT'])
        absent_count = len(processed_data[processed_data['Attendance_Category'] == 'ABSENT'])
        students_without_feedback = len(processed_data[processed_data['Feedback'] == '-'])

        st.markdown(f"""
            <div class="summary-box">
                <div>TOTAL STUDENTS</div>
                <div class="summary-value">{total_students}</div>
            </div>
            <div class="summary-box" style="background-color: #2ecc71; color: white;">
                <div>PRESENT</div>
                <div class="summary-value">{full_present_count}</div>
            </div>
            <div class="summary-box" style="background-color: #f39c12; color: white;">
                <div>PARTIALLY PRESENT</div>
                <div class="summary-value">{partially_present_count}</div>
            </div>
            <div class="summary-box" style="background-color: #e74c3c; color: white;">
                <div>ABSENT</div>
                <div class="summary-value">{absent_count}</div>
            </div>
            <div class="summary-box" style="background-color: gray; color: white;">
                <div>STUDENTS WITHOUT FEEDBACK</div>
                <div class="summary-value">{students_without_feedback}</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Attendance Pie Chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("<h3>Attendance Distribution</h3>", unsafe_allow_html=True)
        category_counts = processed_data['Attendance_Category'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=['#e74c3c', '#2ecc71', '#f39c12'])
        ax1.axis('equal')
        st.pyplot(fig1)
        st.markdown('</div>', unsafe_allow_html=True)

        # Detailed Data Section
        st.markdown('<div class="detailed-data">', unsafe_allow_html=True)
        st.markdown("<h3>Detailed Attendance Data</h3>", unsafe_allow_html=True)

        with st.expander("PRESENT"):
            st.dataframe(processed_data[processed_data['Attendance_Category'] == 'PRESENT'][['Name', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Feedback']])
        with st.expander("PARTIALLY PRESENT"):
            st.dataframe(processed_data[processed_data['Attendance_Category'] == 'PARTIALLY PRESENT'][['Name', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Feedback']])
        with st.expander("ABSENT"):
            st.dataframe(processed_data[processed_data['Attendance_Category'] == 'ABSENT'][['Name', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Feedback']])
        with st.expander("STUDENTS WITHOUT FEEDBACK"):
            st.dataframe(processed_data[processed_data['Feedback'] == '-'][['Name', 'Join_Time', 'Leave_Time', 'Duration_Minutes']])

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Processed data is empty. Please check the uploaded file.")
else:
    st.info("Please upload a CSV file to view the attendance data.")
