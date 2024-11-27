import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to process attendance data and categorize
def process_attendance_data(data):
    data['Join_Time'] = pd.to_datetime(data['Join time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave time'], errors='coerce')
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Initialize all columns to 'No'
    data['Full Present'] = 'No'
    data['Potentially Present'] = 'No'
    data['Short Attendance'] = 'No'
    data['No Response'] = 'No'

    # Categorize based on conditions
    data.loc[(data['Recording disclaimer response'] == 'OK') & (data['Duration_Minutes'] > 100), 'Full Present'] = 'Yes'
    data.loc[(data['Recording disclaimer response'] == 'OK') & (data['Duration_Minutes'] >= 70) & (data['Duration_Minutes'] <= 100), 'Potentially Present'] = 'Yes'
    data.loc[(data['Recording disclaimer response'] == 'OK') & (data['Duration_Minutes'] < 70), 'Short Attendance'] = 'Yes'
    data.loc[data['Recording disclaimer response'].isna(), 'No Response'] = 'Yes'

    return data

# Custom CSS for styling
st.markdown("""
    <style>
        .main-title { text-align: center; font-size: 40px; color: #3c5a99; margin-bottom: 20px; }
        .metrics-card { padding: 15px; margin: 10px; text-align: center; font-size: 20px; color: white; border-radius: 10px; }
        .card-blue { background-color: #007bff; }
        .card-green { background-color: #28a745; }
        .card-yellow { background-color: #ffc107; }
        .card-red { background-color: #dc3545; }
    </style>
""", unsafe_allow_html=True)

# Dashboard title
st.markdown('<div class="main-title">Attendance Dashboard</div>', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)

    # Summary of attendance counts
    full_present_count = processed_data['Full Present'].value_counts().get('Yes', 0)
    potentially_present_count = processed_data['Potentially Present'].value_counts().get('Yes', 0)
    short_attendance_count = processed_data['Short Attendance'].value_counts().get('Yes', 0)
    no_response_count = processed_data['No Response'].value_counts().get('Yes', 0)

    # Display summary metrics in cards
    st.markdown(f"""
        <div style="display: flex; justify-content: space-around;">
            <div class="metrics-card card-blue">Full Present<br>{full_present_count}</div>
            <div class="metrics-card card-green">Potentially Present<br>{potentially_present_count}</div>
            <div class="metrics-card card-yellow">Short Attendance<br>{short_attendance_count}</div>
            <div class="metrics-card card-red">No Response<br>{no_response_count}</div>
        </div>
    """, unsafe_allow_html=True)

    # Attendance data table showing categorized columns
    st.markdown('<h3>Detailed Attendance Data</h3>', unsafe_allow_html=True)
    st.dataframe(processed_data[['Name (original name)', 'Email', 'Duration_Minutes', 'Full Present', 'Potentially Present', 'Short Attendance', 'No Response']])

    # Pie chart for attendance distribution
    st.markdown('<h3>Attendance Distribution</h3>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 6))
    labels = ['Full Present', 'Potentially Present', 'Short Attendance', 'No Response']
    counts = [full_present_count, potentially_present_count, short_attendance_count, no_response_count]
    ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

else:
    st.warning("Please upload a CSV file to proceed.")
