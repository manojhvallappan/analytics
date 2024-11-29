import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sample data
data = {
    "Name": [
        "Shelia Smith", "Violeta Smith", "Michelle Orlando", "Melissa Lamont", "Kristin Hagan", 
        "Fermina Kozakiewicz", "Elsa Olmstead", "Vanessa Gibson", "Christi Williams", 
        "Mitsuko Racki", "Ann Martinez", "Carolina Jenkins", "Susan Muraski", "Kristin Keith", 
        "Catherine Buhr", "Kathrine Judd", "Molly Cunha", "Judith Pace", "June Whitford", 
        "Laura Cameron", "Angela Graham", "Hilda Callahan", "Michelle Dix", "Lorelei Rivera", 
        "Paula Fielding", "Anita Butler", "Deborah Mohr", "Melva Samuel", "Dorothy Myers"
    ],
    "Duration (mins)": [
        2, 23, 1, 29, 2, 17, 130, 130, 130, 130, 126, 127, 129, 130, 4, 130, 129, 127, 130, 
        127, 64, 129, 126, 14, 97, 1, 130, 126, 130
    ],
    "Disclaimer Response": [
        "No Response", "No Response", "No Response", "No Response", "No Response", 
        "OK", "OK", "OK", "OK", "No Response", "OK", "OK", "OK", "OK", 
        "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", "OK", 
        "OK", "OK", "OK", "OK", "OK"
    ],
    "Feedback": [
        "-", "-", "-", "-", "-", "good", "The session was amazing and the next activity seems so necessary to me at this point.",
        "Great session, waiting for the activity next week.", "Loved today's corporate session", "-",
        "Today the corporate skills session is too good, the presentations on SWOT analysis went well!! And , I found many similarities in the presentations like the strengths part especially.",
        "Our cohort wasn't active which led to 0 session engagement.", 
        "Amazing work by all the teams, fun analysis ;>", 
        "Our cohorts zero session engagement and activeness was disappointing. We will talk and try to see what we can do improve ourselves.", 
        "good", "interactive session", "the session was lovely", 
        "Wonderful session on SWOT. Also excited for next week's activity.", 
        "Enjoyed the session", "The session was very helpful.", 
        "The session was very informative as different groups presented SWOT analysis for various companies",
        "Apologies for staying silent initially! Our cohort has done this multiple times earlier and apologized too, and still, we repeat this behavior. This is unacceptable but we will make amends.", 
        "Would love to hear feedback from Kunisha", "Session was good.", 
        "presented swot analysis ppt", "-", "It was helpful", "Great session", 
        "Liked the SWOT Analysis part!"
    ]
}

# Convert data to DataFrame
df = pd.DataFrame(data)

# Clean column names
df.columns = df.columns.str.strip()

# Convert 'Duration (mins)' to numeric and handle missing values
df['Duration (mins)'] = pd.to_numeric(df['Duration (mins)'], errors='coerce')

# Fill missing values in 'Feedback' to avoid length issues
df['Feedback'] = df['Feedback'].fillna("")

# Categorize attendance
def categorize_attendance(row):
    feedback_length = len(row['Feedback']) > 5
    if row['Duration (mins)'] > 100 and row['Disclaimer Response'] == "OK" and feedback_length:
        return "Present"
    elif 50 <= row['Duration (mins)'] <= 100 and row['Disclaimer Response'] == "OK" and feedback_length:
        return "Potentially Present"
    elif row['Duration (mins)'] <= 50 and row['Disclaimer Response'] == "No Response":
        return "Absent"
    else:
        return "Uncategorized"

# Apply categorization
df['Attendance Status'] = df.apply(categorize_attendance, axis=1)

# Streamlit app
st.title("Attendance Dashboard")

# Summary of attendance
st.header("Summary")
status_counts = df['Attendance Status'].value_counts()
st.write(status_counts)

# Bar Chart
st.header("Attendance Status Chart")
fig, ax = plt.subplots()
status_counts.plot(kind='bar', ax=ax, color=['green', 'orange', 'red', 'gray'])
ax.set_title("Attendance Distribution")
ax.set_xlabel("Status")
ax.set_ylabel("Number of Students")
st.pyplot(fig)

# Display detailed data
st.header("Detailed Data")
st.write(df)
