# general_knowledge_quiz.py

import streamlit as st
import pandas as pd
import random

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="General Knowledge Quiz",
    page_icon="🎯",
    layout="centered"
)

# =========================
# TITLE
# =========================
st.subheader("🎯 General Knowledge Quiz")
st.write("Test your knowledge and have fun!")

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv("data/general_knowledge_random.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip()

# =========================
# FILTER SECTION
# =========================
col1, col2 = st.columns(2)

with col1:
    category_list = sorted(df["Category"].dropna().unique())
    category = st.selectbox("Select Category", options = category_list)
    filtered_df = df[df["Category"] == category]


with col2:
    set_list = sorted(filtered_df["Set"].dropna().unique())
    set_name = st.selectbox("Select Set", options = set_list)
    filtered_df = filtered_df[filtered_df["Set"] == set_name]


# =========================
# SESSION STATE RESET
# =========================
current_filter = f"{category}_{set_name}"

if "last_filter" not in st.session_state:
    st.session_state.last_filter = current_filter

if st.session_state.last_filter != current_filter:
    st.session_state.question_no = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected_option = None
    st.session_state.quiz_data = filtered_df.sample(frac=1).reset_index(drop=True)
    st.session_state.last_filter = current_filter

# =========================
# SESSION STATE INIT
# =========================
if "question_no" not in st.session_state:
    st.session_state.question_no = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = filtered_df.sample(frac=1).reset_index(drop=True)

# =========================
# QUIZ DATA
# =========================
quiz_df = st.session_state.quiz_data

# =========================
# NO DATA
# =========================
if len(quiz_df) == 0:
    st.warning("No questions found.")
    st.stop()

# =========================
# QUIZ FINISHED
# =========================
if st.session_state.question_no >= len(quiz_df):

    st.success("🎉 Quiz Completed!")

    total = len(quiz_df)
    score = st.session_state.score
    percent = round((score / total) * 100, 2)

    st.subheader(f"Your Score: {score} / {total}")
    st.subheader(f"Percentage: {percent}%")

    if percent >= 80:
        st.balloons()
        st.success("Excellent Work!")
    elif percent >= 50:
        st.info("Good Job!")
    else:
        st.warning("Keep Practicing!")

    if st.button("🔄 Restart Quiz"):
        st.session_state.question_no = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.selected_option = None
        st.session_state.quiz_data = filtered_df.sample(frac=1).reset_index(drop=True)
        st.rerun()

# =========================
# SHOW QUESTION
# =========================

else:
    # st.subheader(f"Score: {st.session_state.score}/ {len(quiz_df)}")

    row = quiz_df.iloc[st.session_state.question_no]

    with st.container(border=True):
        col1, col2 = st.columns([2.7,1])
        with col1:
            st.subheader(f"Question {st.session_state.question_no + 1} of {len(quiz_df)}")

        with col2:
            st.subheader(f"Score: {st.session_state.score}/ {len(quiz_df)}")

        st.write(f"### {row['Question']}")
# -----------------------------------------

        options = [
            None,
            row["Option1"],
            row["Option2"],
            row["Option3"],
            row["Option4"]
        ]


        selected = st.radio(
            "Choose your answer:",
            options,
            key=f"q_{st.session_state.question_no}"
        )

        # =========================
        # SUBMIT
        # =========================
        if not st.session_state.answered:

            if st.button("✅ Submit Answer"):

                st.session_state.answered = True
                st.session_state.selected_option = selected

                if selected == row["Correct_Option"]:
                    st.session_state.score += 1
                    st.success("✅ Correct!")
                    st.balloons()
                else:
                    st.error("❌ Wrong!")
                    st.info(f"Correct Answer: {row['Correct_Option']}")

        # =========================
        # NEXT
        # =========================
        if st.session_state.answered:

            if st.button("➡ Next Question"):
                st.session_state.question_no += 1
                st.session_state.answered = False
                st.session_state.selected_option = None
                st.rerun()

# =========================
# SIDEBAR
# =========================
# st.sidebar.title("📊 Progress")
# st.sidebar.write(f"Category: {category}")
# st.sidebar.write(f"Set: {set_name}")
# st.sidebar.write(f"Score: {st.session_state.score}")
# st.sidebar.write(f"Answered: {st.session_state.question_no}")

# Score at the end
# st.subheader(f"Score: {st.session_state.score}/ {len(quiz_df)}")