import streamlit as st
import main

# page configuration
st.set_page_config(
    page_title="Flights Ranking App",
    page_icon="✈️",
    layout="centered"
)
# destination input
st.title("✈️ Flight Deal Finder")
st.markdown("Find the best flight deals and email the report.")
st.header("Search Parameters")
dest_input = st.text_input(
    "Destinations (comma-separated)",
    "ATH, BCN, MUC, VIE",
    help="Enter airport codes like ATH, BCN, MUC, separated by commas."
)

# recipient input
email_input = st.text_input(
    "Recipient Emails (comma-separated)",
    "marcelattar@gmail.com",
    help="Enter one or more email addresses, separated by commas."
)


st.divider()

# run button
if st.button("Find and Send Flight Deals", type="primary"):
    # --- Process Inputs ---
    # Split the comma-separated strings into clean lists
    destinations_list = [dest.strip().upper() for dest in dest_input.split(',') if dest.strip()]
    receiver_emails_list = [email.strip() for email in email_input.split(',') if email.strip()]

    if not destinations_list:
        st.error("Please enter at least one destination.")
    elif not receiver_emails_list:
        st.error("Please enter at least one recipient email.")

    else:
        # --- Run the Job ---
        st.info(f"Searching for flights to: {', '.join(destinations_list)}")

        with st.spinner("Please wait... fetching flight data and sending email..."):
            try:
                # Call your refactored job function
                main.job(destinations_list, receiver_emails_list)

                # Show success message
                st.success(f"Done! Report sent successfully to: {', '.join(receiver_emails_list)}")

            except Exception as e:
                # Show any errors
                st.error(f"An error occurred: {e}")
                st.exception(e)

# --- Sidebar (Optional) ---
st.sidebar.header("About")
st.sidebar.info(
    "This app uses the 'flights_to_email' backend to search for "
    "flight prices and send a summary report via email."
)
