import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

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

def process_data(df):
    # Convert 'Join time' and 'Leave time' to datetime format
    df['Join time'] = pd.to_datetime(df['Join time'], errors='coerce')
    df['Leave time'] = pd.to_datetime(df['Leave time'], errors='coerce')
    
    # Calculate the duration in minutes
    df['Duration_Minutes'] = (df['Leave time'] - df['Join time']).dt.total_seconds() / 60

    # Categorize based on duration
    df['Category'] = pd.cut(
        df['Duration_Minutes'], 
        bins=[0, 10, 50, 100, 150, float('inf')], 
        labels=['1–10 mins', '11–50 mins', '51–100 mins', '101–150 mins', 'More than 150 mins'], 
        right=False
    )

    # Convert 'Category' to string type to handle NaN properly
    df['Category'] = df['Category'].astype(str)
    
    # Fill NaN values in the 'Category' column
    df['Category'] = df['Category'].fillna('No Response')
    
    return df

if uploaded_file:
    # Read data
    data = pd.read_csv(uploaded_file)

    # Process data
    data = process_data(data)

    # Layout the dashboard
    st.markdown("<div class='section'><h4>Overall Attendance Metrics</h4></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Students", len(data))
    with col2:
        st.metric("Average Attendance (mins)", data['Duration_Minutes'].mean().round(2))
    with col3:
        st.metric("No Response", data['Category'].isna().sum())

    # Bar Chart of Attendance Categories
    st.markdown("<div class='section'><h4>Attendance Breakdown</h4></div>", unsafe_allow_html=True)
    attendance_counts = data['Category'].value_counts().sort_index()
    fig1 = px.bar(attendance_counts, x=attendance_counts.index, y=attendance_counts.values, color=attendance_counts.index,
                  labels={'x': 'Category', 'y': 'Count'}, title="Attendance Categories")
    st.plotly_chart(fig1)

    # Pie Chart for Attendance Distribution
    st.markdown("<div class='section'><h4>Attendance Distribution</h4></div>", unsafe_allow_html=True)
    fig2 = px.pie(values=attendance_counts.values, names=attendance_counts.index, title="Category Distribution",
                  color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig2)

    # Scatter Plot for Duration vs Join Time
    st.markdown("<div class='section'><h4>Duration vs Join Time</h4></div>", unsafe_allow_html=True)
    if 'Join time' in data.columns and not data['Join time'].isna().all():
        fig3 = px.scatter(data, x='Join time', y='Duration_Minutes', color='Category', title="Join Time vs Duration")
        st.plotly_chart(fig3)
    else:
        st.warning("Join Time data is missing or invalid.")

    # Table for Detailed Data
    st.markdown("<div class='section'><h4>Detailed Attendance Data</h4></div>", unsafe_allow_html=True)
    st.dataframe(data[['Name (original name)', 'Email', 'Join time', 'Leave time', 'Duration_Minutes', 'Category']])

else:
    st.warning("Please upload a CSV file to see the dashboard.")

