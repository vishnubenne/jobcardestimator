import streamlit as st

st.set_page_config(page_title="CE Time Estimator", layout="centered")
st.title("📋 Per-CE Time Estimator")

st.markdown("This tool estimates the time required to process **one Combined Entity (CE)** based on work across Catalog, Content, and Media teams. QA TAT is not included.")

st.markdown("---")
st.header("🔢 Listing Types in this CE")
new_listings = st.number_input("New Listings", min_value=0, step=1)
multi_variants = st.number_input("Multi Variants", min_value=0, step=1)
multi_vendors = st.number_input("Multi Vendors", min_value=0, step=1)
experience_revamps = st.number_input("Experience Revamps", min_value=0, step=1)
listing_combos = st.number_input("New Listing Combos", min_value=0, step=1)
itineraries = st.number_input("Itineraries", min_value=0, step=1)

st.markdown("---")
st.header("✍️ Content Team Tasks")

st.markdown("""
- **Quick Fix** = Minor typo, factual correction, date/name fix, single broken link, formatting change (⏱ 15 mins)
- **Complex Fix** = Page revamp, structural changes, variant additions, redesign (⏱ 2 hours)
""")

writers_count = st.number_input("How many writers are working in parallel?", min_value=1, step=1)

include_landing = st.checkbox("Landing Page Needed")
include_poi = st.checkbox("POI Table Needed")
include_shoulder = st.checkbox("Shoulder Pages Needed")
content_quick_fixes = st.number_input("# of Quick Fixes", min_value=0, step=1)
content_complex_fixes = st.number_input("# of Complex Fixes", min_value=0, step=1)

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

media_time = (
    listing_combos * media_tat_map["New Listings Combo"] +
    new_listings * media_tat_map["New Listing"] +
    multi_vendors * media_tat_map["Multivendor"] +
    experience_revamps * media_tat_map["Experience Revamp"] +
    multi_variants * media_tat_map["Multivariant"] +
    itineraries * media_tat_map["Itinerary"]
)

# --- CATALOG TEAM ---
st.markdown("---")
st.header("📦 Catalog Team Tasks (Auto Calculated)")

catalog_tat_map = {
    "New listing": 0.64,
    "Multi vendor": 1.34,
    "Multi variant": 0.97,
    "Experience revamp": 0.48,
    "New Listings Combo": 0.87
}

catalog_time = (
    new_listings * catalog_tat_map["New listing"] +
    multi_vendors * catalog_tat_map["Multi vendor"] +
    multi_variants * catalog_tat_map["Multi variant"] +
    experience_revamps * catalog_tat_map["Experience revamp"] +
    listing_combos * catalog_tat_map["New Listings Combo"]
)

# --- CONTENT TEAM LOGIC ---
st.markdown("---")
st.header("🧠 Content Team Time Calculation")

content_time = 4  # Research
if include_landing:
    content_time += 4
if include_poi:
    content_time += 4
if include_shoulder:
    content_time += 2
content_time += 2 * itineraries
content_time += 0.25 * content_quick_fixes + 2 * content_complex_fixes

# Divide by number of writers
content_time = content_time / writers_count if writers_count else content_time

# --- FINAL OUTPUT ---
st.markdown("---")
st.header("📊 Time Summary for This CE")

parallel_time = max(content_time, media_time)
total_time_ce = catalog_time + parallel_time

if st.button("Calculate Time for This CE"):
    st.subheader("🕒 Detailed Team Time")
    st.write(f"Catalog Team: {round(catalog_time, 2)} days")
    st.write(f"Content Team: {round(content_time, 2)} days (adjusted for {writers_count} writer(s))")
    st.write(f"Media Team: {round(media_time, 2)} days")
    st.markdown("---")
    st.subheader(f"🚀 **Total Time to Complete This CE: {round(total_time_ce, 2)} days**")
