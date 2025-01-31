# import streamlit as st
# import psycopg2
# from datetime import datetime, timedelta
# import pandas as pd

# @st.cache_resource
# def get_db_connection():
#     return psycopg2.connect(
#         host="129.232.211.166",
#         database="events",
#         user="dylan",
#         port=5432,
#         password="super123duper"
#     )
     

# def fetch_questions(conn):
#     with conn.cursor() as cur:
#         cur.execute("SELECT question_id, question_text, correct_answer FROM questions ORDER BY RANDOM() LIMIT 5;")
#         return cur.fetchall()

# def save_score(conn, team_name, member_name, increment_score):
#     with conn.cursor() as cur:
#         cur.execute("""
#             INSERT INTO teams (team_name)
#             VALUES (%s)
#             ON CONFLICT (team_name) DO NOTHING;
#         """, (team_name,))

#         cur.execute("""
#             INSERT INTO teammates (team_id, member_name, score)
#             VALUES (
#                 (SELECT team_id FROM teams WHERE team_name = %s), 
#                 %s, 
#                 %s
#             )
#             ON CONFLICT (team_id, member_name) 
#             DO UPDATE SET score = teammates.score + EXCLUDED.score;
#         """, (team_name, member_name, increment_score))
        
#         cur.execute("""
#             UPDATE teams
#             SET team_score = (
#                 SELECT COALESCE(SUM(score), 0)
#                 FROM teammates
#                 WHERE team_id = (SELECT team_id FROM teams WHERE team_name = %s)
#             )
#             WHERE team_name = %s;
#         """, (team_name, team_name))
        
#         conn.commit()

# def fetch_team_scores(conn):
#     with conn.cursor() as cur:
#         cur.execute("""
#             SELECT t.team_name, m.member_name, m.score
#             FROM teams t
#             JOIN teammates m ON t.team_id = m.team_id
#             ORDER BY t.team_name, m.score DESC;
#         """)
#         return cur.fetchall()

# def add_question(conn, question, answer):
#     with conn.cursor() as cur:
#         cur.execute(
#             "INSERT INTO questions (question_text, correct_answer) VALUES (%s, %s);",
#             (question, answer)
#         )
#         conn.commit()

# st.markdown(
#             """
#             <div style="background-color: #d4edda; padding: 20px; border-radius: 10px; text-align: center; font-size: 24px; font-weight: bold;">
#                 🎉 30-Second Game 🎉
#             </div>
#             """,
#             unsafe_allow_html=True
#         )    
# if "game_started" not in st.session_state:
#     st.session_state.game_started = False
# if "questions" not in st.session_state:
#     st.session_state.questions = []
# if "current_index" not in st.session_state:
#     st.session_state.current_index = 0
# if "score" not in st.session_state:
#     st.session_state.score = 0
# if "start_time" not in st.session_state:
#     st.session_state.start_time = None
# if "remaining_time" not in st.session_state:
#     st.session_state.remaining_time = 30  

# st.sidebar.subheader("Add New Question")

# question_input = st.sidebar.text_input("Enter the question:")
# answer_input = st.sidebar.text_input("Enter the correct answer:")

# if st.sidebar.button("Submit Question"):
#     if question_input and answer_input:
#         conn = get_db_connection()
#         add_question(conn, question_input, answer_input)
#         st.sidebar.success("New question added successfully!")
#     else:
#         st.sidebar.error("Please provide both a question and an answer.")

# team_name = st.text_input("Enter your team name:")
# member_name = st.text_input("Enter your name:")

# if st.button("Start Game") and team_name and member_name:
#     conn = get_db_connection()
#     st.session_state.questions = fetch_questions(conn)
#     if not st.session_state.questions:
#         st.error("No questions available in the database.")
#     else:
#         st.session_state.game_started = True
#         st.session_state.current_index = 0
#         st.session_state.score = 0
#         st.session_state.start_time = datetime.now()
#         st.session_state.remaining_time = 30 
        
# if st.session_state.game_started:
#     questions = st.session_state.questions
#     current_index = st.session_state.current_index


#     if current_index < len(questions):
        
#         question_id, question, answer = questions[current_index]
        
#         end_time = st.session_state.start_time + timedelta(seconds=30)
#         st.session_state.remaining_time = int((end_time - datetime.now()).total_seconds())

#         if st.session_state.remaining_time <= 0:
#             st.write("Time's up!")
#             st.write(f"Your team score: {st.session_state.score}")
#             conn = get_db_connection()
#             save_score(conn, team_name, member_name, st.session_state.score)
#             st.session_state.game_started = False 
#         else:
#             import time
#             st.markdown(
#                     f"""
#                     <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px;">
#                         <h4>{question}</h4>
#                     </div>
#                     """,
#                     unsafe_allow_html=True
#                 )

#             user_answer = st.text_input("Your Answer:", key=f"answer_{current_index}")

#             if st.button("Submit Answer", key=f"submit_{current_index}"):
#                     if user_answer.lower() == answer.lower():
#                         st.session_state.score += 1
#                         conn = get_db_connection()
#                         save_score(conn, team_name, member_name, 1)  
#                         st.success("Correct answer!")
#                     else:
#                         st.error("Wrong answer!")
                    
#                     st.session_state.current_index += 1
#                     st.session_state.start_time = datetime.now()  

#             # Initialize session state
#             if "remaining_time" not in st.session_state:
#                 st.session_state.remaining_time = 30  # Set initial countdown time

#             # Create a placeholder for dynamic updates
#             placeholder = st.empty()

#             # Countdown logic
#             for seconds in range(st.session_state.remaining_time, -1, -1):
#                 with placeholder:
#                     st.markdown(
#                         f"""
#                         <div style="background-color: #fffbcc; padding: 10px; border-radius: 10px; text-align: center; font-size: 20px;">
#                             Time Remaining: <b>{seconds} seconds</b>
#                         </div>
#                         """,
#                         unsafe_allow_html=True
#                     )
#                 time.sleep(1)  # Pause for 1 second

#             st.success("Time's up! 🎉")


      

#     else:
#         st.markdown(
#             """
#             <div style="background-color: #d4edda; padding: 20px; border-radius: 10px; text-align: center; font-size: 24px; font-weight: bold;">
#                 🎉 Time's Up! 🎉
#             </div>
#             """,
#             unsafe_allow_html=True
#         )        
#         conn = get_db_connection()
#         save_score(conn, team_name, member_name, st.session_state.score)

#         scores = fetch_team_scores(conn)
#         if scores:
#             leaderboard_df = pd.DataFrame(scores, columns=["Team Name", "Member Name", "Score"])
#             leaderboard_df.index += 1 
#             st.subheader("Leaderboard")
            
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.subheader("Player Scores")
#                 st.write(leaderboard_df[['Member Name', 'Score']])
#             with col2:
#                 st.subheader("Team Scores")
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
