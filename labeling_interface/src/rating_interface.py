import streamlit as st
import pickle
import numpy as np
import pandas as pd
from utils import Text, handle_scores, apply_history
import os
from datetime import datetime
import glob
import json
import os.path
import streamlit.components.v1 as components
import hashlib
import random

# login user
def _login():
    """
    Is executed when the login button is clicked.
    Loads the selected dataset + Userprofile and checks whether the given user exists.
    If yes, history is loaded.
    If not, a new history dictionary is instantiated.

    Executes _init() afterward.
    """
    credentials_match = False
    # Try to load Userprofile for "login_name" input from path /data/userprofiles
    if "login_name" in st.session_state and "login_password" in st.session_state:
        userprofile_path = f'/workspace/data/userprofiles/{st.session_state["login_name"]}.json'

        # Check if User profile file exists
        if os.path.isfile(userprofile_path):
            with open(userprofile_path) as user_file:
                user_profile = json.load(user_file)

                # hashing entered "login_password"
                hashed_login_pw = hashlib.sha256(str(st.session_state["login_password"]).encode('utf-8'))
                
                # Now check if the combination of Username + Password matches 
                if (st.session_state["login_name"] == user_profile['username'] and 
                    hashed_login_pw.hexdigest() == user_profile['password']):
                    credentials_match = True
        else:
            # If there is no file for this username, the user has to signup first
            st.error(f'No User with the Username = {st.session_state["login_name"]} exists', icon="🚨")
            return
    else:
        # the keys dont exist in the session_state dict
        st.error(f'No Username or Password given', icon="🚨")
        return

    # Check if Username and Password match, then continue
    if credentials_match:
        # History handling stays the same and saves 'current_match_id'
        st.session_state['name'] = st.session_state["login_name"]
        history_path = f"/workspace/histories/{st.session_state['name']}-{st.session_state['ds_version']}_history.pkl"
        data_path = f"/workspace/data/ARTS_only_texts_{st.session_state['ds_version']}.pkl"

        data = pickle.load(open(data_path, "rb"))
        st.session_state['texts'] = {t_id: Text(t_id, text[0]) for t_id, text in data.iterrows()}
        if os.path.exists(history_path):
            st.session_state['history'] = pickle.load(open(history_path, "rb"))
            st.session_state['current_match_id'] = len(st.session_state['history'].keys())
            apply_history(st.session_state['history'], st.session_state['texts'])
        else:
            # user does not exist
            st.session_state['history'] = {}
            st.session_state['current_match_id'] = 0
        _init()
    else:
        # If the credentials dont match, show error message and exit function
        st.error(f'Username and Password combination do not match', icon="🚨")
        return

def _init():
    """
    Loads the pre-set pairs (determined pairs) for the labeling interface.
    First candidate pairs are set.
    """
    det_pairs_path = f"data/determined_pairs_{int(st.session_state['ds_version']) * 4}.pkl"
    st.session_state['determined_pairs'] = pickle.load(open(det_pairs_path, "rb"))

    if st.session_state['current_match_id'] >= len(st.session_state['determined_pairs']):
        # Case when the user already finished labeling the dataset and logs in
        st.session_state['current_match_id'] = len(st.session_state['determined_pairs']) - 1
        st.write("Congratulations! You are done labeling the dataset! :partying_face:")

    st.session_state['can_a'], st.session_state['can_b'] = st.session_state['determined_pairs'][st.session_state['current_match_id']]
    st.session_state['selection_made'] = False  # Initialize selection state
    st.session_state['likert_made'] = False  # Initialize likert scale state
    st.session_state['likert_made'] = {} # Initialize likert scale values

def _update_history(winner):
    """
    Updates and saves the history: time stamp, candidates, winner are added to the history dictionary.
    Scores are updated for both texts.
    :param winner: id of the NON-CLICKED item by the user
    """
    system_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    st.session_state['history'][st.session_state['current_match_id']] = (
        (st.session_state['can_a'], st.session_state['can_b']),
        st.session_state[f'can_{winner}'],
        system_time,
        st.session_state['likert_values'].get(st.session_state['current_match_id'], {}) # Include likert value in history
    )

    if winner == 'a':
        handle_scores(st.session_state['texts'][st.session_state['can_a']], st.session_state['texts'][st.session_state['can_b']])
    elif winner == 'b':
        handle_scores(st.session_state['texts'][st.session_state['can_b']], st.session_state['texts'][st.session_state['can_a']])

    st.session_state['selection_made'] = True  # Update selection state
    st.session_state['likert_made'] = False # reset likert scala state


