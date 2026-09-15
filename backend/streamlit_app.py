import base64
import streamlit as st
import plotly.graph_objects as go
from collections import Counter
from app.services.report_service import ReportService

st.set_page_config(page_title="HireX", page_icon=None, layout="wide")


def get_base64_image(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None


hero_image_base64 = get_base64_image("assets/hero.jpg")

if hero_image_base64:
    hero_bg = f"url('data:image/jpeg;base64,{hero_image_base64}')"
else:
    hero_bg = "none"

st.markdown(f"""
<style>
    .main {{ background-color: #FAF8F5; }}
    .block-container {{ padding-top: 0rem; }}

    h1, h2, h3, h4, p, div, span, label {{ color: #3D3833; }}

    .header-band {{
        background-image: linear-gradient(135deg, rgba(61,56,51,0.35) 0%, rgba(61,56,51,0.25) 100%), {hero_bg};
        background-size: cover;
        background-position: center 50%;
        border-radius: 0 0 20px 20px;
        padding: 60px 40px 60px 40px;
        margin: 0 -1rem 28px -1rem;
        min-height: 240px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    .header-band h1 {{
        color: #FDF6EC !important;
        margin: 0 0 4px 0;
        font-weight: 800;
        font-size: 3.2rem;
        line-height: 1.1;
        text-shadow: 0 2px 12px rgba(0,0,0,0.6);
    }}
    .header-band p {{
        color: rgba(253,246,236,0.85) !important;
        margin: 0;
        font-size: 0.95rem;
        text-shadow: 0 2px 8px rgba(0,0,0,0.5);
    }}

    .metric-card {{
        background: #FFFFFF; border-radius: 14px; padding: 20px 24px;
        box-shadow: 0 1px 3px rgba(61,56,51,0.08); border: 1px solid #EDE7DF;
        border-top: 4px solid #D9D2C7;
        text-align: center;
    }}
    .metric-card-terracotta {{ border-top-color: #C4784F; }}
    .metric-card-sage {{ border-top-color: #7A8B6F; }}
    .metric-card-mustard {{ border-top-color: #C99A3B; }}
    .metric-card-rose {{ border-top-color: #B67373; }}

    .metric-value {{ font-size: 1.8rem; font-weight: 700; color: #3D3833; }}
    .metric-label {{ color: #8A8178; font-size: 0.85rem; margin-top: 4px; }}

    .candidate-card {{
        background: #FFFFFF; border-radius: 14px; padding: 20px 24px;
        margin-bottom: 16px; box-shadow: 0 1px 3px rgba(61,56,51,0.08);
        border: 1px solid #EDE7DF;
    }}
    .grade-badge {{
        display: inline-block; padding: 4px 14px; border-radius: 20px;
        font-weight: 600; font-size: 0.85rem; color: white !important;
    }}
    .grade-A {{ background-color: #7A8B6F; }}
    .grade-B {{ background-color: #6E8FA3; }}
    .grade-C {{ background-color: #C99A3B; }}
    .grade-D {{ background-color: #B15E4F; }}

    .skill-tag {{
        display: inline-block; background-color: #F3EFE8; color: #6B6357 !important;
        padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; margin: 2px 4px 2px 0;
    }}
    .skill-tag-missing {{ background-color: #F6E9E5; color: #A05A48 !important; }}
    .confidence-tag {{ font-size: 0.75rem; color: #8A8178 !important; font-weight: 500; }}

    /* Text area — matches page background exactly */
    textarea,
    div[data-testid="stTextArea"] textarea {{
        background-color: #FAF8F5 !important;
        color: #3D3833 !important;
        border: 1px solid #E5DED2 !important;
    }}

    /* Number input — matches page background exactly */
    input[type="number"],
    div[data-testid="stNumberInput"] input {{
        background-color: #FAF8F5 !important;
        color: #3D3833 !important;
        border: 1px solid #E5DED2 !important;
    }}

    /* Analyze button — mocha */
    div.stButton > button,
    div.stButton > button p,
    div.stButton > button span,
    div.stButton > button[kind="primary"] {{
        background-color: #8B6F5C !important;
        color: #FDF6EC !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }}
    div.stButton > button:hover {{
        background-color: #6F5847 !important;
        color: #FDF6EC !important;
    }}

    /* +/- buttons — same mocha as Analyze button */
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {{
        background-color: #8B6F5C !important;
        color: #FDF6EC !important;
        border: 1px solid #6F5847 !important;
    }}
    button[data-testid="stNumberInputStepDown"]:hover,
    button[data-testid="stNumberInputStepUp"]:hover {{
        background-color: #6F5847 !important;
    }}

    div[data-testid="stAlert"] {{
        background-color: #F3EFE8 !important;
        border: 1px solid #EDE7DF !important;
    }}
    div[data-testid="stAlert"] p {{
        color: #3D3833 !important;
    }}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_service():
    return ReportService()


def render_grade_badge(grade):
    return f'<span class="grade-badge grade-{grade}">{grade}</span>'


def render_skill_tags(skills, missing=False):
    if not skills:
        return '<span style="color:#B0A99D; font-size:0.85rem;">None</span>'
    cls = "skill-tag-missing" if missing else "skill-tag"
    return "".join(f'<span class="skill-tag {cls}">{s}</span>' for s in skills)


def metric_card(value, label, color_class=""):
    st.markdown(f"""
    <div class="metric-card {color_class}">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


WARM_PALETTE = ["#C4784F", "#7A8B6F", "#C99A3B", "#B15E4F", "#6E8FA3"]


def grade_distribution_chart(evaluations):
    counts = Counter(ev.grade for ev in evaluations)
    grades = ["A", "B", "C", "D"]
    values = [counts.get(g, 0) for g in grades]
    colors = ["#7A8B6F", "#6E8FA3", "#C99A3B", "#B15E4F"]

    fig = go.Figure(data=[go.Bar(
        x=grades, y=values, marker_color=colors, text=values, textposition="outside",
    )])
    fig.update_layout(
        title="Grade Distribution",
        height=280,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="#FAF8F5",
        paper_bgcolor="#FAF8F5",
        font=dict(color="#3D3833"),
        yaxis=dict(showgrid=True, gridcolor="#E8E2D8"),
        showlegend=False,
    )
    return fig


def skills_coverage_chart(evaluations):
    skill_counts = Counter()
    for ev in evaluations:
        for s in ev.matched_skills:
            skill_counts[s] += 1

    if not skill_counts:
        return None

    top_skills = skill_counts.most_common(8)
    labels = [s[0] for s in top_skills]
    values = [s[1] for s in top_skills]
    colors = [WARM_PALETTE[i % len(WARM_PALETTE)] for i in range(len(labels))]

    fig = go.Figure(data=[go.Bar(
        x=values, y=labels, orientation="h", marker_color=colors,
    )])
    fig.update_layout(
        title="Most Common Matched Skills",
        height=280,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="#FAF8F5",
        paper_bgcolor="#FAF8F5",
        font=dict(color="#3D3833"),
        xaxis=dict(showgrid=True, gridcolor="#E8E2D8"),
        yaxis=dict(autorange="reversed"),
    )
    return fig


st.markdown("""
<div class="header-band">
    <h1>HireX</h1>
    <p>Your Recruitment Copilot for smarter hiring.</p>
</div>
""", unsafe_allow_html=True)

st.subheader("Job Description")
jd_text = st.text_area(
    "Paste the job description below", height=160,
    placeholder="e.g. Backend Engineer with 2-4 years experience, Python, PostgreSQL, REST APIs...",
)

col1, col2 = st.columns([1, 5])
with col1:
    top_k = st.number_input("Candidates to show", min_value=1, max_value=10, value=5)
with col2:
    st.write("")
    st.write("")
    run_button = st.button("Analyze & Find Candidates", type="primary")

st.divider()

if run_button:
    if not jd_text.strip():
        st.warning("Please paste a job description first.")
    else:
        with st.spinner("Analyzing job description and evaluating candidates..."):
            service = get_service()
            report = service.generate_report(jd_text, top_k=top_k)

        jd = report["jd_analysis"]
        evaluations = report["candidate_evaluations"]

        st.subheader("Overview")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            metric_card(f"{jd.quality_score}/10", "JD Quality Score", "metric-card-terracotta")
        with m2:
            metric_card(len(evaluations), "Candidates Evaluated", "metric-card-sage")
        with m3:
            a_grade_count = sum(1 for e in evaluations if e.grade == "A")
            metric_card(a_grade_count, "Grade A Matches", "metric-card-mustard")
        with m4:
            avg_matched = round(sum(len(e.matched_skills) for e in evaluations) / len(evaluations), 1) if evaluations else 0
            metric_card(avg_matched, "Avg Skills Matched", "metric-card-rose")

        st.write("")

        if evaluations:
            chart_col1, chart_col2 = st.columns(2)
            with chart_col1:
                st.plotly_chart(grade_distribution_chart(evaluations), use_container_width=True)
            with chart_col2:
                skills_fig = skills_coverage_chart(evaluations)
                if skills_fig:
                    st.plotly_chart(skills_fig, use_container_width=True)
                else:
                    st.info("No matched skills to chart.")

        st.divider()

        st.subheader("Job Description Quality")
        if jd.quality_score < 6:
            st.warning("JD quality is low — candidate matching below may be less reliable since the requirement itself is ambiguous.")
        if jd.weaknesses:
            with st.expander("Weaknesses identified", expanded=(jd.quality_score < 6)):
                for w in jd.weaknesses:
                    st.markdown(f"- {w}")
        if jd.missing_elements:
            with st.expander("Missing elements"):
                for m in jd.missing_elements:
                    st.markdown(f"- {m}")
        if jd.ambiguous_phrases:
            with st.expander("Ambiguous phrases flagged"):
                for a in jd.ambiguous_phrases:
                    st.markdown(f"- \"{a}\"")
        with st.expander("View AI-improved JD"):
            st.markdown(jd.improved_jd)

        st.divider()

        st.subheader(f"Top {len(evaluations)} Candidates")

        if not evaluations:
            st.info("No candidates found.")
        else:
            for ev in evaluations:
                st.markdown(f"""
                <div class="candidate-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="font-size:1.1rem; font-weight:600; color:#3D3833;">{ev.candidate_name}</div>
                        <div>{render_grade_badge(ev.grade)} <span class="confidence-tag">&nbsp;Confidence: {ev.confidence}</span></div>
                    </div>
                    <div style="color:#B0A99D; font-size:0.8rem; margin-bottom:10px;">{ev.source_file}</div>
                    <div style="margin-bottom:8px;">
                        <div style="font-size:0.8rem; color:#8A8178; margin-bottom:4px;">Matched Skills</div>
                        {render_skill_tags(ev.matched_skills)}
                    </div>
                    <div style="margin-bottom:12px;">
                        <div style="font-size:0.8rem; color:#8A8178; margin-bottom:4px;">Missing Skills</div>
                        {render_skill_tags(ev.missing_skills, missing=True)}
                    </div>
                    <div style="color:#5C554C; font-size:0.9rem; margin-bottom:10px;">{ev.reasoning}</div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander(f"Evidence & suggested interview questions — {ev.candidate_name}"):
                    if ev.evidence:
                        st.markdown("**Evidence from resume:**")
                        for e in ev.evidence:
                            st.markdown(f"- {e}")
                    if ev.suggested_interview_questions:
                        st.markdown("**Suggested interview questions:**")
                        for q in ev.suggested_interview_questions:
                            st.markdown(f"- {q}")
else:
    st.info("Paste a job description above and click Analyze & Find Candidates to get started.")