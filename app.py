import streamlit as st
import requests
import pandas as pd

# ----------- UI STYLE ----------- #
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }

    .big-score {
        font-size: 60px;
        font-weight: bold;
        text-align: center;
        color: #4CAF50;
    }

    .card {
        padding: 20px;
        border-radius: 12px;
        background-color: #161B22;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }

    .metric-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #1F2937;
        text-align: center;
        color: white;
        font-weight: bold;
    }

    hr {
        border: 1px solid #30363D;
    }
    </style>
""", unsafe_allow_html=True)

# ----------- TITLE ----------- #
st.markdown(
    "<h1 style='text-align:center; color:#58A6FF;'>GitHub Portfolio Analyzer</h1>",
    unsafe_allow_html=True
)

github_url = st.text_input("Enter GitHub Profile URL")


def get_username(url):
    return url.rstrip("/").split("/")[-1]


# ----------- AI FEEDBACK FUNCTION ----------- #
def generate_ai_feedback(repo_count, language_count, total_stars, recent_year):
    ai_feedback = []

    if repo_count < 5:
        ai_feedback.append("Add at least 3 more repositories to improve consistency score.")

    if language_count < 3:
        ai_feedback.append("Add projects using 1–2 additional programming languages.")

    if total_stars < 20:
        ai_feedback.append("Improve README and share projects to increase visibility.")

    if recent_year < 2024:
        ai_feedback.append("Make regular commits to show active development.")

    return ai_feedback
# --------------------------------------------- #


if st.button("Analyze Profile"):

    if github_url:

        username = get_username(github_url)
        api_url = f"https://api.github.com/users/{username}/repos"

        response = requests.get(api_url)

        if response.status_code == 200:

            repos = response.json()

            if len(repos) == 0:
                st.error("No repositories found.")
                st.stop()

            data = []
            for repo in repos:
                data.append({
                    "Name": repo["name"],
                    "Stars": repo["stargazers_count"],
                    "Forks": repo["forks_count"],
                    "Language": repo["language"],
                    "Created": repo["created_at"]
                })

            df = pd.DataFrame(data)

            st.subheader("Repository Overview")
            st.dataframe(df)

            st.success(f"Found {len(df)} repositories")

            # ---------------- SCORING ---------------- #

            total_score = 0
            feedback = []
            strengths = []
            red_flags = []

            repo_score = 0
            language_score = 0
            impact_score = 0
            activity_score = 0

            repo_count = len(df)
            language_count = df["Language"].nunique()
            total_stars = df["Stars"].sum()
            recent_year = int(df["Created"].str[:4].max())

            # Repository Count
            if repo_count >= 10:
                repo_score = 20
                strengths.append("Good number of repositories showing consistency.")
            else:
                repo_score = repo_count * 2
                feedback.append("Create more repositories to show consistency.")
                red_flags.append("Very few repositories.")

            total_score += repo_score

            # Language Diversity
            if language_count >= 3:
                language_score = 20
                strengths.append("Good language diversity indicating flexibility.")
            else:
                language_score = language_count * 5
                feedback.append("Use more programming languages.")
                red_flags.append("Low language diversity.")

            total_score += language_score

            # Impact Score
            if total_stars > 50:
                impact_score = 20
                strengths.append("Projects show community interest.")
            else:
                impact_score = 10
                feedback.append("Improve README and promotion.")
                red_flags.append("Low project visibility.")

            total_score += impact_score

            # Activity Score
            if recent_year >= 2023:
                activity_score = 20
                strengths.append("Recent activity shows active development.")
            else:
                activity_score = 10
                feedback.append("Low recent activity.")
                red_flags.append("Low recent activity.")

            total_score += activity_score

            # ---------------- CATEGORY ---------------- #

            if total_score >= 80:
                category = "A Portfolio"
            elif total_score >= 60:
                category = "B Portfolio"
            elif total_score >= 40:
                category = "C Portfolio"
            else:
                category = "D Portfolio"

            # ---------------- OUTPUT ---------------- #

            st.subheader("Portfolio Score")

            st.markdown(f"""
            <div class="card">
                <div class="big-score">{total_score}/100</div>
                <p style='text-align:center;'>Portfolio Strength Score</p>
            </div>
            """, unsafe_allow_html=True)

            st.progress(total_score / 100)
            st.success(f"Portfolio Category: {category}")

            # -------- METRIC DASHBOARD -------- #
            st.markdown("<hr>", unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)

            col1.markdown(f"<div class='metric-box'>Repositories<br>{repo_count}</div>", unsafe_allow_html=True)
            col2.markdown(f"<div class='metric-box'>Languages<br>{language_count}</div>", unsafe_allow_html=True)
            col3.markdown(f"<div class='metric-box'>Total Stars<br>{total_stars}</div>", unsafe_allow_html=True)
            col4.markdown(f"<div class='metric-box'>Last Active<br>{recent_year}</div>", unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

            # -------- SCORE BREAKDOWN -------- #
            st.subheader("Score Breakdown")

            breakdown_df = pd.DataFrame({
                "Category": [
                    "Repository Consistency",
                    "Language Diversity",
                    "Project Impact",
                    "Recent Activity"
                ],
                "Score": [
                    repo_score,
                    language_score,
                    impact_score,
                    activity_score
                ]
            })

            st.table(breakdown_df)

            # -------- PORTFOLIO VS IDEAL -------- #
            st.subheader("Your Portfolio vs Ideal Profile")

            comparison_df = pd.DataFrame({
                "Metric": [
                    "Repositories",
                    "Languages Used",
                    "Total Stars",
                    "Activity Score"
                ],
                "Your Profile": [
                    repo_count,
                    language_count,
                    total_stars,
                    100 if recent_year >= 2023 else 50
                ],
                "Ideal Profile": [
                    20,
                    4,
                    50,
                    100
                ]
            })

            st.table(comparison_df)

            # -------- STRENGTHS / WEAKNESSES / FEEDBACK -------- #
            st.markdown("<hr>", unsafe_allow_html=True)

            if strengths:
                st.success("Strengths:")
                for s in strengths:
                    st.write(f"- {s}")

            if feedback:
                st.warning("Feedback:")
                for f in feedback:
                    st.write(f"- {f}")

            if red_flags:
                st.error("Red Flags:")
                for r in red_flags:
                    st.write(f"- {r}")

            # -------- AI SUGGESTIONS -------- #
            ai_feedback = generate_ai_feedback(
                repo_count,
                language_count,
                total_stars,
                recent_year
            )

            if ai_feedback:
                st.info("Top Actions to Improve Score:")
                for f in ai_feedback:
                    st.write(f"✅ {f}")

            # -------- WOW FEATURE -------- #
            potential_score = min(total_score + 10, 100)
            st.info(f"If suggestions are followed, estimated score → {potential_score}/100")

        else:
            st.error("Invalid GitHub username")
