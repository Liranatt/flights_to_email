# In app.py

import streamlit as st
import main  # Import your refactored main.py
import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Flight Deal Finder",
    page_icon="✈️",
    layout="centered"
)

# --- UI Elements ---
st.title("✈️ Flight Deal Finder")
st.markdown("Find the best flight deals and email the report.")

# --- Input Fields ---
st.header("Search Parameters")

# 1. Destination Input
dest_input = st.text_input(
    "Destinations (comma-separated)",
    "ATH, BCN, MUC, VIE",
    help="Enter airport codes like ATH, BCN, MUC, separated by commas."
)

# 2. Recipient Input
email_input = st.text_input(
    "Recipient Emails (comma-separated)",
    "marcelattar@gmail.com",
    help="Enter one or more email addresses, separated by commas."
)

# 3. Date Inputs (NEW)
st.markdown("Select your travel dates:")

# Get default dates from CONFIG.py to be helpful
# We use datetime.date.fromisoformat for parsing
try:
    default_out_date = datetime.date.fromisoformat("2026-03-19")
    default_ret_date = datetime.date.fromisoformat("2026-03-22")
except ValueError:  # Fallback in case the string is invalid
    default_out_date = datetime.date.today() + datetime.timedelta(days=100)
    default_ret_date = default_out_date + datetime.timedelta(days=3)

col1, col2 = st.columns(2)
with col1:
    out_date = st.date_input(
        "Outbound Date",
        default_out_date
    )
with col2:
    ret_date = st.date_input(
        "Return Date",
        default_ret_date
    )

st.divider()

# --- Run Button ---
if st.button("Find and Send Flight Deals", type="primary"):

    # --- Process Inputs ---
    destinations_list = [dest.strip().upper() for dest in dest_input.split(',') if dest.strip()]
    receiver_emails_list = [email.strip() for email in email_input.split(',') if email.strip()]

    # --- Format Date Inputs (NEW) ---
    out_date_str = out_date.strftime("%Y-%m-%d")
    ret_date_str = ret_date.strftime("%Y-%m-%d")

    # --- Validation ---
    if not destinations_list:
        st.error("Please enter at least one destination.")
    elif not receiver_emails_list:
        st.error("Please enter at least one recipient email.")
    # NEW: Add date validation
    elif ret_date <= out_date:
        st.error("Return date must be after the outbound date.")
    else:
        # --- Run the Job ---
        st.info(f"Searching for flights to: {', '.join(destinations_list)}")
        st.write(f"Dates: {out_date_str} to {ret_date_str}")

        with st.spinner("Please wait... fetching flight data and sending email..."):
            try:
                # MODIFIED: Pass the new date strings to the job
                main.job(
                    destinations_list,
                    receiver_emails_list,
                    out_date_str,
                    ret_date_str
                )

                st.success(f"Done! Report sent successfully to: {', '.join(receiver_emails_list)}")

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.exception(e)

# --- Sidebar ---
st.sidebar.header("About")
st.sidebar.info(
    "This app uses the 'flights_to_email' backend to search for "
    "flight prices and send a summary report via email."
)
