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
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
        }
        .summary-box {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
            margin: 10px;
            text-align: center;
            width: 22%;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .full-present {
            background-color: #32CD32;
            color: white;
        }
        .partially-present {
            background-color: #FFD700;
            color: white;
        }
        .absent {
            background-color: #FF4500;
            color: white;
        }
        .total-students {
            background-color: #4682B4;
            color: white;
        }
        .summary-box h3 {
            margin-bottom: 10px;
            font-size: 20px;
        }
        .summary-box p {
            font-size: 18px;
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
        # Attendance summary section in row-wise layout
        total_students = len(processed_data)
        full_present_count = len(processed_data[processed_data['Attendance_Category'] == 'Full Present (100+ mins)'])
        partially_present_count = len(processed_data[processed_data['Attendance_Category'] == 'Partially Present (70-100 mins)'])
        absent_count = len(processed_data[processed_data['Attendance_Category'] == 'Absent'])

        st.markdown('<div class="attendance-summary">', unsafe_allow_html=True)

        # Total Students
        st.markdown(f"""
            <div class="summary-box total-students">
                <h3>Total Students</h3>
                <p>{total_students}</p>
            </div>
        """, unsafe_allow_html=True)

        # Full Present (100+ mins)
        st.markdown(f"""
            <div class="summary-box full-present">
                <h3>Full Present (100+ mins)</h3>
                <p>{full_present_count}</p>
            </div>
        """, unsafe_allow_html=True)

        # Partially Present (70-100 mins)
        st.markdown(f"""
            <div class="summary-box partially-present">
                <h3>Partially Present (70-100 mins)</h3>
                <p>{partially_present_count}</p>
            </div>
        """, unsafe_allow_html=True)

        # Absent
        st.markdown(f"""
            <div class="summary-box absent">
                <h3>Absent</h3>
                <p>{absent_count}</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Attendance Pie Chart
        st.markdown("### Attendance Distribution")
        category_counts = processed_data['Attendance_Category'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=['#98FB98', '#FFD700', '#FF4500'])
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
