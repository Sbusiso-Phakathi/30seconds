# import streamlit as st
# import pyodbc  # MSSQL connection library
# from datetime import datetime
# import pandas as pd
# import random

# # Database connection function
# @st.cache_resource
# def get_db_connection():
#     conn = pyodbc.connect(
#         "Driver={ODBC Driver 17 for SQL Server};"
#         "Server=129.232.211.166;"  # Replace with your MSSQL server address
#         "Database=events;"          # Replace with your database name
#         "UID=dylan;"               # Replace with your username
#         "PWD=super123duper"        # Replace with your password
#     )
#     return conn

# # Fetch random questions from the database
# def fetch_questions(conn):
#     query = """
#         SELECT TOP 5 question_id, question_text, correct_answer 
#         FROM questions 
#         ORDER BY NEWID();
#     """
#     return pd.read_sql(query, conn)

# # Fetch the scores of players from the database
# def fetch_team_scores(conn):
#     query = """
#         SELECT t.team_name, m.member_name, m.score
#         FROM teams t
#         JOIN teammates m ON t.team_id = m.team_id
#         ORDER BY t.team_name, m.score DESC;
#     """
#     return pd.read_sql(query, conn)

# # Save the player's score to the database
# def save_score(conn, team_name, member_name, final_score):
#     # Insert or update the team record
#     query = """
#         IF NOT EXISTS (SELECT 1 FROM teams WHERE team_name = ?)
#         BEGIN
#             INSERT INTO teams (team_name) VALUES (?);
#         END
#     """
#     conn.execute(query, (team_name, team_name))

#     # Insert or update the player score
#     query = """
#         IF EXISTS (SELECT 1 FROM teammates WHERE team_id = (SELECT team_id FROM teams WHERE team_name = ?) AND member_name = ?)
#         BEGIN
#             UPDATE teammates
#             SET score = score + ?
#             WHERE team_id = (SELECT team_id FROM teams WHERE team_name = ?) AND member_name = ?;
#         END
#         ELSE
#         BEGIN
#             INSERT INTO teammates (team_id, member_name, score)
#             VALUES ((SELECT team_id FROM teams WHERE team_name = ?), ?, ?);
#         END
#     """
#     conn.execute(query, (team_name, team_name, final_score, team_name, member_name, team_name, member_name, final_score))

#     # Update the total team score
#     query = """
#         UPDATE teams
#         SET team_score = (SELECT SUM(score) FROM teammates WHERE team_id = (SELECT team_id FROM teams WHERE team_name = ?))
#         WHERE team_name = ?;
#     """
#     conn.execute(query, (team_name, team_name))

#     conn.commit()

# # Add new question to the database
# def add_question(conn, question, answer):
#     query = """
#         INSERT INTO questions (question_text, correct_answer)
#         VALUES (?, ?);
#     """
#     conn.execute(query, (question, answer))
#     conn.commit()

# # Initialize session state
# if "game_ready" not in st.session_state:
#     st.session_state.game_ready = False
# if "game_started" not in st.session_state:
#     st.session_state.game_started = False
# if "questions" not in st.session_state:
#     st.session_state.questions = []
# if "score" not in st.session_state:
#     st.session_state.score = 0
# if "dice_value" not in st.session_state:
#     st.session_state.dice_value = None
# if "answers_correct" not in st.session_state:
#     st.session_state.answers_correct = {}

# # UI Header
# st.markdown(
#     """
#     <div style="background-color: #d4edda; padding: 20px; border-radius: 10px; text-align: center; font-size: 24px; font-weight: bold;">
#         🎉 30-Second Game 🎉
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# # Sidebar: Add New Question
# st.sidebar.subheader("➕ Add New Question")
# question_input = st.sidebar.text_input("Enter the question:")
# answer_input = st.sidebar.text_input("Enter the correct answer:")

# if st.sidebar.button("Submit Question"):
#     if question_input and answer_input:
#         conn = get_db_connection()
#         add_question(conn, question_input, answer_input)
#         st.sidebar.success("✅ New question added successfully!")
#     else:
#         st.sidebar.error("⚠️ Please provide both a question and an answer.")

# # User Inputs
# team_name = st.text_input("Enter your team name:")
# member_name = st.text_input("Enter your name:")

# # Roll Dice Before Starting
# if st.button("🎲 Roll Dice") and team_name and member_name:
#     st.session_state.dice_value = random.choice([0, 1, 2])
#     st.session_state.game_ready = True  

