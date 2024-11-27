import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to process and categorize attendance data
def process_attendance_data(data):
    data.rename(columns={
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
        'Recording disclaimer response': 'Responded',
    }, inplace=True)

    # Convert time columns to datetime
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')

    # Calculate duration in minutes
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Categorize attendance into the specified ranges
    data['Attendance_Category'] = 'No Response'
    data.loc[(data['Duration_Minutes'] > 101) & (data['Duration_Minutes'] <= 150), 'Attendance_Category'] = '101-150 mins'
    data.loc[(data['Duration_Minutes'] >= 51) & (data['Duration_Minutes'] <= 100), 'Attendance_Category'] = '51-100 mins'
    data.loc[(data['Duration_Minutes'] >= 11) & (data['Duration_Minutes'] <= 50), 'Attendance_Category'] = '11-50 mins'
    data.loc[(data['Duration_Minutes'] >= 1) & (data['Duration_Minutes'] < 11), 'Attendance_Category'] = '1-10 mins'

    # Identify no response category if Responded is not 'OK'
    data.loc[data['Responded'] != 'OK', 'Attendance_Category'] = 'No Response'

    return data

# Custom CSS styling
st.markdown("""
    <style>
        .header { text-align: center; font-size: 36px; color: #ff69b4; }
        .section-title { font-size: 24px; color: #32CD32; }
        .stat-box { padding: 10px; margin: 5px; border-radius: 5px; }
        .blue { background-color: #ADD8E6; }
        .green { background-color: #98FB98; }
        .orange { background-color: #FFDAB9; }
        .red { background-color: #FFC0CB; }
        .gray { background-color: #D3D3D3; }
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
            <div class="stat-box blue">101-150 mins<br>{category_counts.get('101-150 mins', 0)}</div>
            <div class="stat-box green">51-100 mins<br>{category_counts.get('51-100 mins', 0)}</div>
            <div class="stat-box orange">11-50 mins<br>{category_counts.get('11-50 mins', 0)}</div>
            <div class="stat-box red">1-10 mins<br>{category_counts.get('1-10 mins', 0)}</div>
            <div class="stat-box gray">No Response<br>{category_counts.get('No Response', 0)}</div>
        </div>
    """, unsafe_allow_html=True)

    # Attendance distribution pie chart
    st.markdown('<div class="section-title">ATTENDANCE DISTRIBUTION</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = ['#ADD8E6', '#98FB98', '#FFDAB9', '#FFC0CB', '#D3D3D3']
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

    for category in ['101-150 mins', '51-100 mins', '11-50 mins', '1-10 mins', 'No Response']:
        with st.expander(f"View {category}"):
            filtered_data = processed_data[processed_data['Attendance_Category'] == category]
            st.dataframe(filtered_data[['Name (original name)', 'Email', 'Duration_Minutes', 'Responded']])

else:
    st.warning("Please upload a CSV file to proceed.")
