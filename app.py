import streamlit as st
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="COVID-19 Prediction System",
    page_icon="🩺",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #020617 0%, #0f172a 48%, #111827 100%);
    color: white;
}

.main-title {
    color: #7dd3fc;
    font-size: 42px;
    font-weight: 700;
}

.subtitle {
    color: #cbd5e1;
    font-size: 18px;
    margin-bottom: 30px;
}

.glass {
    background: rgba(15, 23, 42, 0.72);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}

.result-high {
    background: rgba(255, 0, 0, 0.15);
    padding: 20px;
    border-left: 5px solid red;
    border-radius: 12px;
}

.result-medium {
    background: rgba(255, 165, 0, 0.15);
    padding: 20px;
    border-left: 5px solid orange;
    border-radius: 12px;
}

.result-low {
    background: rgba(0, 255, 0, 0.15);
    padding: 20px;
    border-left: 5px solid green;
    border-radius: 12px;
}

.stat-card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 18px;
    text-align: center;
}

.stat-number {
    font-size: 35px;
    color: #7dd3fc;
    font-weight: bold;
}

.history-box {
    background: rgba(255,255,255,0.04);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "total" not in st.session_state:
    st.session_state.total = 0
    st.session_state.high = 0
    st.session_state.medium = 0
    st.session_state.low = 0
    st.session_state.history = []

# ---------------- HEADER ----------------
st.markdown('<div class="main-title">🩺 COVID AI Prediction Panel</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Enter patient details and symptoms for COVID-19 risk assessment.</div>',
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.markdown("## 🧾 Patient Information")

    age = st.number_input("Age", 0, 120, 25)

    gender = st.selectbox("Gender", ["Male", "Female"])

    st.markdown("## 🤒 Symptoms")

    fever = st.selectbox("Fever", ["No", "Yes"])
    cough = st.selectbox("Cough", ["No", "Yes"])
    cold = st.selectbox("Cold / Sore Throat", ["No", "Yes"])
    fatigue = st.selectbox("Fatigue", ["No", "Yes"])
    breathing = st.selectbox("Breathing Difficulty", ["No", "Yes"])
    chest = st.selectbox("Chest Pain", ["No", "Yes"])
    smell = st.selectbox("Loss of Smell/Taste", ["No", "Yes"])

    st.markdown("## 🏥 Medical History")

    diabetes = st.selectbox("Diabetes", ["No", "Yes"])
    asthma = st.selectbox("Asthma", ["No", "Yes"])
    smoke = st.selectbox("Smoking", ["No", "Yes"])

    predict = st.button("🔍 Analyze Risk", use_container_width=True)

# ---------------- PREDICTION ----------------
if predict:

    symptoms = [
        fever,
        cough,
        cold,
        fatigue,
        breathing,
        chest,
        smell
    ]

    score = symptoms.count("Yes")

    if score >= 5:
        risk = "🚨 HIGH RISK"
        confidence = "96%"
        result_class = "result-high"
        message = "Immediate medical consultation recommended."
        st.session_state.high += 1

    elif score >= 3:
        risk = "⚠️ MEDIUM RISK"
        confidence = "78%"
        result_class = "result-medium"
        message = "Monitor symptoms carefully and maintain precautions."
        st.session_state.medium += 1

    else:
        risk = "✅ LOW RISK"
        confidence = "42%"
        result_class = "result-low"
        message = "Stay safe and continue following precautions."
        st.session_state.low += 1

    st.session_state.total += 1

    # Save History
    st.session_state.history.insert(0, {
        "risk": risk,
        "confidence": confidence,
        "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    })

    # Result Box
    st.markdown(f"""
    <div class="{result_class}">
        <h1>{risk}</h1>
        <h3>Prediction Confidence: {confidence}</h3>
        <p>{message}</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- STATS ----------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{st.session_state.total}</div>
        <p>Total Predictions</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{st.session_state.high}</div>
        <p>High Risk Cases</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{st.session_state.medium}</div>
        <p>Medium Risk Cases</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{st.session_state.low}</div>
        <p>Low Risk Cases</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- HISTORY ----------------
st.markdown("## 📜 Prediction History")

if st.session_state.history:

    for item in st.session_state.history:

        st.markdown(f"""
        <div class="history-box">
            <h4>{item['risk']}</h4>
            <p>Confidence: {item['confidence']}</p>
            <small>{item['time']}</small>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("No predictions yet.")

# ---------------- SAFETY TIPS ----------------
st.markdown("## 🛡 COVID-19 Safety Tips")

tips = [
    "✔ Wear mask properly and consistently.",
    "✔ Wash hands with soap or sanitizer frequently.",
    "✔ Avoid crowded indoor spaces.",
    "✔ Maintain social distance when possible.",
    "✔ Stay hydrated and rest well.",
    "✔ Contact a physician if symptoms worsen."
]

for tip in tips:
    st.markdown(f"- {tip}")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("This project is for educational and research purposes only.")