# if st.session_state.dice_value is not None:
#     st.markdown(f"### 🎲 You rolled: **{st.session_state.dice_value}**")

# # Start Game Button (Disabled Until Dice is Rolled)
# if st.button("🚀 Start Game", disabled=not st.session_state.game_ready):
#     conn = get_db_connection()
#     st.session_state.questions = fetch_questions(conn)
#     if not st.session_state.questions:
#         st.error("⚠️ No questions available in the database.")
#     else:
#         st.session_state.game_started = True
#         st.session_state.answers_correct = {q[0]: None for q in st.session_state.questions}

# # Game Play Section (3x2 Grid Format)
# if st.session_state.game_started:
#     st.markdown("### 🏆 Answer the Questions!")

#     cols = st.columns(3)  # Create 3 columns for the grid
#     for idx, (question_id, question_text, correct_answer) in enumerate(st.session_state.questions):
#         with cols[idx % 3]:  # Distribute questions across 3 columns
#             st.markdown(
#                 f"""
#                 <div style="
#                     background-color: #ffffff;
#                     padding: 10px;
#                     margin: 10px 0;
#                     border-radius: 10px;
#                     box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
#                 ">
#                     <h6 style="margin-bottom: 10px;">{question_text}</h6>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

#             col1, col2 = st.columns([1, 1])
#             with col1:
#                 if st.button(f"✅ Correct", key=f"correct_{question_id}"):
#                     st.session_state.answers_correct[question_id] = True
#             with col2:
#                 if st.button(f"❌ Wrong", key=f"wrong_{question_id}"):
#                     st.session_state.answers_correct[question_id] = False

#     # Submit and Calculate Score
#     if st.button("Submit Results"):
#         total_score = sum(1 for val in st.session_state.answers_correct.values() if val)
#         final_score = max(0, total_score - st.session_state.dice_value)

#         conn = get_db_connection()
#         save_score(conn, team_name, member_name, final_score)

#         st.markdown("### 🎉 Game Over! 🎉")
#         st.write(f"Total Correct Answers: {total_score}")
#         st.write(f"Dice Penalty: {st.session_state.dice_value}")
#         st.write(f"Final Score (after dice penalty): {final_score}")

#         # Fetch & Display Leaderboard
#         scores = fetch_team_scores(conn)
#         if scores:
#             leaderboard_df = pd.DataFrame(scores, columns=["Team Name", "Member Name", "Score"])
#             leaderboard_df.index += 1  

#             st.markdown("## 🏆 Leaderboard")
#             col1, col2 = st.columns(2)

#             with col1:
#                 st.subheader("🔹 Player Scores")
#                 st.write(leaderboard_df[['Member Name', 'Score']])

#             with col2:
#                 st.subheader("🔹 Team Scores")
#                 team_scores = leaderboard_df.groupby('Team Name')['Score'].sum().reset_index()
#                 st.write(team_scores)

#         st.session_state.game_started = False



import streamlit as st
import psycopg2
from datetime import datetime
import pandas as pd
import random  

@st.cache_resource
def get_db_connection():
    return psycopg2.connect(
        host="129.232.211.166",
        database="events",
        user="dylan",
        port=5432,
        password="super123duper"
    )

def fetch_questions(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT question_id, question_text, correct_answer FROM questions ORDER BY RANDOM() LIMIT 5;")
        return cur.fetchall()

def fetch_team_scores(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT t.team_name, m.member_name, m.score
            FROM teams t
            JOIN teammates m ON t.team_id = m.team_id
            ORDER BY t.team_name, m.score DESC;
        """)
        return cur.fetchall()

def save_score(conn, team_name, member_name, final_score):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO teams (team_name)
            VALUES (%s)
            ON CONFLICT (team_name) DO NOTHING;
        """, (team_name,))

        cur.execute("""
            INSERT INTO teammates (team_id, member_name, score)
            VALUES (
                (SELECT team_id FROM teams WHERE team_name = %s), 
                %s, 
                %s
            )
            ON CONFLICT (team_id, member_name) 
            DO UPDATE SET score = teammates.score + EXCLUDED.score;
        """, (team_name, member_name, final_score))
        
        cur.execute("""
            UPDATE teams
            SET team_score = (
                SELECT COALESCE(SUM(score), 0)
                FROM teammates
                WHERE team_id = (SELECT team_id FROM teams WHERE team_name = %s)
            )
            WHERE team_name = %s;
        """, (team_name, team_name))
        
        conn.commit()

def add_question(conn, question, answer):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO questions (question_text, correct_answer) VALUES (%s, %s);",
            (question, answer)
        )
        conn.commit()

