import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def process_attendance_data(data):
    st.write("Columns in the dataset:", data.columns.tolist())  # Debugging: Print all column names

    # Rename columns for consistency, ensure these match exactly with CSV headers
    data.rename(columns={
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
        'Recording disclaimer response': 'Responded',
        'Response 2': 'Feedback'  # Ensure exact match with the actual column name
    }, inplace=True)

    # Ensure 'Feedback' column exists
    if 'Feedback' not in data.columns:
        st.error("Column 'Response 2' not found. Please check the CSV format.")
        return data

    # Convert Join and Leave times to datetime
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')

    # Calculate attendance duration
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Count the number of words in the 'Feedback' column
    data['Word_Count'] = data['Feedback'].apply(lambda x: len(str(x).split()))

    # Categorize attendance
    data['Attendance_Category'] = 'No Response'
    data.loc[
        (data['Responded'] == 'OK') &
        (data['Duration_Minutes'] > 100) &
        (data['Word_Count'] > 20),
        'Attendance_Category'
    ] = 'Full Present (Above 100 mins with Feedback)'

    data.loc[
        (data['Responded'] == 'OK') &
        (data['Duration_Minutes'] > 100) &
        (data['Word_Count'] <= 20),
        'Attendance_Category'
    ] = 'Full Present (Above 100 mins, Feedback < 20 words)'

    return data

# Streamlit UI layout
st.title("Zoom Attendance Analytics")

uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    try:
        # Try different encodings if UTF-8 fails
        data = pd.read_csv(uploaded_file, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            data = pd.read_csv(uploaded_file, encoding='latin1')
        except UnicodeDecodeError:
            st.error("Unable to decode the file. Please ensure it is UTF-8 or Latin1 encoded.")
            st.stop()  # Stop further execution if decoding fails

    # Display a preview of the data
    st.write("File loaded successfully!")
    st.dataframe(data.head())

    # Process the attendance data
    processed_data = process_attendance_data(data)

    if not processed_data.empty:
        # Display processed data
        st.write("Processed Data Preview:")
        st.dataframe(processed_data.head())  # Display a preview

        # Display detailed attendance data for each category
        st.markdown('<div class="section-title">DETAILED ATTENDANCE DATA</div>', unsafe_allow_html=True)
        for category in ['Full Present (Above 100 mins with Feedback)', 'Full Present (Above 100 mins, Feedback < 20 words)']:
            with st.expander(f"View {category}"):
                filtered_data = processed_data[processed_data['Attendance_Category'] == category]
                st.dataframe(filtered_data[['Name (original name)', 'Email', 'Duration_Minutes', 'Responded', 'Feedback']])

else:
    st.warning("Please upload a CSV file to proceed.")
