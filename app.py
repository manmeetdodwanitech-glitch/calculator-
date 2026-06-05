import streamlit as st
import requests

# ── Page Config ────────────────────────────────────────
st.set_page_config(
    page_title="GRADE-X",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Styling ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

.stApp { background: #04040d; }

section[data-testid="stSidebar"] {
    background: #080818 !important;
    border-right: 1px solid #1a1a35;
}

html, body, [class*="css"] {
    font-family: 'Share Tech Mono', monospace !important;
    color: #dde0ff;
}

/* Animated grid */
.stApp::before {
    content:'';
    position:fixed; inset:0;
    background-image:
        linear-gradient(rgba(0,255,159,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,159,0.02) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events:none; z-index:0;
    animation: gridMove 25s linear infinite;
}
@keyframes gridMove { from{background-position:0 0} to{background-position:40px 40px} }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; }

/* Inputs */
.stTextInput input, .stNumberInput input {
    background: #0c0c20 !important;
    border: 1px solid #1a1a35 !important;
    color: #dde0ff !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 4px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #00aaff !important;
    box-shadow: 0 0 0 2px rgba(0,170,255,0.12) !important;
}

/* Labels */
.stTextInput label, .stNumberInput label {
    color: #444466 !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, rgba(0,255,159,0.08), rgba(0,170,255,0.08)) !important;
    border: 1px solid #00ff9f !important;
    color: #00ff9f !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    border-radius: 6px !important;
}
.stButton > button:hover {
    box-shadow: 0 0 20px rgba(0,255,159,0.25) !important;
    border-color: #00ff9f !important;
}

/* Secondary button */
.stButton > button[kind="secondary"] {
    border-color: #1a1a35 !important;
    color: #444466 !important;
    background: none !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #ff4455 !important;
    color: #ff4455 !important;
    box-shadow: none !important;
}

/* Metrics */
[data-testid="metric-container"] {
    background: #0c0c20 !important;
    border: 1px solid #1a1a35 !important;
    border-radius: 8px !important;
    padding: 14px !important;
}
[data-testid="stMetricValue"] { color: #dde0ff !important; font-family: 'Orbitron', monospace !important; }
[data-testid="stMetricLabel"] { color: #444466 !important; font-size: 11px !important; }

/* Progress */
.stProgress > div > div { background: linear-gradient(90deg, #00ff9f, #00aaff) !important; }
.stProgress > div { background: #1a1a35 !important; }

/* Alerts */
.stSuccess { background: rgba(0,255,159,0.07) !important; border-left: 3px solid #00ff9f !important; color: #00ff9f !important; }
.stError   { background: rgba(255,68,85,0.07)  !important; border-left: 3px solid #ff4455 !important; color: #ff4455 !important; }
.stWarning { background: rgba(255,200,0,0.07)  !important; border-left: 3px solid #ffcc00 !important; }
.stInfo    { background: rgba(0,170,255,0.07)  !important; border-left: 3px solid #00aaff !important; }

/* Expander */
.streamlit-expanderHeader {
    background: #0c0c20 !important;
    border: 1px solid #1a1a35 !important;
    color: #dde0ff !important;
}
.streamlit-expanderContent { background: #080818 !important; border: 1px solid #1a1a35 !important; }

/* Divider */
hr { border-color: #1a1a35 !important; }

/* Custom cards */
.grade-card {
    background: #0c0c20;
    border: 1px solid #1a1a35;
    border-radius: 12px;
    padding: 28px 20px;
    text-align: center;
    margin: 12px 0;
}
.grade-letter {
    font-family: 'Orbitron', monospace;
    font-size: 88px;
    font-weight: 900;
    line-height: 1;
    margin-bottom: 10px;
}
.subj-row {
    background: #080818;
    border-radius: 6px;
    padding: 12px 16px;
    margin: 6px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-left: 3px solid #1a1a35;
    font-size: 13px;
}
.hist-card {
    background: #080818;
    border: 1px solid #1a1a35;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# ── API Config ─────────────────────────────────────────
API_URL = "http://localhost:5000/api"

# ── API Functions ──────────────────────────────────────
def api_health():
    try:
        r = requests.get(f"{API_URL}/health", timeout=2)
        return r.status_code == 200
    except:
        return False

def api_calculate(name, subjects):
    try:
        r = requests.post(f"{API_URL}/grade",
            json={"name": name, "subjects": subjects}, timeout=5)
        data = r.json()
        return data["result"] if data["success"] else None, data.get("error")
    except Exception as e:
        return None, str(e)

def api_get_history():
    try:
        r = requests.get(f"{API_URL}/history", timeout=3)
        return r.json().get("history", [])
    except:
        return []

def api_clear_history():
    try:
        requests.post(f"{API_URL}/clear", timeout=3)
        return True
    except:
        return False

def api_grades_info():
    try:
        r = requests.get(f"{API_URL}/grades-info", timeout=2)
        return r.json().get("grades", [])
    except:
        return []

# ── Session State ──────────────────────────────────────
if "subjects" not in st.session_state:
    st.session_state.subjects = [
        {"name": "Mathematics", "marks": 85.0},
        {"name": "Physics",     "marks": 78.0},
        {"name": "Chemistry",   "marks": 92.0},
    ]
if "result" not in st.session_state:
    st.session_state.result = None
if "api_online" not in st.session_state:
    st.session_state.api_online = False

# Check API
st.session_state.api_online = api_health()

# ── SIDEBAR ────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="text-align:center;padding:16px 0 8px;">
        <div style="font-family:Orbitron,monospace;font-size:26px;font-weight:900;
            background:linear-gradient(90deg,#00ff9f,#00aaff,#aa44ff);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            background-clip:text;letter-spacing:4px;">GRADE-X</div>
        <div style="color:#444466;font-size:10px;letter-spacing:3px;margin-top:4px;">
            ACADEMIC INTELLIGENCE
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # API Status
    st.markdown('<p style="color:#444466;font-size:10px;letter-spacing:3px;">// BACKEND STATUS</p>', unsafe_allow_html=True)
    if st.session_state.api_online:
        st.success("🟢 API CONNECTED\nlocalhost:5000")
    else:
        st.warning("🔴 API OFFLINE\nRun: python api.py")

    if st.button("↻ REFRESH", key="refresh_api"):
        st.rerun()

    st.divider()

    # Grade Scale from API or default
    st.markdown('<p style="color:#444466;font-size:10px;letter-spacing:3px;">// GRADE SCALE</p>', unsafe_allow_html=True)

    grade_scale = api_grades_info() if st.session_state.api_online else [
        {"grade": "A+", "min": 90, "max": 100, "remark": "Outstanding",   "color": "#00ff9f"},
        {"grade": "A",  "min": 80, "max": 89,  "remark": "Excellent",     "color": "#44ddff"},
        {"grade": "B",  "min": 70, "max": 79,  "remark": "Good",          "color": "#aaaaff"},
        {"grade": "C",  "min": 60, "max": 69,  "remark": "Average",       "color": "#ffdd44"},
        {"grade": "D",  "min": 50, "max": 59,  "remark": "Below Average", "color": "#ff9944"},
        {"grade": "E",  "min": 40, "max": 49,  "remark": "Poor",          "color": "#ff6644"},
        {"grade": "F",  "min": 0,  "max": 39,  "remark": "Fail",          "color": "#ff4455"},
    ]

    for g in grade_scale:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;
            padding:7px 0;border-bottom:1px solid #1a1a35;">
            <span style="font-family:Orbitron,monospace;font-size:17px;
                font-weight:900;color:{g['color']};width:26px;">{g['grade']}</span>
            <span style="color:#444466;font-size:11px;width:52px;">
                {g['min']}-{g['max']}</span>
            <span style="color:{g['color']};font-size:10px;letter-spacing:1px;">
                {g['remark'].upper()}</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # History
    st.markdown('<p style="color:#444466;font-size:10px;letter-spacing:3px;">// PAST RESULTS</p>', unsafe_allow_html=True)

    hist = api_get_history() if st.session_state.api_online else []

    if not hist:
        st.markdown('<p style="color:#1a1a35;font-size:12px;text-align:center;padding:16px 0;">No history yet</p>', unsafe_allow_html=True)
    else:
        for h in hist[:6]:
            c = h.get("overall_color", "#00ff9f")
            with st.expander(f"{h['name']}  {h['overall_grade']}  {h['average']}%"):
                st.markdown(f"""
                <div style="text-align:center;padding:8px 0;">
                    <div style="font-family:Orbitron,monospace;font-size:36px;
                        font-weight:900;color:{c};text-shadow:0 0 20px {c}88;">
                        {h['overall_grade']}</div>
                    <div style="color:#dde0ff;margin:4px 0;">{h['average']}%</div>
                    <div style="color:{c};font-size:11px;letter-spacing:2px;">
                        {h['overall_remark'].upper()}</div>
                    <div style="color:#444466;font-size:10px;margin-top:6px;">
                        {h.get('time','')}</div>
                </div>
                """, unsafe_allow_html=True)
                for s in h.get("subjects", []):
                    st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;
                        padding:4px 0;border-bottom:1px solid #1a1a35;font-size:12px;">
                        <span>{s['subject']}</span>
                        <span style="color:{s['color']};font-family:Orbitron,monospace;">
                            {s['grade']}</span>
                        <span style="color:#444466;">{s['marks']}</span>
                    </div>
                    """, unsafe_allow_html=True)

        if st.button("🗑  CLEAR HISTORY", key="clear_hist"):
            api_clear_history()
            st.rerun()

# ── MAIN PAGE ──────────────────────────────────────────

# Header
st.markdown("""
<div style="text-align:center;padding:16px 0 8px;">
    <div style="font-family:Orbitron,monospace;font-size:38px;font-weight:900;
        background:linear-gradient(90deg,#00ff9f,#00aaff,#aa44ff);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-clip:text;letter-spacing:6px;margin-bottom:6px;">
        GRADE-X
    </div>
    <div style="color:#444466;font-size:11px;letter-spacing:4px;">
        // ACADEMIC GRADE CALCULATOR
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

left, right = st.columns([1.1, 1], gap="large")

# ── LEFT: INPUT ────────────────────────────────────────
with left:
    st.markdown('<p style="color:#444466;font-size:10px;letter-spacing:3px;margin-bottom:4px;">// STUDENT NAME</p>', unsafe_allow_html=True)
    student_name = st.text_input("name", placeholder="Enter student name...",
        label_visibility="collapsed")
    if not student_name.strip():
        student_name = "Student"

    st.markdown('<p style="color:#444466;font-size:10px;letter-spacing:3px;margin:16px 0 4px;">// SUBJECTS & MARKS (out of 100)</p>', unsafe_allow_html=True)

    # Column headers
    h1, h2, h3 = st.columns([2.2, 1.2, 0.5])
    with h1: st.markdown('<p style="color:#1a1a35;font-size:10px;letter-spacing:2px;">SUBJECT</p>', unsafe_allow_html=True)
    with h2: st.markdown('<p style="color:#1a1a35;font-size:10px;letter-spacing:2px;">MARKS</p>', unsafe_allow_html=True)
    with h3: st.markdown('<p style="color:#1a1a35;font-size:10px;"> </p>', unsafe_allow_html=True)

    # Subject rows
    kept = []
    for i, subj in enumerate(st.session_state.subjects):
        c1, c2, c3 = st.columns([2.2, 1.2, 0.5])
        with c1:
            sname = st.text_input(f"s{i}", value=subj["name"],
                placeholder="Subject...", label_visibility="collapsed", key=f"sn_{i}")
        with c2:
            marks = st.number_input(f"m{i}", value=float(subj["marks"]),
                min_value=0.0, max_value=100.0, step=1.0,
                label_visibility="collapsed", key=f"mk_{i}")
        with c3:
            remove = st.button("✕", key=f"rm_{i}")
        if not remove:
            kept.append({"name": sname, "marks": marks})

    st.session_state.subjects = kept

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    b1, b2 = st.columns(2)
    with b1:
        if st.button("➕  ADD SUBJECT", use_container_width=True):
            st.session_state.subjects.append({
                "name": f"Subject {len(st.session_state.subjects)+1}",
                "marks": 0.0
            })
            st.rerun()
    with b2:
        calc = st.button("⚡  CALCULATE", use_container_width=True, type="primary")

    # Validate and calculate
    if calc:
        if not st.session_state.subjects:
            st.error("Please add at least one subject!")
        else:
            with st.spinner("Sending to API..."):
                if st.session_state.api_online:
                    result, err = api_calculate(student_name, st.session_state.subjects)
                    if result:
                        st.session_state.result = result
                        st.success("✅ Calculated via API!")
                    else:
                        st.error(f"API Error: {err}")
                else:
                    # Local fallback
                    def local_grade(m):
                        if m>=90: return ("A+","Outstanding","#00ff9f",10.0)
                        elif m>=80: return ("A","Excellent","#44ddff",9.0)
                        elif m>=70: return ("B","Good","#aaaaff",8.0)
                        elif m>=60: return ("C","Average","#ffdd44",7.0)
                        elif m>=50: return ("D","Below Average","#ff9944",6.0)
                        elif m>=40: return ("E","Poor","#ff6644",5.0)
                        else: return ("F","Fail","#ff4455",0.0)

                    results = []
                    total = 0
                    for s in st.session_state.subjects:
                        g,r,c,gpa = local_grade(s["marks"])
                        results.append({**s,"grade":g,"remark":r,"color":c,"gpa":gpa,"subject":s["name"]})
                        total += s["marks"]
                    avg = round(total/len(results), 2)
                    og,orr,oc,ogpa = local_grade(avg)
                    st.session_state.result = {
                        "name": student_name, "subjects": results,
                        "average": avg, "overall_grade": og,
                        "overall_remark": orr, "overall_color": oc,
                        "overall_gpa": ogpa
                    }
                    st.warning("⚠️ API offline — calculated locally")

# ── RIGHT: RESULT ──────────────────────────────────────
with right:
    st.markdown('<p style="color:#444466;font-size:10px;letter-spacing:3px;margin-bottom:4px;">// RESULT</p>', unsafe_allow_html=True)

    if st.session_state.result:
        r = st.session_state.result
        c = r["overall_color"]

        # Big grade card
        st.markdown(f"""
        <div class="grade-card" style="border-top:3px solid {c};">
            <div style="color:#444466;font-size:10px;letter-spacing:4px;margin-bottom:10px;">
                {r['name'].upper()}
            </div>
            <div class="grade-letter" style="color:{c};text-shadow:0 0 50px {c}66;">
                {r['overall_grade']}
            </div>
            <div style="font-family:Orbitron,monospace;font-size:30px;
                color:#dde0ff;margin-bottom:4px;">{r['average']}%</div>
            <div style="color:#444466;font-size:12px;letter-spacing:4px;
                margin-bottom:12px;">{r['overall_remark'].upper()}</div>
            <div style="display:inline-block;background:rgba(255,255,255,0.04);
                border:1px solid #1a1a35;border-radius:20px;padding:5px 18px;
                font-size:12px;letter-spacing:2px;">GPA: {r['overall_gpa']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Progress bar
        st.progress(int(r["average"]))

        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("AVERAGE",  f"{r['average']}%")
        m2.metric("GRADE",    r['overall_grade'])
        m3.metric("GPA",      r['overall_gpa'])

        st.markdown('<p style="color:#444466;font-size:10px;letter-spacing:3px;margin:12px 0 4px;">// SUBJECT BREAKDOWN</p>', unsafe_allow_html=True)

        for s in r["subjects"]:
            sc = s["color"]
            st.markdown(f"""
            <div class="subj-row" style="border-left-color:{sc};">
                <span style="flex:1;">{s['subject']}</span>
                <span style="color:#444466;margin:0 12px;">{s['marks']}/100</span>
                <span style="font-family:Orbitron,monospace;font-weight:700;
                    color:{sc};font-size:15px;margin:0 12px;">{s['grade']}</span>
                <span style="color:{sc};font-size:10px;letter-spacing:1px;">
                    {s['remark'].upper()}</span>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:#0c0c20;border:1px solid #1a1a35;border-radius:12px;
            padding:60px 20px;text-align:center;margin-top:4px;">
            <div style="font-size:52px;margin-bottom:16px;">🎓</div>
            <div style="color:#444466;font-size:12px;letter-spacing:3px;line-height:2.8;">
                ENTER MARKS<br>AND PRESS<br>⚡ CALCULATE
            </div>
        </div>
        """, unsafe_allow_html=True)
