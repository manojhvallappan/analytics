import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def process_attendance_data(data):
    # Rename columns to standardize them
    data.rename(columns={
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
        'Recording disclaimer response': 'Responded',
    }, inplace=True)

    # Debug: Display initial column names
    st.write("Columns after renaming:", data.columns)

    # Convert 'Join_Time' and 'Leave_Time' to datetime
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')

    # Debug: Check if any 'NaT' values were generated during datetime conversion
    st.write("Missing values after conversion:", data[['Join_Time', 'Leave_Time']].isna().sum())

    # Calculate Duration in minutes
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Set initial attendance category
    data['Attendance_Category'] = 'No Response'

    # Categorize based on duration and response
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 100), 'Attendance_Category'] = 'Full Present (Above 100 mins)'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 70) & (data['Duration_Minutes'] <= 100), 'Attendance_Category'] = 'Potentially Present (70-100 mins)'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] < 70), 'Attendance_Category'] = 'Short Attendance (Below 70 mins)'

    return data

# Styling the Streamlit app
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

# File uploader for the attendance CSV
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    # Read the uploaded CSV file
    data = pd.read_csv(uploaded_file)

    # Debug: Show the first few rows of the data to ensure it's loaded properly
    st.write("Initial Data", data.head())

    # Process the attendance data
    processed_data = process_attendance_data(data)

    # Debug: Show the processed data after attendance categorization
    st.write("Processed Data", processed_data.head())

    # Count the number of records in each attendance category
    category_counts = processed_data['Attendance_Category'].value_counts()

    # Display the attendance overview
    st.markdown('<div class="section-title">ATTENDANCE OVERVIEW</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div style="display: flex; justify-content: space-evenly;">
            <div class="stat-box green">Full Present (Above 100 mins)<br>{category_counts.get('Full Present (Above 100 mins)', 0)}</div>
            <div class="stat-box yellow">Potentially Present (70-100 mins)<br>{category_counts.get('Potentially Present (70-100 mins)', 0)}</div>
            <div class="stat-box orange">Short Attendance (Below 70 mins)<br>{category_counts.get('Short Attendance (Below 70 mins)', 0)}</div>
            <div class="stat-box red">No Response<br>{category_counts.get('No Response', 0)}</div>
        </div>
    """, unsafe_allow_html=True)

    # Display the attendance distribution as a pie chart
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

    # Display detailed attendance data
    st.markdown('<div class="section-title">DETAILED ATTENDANCE DATA</div>', unsafe_allow_html=True)

    for category in ['Full Present (Above 100 mins)', 'Potentially Present (70-100 mins)', 'Short Attendance (Below 70 mins)', 'No Response']:
        with st.expander(f"View {category}"):
            filtered_data = processed_data[processed_data['Attendance_Category'] == category]
            
            # Debug: Print the number of records in each category
            st.write(f"Filtered {category}: {filtered_data.shape[0]} records")

            # Check if the filtered data is empty and show message if so
            if filtered_data.empty:
                st.write(f"No data available for {category}.")
            else:
                st.dataframe(filtered_data[['Name (original name)', 'Email', 'Duration_Minutes', 'Responded']])

else:
    st.warning("Please upload a CSV file to proceed.")
