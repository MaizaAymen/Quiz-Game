import streamlit as st
import requests

st.title("🎮 Quiz Game")

# Store answers in session state
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Fetch questions from backend
response = requests.get("http://127.0.0.1:8000/questions/")
if response.status_code == 200:
    questions = response.json()

    # Loop through questions and render them
    for idx, q in enumerate(questions):
        st.subheader(f"Q{idx+1}: {q['title']}")
        options = [choice['text'] for choice in q['choices']]
        selected = st.radio("Choisissez votre réponse :", options, key=f"question_{idx}")

        # Store selected answer
        st.session_state.answers[idx] = selected

    # Submit button at the end
    if st.button("🎯 Soumettre mes réponses"):
        st.session_state.submitted = True

    # After submission: show result
    if st.session_state.submitted:
        correct_count = 0
        st.markdown("---")
        st.header("📊 Résultats du quiz")

        for idx, q in enumerate(questions):
            selected = st.session_state.answers.get(idx)
            correct = next((c for c in q['choices'] if c['is_correct']), None)

            if selected == correct['text']:
                correct_count += 1
                st.success(f"✅ Q{idx+1} : Bonne réponse")
            else:
                st.error(f"❌ Q{idx+1} : Mauvaise réponse. La bonne réponse était : {correct['text']}")

        st.markdown(f"### 🏁 Score final : {correct_count} / {len(questions)}")

else:
    st.error("❌ Échec du chargement des questions depuis l'API.")