# Initialize Session State
if "game_ready" not in st.session_state:
    st.session_state.game_ready = False
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "questions" not in st.session_state:
    st.session_state.questions = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "dice_value" not in st.session_state:
    st.session_state.dice_value = None  
if "answers_correct" not in st.session_state:
    st.session_state.answers_correct = {}

# UI Header
st.markdown(
    """
    <div style="background-color: #d4edda; padding: 20px; border-radius: 10px; text-align: center; font-size: 24px; font-weight: bold;">
        🎉 30-Second Game 🎉
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar: Add New Question
st.sidebar.subheader("➕ Add New Question")
question_input = st.sidebar.text_input("Enter the question:")
# answer_input = st.sidebar.text_input("Enter the correct answer:")

if st.sidebar.button("Submit Question"):
    if question_input:
        conn = get_db_connection()
        add_question(conn, question_input, "answer_input")
        st.sidebar.success("✅ New question added successfully!")
    else:
        st.sidebar.error("⚠️ Please provide both a question and an answer.")

# User Inputs
team_name = st.text_input("Enter your team name:")
member_name = st.text_input("Enter your name:")

# Roll Dice Before Starting
if st.button("🎲 Roll Dice") and team_name and member_name:
    st.session_state.dice_value = random.choice([0, 1, 2])
    st.session_state.game_ready = True  

if st.session_state.dice_value is not None:
    st.markdown(f"### 🎲 You rolled: **{st.session_state.dice_value}**")

# Start Game Button (Disabled Until Dice is Rolled)
if st.button("🚀 Start Game", disabled=not st.session_state.game_ready):
    conn = get_db_connection()
    st.session_state.questions = fetch_questions(conn)
    if not st.session_state.questions:
        st.error("⚠️ No questions available in the database.")
    else:
        st.session_state.game_started = True
        st.session_state.answers_correct = {q[0]: None for q in st.session_state.questions}

# Game Play Section (Fixed Size Question Cards)
if st.session_state.game_started:
    st.markdown("### 🏆 Answer the Questions!")

    cols = st.columns(3)  # Create 3 columns for the grid
    for idx, (question_id, question_text, correct_answer) in enumerate(st.session_state.questions):
        with cols[idx % 3]:  # Distribute questions across 3 columns
            st.markdown(
                f"""
                <div style="
                    background-color: #ffffff;
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 10px;
                    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                    height: 120px;  /* Fixed height */
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    text-align: center;
                    overflow: hidden;
                    text-overflow: ellipsis;
                ">
                    <p style="font-size: 14px; font-weight: bold; padding: 5px; margin: 0;">{question_text}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"✅ Correct", key=f"correct_{question_id}"):
                    st.session_state.answers_correct[question_id] = True
            with col2:
                if st.button(f"❌ Wrong", key=f"wrong_{question_id}"):
                    st.session_state.answers_correct[question_id] = False

    # Submit and Calculate Score
    if st.button("Submit Results"):
        total_score = sum(1 for val in st.session_state.answers_correct.values() if val)
        final_score = max(0, total_score - st.session_state.dice_value)

        conn = get_db_connection()
        save_score(conn, team_name, member_name, final_score)

        st.markdown("### 🎉 Game Over! 🎉")
        st.write(f"Total Correct Answers: {total_score}")
        st.write(f"Dice Penalty: {st.session_state.dice_value}")
        st.write(f"Final Score (after dice penalty): {final_score}")

        # Fetch & Display Leaderboard
        scores = fetch_team_scores(conn)
        if scores:
            leaderboard_df = pd.DataFrame(scores, columns=["Team Name", "Member Name", "Score"])
            leaderboard_df.index += 1  

            st.markdown("## 🏆 Leaderboard")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🔹 Player Scores")
                st.write(leaderboard_df[['Member Name', 'Score']])

            with col2:
                st.subheader("🔹 Team Scores")
                team_scores = leaderboard_df.groupby('Team Name')['Score'].sum().reset_index()
                st.write(team_scores)

        st.session_state.game_started = False
