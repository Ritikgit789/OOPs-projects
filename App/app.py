import streamlit as st
import time
from queue_system import Patient, Specialization

# Custom CSS for a better UI
st.markdown("""
    <style>
        .main { background-color: #f0f2f6; }
        div.block-container {padding-top: 2rem;}
        .stButton>button {border-radius: 8px; font-weight: bold;}
        .stTextInput>div>div>input {border-radius: 5px; padding: 10px;}
        .stSelectbox>div>div>select {border-radius: 5px; padding: 5px;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "specializations" not in st.session_state:
    st.session_state.specializations = {
        "Cardiology": Specialization("Cardiology"),
        "Neurology": Specialization("Neurology"),
        "Orthopedics": Specialization("Orthopedics"),
        "General Medicine": Specialization("General Medicine"),
    }

st.title("🏥 Hospital Patient Queue Management System")

# Sidebar with statistics
st.sidebar.header("📊 Queue Statistics")
total_patients = sum(len(spec.list_patients()) for spec in st.session_state.specializations.values())
st.sidebar.subheader(f"👨‍⚕️ Total Patients: {total_patients}")
for spec_name, spec in st.session_state.specializations.items():
    st.sidebar.write(f"🩺 {spec_name}: {len(spec.list_patients())} patients")

# Sidebar navigation
option = st.sidebar.radio("🛠 Choose an action:", 
    ["🏥 Add Patient", "📋 View Queue", "⏩ Next Patient", "❌ Remove Patient", "🔍 Search Patient"])

# 1️⃣ Add a Patient
if option == "🏥 Add Patient":
    st.subheader("➕ Add a New Patient")
    name = st.text_input("👤 Patient Name:")
    specialization = st.selectbox("🏥 Select Specialization", list(st.session_state.specializations.keys()))
    status = st.radio("🚨 Select Urgency Level:", [0, 1, 2], format_func=lambda x: ["🟢 Normal", "🟠 Urgent", "🔴 Super-Urgent"][x])

    if st.button("✅ Add Patient"):
        if name.strip():
            new_patient = Patient(name, status)
            if st.session_state.specializations[specialization].add_patient(new_patient):
                st.success(f"🎉 {name} added to {specialization} queue!")
            else:
                st.error(f"⚠️ Queue is full! Cannot add more patients to {specialization}.")
        else:
            st.warning("⚠️ Please enter a valid patient name!")

# 2️⃣ View Specialization Queue
elif option == "📋 View Queue":
    st.subheader("📋 View Specialization Queue")
    specialization = st.selectbox("🏥 Select Specialization", list(st.session_state.specializations.keys()))

    patients = st.session_state.specializations[specialization].list_patients()
    if patients:
        for idx, patient in enumerate(patients, 1):
            st.write(f"**{idx}. 👤 {patient}**")
    else:
        st.info("📭 No patients in the queue!")

# 3️⃣ Get Next Patient
elif option == "⏩ Next Patient":
    st.subheader("⏩ Retrieve Next Patient")
    specialization = st.selectbox("🏥 Select Specialization", list(st.session_state.specializations.keys()))

    if st.button("🔄 Get Next Patient"):
        next_patient = st.session_state.specializations[specialization].get_next_patient()
        if next_patient:
            st.success(f"🎯 {next_patient.name} is next in {specialization}!")
        else:
            st.warning("📭 No patients left in the queue.")

# 4️⃣ Remove a Patient
elif option == "❌ Remove Patient":
    st.subheader("🗑 Remove a Patient")
    specialization = st.selectbox("🏥 Select Specialization", list(st.session_state.specializations.keys()))
    name = st.text_input("👤 Enter Patient Name:")

    if st.button("🗑 Remove Patient"):
        if st.session_state.specializations[specialization].remove_patient(name):
            st.success(f"✅ {name} removed from {specialization}.")
        else:
            st.error("⚠️ Patient not found in the queue.")

# 5️⃣ Search for a Patient
elif option == "🔍 Search Patient":
    st.subheader("🔍 Search for a Patient")
    search_name = st.text_input("👤 Enter Patient Name to Search:")
    if st.button("🔍 Search"):
        found = False
        for spec_name, spec in st.session_state.specializations.items():
            for patient in spec.list_patients():
                if patient.name.lower() == search_name.lower():
                    st.success(f"✅ {search_name} is in the **{spec_name}** queue as {patient}")
                    found = True
        if not found:
            st.warning("❌ Patient not found in any queue.")
