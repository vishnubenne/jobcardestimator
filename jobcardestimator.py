import streamlit as st

st.set_page_config(page_title="CE Time Estimator", layout="centered")
st.title("📋 Per-CE Time Estimator")

st.markdown("This tool estimates the time required to process **one Combined Entity (CE)** based on work across Content and Media teams. QA TAT is not included. Catalog effort is considered fixed at 2 days.")

# --- CE TYPE ---
is_new_ce = st.checkbox("Is this a new CE?")

st.markdown("---")
st.header("📝 Listing Information")

include_listings = False
if is_new_ce:
    st.markdown("**For New CE:** Enter number of new listings")
    listing_count = st.number_input("Number of new listings", min_value=0, step=1)
    include_listings = True
else:
    include_listings = st.checkbox("Are there any new listings (e.g. multi-vendor, multi-variant)?")
    listing_count = 0
    if include_listings:
        listing_count = st.number_input("Number of new listings in existing CE", min_value=0, step=1)

st.markdown("---")
st.header("✍️ Content Team Inputs")

writers_count = st.number_input("How many writers are working in parallel?", min_value=1, step=1)

# Always included
RESEARCH_HOURS = 4

# Listing content time based on avg full TAT in days
LISTING_TAT_DAYS = 3.72  # You may adjust this to a more dynamic formula later
listing_time = listing_count * LISTING_TAT_DAYS if include_listings else 0

# Optional new CE components
total_hours = RESEARCH_HOURS
if is_new_ce:
    if st.checkbox("Include Landing Page?"):
        total_hours += 4
    if st.checkbox("Include Shoulder Pages?"):
        total_hours += 2
    if st.checkbox("Include POI Table?"):
        total_hours += 4
else:
    if st.checkbox("Landing Page Edits"):
        total_hours += 1
    if st.checkbox("Shoulder Page Edits"):
        total_hours += 1
    quick_fixes = st.number_input("Quick Fixes (15 mins each)", min_value=0, step=1)
    complex_fixes = st.number_input("Complex Fixes (2 hours each)", min_value=0, step=1)
    total_hours += quick_fixes * 0.25 + complex_fixes * 2

# Itineraries (both new & existing CEs)
itineraries = st.number_input("Number of Itineraries", min_value=0, step=1)
total_hours += itineraries * 2

# Convert to days and adjust for writer parallelism
additional_content_time = (total_hours / writers_count) / 8
content_total_time = listing_time + additional_content_time

# --- MEDIA TEAM ---
st.markdown("---")
st.header("🖼 Media Team Tasks (Auto Calculated)")

media_tat_map = {
    "New Listings Combo": 1.64,
    "New Listing": 1.12,
    "Multivendor": 0.85,
    "Experience Revamp": 1.19,
    "Multivariant": 0.89,
    "Itinerary": 2
}

media_time = listing_count * media_tat_map["New Listing"] + itineraries * media_tat_map["Itinerary"]

# --- FINAL OUTPUT ---
st.markdown("---")
st.header("📊 Time Summary for This CE")

catalog_time = 2.0
parallel_time = max(content_total_time, media_time)
total_time_ce = catalog_time + parallel_time

if st.button("Calculate Time for This CE"):
    st.subheader("🕒 Detailed Team Time")
    st.write(f"Catalog Team: {catalog_time} days (fixed)")
    st.write(f"Content Team: {round(content_total_time, 2)} days (includes listings + components, adjusted for {writers_count} writer(s))")
    st.write(f"Media Team: {round(media_time, 2)} days")
    st.markdown("---")
    st.subheader(f"🚀 **Total Time to Complete This CE: {round(total_time_ce, 2)} days**")
