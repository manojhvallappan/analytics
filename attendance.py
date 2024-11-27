import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def process_attendance_data(data):
    data.rename(columns={
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
        'Recording disclaimer response': 'Responded',
    }, inplace=True)

    # Convert Join_Time and Leave_Time to datetime
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')

    # Calculate duration in minutes
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Categorize attendance based on duration and response
    data['Attendance_Category'] = 'No Response'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 100), 'Attendance_Category'] = 'Full Present (Above 100 mins)'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 70) & (data['Duration_Minutes'] <= 100), 'Attendance_Category'] = 'Potentially Present (70-100 mins)'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] < 70), 'Attendance_Category'] = 'Short Attendance (Below 70 mins)'

    return data

# Streamlit UI setup
st.markdown("""
    <style>
        .header { text-align: center; font-size: 36px; color: #ff69b4; }
        .section-title { font-size: 24px; color: #32CD32; }
        .stat-box { padding: 10px; margin: 5px; border-radius: 5px; }
        .green { background-color: #98FB98; }
        .yellow { background-color: #FFD700; }
        .orange { background-color: #FFA07A; }
        .red { background-color: #FFC0CB; }
    </style>
""", unsafe_allow_html=True)

# Dashboard header
st.markdown('<div class="header">STUDENT ATTENDANCE DASHBOARD</div>', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)
    category_counts = processed_data['Attendance_Category'].value_counts()

    # Attendance overview in separate columns
    st.markdown('<div class="section-title">ATTENDANCE OVERVIEW</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div style="display: flex; justify-content: space-evenly;">
            <div class="stat-box green">Full Present (Above 100 mins)<br>{category_counts.get('Full Present (Above 100 mins)', 0)}</div>
            <div class="stat-box yellow">Potentially Present (70-100 mins)<br>{category_counts.get('Potentially Present (70-100 mins)', 0)}</div>
            <div class="stat-box orange">Short Attendance (Below 70 mins)<br>{category_counts.get('Short Attendance (Below 70 mins)', 0)}</div>
            <div class="stat-box red">No Response<br>{category_counts.get('No Response', 0)}</div>
        </div>
    """, unsafe_allow_html=True)

    # Attendance distribution pie chart
    st.markdown('<div class="section-title">ATTENDANCE DISTRIBUTION</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = ['#98FB98', '#FFD700', '#FFA07A', '#FFC0CB']
    ax.pie(
        category_counts, 
        labels=category_counts.index, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=colors
    )
    ax.axis('equal')
    st.pyplot(fig)

    # Expandable detailed sections for each category
    st.markdown('<div class="section-title">DETAILED ATTENDANCE DATA</div>', unsafe_allow_html=True)

    for category in ['Full Present (Above 100 mins)', 'Potentially Present (70-100 mins)', 'Short Attendance (Below 70 mins)', 'No Response']:
        with st.expander(f"View {category}"):
            filtered_data = processed_data[processed_data['Attendance_Category'] == category]
            st.dataframe(filtered_data[['Name (original name)', 'Email', 'Duration_Minutes', 'Responded']])

else:
    st.warning("Please upload a CSV file to proceed.")
