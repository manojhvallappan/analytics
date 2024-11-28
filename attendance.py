import streamlit as st
import pandas as pd

def parse_time_taken(time_str):
    """Convert time taken into minutes."""
    try:
        time_str = time_str.lower()  # Normalize case (e.g., "min" vs "MIN")
        minutes = 0
        if "min" in time_str:
            minutes += int(time_str.split("min")[0].strip())
        if "sec" in time_str:
            seconds = int(time_str.split("sec")[0].strip().split()[-1])
            minutes += seconds / 60
        return minutes
    except Exception as e:
        print(f"Error parsing time: {e}")
        return 0

def classify_attendance(row):
    """Classify attendance based on criteria."""
    time_minutes = parse_time_taken(row['Time taken'])
    response_length = len(row['Response 2']) if isinstance(row['Response 2'], str) else 0

    # Debugging output
    print(f"Time: {time_minutes}, Response Length: {response_length}")

    if time_minutes > 20 and response_length >= 4:
        return "Present"
    elif 15 <= time_minutes <= 20 and response_length >= 4:
        return "Potentially Present"
    elif time_minutes < 15 or response_length < 4:
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

    # Debugging: Check column names
    st.write("Column names", data.columns)

    # Classify attendance
    data['Attendance Status'] = data.apply(classify_attendance, axis=1)

    # Display summary
    summary = data['Attendance Status'].value_counts()
    st.write("Attendance Summary", summary)

    # Display detailed data
    st.write("Detailed Attendance Data")
    st.dataframe(data[['First name', 'Time taken', 'Response 2', 'Attendance Status']])

