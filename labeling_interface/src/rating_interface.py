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
# changing the colours
# Custom CSS for Streamlit
custom_css = """
<style>
body {
    color: #00008B; /* Default text color set to dark blue */
}

/* Change the color of headers */
h1, h2, h3, h4, h5, h6 {
    color: #00008B; /* dark blue */
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


def _login():
    """
    Is executed when the login button is clicked.
    Loads the selected dataset and checks whether the given user exists.
    If yes, history is loaded.
    If not, a new history dictionary is instantiated.

    Executes _init() afterward.
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

def _get_new_pair():
    """
    Function is applied after every user decision.
    Sets next candidate pair to the current session state and saves history.
    """
    st.session_state['current_match_id'] += 1
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
        st.text_input("Repeat your password", key="_password_re", type='password')

        st.selectbox("Gender", ("Male", "Female", "Diverse"), key="_gender")
        st.selectbox("English Level", ("B1.1","B1.2","B2.1", "B2.2", "C1.1", "C1.2", "C2.1", "C2.2"), key="_english_level")
        st.number_input("Enter your Age", step=1, key="_age")

        # To Do: Knowledge of Text-Subjects like Biology, Gaming etc. maybe as Slider(0-100) or 0/1 Checkbox

        # Submit Button
        st.form_submit_button("Submit")


def save_user_profile():
    """
    Saves the user details after Submitting the signup formular
    """
    # To Do: Validate if all Inputs are complete

    # Hashing the passwort before saving it as JSON
    if "_password" in st.session_state:
        hashed_password = hash(st.session_state["_password"])

    # Check/Validate Inputs before? Does the user already exist?
    temp_userprofile = {
        "username":st.session_state["_username"],
        "password":hashed_password,
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
        left: -250px; /* move container to left */
        top: 20px;  
     }
    .container-left1 p {
        font-size: 20px; /* Change the text size to 20 */
    }
    </style>
    """
    st.markdown(css_text, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="container-left1"><p>Please rate your decision:</p></div>', unsafe_allow_html=True)

# Define a function to get a new pair and reset the slider
def _get_new_pair_and_reset_slider():
    #  existing logic to get a new pair
    _get_new_pair()
    # Reset the slider to the default value
    st.session_state.simplicity_slider = "Both texts are actually the same"


# For storing the selected likert value as an integer
# Mapping of textual labels to numerical values
label_to_value = {
    "I'm very sure the left text is simpler": 0,
    "I'm sure the left text is simpler": 1,
    "I'm pretty sure the left text is simpler": 2,
    "Both texts are actually the same": 3,
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
                        width: 200vw !important;
                        left: 50%;
                        right: 50%;
                        transform: translateX(-50%);
                        max-width: 1800px !important;
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
                        max-width: 1200px;
                        margin: 0 auto;
                        top: -250px;
                    }
                    .likert-labels {
                        display: flex;
                        justify-content: space-between;
                        width: 100%;
                        color: black;
                        font-size: 20px;
                        margin-bottom: 10px;
                    }
                </style>
                '''
        st.markdown(css, unsafe_allow_html=True)

        # Defining options for the slider
        options = [
            "I'm very sure the left text is simpler",
            "I'm sure the left text is simpler",
            "I'm pretty sure the left text is simpler",
            "Both texts are actually the same",
            "I'm pretty sure the right text is simpler",
            "I'm sure the right text is simpler",
            "I'm very sure the right text is simpler"
        ]

        # Inject custom CSS to change the slider color to blue
        st.markdown(
            """
           <style>
           .stSlider > label {
            font-size: 40üx !important;  /* Increase font size of the label */
            }
            div[data-baseweb="slider"] > div > div > div {
            background: #00008B !important;
            }
            
            .StyledThumbValue {
            color: #00008B !important; 
            font-size: 16px !important;  /* Increase font size of the thumb value */
            }
            </style>
            """,
            unsafe_allow_html=True
        )


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
    st.session_state['likert_made'] = True
    history = st.session_state['likert_values'].get(st.session_state['current_match_id'], {})


# Defining the simplicity guideline
def _simplicity_guideline():
    # CSS für die Anpassung der Container-Position
    css_text = """
    <style>
    .container-left2 {
        position: relative;
        left: -650px; /* move container to left */
        width:530px;
        top: -100px;  
    }
    .container-left2  {
        font-size: 20px; /* Change the text size to 20 */
        border: 2px solid #001CAD;
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
    if 'current_match_id' in st.session_state and 'determined_pairs' in st.session_state:
        finished = st.session_state['current_match_id']
        total = len(st.session_state['determined_pairs'])
        st.header(f'Current status labeling: ({finished + 1}/{total})', divider='gray')
    else:
        st.header('Current status labeling:', divider='gray')

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

    _simplicity_guideline()
    # Add text above likert scale
    _textlikert()

    # Add Likert scale
    _likert()
    # Submit button to proceed to next pair of texts
    st.button("Submit", on_click=_get_new_pair_and_reset_slider, disabled=not st.session_state.get('likert_made', False))

else:
    # User is not logged in yet
    # load all datasets
    avail_dataset_paths = sorted(glob.glob("/workspace/data/*_only_texts*"), key=lambda x: int(x.split("_")[-1].replace(".pkl", "")))
    ds_names = [path.split("/")[-1].replace(".pkl", "") for path in avail_dataset_paths]

    st.session_state['ds_version'] = st.sidebar.selectbox('Select a dataset', ds_names).split("_")[-1]

    st.sidebar.text_input("Username", key="login_name")

    # type="password" to show input as *****
    st.sidebar.text_input("Enter Password", key="login_password", type="password")

    # Button-click starts login process
    st.sidebar.button("Login", on_click=_login)


    # Button click starts sign-up process
    st.sidebar.button("Sign-Up", on_click=_sign_up, key="sign_up_button")

    # Check if the signup_form Formular was submitted
    if 'FormSubmitter:signup_form-Submit' in st.session_state:
        if st.session_state['FormSubmitter:signup_form-Submit']:
            save_user_profile()


