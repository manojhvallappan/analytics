import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def process_attendance_data(data):
    data.rename(columns={
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
        'Recording disclaimer response': 'Responded',
    }, inplace=True)
    
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')
    
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Apply new attendance categorization
    data['Attendance_Category'] = 'Absent'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 101), 'Attendance_Category'] = 'Full Present'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 71) & (data['Duration_Minutes'] <= 101), 'Attendance_Category'] = 'Potentially Present'

    return data

# Custom CSS styles
st.markdown("""
    <style>
        body {
            background-color: #f9f9f9;
        }
        .header {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #ff69b4; /* Pinkish for header */
            margin-bottom: 20px;
        }
        .section-title {
            font-size: 20px;
            font-weight: bold;
            color: #32CD32; /* Light green for section titles */
        }
        .stat-box {
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            font-size: 16px;
            color: white;
        }
        .pink { background-color: #FFB6C1; } /* Light pink */
        .lavender { background-color: #E6E6FA; } /* Light lavender */
        .yellow { background-color: #FFD700; } /* Yellow */
    </style>
""", unsafe_allow_html=True)

# Display dashboard header
st.markdown('<div class="header">PROFESSIONAL ATTENDANCE DASHBOARD</div>', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)
    category_counts = processed_data['Attendance_Category'].value_counts()

    # Overview section
    st.markdown('<div class="section-title">ATTENDANCE OVERVIEW</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div style="display: flex; justify-content: space-evenly;">
            <div class="stat-box lavender">Full Present<br>{category_counts.get('Full Present', 0)}</div>
            <div class="stat-box yellow">Potentially Present<br>{category_counts.get('Potentially Present', 0)}</div>
            <div class="stat-box pink">Absent<br>{category_counts.get('Absent', 0)}</div>
        </div>
    """, unsafe_allow_html=True)

    # Attendance distribution pie chart
    st.markdown('<div class="section-title">ATTENDANCE DISTRIBUTION</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(6, 6))
    colors = {
        'Full Present': '#E6E6FA',
        'Potentially Present': '#FFD700',
        'Absent': '#FFB6C1'
    }
    ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=[colors[key] for key in category_counts.index])
    ax.axis('equal')
    st.pyplot(fig)

    # Detailed attendance data with expanders
    st.markdown('<div class="section-title">DETAILED ATTENDANCE DATA</div>', unsafe_allow_html=True)
    with st.expander("View Full Present (Above 101 mins)"):
        st.dataframe(processed_data[processed_data['Attendance_Category'] == 'Full Present'][['Name (original name)', 'Email', 'Duration_Minutes', 'Responded']])
    with st.expander("View Potentially Present (71–101 mins)"):
        st.dataframe(processed_data[processed_data['Attendance_Category'] == 'Potentially Present'][['Name (original name)', 'Email', 'Duration_Minutes', 'Responded']])
    with st.expander("View Absent (Below 70 mins or No Response)"):
        st.dataframe(processed_data[processed_data['Attendance_Category'] == 'Absent'][['Name (original name)', 'Email', 'Duration_Minutes', 'Responded']])

else:
    st.warning("Please upload a CSV file to proceed.")
