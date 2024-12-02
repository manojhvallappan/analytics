import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to process the attendance data
def process_attendance_data(data):
    # Try renaming columns to standardized names
    column_mapping = {
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
        'Recording disclaimer response': 'Responded',
    }
    
    # Rename columns if they exist
    data.rename(columns={k: column_mapping.get(k, k) for k in data.columns}, inplace=True)

    # Ensure columns exist before processing
    if 'Join_Time' not in data.columns or 'Leave_Time' not in data.columns or 'Responded' not in data.columns:
        st.error("Missing required columns in the uploaded file.")
        return None

    # Convert the 'Join_Time' and 'Leave_Time' columns to datetime
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')

    # Calculate the duration in minutes
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Categorize the attendance based on response and duration
    data['Attendance_Category'] = 'No Response'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 100), 'Attendance_Category'] = 'Full Present (Above 100 mins)'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 70) & (data['Duration_Minutes'] <= 100), 'Attendance_Category'] = 'Potentially Present (70-100 mins)'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] < 70), 'Attendance_Category'] = 'Short Attendance (Below 70 mins)'

    return data

# Streamlit page styling and header
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

st.markdown('<div class="header">ZOOM ONLINE ATTENDANCE ANALYTICS</div>', unsafe_allow_html=True)

# File uploader to upload the CSV file
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    # Read the uploaded CSV file into a pandas DataFrame
    data = pd.read_csv(uploaded_file)

    # Process the attendance data
    processed_data = process_attendance_data(data)
    
    if processed_data is not None:
        # Calculate the attendance category counts
        category_counts = processed_data['Attendance_Category'].value_counts()

        # Display the attendance overview section
        st.markdown('<div class="section-title">ATTENDANCE OVERVIEW</div>', unsafe_allow_html=True)
        st.markdown(f"""
            <div style="display: flex; justify-content: space-evenly;">
                <div class="stat-box green">Full Present (Above 100 mins)<br>{category_counts.get('Full Present (Above 100 mins)', 0)}</div>
                <div class="stat-box yellow">Potentially Present (70-100 mins)<br>{category_counts.get('Potentially Present (70-100 mins)', 0)}</div>
                <div class="stat-box orange">Short Attendance (Below 70 mins)<br>{category_counts.get('Short Attendance (Below 70 mins)', 0)}</div>
                <div class="stat-box red">No Response<br>{category_counts.get('No Response', 0)}</div>
            </div>
        """, unsafe_allow_html=True)

        # Display the attendance distribution pie chart
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

        # Display the detailed attendance data
        st.markdown('<div class="section-title">DETAILED ATTENDANCE DATA</div>', unsafe_allow_html=True)

        for category in ['Full Present (Above 100 mins)', 'Potentially Present (70-100 mins)', 'Short Attendance (Below 70 mins)', 'No Response']:
            with st.expander(f"View {category}"):
                filtered_data = processed_data[processed_data['Attendance_Category'] == category]
                
                # Check if the filtered data is empty and show a message if so
                if filtered_data.empty:
                    st.write(f"No data available for {category}.")
                else:
                    st.dataframe(filtered_data[['Name (original name)', 'Email', 'Duration_Minutes', 'Responded']])

else:
    # If no file is uploaded, show a warning
    st.warning("Please upload a CSV file to proceed.")
