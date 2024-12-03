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

    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')

    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    data['Attendance_Category'] = 'Absent'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 100), 'Attendance_Category'] = 'Full Present (100+ mins)'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 70) & (data['Duration_Minutes'] <= 100), 'Attendance_Category'] = 'Partially Present (70-100 mins)'

    return data

# Apply custom CSS styling
st.markdown("""
    <style>
        .attendance-summary {
            display: flex;
            justify-content: space-evenly;
            align-items: center;
            gap: 20px;
            padding: 20px 0;
        }
        .summary-item-box {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 23%;
            text-align: center;
            font-weight: bold;
        }
        .full-present {
            background-color: #98FB98;
            color: #006400;
        }
        .partially-present {
            background-color: #FFD700;
            color: #8B8000;
        }
        .absent {
            background-color: #FF6347;
            color: #8B0000;
        }
        .total-students {
            background-color: #87CEFA;
            color: #00008B;
        }
        .attendance-summary h2 {
            width: 100%;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Enhanced Attendance Dashboard with Feedback")

uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)

    if not processed_data.empty:
        # Attendance Summary Header
        st.markdown('<div class="attendance-summary">', unsafe_allow_html=True)

        # Calculate the total number of students
        total_students = len(processed_data)

        # Calculate the number of students for each category
        full_present_count = len(processed_data[processed_data['Attendance_Category'] == 'Full Present (100+ mins)'])
        partially_present_count = len(processed_data[processed_data['Attendance_Category'] == 'Partially Present (70-100 mins)'])
        absent_count = len(processed_data[processed_data['Attendance_Category'] == 'Absent'])

        # Display attendance summary in individual styled boxes horizontally
        st.markdown(f"""
            <div class="summary-item-box total-students">
                <strong>Total Students:</strong> {total_students}
            </div>
            <div class="summary-item-box full-present">
                <strong>Full Present (100+ mins):</strong> {full_present_count}
            </div>
            <div class="summary-item-box partially-present">
                <strong>Partially Present (70-100 mins):</strong> {partially_present_count}
            </div>
            <div class="summary-item-box absent">
                <strong>Absent:</strong> {absent_count}
            </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Attendance Pie Chart
        st.markdown("### Attendance Distribution")
        category_counts = processed_data['Attendance_Category'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=['#98FB98', '#FFD700', '#FF6347'])
        ax1.axis('equal')
        st.pyplot(fig1)

        # Display filtered data for each category
        st.markdown("### Detailed Attendance Data")
        
        # Full Present
        with st.expander("Full Present (100+ mins)"):
            full_present_data = processed_data[processed_data['Attendance_Category'] == 'Full Present (100+ mins)']
            st.dataframe(full_present_data[['Name', 'Join_Time', 'Leave_Time', 'Feedback']])

        # Partially Present
        with st.expander("Partially Present (70-100 mins)"):
            partially_present_data = processed_data[processed_data['Attendance_Category'] == 'Partially Present (70-100 mins)']
            st.dataframe(partially_present_data[['Name', 'Join_Time', 'Leave_Time', 'Feedback']])

        # Absent
        with st.expander("Absent"):
            absent_data = processed_data[processed_data['Attendance_Category'] == 'Absent']
            st.dataframe(absent_data[['Name', 'Join_Time', 'Leave_Time', 'Feedback']])
    else:
        st.warning("Processed data is empty. Please check the uploaded file.")
else:
    st.info("Please upload a CSV file to view the attendance data.")
