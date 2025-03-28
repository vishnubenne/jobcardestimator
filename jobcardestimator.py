import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="CE Time Estimator", layout="centered")
st.title("📋 Per-CE Time Estimator")

st.markdown("This tool estimates the time required to process **one Combined Entity (CE)** across Content, Media, and Catalog teams. Weekends are included in timeline estimation but not counted as working days.")

# --- CE TYPE ---
is_new_ce = st.checkbox("Is this a new CE?")

handover_date = st.date_input("📅 Handover Date from BizOps")

st.markdown("---")
st.header("📝 Listing Types in this CE")

listing_combos = st.number_input("New Listings Combo", min_value=0, step=1)
new_listings = st.number_input("New Listings", min_value=0, step=1)
multi_vendors = st.number_input("Multi Vendors", min_value=0, step=1)
multi_variants = st.number_input("Multi Variants", min_value=0, step=1)
experience_revamps = st.number_input("Experience Revamps", min_value=0, step=1)

# Total listings for reuse
total_listings = listing_combos + new_listings + multi_vendors + multi_variants + experience_revamps

st.markdown("---")
st.header("✍️ Content Team Inputs")

st.markdown("""
**🔧 Fix Definitions:**
- **Quick Fix** = Typos, factual corrections, slight rephrasing, correcting a date or name, replacing a single broken link, minor formatting change (**~15 mins**)  
- **Complex Fix** = Large updates requiring planning or coordination, such as new page creation, structural updates, variant additions, revamps, or redesigns (**~2 hours**)
""")

writers_count = st.number_input("How many writers are working in parallel?", min_value=1, step=1)

# Always included
RESEARCH_HOURS = 4

# Updated content listing TATs (in hours)
content_listing_tat_hours = {
    "New Listings Combo": 2,
    "New Listing": 3,
    "Multivendor": 1,
    "Multivariant": 2,
    "Experience Revamp": 2
}

listing_hours = (
    listing_combos * content_listing_tat_hours["New Listings Combo"] +
    new_listings * content_listing_tat_hours["New Listing"] +
    multi_vendors * content_listing_tat_hours["Multivendor"] +
    multi_variants * content_listing_tat_hours["Multivariant"] +
    experience_revamps * content_listing_tat_hours["Experience Revamp"]
)

# Additional CE-based content work (in hours)
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

# Convert to days
total_content_days = (listing_hours / 8) + ((total_hours / writers_count) / 8)

# --- MEDIA TEAM ---
st.markdown("---")
st.header("🖼 Media Team Tasks (Auto Calculated)")

# Updated: All media tasks take 2 hours per listing type
media_hours = 2 * (listing_combos + new_listings + multi_vendors + multi_variants + experience_revamps + itineraries)
media_time = media_hours / 8  # convert to days

# --- FINAL OUTPUT ---
st.markdown("---")
st.header("📊 Time Summary for This CE")

catalog_time = 2.0
src_time = 1.0
assignment_lag = 1.0

parallel_time = max(total_content_days, media_time)
total_time_ce = catalog_time + parallel_time

def add_working_days(start_date, work_days):
    current = start_date
    days_added = 0
    while days_added < work_days:
        current += timedelta(days=1)
        if current.weekday() < 5:  # Monday to Friday
            days_added += 1
    return current

if st.button("Calculate Time for This CE"):
    content_start_date = add_working_days(handover_date, int(src_time + catalog_time + assignment_lag))
    ce_end_date = add_working_days(content_start_date, int(total_time_ce))

    st.subheader("🕒 Detailed Team Time")
    st.write(f"Catalog Team: {catalog_time} days (fixed)")
    st.write(f"Content Team: {round(total_content_days, 2)} days (adjusted for {writers_count} writer(s))")
    st.write(f"Media Team: {round(media_time, 2)} days")
    st.markdown("---")
    st.subheader("📅 Estimated Dates")
    st.write(f"Content Start Date: {content_start_date.strftime('%A, %d %B %Y')}")
    st.write(f"Estimated Completion Date: {ce_end_date.strftime('%A, %d %B %Y')}")
    st.subheader(f"🚀 Total Time to Complete This CE: {round(total_time_ce, 2)} working days")

