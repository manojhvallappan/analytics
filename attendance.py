import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to process attendance data
def process_attendance_data(data):
    data['Join_Time'] = pd.to_datetime(data['Join time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave time'], errors='coerce')
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Categorizing attendance
    data['Attendance_Category'] = 'No Response'
    data.loc[(data['Recording disclaimer response'] == 'OK') & (data['Duration_Minutes'] > 100), 'Attendance_Category'] = 'Full Present'
    data.loc[(data['Recording disclaimer response'] == 'OK') & (data['Duration_Minutes'] >= 70) & (data['Duration_Minutes'] <= 100), 'Attendance_Category'] = 'Potentially Present'
    data.loc[(data['Recording disclaimer response'] == 'OK') & (data['Duration_Minutes'] < 70), 'Attendance_Category'] = 'Short Attendance'
    return data

# Custom CSS for clean UI
st.markdown("""
    <style>
        body { background-color: #f5f5f5; }
        .header { text-align: center; font-size: 36px; color: #4CAF50; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# Dashboard Header
st.markdown('<div class="header">Attendance Dashboard</div>', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)

    # Tabs for different attendance categories
    tab1, tab2, tab3, tab4 = st.tabs(["Full Present", "Potentially Present", "Short Attendance", "No Response"])

    with tab1:
        st.markdown("### Full Present (More than 100 mins)")
        full_present = processed_data[processed_data['Attendance_Category'] == 'Full Present']
        st.dataframe(full_present[['Name (original name)', 'Email', 'Duration_Minutes', 'Responded']])

    with tab2:
        st.markdown("### Potentially Present (70 - 100 mins)")
        potentially_present = processed_data[processed_data['Attendance_Category'] == 'Potentially Present']
        st.dataframe(potentially_present[['Name (original name)', 'Email', 'Duration_Minutes', 'Responded']])

    with tab3:
        st.markdown("### Short Attendance (Below 70 mins)")
        short_attendance = processed_data[processed_data['Attendance_Category'] == 'Short Attendance']
        st.dataframe(short_attendance[['Name (original name)', 'Email', 'Duration_Minutes', 'Responded']])

    with tab4:
        st.markdown("### No Response (No Disclaimer Acknowledgement)")
        no_response = processed_data[processed_data['Attendance_Category'] == 'No Response']
        st.dataframe(no_response[['Name (original name)', 'Email', 'Duration_Minutes', 'Responded']])

else:
    st.warning("Please upload a CSV file.")
