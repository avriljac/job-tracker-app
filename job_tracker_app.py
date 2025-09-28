import pandas as pd
from datetime import datetime
import os
import streamlit as st

# ---------- CONFIG ----------
FILE = "applications.csv"

COLUMNS = [
    "Date",
    "Company",
    "Role",
    "Application Method",
    "Contact",
    "Status",
    "Follow-up Date",
    "Notes"
]

# Initialize CSV if it doesn't exist
if not os.path.exists(FILE):
    df = pd.DataFrame(columns=COLUMNS)
    df.to_csv(FILE, index=False)

# ---------- FUNCTIONS ----------
def add_application():
    st.subheader("Add a New Application")
    with st.form("application_form"):
        date_applied = st.date_input("Application Date", value=datetime.today())
        company = st.text_input("Company Name")
        role = st.text_input("Role")
        method = st.text_input("Application Method")
        contact = st.text_input("Contact Person (optional)")
        status = st.selectbox("Status", ["Applied", "Interview", "Tech Assessment", "Case Study", "Offer", "Rejected"])
        follow_up = st.date_input("Follow-up Date", value=None)
        notes = st.text_area("Notes (optional)")
        submitted = st.form_submit_button("Add Application")
        
        if submitted:
            df = pd.read_csv(FILE)
            new_row = {
                "Date": date_applied,
                "Company": company,
                "Role": role,
                "Application Method": method,
                "Contact": contact,
                "Status": status,
                "Follow-up Date": follow_up if follow_up else "",
                "Notes": notes
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(FILE, index=False)
            st.success(f"Application added: {company} - {role}")

def view_applications():
    st.subheader("All Applications")
    df = pd.read_csv(FILE)
    
    if df.empty:
        st.info("No applications found. Start by adding a new application.")
        return

    # Filters
    company_filter = st.text_input("Filter by Company")
    status_filter = st.selectbox("Filter by Status", ["All", "Applied", "Interview", "Offer", "Rejected"])
    
    filtered_df = df.copy()
    if company_filter:
        filtered_df = filtered_df[filtered_df["Company"].str.contains(company_filter, case=False)]
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]
    
    # Color-code statuses
    def color_status(val):
        if val == "Applied":
            return 'background-color: lightblue'
        elif val == "Interview":
            return 'background-color: yellow'
        elif val == "Offer":
            return 'background-color: lightgreen'
        elif val == "Rejected":
            return 'background-color: lightcoral'
        return ''
    
    st.dataframe(filtered_df.style.applymap(color_status, subset=['Status']))

    # Delete button for each row
    for idx in filtered_df.index:
        if st.button(f"Delete Application {idx+1}", key=f"del{idx}"):
            df = df.drop(idx)
            df.to_csv(FILE, index=False)
            st.warning(f"Application {idx + 1} deleted!")
            st.experimental_rerun()

def follow_ups_pending():
    st.subheader("Follow-ups Pending")
    df = pd.read_csv(FILE)
    if df.empty:
        st.info("No applications found. Add some applications to track follow-ups.")
        return
    
    df['Follow-up Date'] = pd.to_datetime(df['Follow-up Date'], errors='coerce')
    today = pd.to_datetime(datetime.today().date())
    pending = df[df['Follow-up Date'] <= today]
    
    if pending.empty:
        st.info("No follow-ups pending today.")
        return

    # Highlight pending follow-ups
    def highlight_follow_up(val):
        if pd.to_datetime(val, errors='coerce') <= today:
            return 'background-color: orange'
        return ''
    
    st.dataframe(pending.style.applymap(highlight_follow_up, subset=['Follow-up Date']))

def application_stats():
    st.subheader("Application Stats")
    df = pd.read_csv(FILE)
    if df.empty:
        st.info("No applications found. Add applications to see statistics.")
        return
    
    status_counts = df['Status'].value_counts()
    total = len(df)
    for status, count in status_counts.items():
        percent = (count / total) * 100
        st.write(f"{status}: {count} ({percent:.1f}%)")
    st.write(f"Total Applications: {total}")

# ---------- STREAMLIT MENU ----------
st.title("Job Application Tracker")

menu = ["Home", "Add Application", "View Applications", "Follow-ups Pending", "View Stats"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.write("👋 Welcome to your Job Application Tracker!")
    st.write(
        "Use the sidebar to add new applications, view all applications, "
        "check pending follow-ups, or view your application stats."
    )
elif choice == "Add Application":
    add_application()
elif choice == "View Applications":
    view_applications()
elif choice == "Follow-ups Pending":
    follow_ups_pending()
elif choice == "View Stats":
    application_stats()
