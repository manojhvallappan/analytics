import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def process_attendance_data(data):
    # Rename columns
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

    # Convert time columns to datetime
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')

    # Calculate duration in minutes
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Define attendance categories
    data['Attendance_Category'] = 'Absent'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 100), 'Attendance_Category'] = 'Full Present (101+ mins)'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 71) & (data['Duration_Minutes'] <= 100), 'Attendance_Category'] = 'Partially Present (71-100 mins)'

    return data

# Apply custom CSS styling for a more professional layout
st.markdown("""
    <style>
        .attendance-summary {
            display: flex;
            justify-content: space-between;
            background-color: #f0f8ff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }
        .attendance-summary-item {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 8px;
            width: 22%;
            text-align: center;
            font-size: 16px;
            font-weight: bold;
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
        .expander-title {
            font-size: 20px;
            font-weight: bold;
            color: #333;
        }
        .expander-subtitle {
            color: #555;
        }
        .streamlit-table thead th {
            background-color: #f5f5f5;
            color: #333;
            font-weight: bold;
        }
        .streamlit-table tbody tr:hover {
            background-color: #f0f8ff;
        }
        .progress-bar {
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Progress bar
progress_bar = st.progress(0)

# Upload CSV file
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)
    
    # Update progress bar
    progress_bar.progress(50)

    if not processed_data.empty:
        # Calculate total counts
        total_students = len(processed_data)
        full_present_count = len(processed_data[processed_data['Attendance_Category'] == 'Full Present (101+ mins)'])
        partially_present_count = len(processed_data[processed_data['Attendance_Category'] == 'Partially Present (71-100 mins)'])
        absent_count = len(processed_data[processed_data['Attendance_Category'] == 'Absent'])

        # Update progress bar
        progress_bar.progress(100)

        # Attendance summary in colorful boxes
        st.markdown('<div class="attendance-summary">', unsafe_allow_html=True)

        # Columns for summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
                <div class="attendance-summary-item total-students">
                    <h3>Total Students</h3>
                    <p>{total_students}</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="attendance-summary-item full-present">
                    <h3>Full Present (101+ mins)</h3>
                    <p>{full_present_count}</p>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class="attendance-summary-item partially-present">
                    <h3>Partially Present (71-100 mins)</h3>
                    <p>{partially_present_count}</p>
                </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                <div class="attendance-summary-item absent">
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

        # Detailed Data
        st.markdown("### Detailed Attendance Data")

        # Full Present
        with st.expander("Full Present (101+ mins)", expanded=True):
            full_present_data = processed_data[processed_data['Attendance_Category'] == 'Full Present (101+ mins)']
            st.dataframe(full_present_data[['Name', 'Join_Time', 'Leave_Time', 'Feedback']], use_container_width=True)

        # Partially Present
        with st.expander("Partially Present (71-100 mins)"):
            partially_present_data = processed_data[processed_data['Attendance_Category'] == 'Partially Present (71-100 mins)']
            st.dataframe(partially_present_data[['Name', 'Join_Time', 'Leave_Time', 'Feedback']], use_container_width=True)

        # Absent
        with st.expander("Absent"):
            absent_data = processed_data[processed_data['Attendance_Category'] == 'Absent']
            st.dataframe(absent_data[['Name', 'Join_Time', 'Leave_Time', 'Feedback']], use_container_width=True)

    else:
        st.warning("Processed data is empty. Please check the uploaded file.")
else:
    st.info("Please upload a CSV file to view the attendance data.")
