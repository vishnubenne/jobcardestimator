import streamlit as st

# Issue types and time taken by each team (in hours)
content_issues = {
    "MMP with 5–7 listings": 20,
    "Landing Page": 20,
    "Shoulder Page": 12,
    "Automated Shoulder Page": 4,
    "Itinerary for 5–7 NLS": 8,
    "Research for new CE": 4,
    "MMP listings (6)": 12,
    "POI Content Table": 4,
    "Shoulder Pages (4 + STL + Guided)": 12,
    "Itinerary for MMP (6 listings) – NOT HOHO": 12,
    "Quick Fixes": 0.25,
    "Complex Fixes": 2,
    "Edits/Changes/Marketing Edits": 4
}

catalog_issues = {
    "New listing": 8,
    "Multi vendor": 13.6,
    "Multi variant": 9.6,
    "Experience revamp": 4,
    "Price Change": 1.6,
    "Pricing Discrepancy": 11.2,
    "Product update request": 8,
    "Meeting Point/Where Section": 12,
    "Experience Unavailable": 64,
    "External Email": 24,
    "My Tickets and Vouchers": 15.2,
    "General Catalog": 3.2
}

media_issues = {
    "Research of all images": 4,
    "MMP revamp of existing (6 listings)": 12,
    "MMP launch for 6 new listings": 16,
    "MB Banner": 0.17,
    "Collection Banner": 0.17,
    "Landing Page": 2,
    "Itinerary for MMP (6 listings) – NOT HOHO": 10,
    "Itinerary for 6 NLS (HOHO)": 16,
    "POI Table Media": 1,
    "Lead QA": 1,
    "Changes post QA": 4
}

qa_issues = {
    "New Listing": 16,
    "Multivendor": 16,
    "Multivariant": 16,
    "Revamp": 16,
    "Combos": 16,
    "Shows (LTT/ Broadway)": 16
}

def calculate_total_time(issue_dict, selected_issues):
    total = 0
    for issue, count in selected_issues.items():
        if issue in issue_dict:
            total += issue_dict[issue] * count
    return total

st.title("Job Card Time Estimator")

st.header("Content Team Tasks")
content_selected = {issue: st.number_input(f"{issue}", min_value=0, step=1, key=f"content_{issue}") for issue in content_issues}

st.header("Catalog Team Tasks")
catalog_selected = {issue: st.number_input(f"{issue}", min_value=0, step=1, key=f"catalog_{issue}") for issue in catalog_issues}

st.header("Media Team Tasks")
media_selected = {issue: st.number_input(f"{issue}", min_value=0, step=1, key=f"media_{issue}") for issue in media_issues}

st.header("IO/QA Team Tasks")
qa_selected = {issue: st.number_input(f"{issue}", min_value=0, step=1, key=f"qa_{issue}") for issue in qa_issues}

if st.button("Calculate Total Time"):
    total_content = calculate_total_time(content_issues, content_selected)
    total_catalog = calculate_total_time(catalog_issues, catalog_selected)
    total_media = calculate_total_time(media_issues, media_selected)
    total_qa = calculate_total_time(qa_issues, qa_selected)
    grand_total = total_content + total_catalog + total_media + total_qa

    st.subheader("Time Estimates (in hours)")
    st.write(f"Content Team: {total_content} hours")
    st.write(f"Catalog Team: {total_catalog} hours")
    st.write(f"Media Team: {total_media} hours")
    st.write(f"IO/QA Team: {total_qa} hours")
    st.markdown(f"### Grand Total: {grand_total} hours")

