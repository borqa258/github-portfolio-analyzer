import streamlit as st
import requests
import pandas as pd

st.title("GitHub Portfolio Analyzer")

github_url = st.text_input("Enter GitHub Profile URL")


def get_username(url):
    return url.rstrip("/").split("/")[-1]


if st.button("Analyze Profile"):

    if github_url:

        username = get_username(github_url)
        api_url = f"https://api.github.com/users/{username}/repos"

        response = requests.get(api_url)

        if response.status_code == 200:

            repos = response.json()

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

            repo_count = len(df)
            language_count = df["Language"].nunique()
            total_stars = df["Stars"].sum()
            recent_year = int(df["Created"].str[:4].max())

            # Repository Count
            if repo_count >= 10:
                total_score += 20
                strengths.append("Good number of repositories showing consistency.")
            else:
                total_score += repo_count * 2
                feedback.append("Create more repositories to show consistency.")
                red_flags.append("Very few repositories. Recruiters may see limited experience.")

            # Language Diversity
            if language_count >= 3:
                total_score += 20
                strengths.append("Good language diversity indicating technical flexibility.")
            else:
                total_score += language_count * 5
                feedback.append("Use more programming languages to show technical depth.")
                red_flags.append("Low language diversity. Profile looks technically narrow.")

            # Impact Score
            if total_stars > 50:
                total_score += 20
                strengths.append("Projects show community interest and impact.")
            else:
                total_score += 10
                feedback.append("Projects have low visibility. Improve README and promotion.")
                red_flags.append("Low project visibility.")

            # Activity Score
            if recent_year >= 2024:
                total_score += 20
                strengths.append("Profile shows recent development activity.")
            else:
                total_score += 10
                feedback.append("Recent activity is low. Recruiters prefer active profiles.")
                red_flags.append("Profile looks inactive due to old commits.")

            # Documentation Score (basic assumption)
            total_score += 10
            feedback.append("Add detailed README files explaining problem and solution.")

            # ---------------- OUTPUT ---------------- #

            st.subheader("GitHub Portfolio Score")
            st.metric("Portfolio Score", f"{total_score}/100")
            st.progress(total_score)


            st.subheader("Actionable Feedback")
            for f in feedback:
                st.write("✅", f)

            st.subheader("Recruiter Insights")

            st.write("### ✅ Strengths")
            if strengths:
                for s in strengths:
                    st.write("✔️", s)
            else:
                st.write("No major strengths detected yet.")

            st.write("### ⚠️ Red Flags")
            if red_flags:
                for r in red_flags:
                    st.write("❗", r)
            else:
                st.write("No major red flags detected.")

        else:
            st.error("Invalid GitHub username")
