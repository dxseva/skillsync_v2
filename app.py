"""
SkillSync Pro v2 — AI Career Guide for Students & Graduates
Conversational flow: goal → clarifying questions → job matches → roadmap
"""
import streamlit as st
import sys, os

# Ensure src is importable from app dir
sys.path.insert(0, os.path.dirname(__file__))

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SkillSync Pro",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #0b0f1a;
    color: #e8eaf0;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
}

.main .block-container {
    max-width: 780px;
    padding: 2rem 1.5rem 4rem;
}

/* Header */
.ss-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.ss-header h1 {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6ee7f7 0%, #a78bfa 60%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    letter-spacing: -1px;
}
.ss-header p {
    color: #8b92a8;
    font-size: 1.05rem;
    margin-top: 0.5rem;
}

/* Step badges */
.step-badge {
    display: inline-block;
    background: linear-gradient(135deg, #6ee7f7, #a78bfa);
    color: #0b0f1a;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.75rem;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.5px;
    margin-bottom: 0.75rem;
}

/* Cards */
.job-card {
    background: #151b2e;
    border: 1px solid #252d44;
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
    position: relative;
}
.job-card:hover {
    border-color: #a78bfa;
}
.job-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e8eaf0;
    margin: 0 0 0.25rem;
}
.job-card-meta {
    font-size: 0.82rem;
    color: #6b7591;
    margin-bottom: 0.6rem;
}
.job-card-snippet {
    font-size: 0.88rem;
    color: #a0a9c0;
    line-height: 1.5;
}
.score-badge {
    position: absolute;
    top: 1.25rem;
    right: 1.25rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    padding: 3px 12px;
    border-radius: 20px;
    color: #0b0f1a;
}
.score-high { background: #4ade80; }
.score-mid  { background: #facc15; }
.score-low  { background: #f87171; }

/* Progress bar (match %) */
.match-bar-wrap {
    margin: 0.4rem 0;
}
.match-bar-bg {
    background: #252d44;
    border-radius: 8px;
    height: 7px;
    width: 100%;
}
.match-bar-fill {
    border-radius: 8px;
    height: 7px;
    background: linear-gradient(90deg, #6ee7f7, #a78bfa);
}

/* Roadmap steps */
.road-step {
    background: #151b2e;
    border-left: 3px solid #a78bfa;
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.25rem;
    margin-bottom: 0.8rem;
}
.road-step-skill {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: #e8eaf0;
}
.road-step-time {
    display: inline-block;
    background: #1e2840;
    color: #a78bfa;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 10px;
    margin-left: 0.5rem;
}
.road-step-status-learn  { color: #f87171; font-size: 0.78rem; font-weight: 600; }
.road-step-status-improve { color: #facc15; font-size: 0.78rem; font-weight: 600; }
.road-step-body {
    font-size: 0.87rem;
    color: #a0a9c0;
    margin-top: 0.4rem;
    line-height: 1.55;
}
.road-step-resources {
    font-size: 0.8rem;
    color: #5a6278;
    margin-top: 0.3rem;
}

/* Already strong */
.strong-chip {
    display: inline-block;
    background: #162e20;
    color: #4ade80;
    border: 1px solid #2d5a3a;
    font-size: 0.8rem;
    padding: 3px 10px;
    border-radius: 20px;
    margin: 3px;
}

/* Info box */
.info-box {
    background: #111827;
    border: 1px solid #1e2840;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    font-size: 0.88rem;
    color: #8b92a8;
    margin: 1rem 0;
}

/* Streamlit button override */
.stButton > button {
    background: linear-gradient(135deg, #a78bfa, #6ee7f7);
    color: #0b0f1a;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 0.55rem 1.5rem;
    font-size: 0.92rem;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.88; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input {
    background: #151b2e !important;
    border: 1px solid #252d44 !important;
    color: #e8eaf0 !important;
    border-radius: 10px !important;
}

.stCheckbox > label { color: #a0a9c0 !important; }

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Divider */
.divider {
    border: none;
    border-top: 1px solid #1e2840;
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ss-header">
  <h1>SkillSync Pro</h1>
  <p>AI Career Guide for Students & Graduates — powered by live HH.ru data</p>
</div>
""", unsafe_allow_html=True)

# ─── Session state init ──────────────────────────────────────────────────────
def _init():
    defaults = {
        "step": "goal",          # goal → profile → results → roadmap
        "goal": "",
        "profile": {},
        "jobs": [],
        "recommendations": [],
        "selected_job": None,
        "roadmap": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()

# ─── STEP 1: Career goal ─────────────────────────────────────────────────────
if st.session_state.step == "goal":
    st.markdown('<div class="step-badge">STEP 1 OF 4 — YOUR GOAL</div>', unsafe_allow_html=True)
    st.markdown("### 👋 What career are you aiming for?")
    st.markdown('<div class="info-box">Tell me in plain English — a role, a field, or even just a dream. Examples:<br><em>"I want to become a lawyer"</em> · <em>"data analyst"</em> · <em>"UX designer"</em> · <em>"I love psychology and want to work with people"</em></div>', unsafe_allow_html=True)

    goal = st.text_input(
        "Your career goal or interest",
        placeholder="e.g. I want to become a lawyer, or I'm interested in data science...",
        label_visibility="collapsed",
        key="goal_input",
    )

    if st.button("Continue →", key="btn_goal") and goal.strip():
        st.session_state.goal = goal.strip()
        st.session_state.step = "profile"
        st.rerun()

# ─── STEP 2: Clarifying profile ──────────────────────────────────────────────
elif st.session_state.step == "profile":
    st.markdown('<div class="step-badge">STEP 2 OF 4 — YOUR PROFILE</div>', unsafe_allow_html=True)
    st.markdown(f"### 🎓 Tell me a bit more about yourself")
    st.markdown(f'<div class="info-box">Goal: <strong>{st.session_state.goal}</strong><br>A few quick questions to find the best-matching vacancies for you.</div>', unsafe_allow_html=True)

    from src.config import CITY_AREA_IDS

    with st.form("profile_form"):
        skills = st.text_area(
            "What relevant skills or experience do you already have?",
            placeholder="e.g. Completed law courses, did internship at a local firm, know Excel and Word, speak English B2...",
            height=100,
        )
        skill_level = st.select_slider(
            "Your overall skill level",
            options=["beginner", "intermediate", "advanced"],
            value="intermediate",
        )
        year = st.selectbox(
            "Your current study status",
            options=[0, 1, 2, 3, 4, 5, 6],
            format_func=lambda y: "Recent graduate / already graduated" if y == 0 else f"Year {y} student",
            index=3,
        )
        city = st.selectbox(
            "Preferred city",
            options=list(CITY_AREA_IDS.keys()),
            index=0,
        )
        fmt = st.selectbox(
            "Preferred work format",
            options=["any", "remote", "office", "hybrid"],
            format_func=lambda x: {"any": "Any format", "remote": "Remote only", "office": "Office only", "hybrid": "Hybrid"}[x],
        )
        relocation = st.checkbox("I'm willing to relocate")

        submitted = st.form_submit_button("Find matching vacancies →")

    if submitted:
        st.session_state.profile = {
            "skills": skills,
            "skill_level": skill_level,
            "year": year,
            "city": city,
            "format": fmt,
            "relocation": relocation,
        }
        st.session_state.step = "results"
        st.rerun()

    if st.button("← Back", key="btn_back_profile"):
        st.session_state.step = "goal"
        st.rerun()

# ─── STEP 3: Results ─────────────────────────────────────────────────────────
elif st.session_state.step == "results":
    st.markdown('<div class="step-badge">STEP 3 OF 4 — MATCHING VACANCIES</div>', unsafe_allow_html=True)

    # Fetch + score jobs if not done yet
    if not st.session_state.recommendations:
        from src.fetcher import fetch_live_jobs, HHApiError
        from src.recommender import get_recommendations

        raw_jobs = []
        try:
            with st.spinner("🔍 Searching HH.ru for relevant vacancies..."):
                raw_jobs = fetch_live_jobs(st.session_state.goal, st.session_state.profile)
        except HHApiError as e:
            st.error(f"❌ **Could not reach HH.ru:**\n\n{e}")
            st.info("**Common causes:**\n- No internet connection\n- HH.ru is temporarily down\n- A firewall/VPN is blocking the request\n\nTry opening https://api.hh.ru/vacancies in your browser — if it loads, just click Try Again below.")
            if st.button("← Try again"):
                st.session_state.step = "profile"
                st.rerun()
            st.stop()

        if not raw_jobs:
            st.error("❌ HH.ru responded but returned 0 vacancies for your goal and filters.")
            st.info("Try: broadening your goal (e.g. 'lawyer' instead of 'tax lawyer'), removing the city filter, or changing work format to 'Any'.")
            if st.button("← Adjust filters"):
                st.session_state.recommendations = []
                st.session_state.step = "profile"
                st.rerun()
            st.stop()

        with st.spinner(f"🧠 Ranking {len(raw_jobs)} vacancies by semantic match — this may take ~30s on first run (loading models)..."):
            recs = get_recommendations(
                raw_jobs,
                st.session_state.goal,
                st.session_state.profile,
            )

        if not recs:
            st.error("Could not find strong matches. Try adjusting your filters.")
            if st.button("← Back"):
                st.session_state.step = "profile"
                st.rerun()
            st.stop()

        # Auto-translate Russian snippets to English for display (#3)
        from src.translator import translate_ru_to_en
        with st.spinner("🌐 Translating job descriptions to English..."):
            for rec in recs:
                req = rec.get("requirement", "")
                resp = rec.get("responsibility", "")
                snippet_ru = (req + " " + resp).strip()
                rec["snippet_en"] = translate_ru_to_en(snippet_ru) if snippet_ru else ""

        st.session_state.recommendations = recs

    recs = st.session_state.recommendations

    st.markdown(f"### 🏆 Top {len(recs)} Vacancies for You")
    st.markdown(f'<div class="info-box">Goal: <strong>{st.session_state.goal}</strong> · Found <strong>{len(recs)}</strong> best matches from live HH.ru data · Ranked by semantic similarity</div>', unsafe_allow_html=True)

    # Display job cards
    for i, job in enumerate(recs, 1):
        score = job["match_score"]
        score_cls = "score-high" if score >= 70 else ("score-mid" if score >= 50 else "score-low")
        bar_w = min(int(score), 100)

        snippet = job.get("snippet_en", "")
        if not snippet:
            req = job.get("requirement", "")
            resp = job.get("responsibility", "")
            snippet = (req + " " + resp).strip()
        snippet_display = snippet[:250] + ("..." if len(snippet) > 250 else "")

        salary = job.get("salary")
        salary_str = ""
        if salary:
            frm = salary.get("from")
            to = salary.get("to")
            currency = salary.get("currency", "RUB")
            if frm and to:
                salary_str = f"💰 {frm:,}–{to:,} {currency}"
            elif frm:
                salary_str = f"💰 from {frm:,} {currency}"
            elif to:
                salary_str = f"💰 up to {to:,} {currency}"

        area = job.get("area", "")
        sched = job.get("schedule", "")
        exp = job.get("experience", "")

        st.markdown(f"""
<div class="job-card">
  <div class="score-badge {score_cls}">{score}%</div>
  <div class="job-card-title">{i}. {job.get('name', 'Vacancy')}</div>
  <div class="job-card-meta">{job.get('employer_en') or job.get('employer', '')} · {area} · {sched} · {exp} {salary_str}</div>
  <div class="match-bar-wrap">
    <div class="match-bar-bg"><div class="match-bar-fill" style="width:{bar_w}%"></div></div>
  </div>
  <div class="job-card-snippet">{snippet_display or "No description available."}</div>
  <div style="margin-top:0.6rem"><a href="{job.get('url','#')}" target="_blank" style="color:#6ee7f7;font-size:0.82rem;text-decoration:none;">🔗 View full vacancy on HH.ru →</a></div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown("### 🗺️ Build your personal roadmap")
    st.markdown("Choose the vacancy that interests you most, and I'll create a step-by-step learning plan to help you get there.")

    choice = st.selectbox(
        "Select a vacancy to build roadmap for:",
        options=list(range(1, len(recs) + 1)),
        format_func=lambda i: f"{i}. {recs[i-1].get('name','')} — {recs[i-1]['match_score']}% match",
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Build My Roadmap →", key="btn_roadmap"):
            st.session_state.selected_job = recs[choice - 1]
            st.session_state.roadmap = None  # reset
            st.session_state.step = "roadmap"
            st.rerun()
    with col2:
        if st.button("🔄 Search again", key="btn_search_again"):
            st.session_state.recommendations = []
            st.session_state.step = "profile"
            st.rerun()

# ─── STEP 4: Roadmap ─────────────────────────────────────────────────────────
elif st.session_state.step == "roadmap":
    st.markdown('<div class="step-badge">STEP 4 OF 4 — YOUR PERSONAL ROADMAP</div>', unsafe_allow_html=True)

    job = st.session_state.selected_job

    # Generate roadmap if not cached
    if st.session_state.roadmap is None:
        from src.roadmap import generate_roadmap
        from src.fetcher import fetch_vacancy_details

        # Fetch structured key_skills from HH API (#14)
        key_skills = []
        with st.spinner("🔑 Fetching structured skills from HH.ru..."):
            try:
                details = fetch_vacancy_details(job.get("id", ""))
                key_skills = details.get("key_skills", [])
            except Exception:
                pass  # fallback to text-based extraction

        with st.spinner("🧩 Analyzing skill gaps and building your roadmap..."):
            roadmap = generate_roadmap(
                job,
                st.session_state.profile.get("skills", ""),
                key_skills=key_skills if key_skills else None,
                skill_level=st.session_state.profile.get("skill_level", "intermediate"),
            )
        st.session_state.roadmap = roadmap

    r = st.session_state.roadmap

    st.markdown(f"### 🎯 Roadmap to: {r['job_title']}")
    st.markdown(f'<div class="info-box">Current match: <strong>{job["match_score"]}%</strong> · After completing roadmap: <strong>{r["match_after_preparation"]}</strong><br>⏱ {r["total_estimated_time"]}</div>', unsafe_allow_html=True)

    # Already strong
    if r.get("already_strong"):
        st.markdown("#### ✅ Skills you already have")
        chips = "".join(f'<span class="strong-chip">✓ {s}</span>' for s in r["already_strong"])
        st.markdown(f'<div style="margin-bottom:1rem">{chips}</div>', unsafe_allow_html=True)

    # Skills to develop
    if r.get("roadmap_steps"):
        st.markdown("#### 📚 Skills to develop")
        for step in r["roadmap_steps"]:
            status_cls = "road-step-status-improve" if step["status"] == "Improve" else "road-step-status-learn"
            status_icon = "🟡" if step["status"] == "Improve" else "🔴"

            st.markdown(f"""
<div class="road-step">
  <div>
    <span class="road-step-skill">{step['skill']}</span>
    <span class="road-step-time">{step['estimated_time']}</span>
    <span class="{status_cls}" style="margin-left:0.5rem">{status_icon} {step['status']} · {step['level']} level · current match: {step['current_match_pct']}%</span>
  </div>
  <div class="road-step-body">{step['suggested_actions']}</div>
  <div class="road-step-resources">📖 Resources: {step['resources']}</div>
</div>
""", unsafe_allow_html=True)

        st.markdown(f'<div class="info-box" style="margin-top:1.5rem">💡 <strong>Note:</strong> {r["notes"]}</div>', unsafe_allow_html=True)
    else:
        st.success("🎉 You look like a strong candidate already! Focus on polishing your CV, practicing interviews, and networking. Apply now!")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("← Choose different vacancy", key="btn_back_results"):
            st.session_state.roadmap = None
            st.session_state.step = "results"
            st.rerun()
    with col2:
        if st.button("🔄 New search", key="btn_new_search"):
            for k in ["goal", "profile", "jobs", "recommendations", "selected_job", "roadmap"]:
                st.session_state[k] = [] if k in ["jobs", "recommendations"] else ({} if k == "profile" else (None if k in ["selected_job", "roadmap"] else ""))
            st.session_state.step = "goal"
            st.rerun()
    with col3:
        if st.button("🔄 Regenerate roadmap", key="btn_regen"):
            st.session_state.roadmap = None
            st.rerun()
