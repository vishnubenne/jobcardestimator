import streamlit as st

st.set_page_config(page_title="CE Weekly Planner", layout="centered")
st.title("🗓️ CE Weekly Time Estimator")
st.markdown("Efficiently plan and estimate your weekly bandwidth by CE and team")

# --- INPUT SECTION ---

num_ces = st.number_input("🔢 How many Combined Entities (CEs) are you working on this week?", min_value=1, step=1)

st.markdown("---")
st.header("✍️ Content Team (per CE)")

content_itineraries_per_ce = st.number_input("How many itineraries per CE?", min_value=0, step=1)
content_quick_fixes = st.number_input("Quick Fixes (across all CEs)", min_value=0, step=1)
content_complex_fixes = st.number_input("Complex Fixes (across all CEs)", min_value=0, step=1)

# Content time per CE (excluding overlapping edits)
def calculate_content_time_per_ce(itineraries):
    return 4 + 4 + 4 + 2 + (2 * itineraries)  # research + landing + POI + shoulder + itinerary

# Fixes (outside CE structure)
def calculate_content_fixes_time(quick, complex):
    return (quick * 0.25) + (complex * 2)

# --- MEDIA TEAM ---
st.markdown("---")
st.header("🖼 Media Team (per CE)")

media_new_listings_combo = st.number_input("New Listings Combo", min_value=0, step=1)
media_new_listings = st.number_input("New Listing", min_value=0, step=1)
media_multivendor = st.number_input("Multivendor", min_value=0, step=1)
media_experience_revamp = st.number_input("Experience Revamp", min_value=0, step=1)
media_multivariant = st.number_input("Multivariant", min_value=0, step=1)
media_qa_fixes = st.number_input("QA Fixes", min_value=0, step=1)
media_itineraries = st.number_input("# of Itinerary tickets", min_value=0, step=1)

media_tat_map = {
    "New Listings Combo": 1.64,
    "New Listing": 1.12,
    "Multivendor": 0.85,
    "Experience Revamp": 1.19,
    "Multivariant": 0.89,
    "QA Fixes": 0.5,
    "Itinerary": 2
}

media_total = (
    media_new_listings_combo * media_tat_map["New Listings Combo"] +
    media_new_listings * media_tat_map["New Listing"] +
    media_multivendor * media_tat_map["Multivendor"] +
    media_experience_revamp * media_tat_map["Experience Revamp"] +
    media_multivariant * media_tat_map["Multivariant"] +
    media_qa_fixes * media_tat_map["QA Fixes"] +
    media_itineraries * media_tat_map["Itinerary"]
)

# --- CATALOG TEAM ---
st.markdown("---")
st.header("📦 Catalog Team Tasks")

catalog_inputs = {}
catalog_tat_days = {
    "New listing": 0.64,
    "Multi vendor": 1.34,
    "Multi variant": 0.97,
    "Experience revamp": 0.48,
    "Price Change": 0.2,
    "Pricing Discrepancy": 1.4,
    "Product update request": 1,
    "Meeting Point/Where Section": 1.5,
    "Experience Unavailable": 8,
    "External Email": 3,
    "My Tickets and Vouchers": 1.9,
    "General Catalog": 0.4
}

for task in catalog_tat_days:
    catalog_inputs[task] = st.number_input(task, min_value=0, step=1, key=f"catalog_{task}")

catalog_total = sum([catalog_inputs[task] * catalog_tat_days[task] for task in catalog_inputs])

# --- OUTPUT ---
st.markdown("---")
st.header("📊 Weekly Summary")

if st.button("Calculate Total Time"):
    content_total_per_ce = calculate_content_time_per_ce(content_itineraries_per_ce)
    content_total = content_total_per_ce * num_ces + calculate_content_fixes_time(content_quick_fixes, content_complex_fixes)

    media_time_per_ce = media_total / num_ces if num_ces else 0
    parallel_ce_time = max(content_total_per_ce, media_time_per_ce)
    total_time_per_ce = parallel_ce_time + (catalog_total / num_ces if num_ces else 0)
    total_time_all_ces = total_time_per_ce * num_ces

    st.subheader("⏱️ Time Estimates (in days)")
    st.write(f"Content Team: {round(content_total, 2)} days")
    st.write(f"Media Team: {round(media_total, 2)} days")
    st.write(f"Catalog Team: {round(catalog_total, 2)} days")
    st.write(f"---")
    st.write(f"Average Time to Complete 1 CE: **{round(total_time_per_ce, 2)} days**")
    st.write(f"Total Time for {num_ces} CEs: **{round(total_time_all_ces, 2)} days**")