# Initialize 'responses' in session state if not already present
if 'responses' not in st.session_state:
    st.session_state['responses'] = []

def submit_form():
    # Update session state to indicate form submission and hide additional questions
    st.session_state.update({
        'questionnaire_submitted': True,
        'show_additional_questions': False
    })
    st.session_state.update({'simplicity_slider': 'move the slider'})

    # If there are additional question IDs in session state
    if 'additional_question_ids' in st.session_state:
        # Determine user ID
        user_id = st.session_state['name'] if 'name' in st.session_state else st.session_state['login_name']

        question_1 = st.session_state['current_question_1']
        answer_1 = st.session_state['selected_answer_1']
        correct_answer_1 = st.session_state.get('correct_answer_1', '')  
        text_id_1 = st.session_state['additional_question_ids'][0]

        question_2 = st.session_state['current_question_2']
        answer_2 = st.session_state['selected_answer_2']
        correct_answer_2 = st.session_state.get('correct_answer_2', '')  
        text_id_2 = st.session_state['additional_question_ids'][1]

        # Create response dictionaries for both questions
        response_1 = {
            'User-ID': user_id, 'Text-ID': text_id_1, 'Frage': question_1,
            'Antwort': answer_1, 'richtige_Antwort': correct_answer_1
        }
        response_2 = {
            'User-ID': user_id, 'Text-ID': text_id_2, 'Frage': question_2,
            'Antwort': answer_2, 'richtige_Antwort': correct_answer_2
        }

        # Define the path for the CSV file to save responses
        csv_path = f'/workspace/data/{user_id}_responses.csv'
        # Check if the CSV file exists
        if os.path.exists(csv_path):
            existing_responses_df = pd.read_csv(csv_path, sep=';')
            # Check if the responses are already saved
            if (existing_responses_df['Text-ID'] == text_id_1).any() and (existing_responses_df['Text-ID'] == text_id_2).any():
                st.warning("The answers have already been saved.")
                return

        # Append responses to session state
        st.session_state['responses'].append(response_1)
        st.session_state['responses'].append(response_2)

        # Save responses to CSV creating or appending a new file
        if os.path.exists(csv_path):
            existing_responses_df = pd.read_csv(csv_path, sep=';')
            new_responses_df = pd.DataFrame([response_1, response_2])
            updated_responses_df = pd.concat([existing_responses_df, new_responses_df], ignore_index=True)
            updated_responses_df.to_csv(csv_path, index=False, sep=';')
        else:
            responses_df = pd.DataFrame([response_1, response_2])
            responses_df.to_csv(csv_path, index=False, sep=';')

    # Clear additional question data from session state
    if 'additional_question_ids' in st.session_state:
        del st.session_state['additional_question_ids']
    if 'current_question_1' in st.session_state:
        del st.session_state['current_question_1']
    if 'current_answers_1' in st.session_state:
        del st.session_state['current_answers_1']
    if 'current_question_2' in st.session_state:
        del st.session_state['current_question_2']
    if 'current_answers_2' in st.session_state:
        del st.session_state['current_answers_2']
    if 'selected_answer_1' in st.session_state:
        del st.session_state['selected_answer_1']
    if 'selected_answer_2' in st.session_state:
        del st.session_state['selected_answer_2']

