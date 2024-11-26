import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Add custom CSS for professional styling
st.markdown("""
    <style>
        body {
            background-color: #f0f4f7; /* Light blue background */
        }
        .header {
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            color: #34495e;
            margin-bottom: 30px;
        }
        .sidebar-title {
            font-size: 22px;
            font-weight: bold;
            color: #ffffff;
            text-align: center;
            padding: 15px 0;
            background-color: #2ecc71; /* Green sidebar title background */
            border-radius: 10px;
        }
        .card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .small-card {
            text-align: center;
            padding: 15px;
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)
st.sidebar.button("Overview")
st.sidebar.button("Reports")
st.sidebar.button("Settings")
st.sidebar.button("Help")

# Header
st.markdown('<div class="header">Professional Dashboard</div>', unsafe_allow_html=True)

# Example data for visualization
data = pd.DataFrame({
    "Category": ["A", "B", "C", "D"],
    "Values": [30, 20, 25, 25]
})

# Layout: 3 columns (Example)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Pie Chart")
    fig, ax = plt.subplots()
    ax.pie(data['Values'], labels=data['Category'], autopct="%1.1f%%", startangle=90)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Line Chart")
    fig, ax = plt.subplots()
    ax.plot(data['Category'], data['Values'], marker="o", linestyle="--", color="#1f77b4")
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Bar Chart")
    fig, ax = plt.subplots()
    ax.bar(data['Category'], data['Values'], color="#2ecc71")
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# Summary Statistics Section
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Summary Statistics")
st.markdown(f"""
    <div style="display: flex; justify-content: space-evenly;">
        <div class="small-card" style="background-color: #f1c40f;">Total: {sum(data['Values'])}</div>
        <div class="small-card" style="background-color: #3498db;">Max: {max(data['Values'])}</div>
        <div class="small-card" style="background-color: #e74c3c;">Min: {min(data['Values'])}</div>
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
