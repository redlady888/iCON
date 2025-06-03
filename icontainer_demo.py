# i-CONtainer Demo App (Streamlit)

import streamlit as st
from PIL import Image

# --- CONFIG ---
st.set_page_config(page_title="i-CONtainer Demo", layout="centered")

# --- LOGO + THEME ---
logo = "de8ff003-630f-4193-b36e-5ace02f85b89.png"

# --- Editable Gas Thresholds ---
gas_limits = {
    "Meat":     {"CO2": 1000, "NH3": 50, "H2S": 30, "VOC": 120},
    "Eggs":     {"CO2": 900,  "NH3": 40, "H2S": 25, "VOC": 100},
    "Vegetable":{"CO2": 800,  "NH3": 20, "H2S": 10, "VOC": 80},
    "Sandwich": {"CO2": 950,  "NH3": 35, "H2S": 15, "VOC": 110},
    "Pasta":    {"CO2": 850,  "NH3": 25, "H2S": 12, "VOC": 90},
    "Rice":     {"CO2": 800,  "NH3": 22, "H2S": 10, "VOC": 85},
}

# --- Main App State ---
if "page" not in st.session_state:
    st.session_state.page = "home"

if "products" not in st.session_state:
    st.session_state.products = ["i-CONtainer"]

if "current_product" not in st.session_state:
    st.session_state.current_product = "i-CONtainer"

if "show_input_popup" not in st.session_state:
    st.session_state.show_input_popup = False

if "subscription" not in st.session_state:
    st.session_state.subscription = "$1/month"

# --- HEADER BAR ---
st.markdown("""
    <style>
        body {
            background-color: #1e1e2f;
            color: #ffffff;
        }
        .stButton button {
            background-color: #7c4dff;
            color: white;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #9e7dff;
        }
    </style>
""", unsafe_allow_html=True)

with st.container():
    col1, col2, col3 = st.columns([1, 5, 2])
    with col1:
        st.image(logo, width=60)
    with col2:
        st.markdown("## taste without waste.")
    with col3:
        sub = st.selectbox("Subscription", ["$1/month", "$200/year", "$500/3 years"], index=["$1/month", "$200/year", "$500/3 years"].index(st.session_state.subscription))
        st.session_state.subscription = sub

# --- PAGE ROUTING ---
if st.session_state.page == "home":
    st.title("Welcome to i-CONtainer")
    st.markdown("**Smarter food storage. Cleaner eating.**")
    if st.button("Start Demo"):
        st.session_state.page = "input"
        st.rerun()

elif st.session_state.page == "input" and st.session_state.current_product == "i-CONtainer":
    st.title("Enter Food Details")
    food = st.selectbox("Select Food Type", list(gas_limits.keys()), index=0)

    st.subheader("Sensor Data Input (ppm)")
    co2 = st.slider("CO₂", 0, 2000, 500)
    nh3 = st.slider("Ammonia (NH₃)", 0, 100, 20)
    h2s = st.slider("Hydrogen Sulfide (H₂S)", 0, 100, 10)
    voc = st.slider("VOCs", 0, 300, 100)

    if st.button("Check Spoilage Status"):
        st.session_state.food = food
        st.session_state.inputs = {"CO2": co2, "NH3": nh3, "H2S": h2s, "VOC": voc}
        st.session_state.page = "result"
        st.rerun()

elif st.session_state.page == "input":
    st.title(f"{st.session_state.current_product}")
    st.subheader("Coming Soon")
    st.button("Set Up Product")

elif st.session_state.page == "result":
    food = st.session_state.food
    inputs = st.session_state.inputs
    limits = gas_limits[food]

    status = "Fresh, enjoy"
    color = "green"

    for gas in inputs:
        val = inputs[gas]
        threshold = limits[gas]
        if val > threshold:
            status = "Spoiled, do not eat"
            color = "red"
            break
        elif val > 0.8 * threshold and status != "Spoiled":
            status = "Warning, consume food soon"
            color = "orange"

    st.title("Analysis Result")
    st.markdown(f"### 🍽️ Food: **{food}**")
    st.markdown(f"### 🧪 Status: **:{color}[{status}]**")

    with st.expander("See Gas Details"):
        for gas in inputs:
            val = inputs[gas]
            threshold = limits[gas]
            if val > threshold:
                tag = f"<span style='color:red;font-weight:bold;'>Above Limit</span>"
            elif val > 0.8 * threshold:
                tag = f"<span style='color:orange;font-weight:bold;'>Warning</span>"
            else:
                tag = f"<span style='color:lightgreen;font-weight:bold;'>Normal</span>"
            st.markdown(f"{gas}: {val} ppm (Threshold: {threshold} ppm) → {tag}", unsafe_allow_html=True)

    if st.button("Restart"):
        st.session_state.page = "home"
        st.rerun()

# --- SIDEBAR ---
st.sidebar.markdown("### 👤 Account")
st.sidebar.text_input("Username", value="User", key="username")

st.sidebar.markdown("### Your Products")
for p in st.session_state.products:
    if st.sidebar.button(p, key=f"product_{p}"):
        st.session_state.current_product = p
        st.session_state.page = "input"
        st.rerun()

st.sidebar.markdown(f"**Selected:** {st.session_state.current_product}")

if st.sidebar.button("➕ Add Product"):
    st.session_state.show_input_popup = True
    st.rerun()

if st.session_state.show_input_popup:
    new_product = st.text_input("Enter product name")
    if st.button("Add to List") and new_product:
        st.session_state.products.append(new_product)
        st.session_state.current_product = new_product
        st.session_state.page = "input"
        st.session_state.show_input_popup = False
        st.rerun()

st.sidebar.markdown("### 🚀 Future Features")
st.sidebar.info("• Grocery Expiry Tracker\n• Health Nutrient Recommendations\n• Smart Fridge Linking")
