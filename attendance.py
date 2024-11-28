import streamlit as st
import pandas as pd

def parse_time_taken(time_str):
    """Convert time taken into minutes."""
    try:
        parts = time_str.split()
        minutes = 0
        if "min" in parts:
            minutes += int(parts[0])
        if "sec" in parts[-1]:
            seconds = int(parts[-2])
            minutes += seconds / 60
        return minutes
    except:
        return 0

def classify_attendance(row):
    """Classify attendance based on criteria."""
    time_minutes = parse_time_taken(row['Time taken'])
    response_length = len(row['Response 2']) if isinstance(row['Response 2'], str) else 0

    if time_minutes > 20 and response_length > 10:
        return "Present"
    elif 15 <= time_minutes <= 20 and response_length > 10:
        return "Potentially Present"
    elif time_minutes < 15 or response_length < 5:
        return "Absent"
    else:
        return "Absent"

# Streamlit UI
st.title("Attendance Dashboard")
st.write("Upload the attendance CSV file to calculate attendance.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    # Load data
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded Data", data.head())

    # Classify attendance
    data['Attendance Status'] = data.apply(classify_attendance, axis=1)

    # Display summary
    summary = data['Attendance Status'].value_counts()
    st.write("Attendance Summary", summary)

    # Display detailed data
    st.write("Detailed Attendance Data")
    st.dataframe(data[['First name', 'Time taken', 'Response 2', 'Attendance Status']])
