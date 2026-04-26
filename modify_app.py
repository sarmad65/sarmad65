import os

file_path = r"c:\Users\Admin\Desktop\mymodel\app.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update set_page_config
content = content.replace("""st.set_page_config(
    page_title="CardioSense AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded",
)""", """if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CardioSense AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state=st.session_state.sidebar_state,
)""")

# 2. Add sidebar toggles
sidebar_orig = """with st.sidebar:
    st.markdown(f\"\"\"
    <div style='text-align:center; margin-bottom:1.5rem;'>"""

sidebar_new = """with st.sidebar:
    # ── Theme and Sidebar Toggles ──
    st.markdown("<div class='section-title'>⚙️ App Settings</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        is_light = st.toggle("🌞 Light Mode", value=(st.session_state.theme == "Light"))
        new_theme = "Light" if is_light else "Dark"
        if new_theme != st.session_state.theme:
            st.session_state.theme = new_theme
            st.rerun()
    with c2:
        if st.button("↕️ Toggle Sidebar", use_container_width=True):
            st.session_state.sidebar_state = "collapsed" if st.session_state.sidebar_state == "expanded" else "expanded"
            st.rerun()

    st.markdown("---")

    st.markdown(f\"\"\"
    <div style='text-align:center; margin-bottom:1.5rem;'>"""

content = content.replace(sidebar_orig, sidebar_new)

# 3. Replace CSS Block
css_start = content.find("st.markdown(\"\"\"\n<style>")
css_end = content.find("</style>\n\"\"\", unsafe_allow_html=True)") + len("</style>\n\"\"\", unsafe_allow_html=True)")

if css_start != -1 and css_end != -1:
    css_dynamic = """# ─── Global CSS / Fonts / Animations ─────────────────────────────────────────
if st.session_state.theme == "Dark":
    theme_vars = \"\"\"
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
    \"\"\"
    matplotlib_bg = '#131627'
    matplotlib_text = '#e2e8f0'
    matplotlib_muted = '#94a3b8'
else:
    theme_vars = \"\"\"
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
    \"\"\"
    matplotlib_bg = '#ffffff'
    matplotlib_text = '#0f172a'
    matplotlib_muted = '#64748b'

css_string = f\"\"\"
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ── Root palette ── */
:root {{
{theme_vars}
}}

/* ── Base ── */
html, body, [class*="css"] {{
    font-family: 'Outfit', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}}

/* Hide default Streamlit chrome */
#MainMenu, footer, header {{ visibility: hidden; }}

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

/* ── Divider ── */
hr {{ border-color: var(--border) !important; }}
</style>
\"\"\"
st.markdown(css_string, unsafe_allow_html=True)"""
    
    # Replace the markdown block with dynamic one
    # Note: we need to replace the exact CSS block. It starts with st.markdown and ends with unsafe_allow_html=True
    # However we need to find exactly # ─── Global CSS / Fonts / Animations ─────────────────────────────────────────
    css_start_idx = content.find("# ─── Global CSS / Fonts / Animations ─────────────────────────────────────────\n")
    if css_start_idx != -1:
        # The CSS section is from css_start_idx to css_end
        content = content[:css_start_idx] + css_dynamic + content[css_end:]

# 4. Matplotlib fixes
content = content.replace("fig.patch.set_facecolor('#131627')", "fig.patch.set_facecolor(matplotlib_bg)")
content = content.replace("ax.set_facecolor('#131627')", "ax.set_facecolor(matplotlib_bg)")
content = content.replace("color='#94a3b8'", "color=matplotlib_muted")
content = content.replace("colors='#94a3b8'", "colors=matplotlib_muted")
content = content.replace("color='#e2e8f0'", "color=matplotlib_text")
content = content.replace("ax.xaxis.grid(True, color=(1, 1, 1, 0.06), linewidth=0.8)", "ax.xaxis.grid(True, color=matplotlib_text, alpha=0.06, linewidth=0.8)")

# 5. HTML style fixes using f-strings and CSS vars
content = content.replace("color:#e2e8f0;", "color:var(--text);")
content = content.replace("color:#94a3b8;", "color:var(--muted);")
content = content.replace("color:#475569;", "color:var(--muted);")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
