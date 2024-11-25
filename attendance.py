import streamlit as st
import pandas as pd
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
        .stat-box {
            text-align: center;
            padding: 15px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            margin: 10px;
            color: white;
        }
        .green {
            background-color: #4CAF50;
        }
        .blue {
            background-color: #2196F3;
        }
        .yellow {
            background-color: #FFC107;
        }
        .orange {
            background-color: #FF9800;
        }
        .red {
            background-color: #F44336;
        }
    </style>
    <div class="main-title">Dynamic Attendance Dashboard</div>
""", unsafe_allow_html=True)

# Sample CSV upload
uploaded_file = st.file_uploader("Upload Attendance Data (CSV)", type=["csv"])

if uploaded_file:
    # Read data
    data = pd.read_csv(uploaded_file)

    # Preprocessing function to calculate attendance duration and categorize
    def process_data(df):
        # Correct column names based on the CSV structure
        df['Join time'] = pd.to_datetime(df['Join time'], errors='coerce')
        df['Leave time'] = pd.to_datetime(df['Leave time'], errors='coerce')
        df['Duration_Minutes'] = (df['Leave time'] - df['Join time']).dt.total_seconds() / 60

        # Categorize attendance based on duration
        df['Category'] = pd.cut(
            df['Duration_Minutes'], 
            bins=[0, 10, 50, 100, 150, float('inf')], 
            labels=['1–10 mins', '11–50 mins', '51–100 mins', '101–150 mins', 'More than 150 mins'], 
            right=False
        )
        # Handle no response
        df['Category'] = df['Category'].fillna('No Response')
        return df

    # Process data
    data = process_data(data)

    # Attendance category counts
    attendance_counts = data['Category'].value_counts().sort_index()

    # Layout the dashboard with professional appearance
    st.markdown("<div class='section'><h4>Overall Attendance Metrics</h4></div>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(f"<div class='stat-box green'>101–150 mins<br>{attendance_counts.get('101–150 mins', 0)}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stat-box blue'>51–100 mins<br>{attendance_counts.get('51–100 mins', 0)}</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='stat-box yellow'>11–50 mins<br>{attendance_counts.get('11–50 mins', 0)}</div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='stat-box orange'>1–10 mins<br>{attendance_counts.get('1–10 mins', 0)}</div>", unsafe_allow_html=True)
    with col5:
        st.markdown(f"<div class='stat-box red'>No Response<br>{attendance_counts.get('No Response', 0)}</div>", unsafe_allow_html=True)

    # Bar Chart of Attendance Categories
    st.markdown("<div class='section'><h4>Attendance Breakdown</h4></div>", unsafe_allow_html=True)
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
        st.warning("Join time data is missing or invalid.")

    # Table for Detailed Data
    st.markdown("<div class='section'><h4>Detailed Attendance Data</h4></div>", unsafe_allow_html=True)
    st.dataframe(data[['Name (original name)', 'Email', 'Join time', 'Leave time', 'Duration_Minutes', 'Category']])

else:
    st.warning("Please upload a CSV file to see the dashboard.")
