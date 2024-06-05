import streamlit as st
import json

# Load questions and rules from JSON file
with open('rules-next.json') as json_file:
    data = json.load(json_file)
    questions = data['questions']
    recommendations = data['recommendations']

def get_recommendation_details(answer):
    recommendation = recommendations.get(answer, {"title": "No recommendation found.", "description": ""})
    return recommendation['title'], recommendation['description']

def check_conditions(conditions, user_answers):
    for condition in conditions:
        question_key = condition['question_key']
        expected_answer = condition['expected_answer']
        if user_answers.get(question_key) != expected_answer:
            return False
    return True

# Main
st.set_page_config(page_title="Equipment Integration Guide", page_icon=":information_source:", layout='wide', initial_sidebar_state='auto')

st.title('Equipment Integration - Guide')


st.markdown("""
<style>
    .intro { color: #4a69cl blue; font-family: 'Helvetica'; font-size: 10px; margin-bottom: 20px;}
    .usage { background-color: #b8e994; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
    .note { font-style: italic; }
</style>
<div class="intro">
    <h1>Welcome to the Equipment Integration Tool</h1>
    <p>This tool assists engineers and technicians in integrating equipment with standard systems such as IIoT edge platform / Central Aggregation Server . It provides an interactive guide and recommendations based on your specific conditions along with nescassary documentation wherever required, ensuring a smooth integration process.</p>
</div>
<div class="usage">
    <strong>How to Use This Tool:</strong>
    <p>Navigate through the questions to specify your equipment and integration requirements. Based on your inputs, the tool will provide tailored recommendations and steps for your scenario.</p>
</div>
<div class="note">
    <strong>Note:</strong> Start by answering the question below to get customized integration guidance.
</div>
""", unsafe_allow_html=True)
current_question_key = "preconditions"
user_answers = {}

while current_question_key:
    question = questions[current_question_key]
    answer = st.radio(question['question'], question['options'], index=None)
    user_answers[current_question_key] = answer
   # Show description if the answer is IIoT Edge Platform, IIoT Edge Platform - Edge Device Hardware Installation, or Central Aggregation Server
    if answer in question.get("descriptions", {}):
        st.markdown(question["descriptions"][answer], unsafe_allow_html=True)

    # Determine the next question
    if question['next']:
        current_question_key = question['next'].get(answer)
    else:
        current_question_key = None

if st.button('Get Recommendation'):
    # Initialize variables to store the selected recommendation
    selected_title = "No recommendation found for your selected answers."
    selected_description = "<div style='background-color: #ffffff; margin: 10px; padding: 10px; border-radius: 10px; width: 95%;'><div style='background-color: #ebebeb; border-left: 6px solid #ffa500; padding: 20px; border-radius: 10px;'><strong>Attention:<br></strong> Please re-evaluate your answers to the given questions.<br>Make sure that you did not choose a PLC that can be integrated with one or the other integration path only.<br>Make sure that you did not select `No`, once we ask for confirmation of the PLC type.</div></div>"
    
    # Loop through recommendations and check conditions for each
    for recommendation_title, recommendation_data in recommendations.items():
        if recommendation_title != "Custom Recommendation":
            conditions = recommendation_data.get("conditions", [])
            if check_conditions(conditions, user_answers):
                selected_title = recommendation_title
                selected_description = recommendation_data['description']
                break  # Stop checking conditions once a matching recommendation is found

    with st.container(border=True):
        st.subheader(f'Recommended Steps: {selected_title}')
        st.markdown(selected_description, unsafe_allow_html=True)
    
    with st.expander("Your Answers"):
        st.subheader(f'Answers - Raw Data')
        st.write(user_answers)