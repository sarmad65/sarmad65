import streamlit as st
import numpy as np
import pandas as pd
import joblib
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
import base64
import os

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"
if "show_maximize" not in st.session_state:
    st.session_state.show_maximize = False

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CardioSense AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state,
)

# ─── Load Heart Image as Base64 ───────────────────────────────────────────────
_heart_path = os.path.join(os.path.dirname(__file__), "heart.png")
with open(_heart_path, "rb") as _f:
    _heart_b64 = base64.b64encode(_f.read()).decode()
HEART_IMG = f'<img src="data:image/png;base64,{_heart_b64}" style="width:{{size}}; height:{{size}}; object-fit:contain; {{extra}}"/>'

# ─── Global CSS / Fonts / Animations ─────────────────────────────────────────
if st.session_state.theme == "Dark":
    theme_vars = """
    --bg:        #0d0f1a;
    --card:      #131627;
    --card2:     #1a1e35;
    --accent1:   #e84393;
    --accent2:   #a855f7;
    --accent3:   #22d3ee;
    --accent4:   #f97316;
    --safe:      #10b981;
    --danger:    #ef4444;
    --text:      #e2e8f0;
    --muted:     #94a3b8;
    --border:    rgba(255,255,255,0.08);
    --sidebar-bg-top: #0f1123;
    --sidebar-bg-bot: #1a0a2e;
    --hero-bg-top: #1a0a2e;
    --hero-bg-mid: #0d0f1a;
    --hero-bg-bot: #12101f;
    """
    matplotlib_bg = '#131627'
    matplotlib_text = '#e2e8f0'
    matplotlib_muted = '#94a3b8'
else:
    theme_vars = """
    --bg:        #f8fafc;
    --card:      #ffffff;
    --card2:     #f1f5f9;
    --accent1:   #e84393;
    --accent2:   #a855f7;
    --accent3:   #06b6d4;
    --accent4:   #ea580c;
    --safe:      #059669;
    --danger:    #dc2626;
    --text:      #0f172a;
    --muted:     #64748b;
    --border:    rgba(0,0,0,0.1);
    --sidebar-bg-top: #f8fafc;
    --sidebar-bg-bot: #e2e8f0;
    --hero-bg-top: #f1f5f9;
    --hero-bg-mid: #f8fafc;
    --hero-bg-bot: #e2e8f0;
    """
    matplotlib_bg = '#ffffff'
    matplotlib_text = '#0f172a'
    matplotlib_muted = '#64748b'

