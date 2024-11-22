import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate duration and filter based on the criteria
def process_attendance_data(data):
    # Rename columns for consistency
    data.rename(columns={
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
        'Recording disclaimer response': 'Responded',
    }, inplace=True)
    
    # Convert 'Join_Time' and 'Leave_Time' to datetime
    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')
    
    # Calculate Duration in minutes
    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    # Filter students who have responded with "OK" to the disclaimer and attended for more than 110 minutes
    qualified_data = data[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 110)]

    # Filter students who have responded with "OK" to the disclaimer and attended for 80+ minutes but <= 110 minutes
    potentially_present_data = data[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 80) & (data['Duration_Minutes'] <= 110)]
    
    # Filter students who have not responded or attended for less than 80 minutes
    absent_data = data[~data.index.isin(qualified_data.index) & ~data.index.isin(potentially_present_data.index)]
    
    # Add a column to categorize students as Qualified, Potentially Present, or Absent
    data['Attendance_Status'] = 'Absent'
    data.loc[qualified_data.index, 'Attendance_Status'] = 'Qualified'
    data.loc[potentially_present_data.index, 'Attendance_Status'] = 'Potentially Present'
    
    return data, qualified_data, potentially_present_data, absent_data

# Add a custom header
st.markdown("""
    <style>
        .header {
            text-align: center;
            font-size: 30px;
            color: #4CAF50;
            font-weight: bold;
            padding: 20px;
            background-color: #f4f4f4;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Display title and custom header
st.markdown('<div class="header">Attendance Dashboard</div>', unsafe_allow_html=True)

# If a file is uploaded
uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    # Read the CSV file into a DataFrame
    data = pd.read_csv(uploaded_file)
    
    # Process attendance data
    processed_data, qualified_data, potentially_present_data, absent_data = process_attendance_data(data)

    # Display the filtered data with students who have responded and attended for more than 110 minutes
    st.subheader("Attendance Report")

    # Display pie chart for qualified, potentially present, and absent students
    if len(processed_data) > 0:
        # Pie chart data
        status_counts = processed_data['Attendance_Status'].value_counts()

        fig, ax = plt.subplots(figsize=(6, 6))
        colors = {'Qualified': '#4CAF50', 'Potentially Present': '#2196F3', 'Absent': '#F44336'}
        ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90, colors=[colors[key] for key in status_counts.index])
        ax.axis('equal')  # Equal aspect ratio ensures the pie is circular.
        st.write("### Student Attendance Status")
        st.pyplot(fig)

        # Display number of students in each category
        st.write(f"### Number of Students in Each Category:")
        st.markdown(f"**Qualified Students**: {len(qualified_data)} (Attended > 110 minutes and Responded OK)")
        st.markdown(f"**Potentially Present Students**: {len(potentially_present_data)} (Attended between 80-110 minutes and Responded OK)")
        st.markdown(f"**Absent Students**: {len(absent_data)} (Did not respond or attended < 80 minutes)")

        # Add some spacing for clarity
        st.markdown("<hr>", unsafe_allow_html=True)

        # Show details of Qualified students
        st.write("### Qualified Students (Attended > 110 minutes and Responded OK)")
        st.dataframe(qualified_data)

        # Add some spacing
        st.markdown("<hr>", unsafe_allow_html=True)

        # Show details of Potentially Present students
        st.write("### Potentially Present Students (Attended between 80-110 minutes and Responded OK)")
        st.dataframe(potentially_present_data)

        # Add some spacing
        st.markdown("<hr>", unsafe_allow_html=True)

        # Show details of Absent students
        st.write("### Absent Students (Did not respond or attended < 80 minutes)")
        st.dataframe(absent_data)

    else:
        st.warning("No students qualify for attendance based on the given criteria.")
else:
    st.warning("Please upload a CSV file to proceed.")


