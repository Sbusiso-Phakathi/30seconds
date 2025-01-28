import streamlit as st
import psycopg2
from datetime import datetime, timedelta
import pandas as pd

@st.cache_resource
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="action",
        user="postgres",
        port=5430
    )

def fetch_questions(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT question_id, question_text, correct_answer FROM questions ORDER BY RANDOM() LIMIT 5;")
        return cur.fetchall()

def save_score(conn, team_name, member_name, increment_score):
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
        """, (team_name, member_name, increment_score))
        
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

def fetch_team_scores(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT t.team_name, m.member_name, m.score
            FROM teams t
            JOIN teammates m ON t.team_id = m.team_id
            ORDER BY t.team_name, m.score DESC;
        """)
        return cur.fetchall()

def add_question(conn, question, answer):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO questions (question_text, correct_answer) VALUES (%s, %s);",
            (question, answer)
        )
        conn.commit()

st.title("30-Second Trivia Game")

if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "remaining_time" not in st.session_state:
    st.session_state.remaining_time = 30  

st.sidebar.subheader("Add New Question")

question_input = st.sidebar.text_input("Enter the question:")
answer_input = st.sidebar.text_input("Enter the correct answer:")

if st.sidebar.button("Submit Question"):
    if question_input and answer_input:
        conn = get_db_connection()
        add_question(conn, question_input, answer_input)
        st.sidebar.success("New question added successfully!")
    else:
        st.sidebar.error("Please provide both a question and an answer.")

team_name = st.text_input("Enter your team name:")
member_name = st.text_input("Enter your name:")

if st.button("Start Game") and team_name and member_name:
    conn = get_db_connection()
    st.session_state.questions = fetch_questions(conn)
    if not st.session_state.questions:
        st.error("No questions available in the database.")
    else:
        st.session_state.game_started = True
        st.session_state.current_index = 0
        st.session_state.score = 0
        st.session_state.start_time = datetime.now()
        st.session_state.remaining_time = 30  

if st.session_state.game_started:
    questions = st.session_state.questions
    current_index = st.session_state.current_index

    if current_index < len(questions):
        question_id, question, answer = questions[current_index]
        
        end_time = st.session_state.start_time + timedelta(seconds=30)
        st.session_state.remaining_time = int((end_time - datetime.now()).total_seconds())

        if st.session_state.remaining_time <= 0:
            st.write("Time's up!")
            st.write(f"Your team score: {st.session_state.score}")
            conn = get_db_connection()
            save_score(conn, team_name, member_name, st.session_state.score)
            st.session_state.game_started = False 
        else:
            st.markdown(
                f"""
                <div style="background-color: #fffbcc; padding: 10px; border-radius: 10px; text-align: center; font-size: 20px;">
                    Time Remaining: <b>{st.session_state.remaining_time} seconds</b>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            f"""
            <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px;">
                <h4>{question}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )

        user_answer = st.text_input("Your Answer:", key=f"answer_{current_index}")

        if st.button("Submit Answer", key=f"submit_{current_index}"):
            if user_answer.lower() == answer.lower():
                st.session_state.score += 1
                conn = get_db_connection()
                save_score(conn, team_name, member_name, 1)  
                st.success("Correct answer!")
            else:
                st.error("Wrong answer!")
            
            st.session_state.current_index += 1
            st.session_state.start_time = datetime.now()  

    else:
        st.write(f"Game Over! Your team score: {st.session_state.score}")
        conn = get_db_connection()
        save_score(conn, team_name, member_name, st.session_state.score)

        scores = fetch_team_scores(conn)
        if scores:
            leaderboard_df = pd.DataFrame(scores, columns=["Team Name", "Member Name", "Score"])
            leaderboard_df.index += 1 
            st.subheader("Leaderboard")
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Player Scores")
                st.write(leaderboard_df[['Member Name', 'Score']])
            with col2:
                st.subheader("Team Scores")
                team_scores = leaderboard_df.groupby('Team Name')['Score'].sum().reset_index()
                st.write(team_scores)

        st.session_state.game_started = False  
