import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Custom CSS for dark theme
st.markdown("""
    <style>
        body {
            background-color: #1e1e1e; /* Dark background */
            color: #ffffff; /* White text */
        }
        .header {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: #f39c12; /* Vibrant orange header */
            margin-bottom: 20px;
        }
        .card {
            background-color: #2c3e50; /* Dark gray card background */
            border-radius: 10px;
            padding: 15px;
            margin: 15px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        }
        .chart-title {
            font-size: 18px;
            font-weight: bold;
            color: #e74c3c; /* Red for chart titles */
            text-align: center;
            margin-bottom: 10px;
        }
        .small-stat {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            padding: 10px;
            color: #ffffff; /* White text */
            border-radius: 8px;
        }
        .stat-green {
            background-color: #27ae60; /* Green stat card */
        }
        .stat-blue {
            background-color: #2980b9; /* Blue stat card */
        }
        .stat-yellow {
            background-color: #f1c40f; /* Yellow stat card */
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header">Professional Dark-Themed Dashboard</div>', unsafe_allow_html=True)

# Sample Data
data = pd.DataFrame({
    "Category": ["Completed", "In Progress", "Pending", "Overdue"],
    "Values": [759, 457, 123, 95]
})

# Layout: Multiple Rows
# First row: Two Pie Charts
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Task Status Distribution</div>', unsafe_allow_html=True)
    fig1, ax1 = plt.subplots()
    ax1.pie(data['Values'], labels=data['Category'], autopct='%1.1f%%', startangle=90, colors=["#27ae60", "#3498db", "#f1c40f", "#e74c3c"])
    ax1.axis('equal')  # Equal aspect ratio ensures a circular pie chart
    st.pyplot(fig1)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Task Completion Progress</div>', unsafe_allow_html=True)
    fig2, ax2 = plt.subplots()
    ax2.pie([75, 25], labels=["Completed", "Remaining"], autopct='%1.1f%%', startangle=90, colors=["#27ae60", "#e74c3c"])
    ax2.axis('equal')
    st.pyplot(fig2)
    st.markdown('</div>', unsafe_allow_html=True)

# Second Row: Line Chart
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">Task Progress Over Time</div>', unsafe_allow_html=True)
fig3, ax3 = plt.subplots()
ax3.plot(range(1, 11), [5, 10, 15, 20, 25, 30, 40, 50, 70, 100], marker="o", linestyle="--", color="#f39c12")
ax3.set_title("Progress Over Time", color="#ffffff")
ax3.set_facecolor("#2c3e50")
ax3.spines['bottom'].set_color('#ffffff')
ax3.spines['left'].set_color('#ffffff')
ax3.tick_params(axis='x', colors='#ffffff')
ax3.tick_params(axis='y', colors='#ffffff')
st.pyplot(fig3)
st.markdown('</div>', unsafe_allow_html=True)

# Third Row: Summary Stats
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="chart-title">Summary Statistics</div>', unsafe_allow_html=True)
col3, col4, col5 = st.columns(3)

with col3:
    st.markdown('<div class="small-stat stat-green">Total: 759</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="small-stat stat-blue">Completed: 457</div>', unsafe_allow_html=True)
with col5:
    st.markdown('<div class="small-stat stat-yellow">Pending: 123</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
