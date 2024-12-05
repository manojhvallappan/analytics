import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

    # Convert Join and Leave Time to datetime
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')

    # Calculate duration in minutes
    data['Duration (minutes)'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60
    data['Attendance_Category'] = 'ABSENT'

    # Categorize attendance
    data.loc[(data['Responded'] == 'OK') & (data['Duration (minutes)'] > 100), 'Attendance_Category'] = 'PRESENT'
    data.loc[(data['Responded'] == 'OK') & (data['Duration (minutes)'].between(70, 100)), 'Attendance_Category'] = 'PARTIALLY PRESENT'

    return data

# Custom CSS for styling
st.markdown("""
    <style>
        body { background-color: #f4f4f4; font-family: 'Arial', sans-serif; }
        .attendance-summary { display: flex; justify-content: space-around; padding: 20px; margin: 20px 0; }
        .summary-item-box { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); width: 23%; text-align: center; font-weight: bold; }
        .full-present { background-color: #2ecc71; color: white; }
        .partially-present { background-color: #f39c12; color: white; }
        .absent { background-color: #e74c3c; color: white; }
        .total-students { background-color: #3498db; color: white; }
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
        students_without_feedback = len(processed_data[processed_data['Feedback'].isna()])

        st.markdown('<div class="attendance-summary">', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="summary-item-box total-students"><strong>Total Students:</strong> {total_students}</div>
            <div class="summary-item-box full-present"><strong>PRESENT:</strong> {full_present_count}</div>
            <div class="summary-item-box partially-present"><strong>PARTIALLY PRESENT:</strong> {partially_present_count}</div>
            <div class="summary-item-box absent"><strong>ABSENT:</strong> {absent_count}</div>
            <div class="summary-item-box" style="background-color: gray; color: white;"><strong>Students Without Feedback:</strong> {students_without_feedback}</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Attendance distribution pie chart
        st.markdown("### ATTENDANCE DISTRIBUTION")
        category_counts = processed_data['Attendance_Category'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=['#e74c3c', '#2ecc71', '#f39c12'])
        ax1.axis('equal')
        st.pyplot(fig1)

        # Detailed data with expandable sections
        for category, label in [("PRESENT", "PRESENT"), ("PARTIALLY PRESENT", "PARTIALLY PRESENT"), ("ABSENT", "ABSENT"), ("-", "STUDENTS WITHOUT FEEDBACK")]:
            with st.expander(label):
                filtered_data = processed_data[processed_data['Attendance_Category'] == category] if category != "-" else processed_data[processed_data['Feedback'].isna()]
                if not filtered_data.empty:
                    st.dataframe(filtered_data[['Name', 'Join_Time', 'Leave_Time', 'Duration (minutes)', 'Login_Count', 'Logout_Count', 'Feedback']])
                else:
                    st.write("No data available.")
    else:
        st.warning("Processed data is empty. Please check your CSV file.")
else:
    st.info("Please upload a CSV file.")