def _display_additional_questions():
    # Set the title for the additional questions section
    st.title("Content-related questions about the last 10 text selections")
    csv_path = "/workspace/data/MPC-Fragen.csv"

    # Check if the CSV file exists
    if not os.path.exists(csv_path):
        st.error(f'The file {csv_path} not found.')
        return
    else:
        # Initialize additional question IDs if not already in session state
        if 'additional_question_ids' not in st.session_state:
            df = pd.read_csv(csv_path, delimiter=';')
            history_ids = list(st.session_state['history'].keys())
            last_10_matches = history_ids[-10:]
            text_ids = [st.session_state['history'][match][0][i] for match in last_10_matches for i in range(2)]
            text_ids = list(set(text_ids))
            if len(text_ids) < 2:
                st.error('Not enough unique text IDs for the additional questions.')
                return
            st.session_state['additional_question_ids'] = random.sample(text_ids, 2)

        # Read the CSV file with Mcp-questions
        df = pd.read_csv(csv_path, delimiter=';')
        
        # Load and set the first question and answers
        if 'current_question_1' not in st.session_state or 'current_answers_1' not in st.session_state:
            question_row_1 = df[df['Text-ID'] == st.session_state['additional_question_ids'][0]].iloc[0]
            question_1 = question_row_1['Multiple_Choice_Frage']
            answers_1 = question_row_1[['Antwort_A', 'Antwort_B', 'Antwort_C', 'Antwort_D']].tolist()
            correct_answer_1 = question_row_1['richtige_Antwort']

            st.session_state['current_question_1'] = question_1
            st.session_state['current_answers_1'] = answers_1
            st.session_state['correct_answer_1'] = correct_answer_1

        question_1 = st.session_state['current_question_1']
        answers_1 = st.session_state['current_answers_1']

        st.write(question_1)
        selected_answer_1 = st.radio("Please select an answer for question 1:", answers_1, index=None, key='selected_answer_1')
        
        # Load and set the second question and answers
        if 'current_question_2' not in st.session_state or 'current_answers_2' not in st.session_state:
            question_row_2 = df[df['Text-ID'] == st.session_state['additional_question_ids'][1]].iloc[0]
            question_2 = question_row_2['Multiple_Choice_Frage']
            answers_2 = question_row_2[['Antwort_A', 'Antwort_B', 'Antwort_C', 'Antwort_D']].tolist()
            correct_answer_2 = question_row_2['richtige_Antwort']

            st.session_state['current_question_2'] = question_2
            st.session_state['current_answers_2'] = answers_2
            st.session_state['correct_answer_2'] = correct_answer_2 

        question_2 = st.session_state['current_question_2']
        answers_2 = st.session_state['current_answers_2']

        st.write(question_2)
        selected_answer_2 = st.radio("Please select an answer for question 2:", answers_2, index=None, key='selected_answer_2')

        # Form to submit answers to additional questions
        with st.form("Question_form", clear_on_submit=True):
            st.write("Please answer both questions to continue")
            submit_button = st.form_submit_button(
                label='Submit',
                on_click=submit_form,
                disabled=not (st.session_state.get('selected_answer_1') and st.session_state.get('selected_answer_2'))
            )

def _get_new_pair():
    """
    Function is applied after every user decision.
    Sets next candidate pair to the current session state and saves history.
    """
    if not st.session_state.get('show_additional_questions', False):
        st.session_state['current_match_id'] += 1

    if st.session_state['current_match_id'] % 10 == 0:
        st.session_state['show_additional_questions'] = True

    if st.session_state['current_match_id'] >= len(st.session_state['determined_pairs']):
        # user finished labeling
        _save_history()
        st.session_state['current_match_id'] = len(st.session_state['determined_pairs']) - 1
        st.write("Congratulations! You are done labeling the dataset! :partying_face:")

    st.session_state['selection_made'] = False  # Reset selection state
    st.session_state['likert_made'] = False  # Reset likert scale state
    st.session_state['can_a'], st.session_state['can_b'] = st.session_state['determined_pairs'][st.session_state['current_match_id']]
    _save_history()

def _save_history():
    """
    Current history is dumped.
    """
    history_path = f"/workspace/histories/{st.session_state['name']}-{st.session_state['ds_version']}_history.pkl"
    pickle.dump(st.session_state['history'], open(history_path, "wb"))

def _sign_up():
    """
    Opening the Sign-Up form to register a new user.
    """
    with st.form("signup_form", border=True):
        st.markdown("Please enter your user details")
        st.text_input("Enter Username", key="_username")

        # To Do: Check if both password inputs are the same
        st.text_input("Enter Password", key="_password", type='password')

        # Might not be needed, bcs the user can see his "****" password, if he wants to
        # st.text_input("Repeat your password", key="_password_re", type='password')

        st.selectbox("Gender", ("Male", "Female", "Diverse"), key="_gender")
        st.selectbox("English Level", ("B1.1","B1.2","B2.1", "B2.2", "C1.1", "C1.2", "C2.1", "C2.2"), key="_english_level")
        st.number_input("Enter your Age", step=1, key="_age")

        # Submit Button
        st.form_submit_button("Submit")


