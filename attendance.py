import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Custom CSS for a dashboard-like interface
st.markdown("""
    <style>
        body {
            background-color: #f4f4f4;
            font-family: 'Arial', sans-serif;
        }
        .container {
            width: 90%;
            margin: auto;
        }
        .header {
            text-align: center;
            color: #2c3e50;
            font-size: 36px;
            font-weight: bold;
            padding: 20px;
        }
        .summary-section {
            display: flex;
            justify-content: space-around;
            padding: 20px;
        }
        .summary-box {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 20%;
            text-align: center;
        }
        .summary-value {
            font-size: 36px;
            font-weight: bold;
        }
        .chart-section {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
        }
        .chart-box {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 45%;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown('<div class="header">ZOOM LOG ANALYTICS DASHBOARD</div>', unsafe_allow_html=True)

# Example data (replace with your actual data)
total_students = 381
full_present_count = 86
partially_present_count = 11
absent_count = 284
students_without_feedback = 188

# Attendance Summary Section
st.markdown('<div class="summary-section">', unsafe_allow_html=True)
st.markdown(f"""
    <div class="summary-box">
        <div><strong>TOTAL STUDENTS</strong></div>
        <div class="summary-value">{total_students}</div>
    </div>
    <div class="summary-box" style="background-color: #2ecc71; color: white;">
        <div><strong>PRESENT</strong></div>
        <div class="summary-value">{full_present_count}</div>
    </div>
    <div class="summary-box" style="background-color: #f39c12; color: white;">
        <div><strong>PARTIALLY PRESENT</strong></div>
        <div class="summary-value">{partially_present_count}</div>
    </div>
    <div class="summary-box" style="background-color: #e74c3c; color: white;">
        <div><strong>ABSENT</strong></div>
        <div class="summary-value">{absent_count}</div>
    </div>
    <div class="summary-box" style="background-color: gray; color: white;">
        <div><strong>STUDENTS WITHOUT FEEDBACK</strong></div>
        <div class="summary-value">{students_without_feedback}</div>
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Example Data for Pie Chart
data = {
    'Category': ['PRESENT', 'PARTIALLY PRESENT', 'ABSENT'],
    'Count': [full_present_count, partially_present_count, absent_count]
}
df = pd.DataFrame(data)

# Pie Chart Section
st.markdown('<div class="chart-section">', unsafe_allow_html=True)
st.markdown('<div class="chart-box">', unsafe_allow_html=True)
st.markdown('<h3>Attendance Distribution</h3>', unsafe_allow_html=True)

fig, ax = plt.subplots()
ax.pie(df['Count'], labels=df['Category'], autopct='%1.1f%%', colors=['#2ecc71', '#f39c12', '#e74c3c'], startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.
st.pyplot(fig)

st.markdown('</div>', unsafe_allow_html=True)

# Bar Chart Section
st.markdown('<div class="chart-box">', unsafe_allow_html=True)
st.markdown('<h3>Feedback Summary</h3>', unsafe_allow_html=True)

bar_data = {
    'Feedback Status': ['Provided', 'Not Provided'],
    'Count': [total_students - students_without_feedback, students_without_feedback]
}
bar_df = pd.DataFrame(bar_data)

fig, ax = plt.subplots()
ax.bar(bar_df['Feedback Status'], bar_df['Count'], color=['#3498db', 'gray'])
ax.set_ylabel('Number of Students')
ax.set_title('Feedback Status')
st.pyplot(fig)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
