import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to process attendance data
def process_attendance_data(data):
    # Check if required columns exist
    required_columns = ['Join time', 'Leave time', 'Recording disclaimer response']
    missing_columns = [col for col in required_columns if col not in data.columns]

    if missing_columns:
        st.error(f"Missing columns in uploaded file: {', '.join(missing_columns)}")
        return None

    # Rename columns
    data.rename(columns={
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
        'Recording disclaimer response': 'Responded',
    }, inplace=True)

    # Convert times to datetime
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')

    # Calculate duration in minutes
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Categorize attendance based on conditions
    data['Attendance_Category'] = 'No Response'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 100), 'Attendance_Category'] = 'Full Present (Above 100 mins)'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 70) & (data['Duration_Minutes'] <= 100), 'Attendance_Category'] = 'Potentially Present (70-100 mins)'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] < 70), 'Attendance_Category'] = 'Short Attendance (Below 70 mins)'

    return data

# Custom styles for dashboard
st.markdown("""
    <style>
        .header { text-align: center; font-size: 36px; color: #ff69b4; }
        .section-title { font-size: 24px; color: #32CD32; }
        .stat-box { padding: 10px; margin: 5px; border-radius: 5px; }
        .green { background-color: #98FB98; }
        .yellow { background-color: #FFD700; }
        .purple { background-color: #D8BFD8; }
        .red { background-color: #FFC0CB; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header">ZOOM ONLINE ATTENDANCE ANALYTICS</div>', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    
    # Display column names for debugging
    st.write("Uploaded CSV Columns:", data.columns.tolist())

    processed_data = process_attendance_data(data)

    if processed_data is not None:
        category_counts = processed_data['Attendance_Category'].value_counts()

        # Overview section
        st.markdown('<div class="section-title">ATTENDANCE OVERVIEW</div>', unsafe_allow_html=True)
        st.markdown(f"""
            <div style="display: flex; justify-content: space-evenly;">
                <div class="stat-box green">Full Present (Above 100 mins)<br>{category_counts.get('Full Present (Above 100 mins)', 0)}</div>
                <div class="stat-box purple">Potentially Present (70-100 mins)<br>{category_counts.get('Potentially Present (70-100 mins)', 0)}</div>
                <div class="stat-box yellow">Short Attendance (Below 70 mins)<br>{category_counts.get('Short Attendance (Below 70 mins)', 0)}</div>
                <div class="stat-box red">No Response<br>{category_counts.get('No Response', 0)}</div>
            </div>
        """, unsafe_allow_html=True)

        # Attendance distribution pie chart
        st.markdown('<div class="section-title">ATTENDANCE DISTRIBUTION</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 8))
        colors = ['#98FB98', '#D8BFD8', '#FFD700', '#FFC0CB']
        ax.pie(
            category_counts, 
            labels=category_counts.index, 
            autopct='%1.1f%%', 
            startangle=90, 
            colors=colors
        )
        ax.axis('equal')
        st.pyplot(fig)

        # Feedback section
        st.markdown('<div class="section-title">STUDENT FEEDBACK</div>', unsafe_allow_html=True)
        st.text_area("Provide feedback for the session:")

        # Detailed attendance data
        st.markdown('<div class="section-title">DETAILED ATTENDANCE DATA</div>', unsafe_allow_html=True)
        for category in ['Full Present (Above 100 mins)', 'Potentially Present (70-100 mins)', 'Short Attendance (Below 70 mins)', 'No Response']:
            with st.expander(f"View {category}"):
                filtered_data = processed_data[processed_data['Attendance_Category'] == category]
                if filtered_data.empty:
                    st.write(f"No data available for {category}.")
                else:
                    st.dataframe(filtered_data[['Name (original name)', 'Email', 'Duration_Minutes', 'Responded']])
else:
    st.warning("Please upload a CSV file to proceed.")