def save_user_profile():
    """
    Saves the user details after Submitting the signup formular
    """
    # Validate if all Inputs are complete, if one is missing, show error message
    if ("_username" in st.session_state and "_password" in st.session_state and
        "_gender" in st.session_state and "_english_level" in st.session_state and
        "_age" in st.session_state):

        if (not st.session_state["_username"] or not st.session_state["_password"] or
            not st.session_state["_gender"] or not st.session_state["_english_level"] or
            not st.session_state["_age"]):

            st.error(f'The sign-up details were incomplete', icon="🚨")
            return

    # Hashing the passwort before saving it as JSON
    if "_password" in st.session_state:
        hashed_password = hashlib.sha256(str(st.session_state["_password"]).encode('utf-8'))

    # create clean dictionary
    temp_userprofile = {
        "username":st.session_state["_username"],
        "password":hashed_password.hexdigest(),
        "gender":st.session_state["_gender"],
        "english_level":st.session_state["_english_level"],
        "age":st.session_state["_age"]
    }

    # Building filepath
    my_file_path = f'/workspace/data/userprofiles/{temp_userprofile["username"]}.json'

    # One JSON file per User, bcs it could lead to problems, when all Clients want to write to the same JSON file
    if not os.path.isfile(my_file_path):
        with open(my_file_path, 'w', encoding='utf-8') as f:
            json.dump(temp_userprofile, f, ensure_ascii=False, indent=4)
        #If the file is created, Sign-Up was successful
        if os.path.isfile(my_file_path):
            st.success('Sign-Up was successful', icon="✅")
    else:
        st.error(f'A user with this username: {temp_userprofile["username"]} already exists', icon="🚨")


