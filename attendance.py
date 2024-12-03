import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def process_attendance_data(data):
    data.rename(columns={
        'Join time': 'Join_Time',
        'Leave time': 'Leave_Time',
        'Name (original name)': 'Name',
        'Recording disclaimer response': 'Responded',
        'Feedback': 'Feedback',
        'Times of Login': 'Login_Count',
        'Times of Logout': 'Logout_Count',
        'Rating': 'Rating'
    }, inplace=True)

    data['Join_Time'] = pd.to_datetime(data['Join_Time'], errors='coerce')
    data['Leave_Time'] = pd.to_datetime(data['Leave_Time'], errors='coerce')

    data['Duration_Minutes'] = (data['Leave_Time'] - data['Join_Time']).dt.total_seconds() / 60

    data['Attendance_Category'] = 'Absent'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] > 100), 'Attendance_Category'] = 'Full Present (100+ mins)'
    data.loc[(data['Responded'] == 'OK') & (data['Duration_Minutes'] >= 70) & (data['Duration_Minutes'] <= 100), 'Attendance_Category'] = 'Partially Present (70-100 mins)'
    data.loc[(data['Responded'] != 'OK') | (data['Duration_Minutes'].isna()), 'Attendance_Category'] = 'No Response'

    return data

st.title("Enhanced Attendance Dashboard with Feedback, Logins, and Rating")

uploaded_file = st.file_uploader("Upload Attendance CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    processed_data = process_attendance_data(data)

    if not processed_data.empty:
        st.subheader("Attendance Summary")

        # Attendance Pie Chart
        st.markdown("### Attendance Distribution")
        category_counts = processed_data['Attendance_Category'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90, colors=['#98FB98', '#FFD700', '#FF4500'])
        ax1.axis('equal')
        st.pyplot(fig1)

        # Detailed Category View
        for category in ['Full Present (100+ mins)', 'Partially Present (70-100 mins)', 'No Response']:
            st.markdown(f"### {category} (Total: {category_counts.get(category, 0)})")
            filtered_data = processed_data[processed_data['Attendance_Category'] == category]
            if filtered_data.empty:
                st.write(f"No students found in the {category} category.")
            else:
                st.dataframe(filtered_data[['Name', 'Email', 'Join_Time', 'Leave_Time', 'Duration_Minutes', 
                                           'Login_Count', 'Logout_Count', 'Rating', 'Feedback']])

        # Bar Graph: Logins vs. Rating
        st.markdown("### Login Counts and Ratings Bar Chart")
        fig2, ax2 = plt.subplots()
        processed_data_grouped = processed_data.groupby('Name').agg({'Login_Count': 'sum', 'Rating': 'mean'}).reset_index()
        ax2.bar(processed_data_grouped['Name'], processed_data_grouped['Login_Count'], color='skyblue', label='Logins')
        ax2.set_xlabel('Name')
        ax2.set_ylabel('Number of Logins', color='blue')

        ax3 = ax2.twinx()
        ax3.plot(processed_data_grouped['Name'], processed_data_grouped['Rating'], color='orange', marker='o', label='Rating')
        ax3.set_ylabel('Rating', color='orange')

        fig2.tight_layout()
        st.pyplot(fig2)

    else:
        st.warning("Processed data is empty. Please check the uploaded file.")
else:
    st.info("Please upload a CSV file to view the attendance data.")
