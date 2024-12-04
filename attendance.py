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
    data['Duration (minutes)'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    data['Attendance_Category'] = 'ABSENT'
    data.loc[(data['Responded'] == 'OK') & (data['Duration (minutes)'] > 100), 'Attendance_Category'] = 'PRESENT'
    data.loc[(data['Responded'] == 'OK') & (data['Duration (minutes)'].between(70, 100)), 'Attendance_Category'] = 'PARTIALLY PRESENT'

    return data

# Custom CSS for the layout and style
st.markdown("""
    <style>
        body { font-family: 'Arial', sans-serif; background-color: #f8f9fa; }
        .main-container { display: grid; grid-template-columns: 1fr 3fr; gap: 20px; margin-top: 20px; }
        .left-panel, .right-panel { padding: 20px; background: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .left-panel { background-color: #3498db; color: white; }
        .summary-box { display: flex; justify-content: space-between; padding: 15px; margin-bottom: 10px; background-color: #fff; color: #333; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .summary-title { font-size: 20px; font-weight: bold; color: #34495e; }
        .summary-value { font-size: 22px; color: #2ecc71; }
        .chart-container, .table-container { margin-top: 20px; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        h3 { color: #3498db; }
    </style>
""", unsafe_allow_html=True)

st.title("ZOOM LOG ANALYTICS DASHBOARD")

uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)

    if not processed_data.empty:
        total_students = len(processed_data)
        full_present_count = len(processed_data[processed_data['Attendance_Category'] == 'PRESENT'])
        partially_present_count = len(processed_data[processed_data['Attendance_Category'] == 'PARTIALLY PRESENT'])
        absent_count = len(processed_data[processed_data['Attendance_Category'] == 'ABSENT'])
        students_without_feedback = len(processed_data[processed_data['Feedback'] == '-'])

        # Dashboard Layout
        st.markdown('<div class="main-container">', unsafe_allow_html=True)

        # Left Panel (Summary)
        st.markdown('<div class="left-panel">', unsafe_allow_html=True)
        st.markdown("<h3>Summary Statistics</h3>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="summary-box"><div>Total Students</div><div class="summary-value">{total_students}</div></div>
            <div class="summary-box"><div>PRESENT</div><div class="summary-value">{full_present_count}</div></div>
            <div class="summary-box"><div>PARTIALLY PRESENT</div><div class="summary-value">{partially_present_count}</div></div>
            <div class="summary-box"><div>ABSENT</div><div class="summary-value">{absent_count}</div></div>
            <div class="summary-box" style="background-color: gray; color: white;"><div>Without Feedback</div><div class="summary-value">{students_without_feedback}</div></div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Right Panel (Charts & Tables)
        st.markdown('<div class="right-panel">', unsafe_allow_html=True)

        # Attendance Pie Chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("### Attendance Distribution", unsafe_allow_html=True)
        category_counts = processed_data['Attendance_Category'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=['#e74c3c', '#2ecc71', '#f39c12'])
        ax.axis('equal')
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

        # Detailed Attendance Table
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.markdown("### Detailed Attendance Data", unsafe_allow_html=True)
        st.dataframe(processed_data[['Name', 'Join_Time', 'Leave_Time', 'Duration (minutes)', 'Feedback']], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.warning("Processed data is empty. Please check the uploaded file.")
else:
    st.info("Please upload a CSV file to view the attendance data.")