# Textboxes above the likert scala
def _textlikert():
    css_text = """
    <style>
    .container-left1 {
        position: relative;
        left: -20vw;; /* move container to left */
        top: 2vh;  
     }
    </style>
    """
    st.markdown(css_text, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="container-left1"><p>Please decide which text is simpler:</p></div>', unsafe_allow_html=True)

# Define a function to get a new pair and reset the slider
def _get_new_pair_and_reset_slider():
    #  existing logic to get a new pair
    _get_new_pair()
    # Reset the slider to the default value
    st.session_state.simplicity_slider = "move the slider"

# Mapping of textual labels to numerical values
label_to_value = {
    "I'm very sure the left text is simpler": 0,
    "I'm sure the left text is simpler": 1,
    "I'm pretty sure the left text is simpler": 2,
    "move the slider": 3,
    "I'm pretty sure the right text is simpler": 4,
    "I'm sure the right text is simpler": 5,
    "I'm very sure the right text is simpler": 6
}

# likert scala
def _likert():
    # Create a container
    with st.container():
        # Injecting custom CSS to style the container and hide the slider labels
        css = '''
                <style>
                    /* Ensure the main container fits within the viewport */
                    div[data-testid="stVerticalBlock"] {
                        margin: 0 auto !important; /* Center container */
                    }
                    /* Ensure the slider container stretches to full viewport width */
                    div[data-testid="stSlider"] {
                        position: relative;
                        width: 100vw !important;
                        left: 50%;
                        transform: translateX(-50%);
                        max-width: 90vw !important;
                        padding: 0 !important; /* No padding */
                    }
                    /* Set the tick bar width */
                    div[data-testid="stTickBar"] {

                    }
                    /* Ensure no horizontal overflow */
                    html, body {
                        overflow-x: hidden !important;
                    }
                    div[data-testid="stTickBarMin"],
                    div[data-testid="stTickBarMax"] {
                        flex: 1 1 1;
                    }
                    /* Style for likert labels container */
                    .likert-container {
                        width: 100%;
                        max-width: 80vw;
                        margin: 0 auto;
                        top: -20vh;
                    }
                    .likert-labels {
                        display: flex;
                        justify-content: space-between;
                        width: 100%;
                        color: black;
                        font-size: 1rem;
                        margin-bottom: 1vh;
                    }
                </style>
                '''
        st.markdown(css, unsafe_allow_html=True)

        # Defining options for the slider
        options = [
            "I'm very sure the left text is simpler",
            "I'm sure the left text is simpler",
            "I'm pretty sure the left text is simpler",
            "move the slider",
            "I'm pretty sure the right text is simpler",
            "I'm sure the right text is simpler",
            "I'm very sure the right text is simpler"
        ]

        # Create slider
        simplicity_rating = st.select_slider(
            " ",
            options=options,
            format_func=lambda x: f"{x}",
            key="simplicity_slider"
        )

        # Get the numerical value corresponding to the selected label
        selected_value = label_to_value[simplicity_rating]

        # Save results in dictionary
        ratings = {selected_value}

    # Save the ratings to session state
    if 'likert_values' not in st.session_state:
        st.session_state['likert_values'] = {}

    if 'current_match_id' in st.session_state:
        st.session_state['likert_values'][st.session_state['current_match_id']] = ratings

    # Indicate that the likert scale rating has been made
    st.session_state['likert_made'] = True if selected_value != 3 else False
    history = st.session_state['likert_values'].get(st.session_state['current_match_id'], {})

# Defining the simplicity guideline
def _simplicity_guideline():
    # CSS for container position
    css_text = """
    <style>
    .container-left2 {
        position: absolute;
        left: -30vw; /* move container to left */
        width: 20vw;
        top: -52vh;
    }
    .container-left2  {
        font-size: 1.2 rem; 
        border: 1px solid;
    }
    </style>
    """
    st.markdown(css_text, unsafe_allow_html=True)

    with st.container():
        st.markdown(
            """
            <div class="container-left2">
                <h2>Simplicity:</h2>
                <p>Imagine you are writing an exam where you are allowed to google and
                 where the task is to understand the two given texts.</p>
                <h2>Which of the two texts...</h2>
                <ul>
                    <li>generates less cognitive load?</li>
                    <li>can you understand more quickly?</li>
                    <li>are you more confident to answer questions about?</li>
                    <li>is easier for you to reformulate without changing the meaning?</li>
                </ul>
            </div>
            """, unsafe_allow_html=True
        )

if "name" in st.session_state:
    # User is already logged in
    # Build progress status
    if not st.session_state.get('show_additional_questions', False):
        if 'current_match_id' in st.session_state and 'determined_pairs' in st.session_state:
            finished = st.session_state['current_match_id']
            total = len(st.session_state['determined_pairs'])
            st.header(f'Current status labeling: ({finished + 1}/{total})', divider='gray')
        else:
            st.header('Current status labeling:', divider='gray')

    # Check if we need to display additional questions
    if st.session_state.get('show_additional_questions', False):
        _display_additional_questions()

    else:
        # Build Interface
        tab1, tab2 = st.columns(2)
        i_a, i_b = st.session_state['can_a'], st.session_state['can_b']

        can_a_text = f"{i_a}: {st.session_state['texts'][i_a].get_text()}"
        can_b_text = f"{i_b}: {st.session_state['texts'][i_b].get_text()}"

        # Winner is the more complex text. As the user should click on the easier text, the arguments are switched
        # Display text a and b in columns with increased height and width
        with tab1:
            st.markdown(f'<div style="border: 1px solid gray; padding: 20px; height: 400px;">{can_a_text}</div>', unsafe_allow_html=True)
        with tab2:
            st.markdown(f'<div style="border: 1px solid gray; padding: 20px; height: 400px;">{can_b_text}</div>', unsafe_allow_html=True)

        # Add simplicity guideline
        _simplicity_guideline()

        # Add text above likert scale
        _textlikert()

        # Add Likert scale
        _likert()

        # Determine winner based on user's choice
        # Attempt to retrieve the value of 'simplicity_slider' from st.session_state.
        # If the key does not exist, default to "move the slider".
        simplicity_rating = st.session_state.get('simplicity_slider', "move the slider")
        if simplicity_rating in [
            "I'm very sure the left text is simpler",
            "I'm sure the left text is simpler",
            "I'm pretty sure the left text is simpler"
        ]:
            winner = 'a'
        elif simplicity_rating in [
            "I'm pretty sure the right text is simpler",
            "I'm sure the right text is simpler",
            "I'm very sure the right text is simpler"
        ]:
            winner = 'b'
        else:
            winner = None

    # Handle scores based on the determined winner
        if winner == 'a':
            handle_scores(st.session_state['texts'][st.session_state['can_a']], st.session_state['texts'][st.session_state['can_b']])
            _update_history('a')
        elif winner == 'b':
            handle_scores(st.session_state['texts'][st.session_state['can_b']], st.session_state['texts'][st.session_state['can_a']])
            _update_history('b')

    # Submit button to proceed to next pair of texts
    # Not able to click, when on "choose" because there would be no winner
        st.button("Submit", on_click=_get_new_pair_and_reset_slider, disabled=simplicity_rating == "move the slider")

else:
    # User is not logged in yet
    # load all datasets
    avail_dataset_paths = sorted(glob.glob("/workspace/data/*_only_texts*"), key=lambda x: int(x.split("_")[-1].replace(".pkl", "")))
    ds_names = [path.split("/")[-1].replace(".pkl", "") for path in avail_dataset_paths]

    st.session_state['ds_version'] = st.sidebar.selectbox('Select a dataset', ds_names).split("_")[-1]

    st.sidebar.text_input("Username", key="login_name")

    # type="password" to show input as *****
    st.sidebar.text_input("Password", key="login_password", type="password")

    # Button-click starts login process
    st.sidebar.button("Login", on_click=_login)

    # Button click starts sign-up process
    st.sidebar.button("Sign-Up", on_click=_sign_up, key="sign_up_button")

    # Check if the signup_form Formular was submitted
    if 'FormSubmitter:signup_form-Submit' in st.session_state:
        if st.session_state['FormSubmitter:signup_form-Submit']:
            save_user_profile()