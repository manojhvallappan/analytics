import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Dashboard Title
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 20px;
        }
        .section {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            margin: 10px;
            background-color: #f9f9f9;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
    <div class="main-title">Dynamic Attendance Dashboard</div>
""", unsafe_allow_html=True)

# Sample CSV upload
uploaded_file = st.file_uploader("Upload Attendance Data (CSV)", type=["csv"])

if uploaded_file:
    # Read data
    data = pd.read_csv(uploaded_file)

    # Processing data
    def process_data(df):
        # Convert time columns to datetime
        df['Join_Time'] = pd.to_datetime(df['Join time'], errors='coerce')
        df['Leave_Time'] = pd.to_datetime(df['Leave time'], errors='coerce')
        
        # Calculate duration in minutes
        df['Duration_Minutes'] = (df['Leave_Time'] - df['Join_Time']).dt.total_seconds() / 60

        # Define attendance categories
        df['Attendance_Category'] = 'Absent'
        df.loc[(df['Duration_Minutes'] >= 100) & (df['Recording disclaimer response'] == 'OK'), 'Attendance_Category'] = 'Full Attendance'
        df.loc[(df['Duration_Minutes'] >= 70) & (df['Duration_Minutes'] < 100) & (df['Recording disclaimer response'] == 'OK'), 'Attendance_Category'] = 'Partial Attendance'
        
        return df

    data = process_data(data)

    # Layout the dashboard
    st.markdown("<div class='section'><h4>Overall Attendance Metrics</h4></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Students", len(data))
    with col2:
        st.metric("Average Attendance (mins)", data['Duration_Minutes'].mean().round(2))
    with col3:
        st.metric("No Response", data['Attendance_Category'].isna().sum())

    # Attendance Categories Breakdown
    st.markdown("<div class='section'><h4>Attendance Breakdown</h4></div>", unsafe_allow_html=True)
    attendance_counts = data['Attendance_Category'].value_counts().sort_index()
    fig1 = px.bar(attendance_counts, x=attendance_counts.index, y=attendance_counts.values, color=attendance_counts.index,
                  labels={'x': 'Category', 'y': 'Count'}, title="Attendance Categories")
    st.plotly_chart(fig1)

    # Pie Chart for Attendance Distribution
    st.markdown("<div class='section'><h4>Attendance Distribution</h4></div>", unsafe_allow_html=True)
    fig2 = px.pie(values=attendance_counts.values, names=attendance_counts.index, title="Category Distribution",
                  color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig2)

    # Table for Detailed Data
    st.markdown("<div class='section'><h4>Detailed Attendance Data</h4></div>", unsafe_allow_html=True)
    st.dataframe(data[['Name (original name)', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 'Attendance_Category']])

else:
    st.warning("Please upload a CSV file to see the dashboard.")
