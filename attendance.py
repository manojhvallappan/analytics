import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample function for processing data
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

# Custom CSS for UI enhancement
st.markdown("""
    <style>
        body { background-color: #f5f7fa; }
        .main-title { text-align: center; font-size: 40px; color: #3c5a99; margin-bottom: 20px; }
        .metrics-card { padding: 15px; margin: 10px; text-align: center; font-size: 20px; color: white; border-radius: 10px; }
        .card-blue { background-color: #007bff; }
        .card-green { background-color: #28a745; }
        .card-yellow { background-color: #ffc107; }
        .card-red { background-color: #dc3545; }
    </style>
""", unsafe_allow_html=True)

# Dashboard Title
st.markdown('<div class="main-title">Attendance Dashboard</div>', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)
    category_counts = processed_data['Attendance_Category'].value_counts()

    # Metrics Summary Section
    st.markdown("""
        <div style="display: flex; justify-content: space-around;">
            <div class="metrics-card card-blue">Full Present<br>{}</div>
            <div class="metrics-card card-green">Potentially Present<br>{}</div>
            <div class="metrics-card card-yellow">Short Attendance<br>{}</div>
            <div class="metrics-card card-red">No Response<br>{}</div>
        </div>
    """.format(
        category_counts.get('Full Present', 0),
        category_counts.get('Potentially Present', 0),
        category_counts.get('Short Attendance', 0),
        category_counts.get('No Response', 0)
    ), unsafe_allow_html=True)

    # Pie Chart for Attendance Distribution
    st.markdown('<h3>Attendance Distribution</h3>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # DataTable Section
    st.markdown('<h3>Detailed Attendance Data</h3>', unsafe_allow_html=True)
    st.dataframe(processed_data)

else:
    st.warning("Please upload a CSV file.")