css_string = f"""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Root palette ── */
:root {{
{theme_vars}
}}

/* ── Base ── */
html, body, [class*="css"], .stApp {{
    font-family: 'Outfit', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}}

/* Hide default Streamlit menu and footer, but keep header for potential native buttons if needed, 
   or hide it selectively to keep our floating button visible. */
#MainMenu, footer {{ visibility: hidden; }}
header {{ background: transparent !important; }}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, var(--sidebar-bg-top) 0%, var(--sidebar-bg-bot) 100%) !important;
    border-right: 1px solid var(--border) !important;
}}
section[data-testid="stSidebar"] * {{ color: var(--text) !important; }}

/* ── Sliders & number inputs ── */
div[data-baseweb="slider"] .rc-slider-track   {{ background: linear-gradient(90deg, var(--accent1), var(--accent2)) !important; }}
div[data-baseweb="slider"] .rc-slider-handle  {{ border-color: var(--accent2) !important; background: var(--accent2) !important; }}

/* ── Select boxes ── */
div[data-baseweb="select"] > div {{
    background: var(--card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: linear-gradient(135deg, var(--accent1) 0%, var(--accent2) 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
    padding: 0.75rem 2.5rem !important;
    cursor: pointer !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    letter-spacing: 0.5px !important;
}}
.stButton > button:hover {{
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 30px rgba(232,67,147,0.45) !important;
}}

/* ── Progress bar ── */
div[data-testid="stProgressBar"] > div > div {{ background: linear-gradient(90deg, var(--accent1), var(--accent2)) !important; }}

/* ── Metric cards ── */
div[data-testid="metric-container"] {{
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 1rem 1.2rem !important;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: var(--bg); }}
::-webkit-scrollbar-thumb {{ background: var(--accent2); border-radius: 10px; }}

/* ── Hero banner ── */
.hero-banner {{
    background: linear-gradient(135deg, var(--hero-bg-top) 0%, var(--hero-bg-mid) 40%, var(--hero-bg-bot) 100%);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}}
.hero-banner::before {{
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(232,67,147,0.22) 0%, transparent 70%);
    pointer-events: none;
}}
.hero-banner::after {{
    content: "";
    position: absolute;
    bottom: -80px; left: 30%;
    width: 300px; height: 300px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(168,85,247,0.15) 0%, transparent 70%);
    pointer-events: none;
}}
.hero-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent1), var(--accent2), var(--accent3));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 0.5rem;
}}
.hero-sub {{
    font-size: 1.05rem;
    color: var(--muted);
    font-weight: 400;
    max-width: 600px;
}}

/* ── Section header ── */
.section-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: var(--text);
    border-left: 4px solid var(--accent1);
    padding-left: 0.75rem;
    margin-bottom: 1.2rem;
}}

/* ── Result card ── */
.result-card {{
    border-radius: 22px;
    padding: 2rem 2.5rem;
    text-align: center;
    margin-top: 1.5rem;
    animation: fadeIn 0.6s ease;
}}
.result-card.safe {{
    background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(16,185,129,0.05));
    border: 1px solid rgba(16,185,129,0.4);
}}
.result-card.danger {{
    background: linear-gradient(135deg, rgba(239,68,68,0.18), rgba(232,67,147,0.08));
    border: 1px solid rgba(239,68,68,0.45);
}}
.result-emoji {{ font-size: 4rem; line-height: 1; margin-bottom: 0.5rem; }}
.result-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.85rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
}}
.result-title.safe  {{ color: var(--safe); }}
.result-title.danger {{ color: var(--danger); }}
.result-subtitle {{ font-size: 1rem; color: var(--muted); }}

/* ── Probability bar ── */
.prob-bar-wrap {{
    background: rgba(128,128,128,0.2);
    border-radius: 50px;
    height: 18px;
    margin: 1rem 0;
    overflow: hidden;
}}
.prob-bar-inner {{
    height: 100%;
    border-radius: 50px;
    transition: width 1s ease;
}}

/* ── Info pill ── */
.info-pill {{
    display: inline-block;
    background: rgba(168,85,247,0.15);
    border: 1px solid rgba(168,85,247,0.35);
    border-radius: 50px;
    padding: 4px 16px;
    font-size: 0.8rem;
    color: var(--accent2);
    font-weight: 600;
    letter-spacing: 0.4px;
}}

/* ── Feature importance card ── */
.feat-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 1.5rem;
}}

/* ── Animations ── */
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(18px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes pulse {{
    0%, 100% {{ transform: scale(1); }}
    50%       {{ transform: scale(1.06); }}
}}
.pulse {{ animation: pulse 2s ease-in-out infinite; }}

/* ── Heartbeat wave (CSS only) ── */
.heartbeat {{ 
    display: inline-block;
    animation: heartbeat 1.4s ease-in-out infinite;
    transform-origin: center;
}}
@keyframes heartbeat {{
    0%   {{ transform: scale(1);   }}
    14%  {{ transform: scale(1.25);}}
    28%  {{ transform: scale(1);   }}
    42%  {{ transform: scale(1.15);}}
    70%  {{ transform: scale(1);   }}
    100% {{ transform: scale(1);   }}
}}

/* ── Number input ── */
input[type=number] {{
    background: var(--card2) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
}}

/* ── Tabs ── */
button[data-baseweb="tab"] {{ 
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    color: var(--muted) !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: var(--accent1) !important;
    border-bottom-color: var(--accent1) !important;
}}

/* ── Floating Maximize Button Container ── */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"]:has(button[key="floating_max_btn"]) {{
    position: fixed !important;
    top: 20px !important;
    right: 20px !important;
    z-index: 999999 !important;
    width: auto !important;
}}

/* Target the button itself */
div[data-testid="stButton"] button[key="floating_max_btn"] {{
    background: linear-gradient(135deg, var(--accent1) 0%, var(--accent2) 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 50% !important;
    width: 60px !important;
    height: 60px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5) !important;
    font-size: 1.5rem !important;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}}
div[data-testid="stButton"] button[key="floating_max_btn"]:hover {{
    transform: scale(1.1) rotate(10deg) !important;
    box-shadow: 0 6px 25px rgba(232,67,147,0.6) !important;
}}
</style>
"""
st.markdown(css_string, unsafe_allow_html=True)

# ─── Floating Maximize Button Logic ───
if st.session_state.sidebar_state == "collapsed":
    # This button will be styled by the CSS above to float at the top-right
    if st.button("➕", key="floating_max_btn", help="Maximize Sidebar"):
        st.session_state.sidebar_state = "expanded"
        st.rerun()

