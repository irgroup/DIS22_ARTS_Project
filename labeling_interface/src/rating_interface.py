import streamlit as st
import pickle
import numpy as np
import pandas as pd
from utils import Text, handle_scores, apply_history
import os
from datetime import datetime
import glob

def _login():
    """
    Is executed when the login button is clicked.
    Loads the selected dataset and checks whether the given user exists.
    If yes, history is loaded.
    If not, a new history dictionary is instantiated.

    Executes _init() afterwards.
    """
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
    st.session_state['likert_values'] = {}  # Initialize likert scale values
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
        st.session_state['likert_values'].get(st.session_state['current_match_id'], {}) # Include likert values in history
    )
    st.session_state['current_match_id'] += 1
    if st.session_state['current_match_id'] >= len(st.session_state['determined_pairs']):
        # user finished labeling
        _save_history()
        st.session_state['current_match_id'] = len(st.session_state['determined_pairs']) - 1
        st.write("Congratulations! You are done labeling the dataset! :partying_face:")

    if winner == 'a':
        handle_scores(st.session_state['texts'][st.session_state['can_a']], st.session_state['texts'][st.session_state['can_b']])
    elif winner == 'b':
        handle_scores(st.session_state['texts'][st.session_state['can_b']], st.session_state['texts'][st.session_state['can_a']])

    st.session_state['selection_made'] = True  # Update selection state
    st.session_state['likert_made'] = False  # Reset likert scale state

def _get_new_pair():
    """
    Function is applied after every user decision.
    Sets next candidate pair to the current session state and saves history.
    """
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
    with st.form("my_form"):
        st.markdown("Please enter your user details")
        st.text_input("Enter Username", key="test_username")
        st.text_input("Enter Password", key="test_password", type='password')
        st.text_input("Repeat your password", key="test_password_re", type='password')
        st.number_input("Enter your Age", step=1)
        
        submitted = st.form_submit_button("Submit")

# Likert scala
def _likert():
    # Create a container
    with st.container():
        # Injecting custom CSS to style the container width
        css = '''
                <style>
                    /* Ensure the main container fits within the viewport */
                    div[data-testid="stVerticalBlock"] {
                        margin: 0 auto !important; /* Center container */
                    }
                    /* Ensure the slider container stretches to full viewport width */
                    div[data-testid="stSlider"] {
                        position: relative;
                        width: 200vw !important;
                        left: 50%;
                        right: 50%;
                        transform: translateX(-50%);
                        max-width: 1200px !important;
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
                </style>
                '''
        st.markdown(css, unsafe_allow_html=True)

        # Defining options for slider
        options = [
            "I'm sure the left text is more simple",
            "Both texts are actually the same",
            "I'm sure the right text is more simple"
        ]

        # Create slider
        simplicity_rating = st.select_slider(
            "How do you rate the simplicity of the texts?",
            options=options,
            format_func=lambda x: f"{x}",
            key="simplicity_slider"
        )

        # Save results in dictionary
        ratings = {
            "Simplicity Rating": simplicity_rating
        }

    # Save the ratings to session state
    if 'likert_values' not in st.session_state:
        st.session_state['likert_values'] = {}

    if 'current_match_id' in st.session_state:
        st.session_state['likert_values'][st.session_state['current_match_id']] = ratings

    # Indicate that the likert scale rating has been made
    st.session_state['likert_made'] = True

if "name" in st.session_state:
    # User is already logged in
    # Build progress status
    if 'current_match_id' in st.session_state and 'determined_pairs' in st.session_state:
        finished = st.session_state['current_match_id']
        total = len(st.session_state['determined_pairs'])
        st.header(f'Click on the text which is easier to understand ({finished + 1}/{total})', divider='rainbow')
    else:
        st.header('Click on the text which is easier to understand', divider='rainbow')

    # Build Interface
    tab1, tab2 = st.columns(2)
    i_a, i_b = st.session_state['can_a'], st.session_state['can_b']

    can_a_text = f"{i_a}: {st.session_state['texts'][i_a].get_text()}"
    can_b_text = f"{i_b}: {st.session_state['texts'][i_b].get_text()}"

    # Winner is the more complex text. As the user should click on the easier text, the arguments are switched
    # Buttons for the user decision:
    with tab1:
        if st.button(can_a_text, key="b_can_a"):
            _update_history('b')

    with tab2:
        if st.button(can_b_text, key="b_can_b"):
            _update_history('a')

    # Add Likert scale
    _likert()

    # button to proceed to  next pair of texts
    st.button("Nächste Seite", on_click=_get_new_pair, disabled=not (st.session_state.get('selection_made', False) and st.session_state.get('likert_made', False)))

else:
    # User is not logged in yet
    # load all datasets
    avail_dataset_paths = sorted(glob.glob("/workspace/data/*_only_texts*"), key=lambda x: int(x.split("_")[-1].replace(".pkl", "")))
    ds_names = [path.split("/")[-1].replace(".pkl", "") for path in avail_dataset_paths]

    st.session_state['ds_version'] = st.sidebar.selectbox('Select a dataset', ds_names).split("_")[-1]

    st.sidebar.text_input("Username", key="login_name")

    # type="password" to show input as *****
    st.sidebar.text_input("Enter Password", key="login_password", type="password")

    st.sidebar.button("Login", on_click=_login)

    # Starts sign-up process 
    st.sidebar.button("Sign-Up", on_click=_sign_up, key="sign_up_button")

# Debug
if "test_username" in st.session_state:
    st.write("Current Username is", st.session_state["test_username"])

# Defining the simplicity guideline
st.sidebar.subheader("Simplicity:")
st.sidebar.write("Imagine you are writing an exam where you are allowed to google and where the task is to understand the two given texts.")
st.sidebar.subheader("Which of the two texts...")
st.sidebar.markdown("* generates less cognitive load?")
st.sidebar.markdown("* can you understand more quickly?")
st.sidebar.markdown("* are you more confident to answer questions about?")
st.sidebar.markdown("* is easier for you to reformulate without changing the meaning?")
