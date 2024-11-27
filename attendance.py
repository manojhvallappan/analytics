import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def process_attendance_data(data):
    # Data Processing and Categorization
    data['Join_Time'] = pd.to_datetime(data['Join time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave time'], errors='coerce')
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Categorize Attendance
    data['Attendance_Category'] = 'No Response'
    data.loc[(data['Recording disclaimer response'] == 'OK') & (data['Duration_Minutes'] > 100), 'Attendance_Category'] = 'Full Present'
    data.loc[(data['Recording disclaimer response'] == 'OK') & (data['Duration_Minutes'] >= 70) & (data['Duration_Minutes'] <= 100), 'Attendance_Category'] = 'Potentially Present'
    data.loc[(data['Recording disclaimer response'] == 'OK') & (data['Duration_Minutes'] < 70), 'Attendance_Category'] = 'Short Attendance'
    return data

# CSS for styling
st.markdown("""
    <style>
        .main-title { text-align: center; font-size: 36px; color: #007BFF; margin-bottom: 30px; }
        .tab-content { font-size: 18px; padding: 15px; }
        .section-title { font-size: 24px; color: #28a745; margin-top: 20px; }
        .highlight { background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# Dashboard Title
st.markdown('<div class="main-title">Professional Attendance Dashboard</div>', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    # Data Processing
    data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)

    # Attendance Data by Category
    full_present_data = processed_data[processed_data['Attendance_Category'] == 'Full Present']
    potentially_present_data = processed_data[processed_data['Attendance_Category'] == 'Potentially Present']
    short_attendance_data = processed_data[processed_data['Attendance_Category'] == 'Short Attendance']
    no_response_data = processed_data[processed_data['Attendance_Category'] == 'No Response']

    # Tabs for separate category tables
    tab1, tab2, tab3, tab4 = st.tabs(["Full Present", "Potentially Present", "Short Attendance", "No Response"])

    with tab1:
        st.markdown('<div class="section-title">Full Present (Above 100 mins)</div>', unsafe_allow_html=True)
        st.dataframe(full_present_data[['Name (original name)', 'Email', 'Duration_Minutes', 'Responded']])

    with tab2:
        st.markdown('<div class="section-title">Potentially Present (70–100 mins)</div>', unsafe_allow_html=True)
        st.dataframe(potentially_present_data[['Name (original name)', 'Email', 'Duration_Minutes', 'Responded']])

    with tab3:
        st.markdown('<div class="section-title">Short Attendance (Below 70 mins)</div>', unsafe_allow_html=True)
        st.dataframe(short_attendance_data[['Name (original name)', 'Email', 'Duration_Minutes', 'Responded']])

    with tab4:
        st.markdown('<div class="section-title">No Response</div>', unsafe_allow_html=True)
        st.dataframe(no_response_data[['Name (original name)', 'Email', 'Duration_Minutes', 'Responded']])

    # Summary Distribution Chart
    st.markdown('<div class="section-title">Attendance Distribution</div>', unsafe_allow_html=True)
    category_counts = processed_data['Attendance_Category'].value_counts()
    
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = ['#007BFF', '#28a745', '#FFC107', '#DC3545']
    ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')
    st.pyplot(fig)

else:
    st.warning("Please upload a CSV file to view the dashboard.")