# ─── Load Model ──────────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    model   = joblib.load("heart_model.pkl")
    imputer = joblib.load("imputer.pkl")
    return model, imputer

model, imputer = load_artifacts()

FEATURES = ['age','sex','cp','trestbps','chol','fbs','restecg',
            'thalch','exang','oldpeak','slope','ca','thal']

FEATURE_LABELS = {
    'age':     'Age (years)',
    'sex':     'Sex',
    'cp':      'Chest Pain Type',
    'trestbps':'Resting Blood Pressure (mmHg)',
    'chol':    'Serum Cholesterol (mg/dl)',
    'fbs':     'Fasting Blood Sugar > 120',
    'restecg': 'Resting ECG Result',
    'thalch':  'Max Heart Rate Achieved',
    'exang':   'Exercise Induced Angina',
    'oldpeak': 'ST Depression (oldpeak)',
    'slope':   'Slope of Peak ST Segment',
    'ca':      'Major Vessels Colored (Fluoroscopy)',
    'thal':    'Thalassemia',
}

# ─── Hero Banner ─────────────────────────────────────────────────────────────
_hero_heart = HEART_IMG.format(size="110px", extra="filter: drop-shadow(0 0 20px rgba(232,67,147,0.5));")
st.markdown(f"""
<div class="hero-banner" style="display: flex; align-items: center; gap: 2rem;">
    <div class="heartbeat" style="flex-shrink: 0;">
        {_hero_heart}
    </div>
    <div>
        <div class="hero-title">CardioSense AI</div>
        <div class="hero-sub">
            Advanced Machine Learning for Cardiovascular Risk Assessment. 
            Empowering proactive health decisions with data-driven insights.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar Inputs ───────────────────────────────────────────────────────────
_sidebar_heart = HEART_IMG.format(size="90px", extra="display:block; margin:0 auto 0.5rem; filter: drop-shadow(0 0 14px rgba(232,67,147,0.6));")
with st.sidebar:
    # ── Theme and Sidebar Toggles ──
    st.markdown("<div class='section-title'>⚙️ App Settings</div>", unsafe_allow_html=True)
    is_light = st.toggle("🌞 Light Mode", value=(st.session_state.theme == "Light"))
    new_theme = "Light" if is_light else "Dark"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

    st.markdown("---")

    st.markdown(f"""
    <div style='text-align:center; margin-bottom:1.5rem;'>
      <div class='heartbeat'>{_sidebar_heart}</div>
      <div style='font-family:"Space Grotesk",sans-serif; font-size:1.4rem;
                  font-weight:800; background:linear-gradient(135deg,#e84393,#a855f7);
                  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                  background-clip:text;'>Patient Profile</div>
      <div style='color:var(--muted); font-size:0.82rem; margin-top:4px;'>
        Fill in clinical parameters
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Demographics
    st.markdown("<div class='section-title'>👤 Demographics</div>", unsafe_allow_html=True)
    age  = st.slider("Age", 20, 90, 55)
    sex  = st.selectbox("Sex", ["Male", "Female"])

    # Clinical
    st.markdown("<div class='section-title'>🩺 Clinical Findings</div>", unsafe_allow_html=True)
    cp_map     = {"Typical Angina": 0, "Atypical Angina": 1, "Non-Anginal": 2, "Asymptomatic": 3}
    cp         = st.selectbox("Chest Pain Type", list(cp_map.keys()))
    trestbps   = st.slider("Resting BP (mmHg)", 80, 200, 130)
    chol       = st.slider("Cholesterol (mg/dl)", 100, 600, 240)
    fbs        = st.selectbox("Fasting Blood Sugar > 120 mg/dl", ["No", "Yes"])
    restecg_map = {"Normal": 0, "LV Hypertrophy": 1, "ST-T Abnormality": 2}
    restecg    = st.selectbox("Resting ECG", list(restecg_map.keys()))

    # Exercise
    st.markdown("<div class='section-title'>🏃 Exercise Test</div>", unsafe_allow_html=True)
    thalch     = st.slider("Max Heart Rate Achieved", 60, 220, 150)
    exang      = st.selectbox("Exercise Induced Angina", ["No", "Yes"])
    oldpeak    = st.slider("ST Depression (Oldpeak)", 0.0, 7.0, 1.0, step=0.1)
    slope_map  = {"Upsloping": 1, "Flat": 2, "Downsloping": 3}
    slope      = st.selectbox("ST Slope", list(slope_map.keys()))

    # Additional
    st.markdown("<div class='section-title'>🔬 Additional Tests</div>", unsafe_allow_html=True)
    ca         = st.slider("Major Vessels (Fluoroscopy)", 0, 4, 0)
    thal_map   = {"Normal": 3, "Fixed Defect": 6, "Reversable Defect": 7}
    thal       = st.selectbox("Thalassemia", list(thal_map.keys()))

    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("🔮 Analyze Risk Now", use_container_width=True)

# ─── Build Input Vector ───────────────────────────────────────────────────────
sex_val     = 1 if sex == "Male" else 0
fbs_val     = 1 if fbs == "Yes" else 0
exang_val   = 1 if exang == "Yes" else 0
cp_val      = cp_map[cp]
restecg_val = restecg_map[restecg]
slope_val   = slope_map[slope]
thal_val    = thal_map[thal]

input_data = np.array([[age, sex_val, cp_val, trestbps, chol, fbs_val,
                         restecg_val, thalch, exang_val, oldpeak,
                         slope_val, ca, thal_val]], dtype=float)

input_imputed = imputer.transform(input_data)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 Prediction", "📊 Feature Importance", "ℹ️ About"])

# ════════════════════════════════════════════════════════════
# TAB 1 — PREDICTION
# ════════════════════════════════════════════════════════════
with tab1:
    if st.session_state.sidebar_state == "collapsed":
        st.info("💡 Sidebar is hidden. Expand it to edit the patient profile and run the analysis.")
        if st.button("🚀 Expand Sidebar & Edit Profile", use_container_width=True):
            st.session_state.sidebar_state = "expanded"
            st.rerun()
    
    if predict_btn:
        with st.spinner(""):
            progress = st.progress(0)
            for pct in range(0, 101, 5):
                time.sleep(0.03)
                progress.progress(pct)
            progress.empty()

        proba      = model.predict_proba(input_imputed)[0]
        risk_score = proba[1]          # probability of heart disease
        pred_class = int(risk_score >= 0.50)

        # ── Result Card ──
        if pred_class == 0:
            st.markdown(f"""
            <div class="result-card safe">
              <div class="result-emoji pulse">💚</div>
              <div class="result-title safe">Low Risk Detected</div>
              <div class="result-subtitle">
                Based on the provided clinical parameters, heart disease is unlikely.
              </div>
            </div>""", unsafe_allow_html=True)
            bar_color = "linear-gradient(90deg,#10b981,#34d399)"
        else:
            st.markdown(f"""
            <div class="result-card danger">
              <div class="result-emoji pulse">💔</div>
              <div class="result-title danger">Elevated Risk Detected</div>
              <div class="result-subtitle">
                Clinical indicators suggest a higher probability of heart disease.
                Please consult a cardiologist.
              </div>
            </div>""", unsafe_allow_html=True)
            bar_color = "linear-gradient(90deg,#ef4444,#e84393)"

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Probability Display ──
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.markdown(f"""
            <div style='text-align:center; margin-bottom:0.4rem;'>
              <span style='font-size:0.9rem; color:var(--muted); font-weight:500;'>
                HEART DISEASE PROBABILITY
              </span><br>
              <span style='font-family:"Space Grotesk",sans-serif; font-size:3.5rem;
                           font-weight:800; background:{bar_color};
                           -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                           background-clip:text;'>
                {risk_score*100:.1f}%
              </span>
            </div>
            <div class='prob-bar-wrap'>
              <div class='prob-bar-inner' style='width:{risk_score*100:.1f}%; background:{bar_color};'></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Threshold analysis metrics ──
        st.markdown("<div class='section-title'>📐 Threshold Analysis</div>", unsafe_allow_html=True)
        thresholds = [0.40, 0.45, 0.50, 0.55, 0.60, 0.65]
        
        # Find the switch point
        last_pos = None
        first_neg = None
        for th in sorted(thresholds):
            if risk_score >= th:
                last_pos = th
            elif first_neg is None:
                first_neg = th

        cols = st.columns(len(thresholds))
        for i, th in enumerate(thresholds):
            is_pos = risk_score >= th
            label  = "🔴 Positive" if is_pos else "🟢 Negative"
            active = "⭐ " if th == 0.50 else ""
            with cols[i]:
                st.metric(f"{active}T={th:.2f}", label)
        
        # Summary of Thresholds
        st.markdown("<br>", unsafe_allow_html=True)
        if last_pos is not None and first_neg is not None:
            summary_msg = f"The classification remains <b style='color:var(--danger)'>Positive</b> up to a threshold of <b>{last_pos:.2f}</b> and switches to <b style='color:var(--safe)'>Negative</b> at <b>{first_neg:.2f}</b>."
        elif last_pos is not None:
            summary_msg = f"The classification is <b style='color:var(--danger)'>Positive</b> across all evaluated thresholds (up to {max(thresholds):.2f})."
        else:
            summary_msg = f"The classification is <b style='color:var(--safe)'>Negative</b> across all evaluated thresholds (starting from {min(thresholds):.2f})."

        st.markdown(f"""
        <div style='background:var(--card2); border-left:4px solid var(--accent2); padding:1rem 1.5rem; border-radius:0 12px 12px 0;'>
            <div style='font-size:0.9rem; color:var(--muted); font-weight:600; margin-bottom:0.3rem;'>📊 CLASSIFICATION SUMMARY</div>
            <div style='font-size:1.05rem;'>{summary_msg}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Patient Summary Table ──
        st.markdown("<div class='section-title'>🗒️ Input Summary</div>", unsafe_allow_html=True)
        summary_data = {
            "Parameter": [
                "Age", "Sex", "Chest Pain", "Resting BP", "Cholesterol",
                "Fasting BS", "Resting ECG", "Max Heart Rate", "Exer. Angina",
                "Oldpeak", "ST Slope", "Vessels", "Thalassemia"
            ],
            "Value": [
                age, sex, cp, f"{trestbps} mmHg", f"{chol} mg/dl",
                fbs, restecg, thalch, exang,
                oldpeak, slope, ca, thal
            ]
        }
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True, hide_index=True)

    else:
        # ── Idle state ──
        _idle_heart = HEART_IMG.format(size="160px", extra="display:block; margin:0 auto 1rem; filter: drop-shadow(0 0 30px rgba(232,67,147,0.75));")
        st.markdown(f"""
        <div style='text-align:center; padding:4rem 2rem;'>
          <div class='heartbeat'>{_idle_heart}</div>
          <div style='font-family:"Space Grotesk",sans-serif; font-size:1.8rem;
                      font-weight:700; color:var(--text); margin-bottom:0.6rem;'>
            Ready to Analyze
          </div>
          <div style='color:var(--muted); font-size:1rem; max-width:420px; margin:0 auto;'>
            Complete the patient profile in the sidebar, then click
            <strong style='color:#e84393;'>Analyze Risk Now</strong> to get AI-powered insights.
          </div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# TAB 2 — FEATURE IMPORTANCE
# ════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-title'>📊 Feature Importance (XGBoost)</div>", unsafe_allow_html=True)

    importances = model.feature_importances_
    feat_series = pd.Series(importances, index=FEATURES).sort_values(ascending=True)

    # Matplotlib figure styled dynamically
    rcParams['font.family'] = 'DejaVu Sans'
    fig, ax = plt.subplots(figsize=(9, 5.5))
    fig.patch.set_facecolor(matplotlib_bg)
    ax.set_facecolor(matplotlib_bg)

    colors = []
    max_v = feat_series.max()
    for v in feat_series.values:
        t = v / max_v
        r = int(232 + (239 - 232) * t)
        g = int(67  + (68  - 67)  * (1 - t))
        b = int(147 + (68  - 147) * t)
        colors.append(f"#{r:02x}{g:02x}{b:02x}")

    bars = ax.barh(
        [FEATURE_LABELS.get(f, f) for f in feat_series.index],
        feat_series.values,
        color=colors,
        height=0.65,
        edgecolor='none'
    )

    # Value labels
    for bar, val in zip(bars, feat_series.values):
        ax.text(val + 0.002, bar.get_y() + bar.get_height() / 2,
                f"{val:.3f}", va='center', ha='left',
                color=matplotlib_muted, fontsize=8.5)

    ax.set_xlabel("Importance Score", color=matplotlib_muted, fontsize=10)
    ax.set_title("XGBoost Feature Importances", color=matplotlib_text,
                 fontsize=13, fontweight='bold', pad=14)
    ax.tick_params(colors=matplotlib_muted, labelsize=9)
    ax.spines[:].set_visible(False)
    ax.xaxis.grid(True, color=matplotlib_text, alpha=0.06, linewidth=0.8)
    ax.set_axisbelow(True)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    # ── Top-3 Callout ──
    top3 = pd.Series(importances, index=FEATURES).sort_values(ascending=False).head(3)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🏆 Top 3 Predictors</div>", unsafe_allow_html=True)
    medals = ["🥇", "🥈", "🥉"]
    cols = st.columns(3)
    for i, (feat, score) in enumerate(top3.items()):
        with cols[i]:
            st.markdown(f"""
            <div style='background:var(--card2); border:1px solid var(--border);
                        border-radius:16px; padding:1.2rem; text-align:center;'>
              <div style='font-size:2rem;'>{medals[i]}</div>
              <div style='font-family:"Space Grotesk",sans-serif; font-size:1rem;
                          font-weight:700; color:var(--text); margin:0.4rem 0 0.2rem;'>
                {FEATURE_LABELS.get(feat, feat)}
              </div>
              <div style='font-size:1.5rem; font-weight:800;
                          background:linear-gradient(135deg,#e84393,#a855f7);
                          -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                          background-clip:text;'>
                {score:.3f}
              </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# TAB 3 — ABOUT
# ════════════════════════════════════════════════════════════
with tab3:
    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown("""
        <div style='padding:0.5rem 0;'>
          <div style='font-family:"Space Grotesk",sans-serif; font-size:1.7rem;
                      font-weight:800; color:var(--text); margin-bottom:1rem;'>
            About CardioSense AI
          </div>
          <p style='color:var(--muted); line-height:1.8; font-size:0.97rem;'>
            <strong style='color:var(--text);'>CardioSense AI</strong> is a machine-learning powered
            clinical decision support tool for heart disease risk assessment. It leverages the
            <strong style='color:#e84393;'>Cleveland Heart Disease Dataset</strong> — one of
            the most widely used benchmarks in cardiovascular research.
          </p>
          <p style='color:var(--muted); line-height:1.8; font-size:0.97rem;'>
            The model was built using <strong style='color:#a855f7;'>XGBoost</strong> with
            careful hyperparameter tuning, validated via
            <strong style='color:#22d3ee;'>10-Fold Stratified Cross-Validation</strong>
            to ensure robustness and generalizability.
          </p>

          <div style='margin-top:1.5rem;'>
            <div class='section-title'>⚙️ Model Configuration</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        config = {
            "Algorithm":       "XGBoost (XGBClassifier)",
            "n_estimators":    "300",
            "max_depth":       "4",
            "learning_rate":   "0.05",
            "subsample":       "0.85",
            "colsample_bytree":"0.85",
            "scale_pos_weight":"1.1",
            "eval_metric":     "AUCPR",
            "Validation":      "10-Fold Stratified CV",
            "Imputation":      "Median (SimpleImputer)",
        }
        df_cfg = pd.DataFrame(config.items(), columns=["Parameter", "Value"])
        st.dataframe(df_cfg, use_container_width=True, hide_index=True)

    with col_b:
        st.markdown("""
        <div style='background:var(--card2); border:1px solid var(--border);
                    border-radius:20px; padding:1.8rem;'>
          <div style='font-family:"Space Grotesk",sans-serif; font-size:1.1rem;
                      font-weight:700; color:var(--text); margin-bottom:1.2rem;'>
            📋 13 Clinical Features
          </div>
        """, unsafe_allow_html=True)

        for feat, label in FEATURE_LABELS.items():
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:10px; margin-bottom:8px;'>
              <div style='width:8px; height:8px; border-radius:50%;
                          background:linear-gradient(135deg,#e84393,#a855f7);
                          flex-shrink:0;'></div>
              <span style='color:var(--muted); font-size:0.87rem;'>{label}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style='background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3);
                    border-radius:16px; padding:1.2rem; margin-top:1rem;'>
          <div style='font-weight:700; color:#ef4444; margin-bottom:0.4rem;'>
            ⚠️ Medical Disclaimer
          </div>
          <div style='color:var(--muted); font-size:0.85rem; line-height:1.6;'>
            This tool is for <em>educational and research purposes only</em>.
            It is <strong>not</strong> a substitute for professional medical advice,
            diagnosis, or treatment. Always consult a qualified cardiologist.
          </div>
        </div>
        """, unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:var(--muted); font-size:0.82rem; padding:0.8rem 0;'>
  CardioSense AI &nbsp;·&nbsp; Built with ❤️ using XGBoost + Streamlit
  &nbsp;·&nbsp; Cleveland Heart Disease Dataset
</div>
""", unsafe_allow_html=True)
