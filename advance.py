import streamlit as st
import json
import re
import os

USER_DATA_FILE = os.path.join(os.getcwd(), "users.json")
PASSWORD_HISTORY_LIMIT = 14  # Number of previous passwords to remember

# Function to load existing users from file
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to save users to file
def save_users(users):
    with open(USER_DATA_FILE, "w") as file:
        # json.dump(users, file, indent=4)
        json_str = json.dumps(users, indent=None, separators=(',', ':'))  # Compact JSON
        json_str = json_str.replace('},', '},\n')  # Add newline after each object
        file.write(f"{{\n{json_str[1:-1]}\n}}")  # Wrap it in curly braces with newlines

def get_vowels(password):
    return sum(1 for char in password if char.lower() in "aeiou")

def get_consonants(password):
    return sum(1 for char in password if char.isalpha() and char.lower() not in "aeiou")

def consecutive_numbers(password):
    return any(password[i].isdigit() and password[i+1].isdigit() and int(password[i+1]) == int(password[i]) + 1 for i in range(len(password) - 1))

# tested = st.session_state.tested_passwords
# lastfail = st.session_state.last_fail

if "tested" not in st.session_state:
    st.session_state.tested = []  # Store all tested passwords
if "attempts" not in st.session_state:
    st.session_state.attempts = 0  # Track number of changes

def check_password_strength(password, username, tested, lastfail):
    score = 0
    common = ["123456", "password", "12345678", "qwerty", "123456789"]
    checks = [
        {"test": lambda p: p in tested, "txt": "You have already tried this password."},
        {"test": lambda p: p.lower() in common, "txt": "This password is too common"},
        {"test": lambda p: username.lower() in p.lower(), "txt": "The password must not contain your username."},
        {"test": lambda p: len(p) < 8, "txt": "Password too short."},
        {"test": lambda p: len(p) > 16, "txt": "Password too long."},
        {"test": lambda p: not (re.search(r'[a-z]', p) and re.search(r'[A-Z]', p)), "txt": "The password must contain at least one lowercase and one uppercase letter."},
        {"test": lambda p: not re.search(r'\d', p), "txt": "The password must contain at least one number."},
        {"test": lambda p: not re.search(r'[^A-Za-z0-9]', p), "txt": "The password must contain at least one special character."},
        {"test": lambda p: re.search(r'[^A-Za-z0-9+\u00a7~?@$&!#%*]', p), "txt": "The password cannot contain anything other than numbers, letters, or these characters: +\u00a7~?@$&"},
        {"test": lambda p: p[-1].isdigit(), "txt": "The password must not end with a number."},
        {"test": lambda p: re.search(r'(19[0-9]{2})|(20[012][0-9])', p), "txt": "The password must not contain a number that can be interpreted as a year between 1900 and 2029."},
        {"test": lambda p: re.search(r'[a-zA-Z]{4}', p.lower()), "txt": "The password must not contain more than 3 letters in a row."},
        {"test": lambda p: re.search(r'(.)\1', p), "txt": "The password cannot contain the same character twice."},
        {"test": lambda p: get_consonants(p) > get_vowels(p), "txt": "The password must not contain more consonants than vowels."},
        {"test": lambda p: consecutive_numbers(p), "txt": "The password must not contain two digits in a row such that the second digit is equal to the first plus one."},
        {"test": lambda p: lastfail is not None and p.startswith(lastfail), "txt": "The password cannot start with {lastfail}."},
    ]

    for check in checks:
        if check["test"](password):
            if password not in st.session_state.tested:  # Avoid duplicate counting
                st.session_state.tested.append(password)
                st.session_state.attempts += 1  # Correctly track attempts
            lastfail = password[:3] if lastfail is None else lastfail
            return check["txt"].format(lastfail=lastfail)  # Keep the return here
    
    
    # Scoring system based on criteria met
    score += 1 if password.lower() not in common else 0
    score += 1 if len(password) >= 8 else 0
    score += 1 if re.search(r"[A-Z]", password) else 0
    score += 1 if re.search(r"[a-z]", password) else 0
    score += 1 if re.search(r"\d", password) else 0
    score += 1 if re.search(r"[!@#$%^&*?~()_={};'<,>./:|]", password) else 0
    score += 1 if len(password) <= 16 else 0

    return score


if "step" not in st.session_state:
        st.session_state.step = 1
if "user_data" not in st.session_state:
    st.session_state.user_data = {}  
if "current_username" not in st.session_state:
    st.session_state.current_username = None

users = load_users()
    

def next_step():
    st.session_state.step += 1

def check_password_history(username, new_password):
    """Check if the new password has been used recently."""
    if username in users and "password_history" in users[username]:
        return new_password in users[username]["password_history"]
    return False

def update_password_history(username, new_password,):
    """Update the password history for the user."""
    if username not in users:
        users[username] = {"password": "", "password_history": []}
    if "password_history" not in users[username]:
        users[username]["password_history"] = []
    
    users[username]["password_history"].insert(0, new_password)
    users[username]["password_history"] = users[username]["password_history"][:PASSWORD_HISTORY_LIMIT]
    users[username]["password"] = new_password
    save_users(users)

def register_page():
    st.title("Register")

    # Initialize tested and lastfail in session state if not already set
    if "tested_passwords" not in st.session_state:
        st.session_state.tested_passwords = []
    if "last_fail" not in st.session_state:
        st.session_state.last_fail = None

    # Get user input
    if st.session_state.step == 1:
        username = st.text_input("Enter your username")
        password = st.text_input("Enter Your Password", type="password")
        cols = st.columns([3, 8, 6])  # Adjust column widths for alignment

        with cols[0]:
            continue_clicked = st.button("Continue")

        with cols[2]:  # Placing "Login" button in the last column
            login_clicked = st.button("Already have an account? Login")

        # Handle button actions separately
        if continue_clicked:
            if not username.strip() or not password.strip():
                    st.error("⚠️ Please fill in both username and password fields.")
            elif username and password:  # Ensure username is not empty
                if username in users:
                    st.error("This username is already taken. Please choose another one.")
                else:
                    score = check_password_strength(
                        password, 
                        username, 
                        st.session_state.tested_passwords, 
                        st.session_state.last_fail  
                    )  # Extract only the score

                    if isinstance(score, str):  # If a rule failed, score is an error message
                        st.session_state.last_fail = password[:3]  # Store last failed prefix
                        st.error(f"❌ {score}")
                    elif score >= 4:  # Only save if password is strong enough
                        st.session_state.current_username = username  # Temporarily store username
                        st.session_state.current_password = password  # Temporarily store password
                        next_step()
                    else:
                        st.error("❌ Password is too weak. Improve it using the suggestions above.")

        if login_clicked:
            st.session_state["page"] = "Login"

    elif st.session_state.step == 2:
        confirm_password = st.text_input("Enter Your Password Again", type="password")

        cols = st.columns([3, 8, 6])  # Keep the same column structure

        with cols[0]:
            submit_clicked = st.button("Submit")

        with cols[2]:  # Align "Login" button with "Submit"
            login_clicked = st.button("Already have an account? Login")

        # Handle button actions separately
        if submit_clicked:
            if confirm_password:
                if st.session_state.current_password != confirm_password:
                    st.error("⚠️ Passwords do not match. Please try again.")
                else:
                    score =+ 2
                    users[st.session_state.current_username] = {
                        "password": st.session_state.current_password, "password_history": [st.session_state.current_password]
                    }
                    save_users(users)  # Save to file
                    print(score) 
                    st.success(f"User {st.session_state.current_username} registered successfully!")
                    st.info(f"You got your password in {st.session_state.attempts} tries.")
                    st.session_state.step = 1  # Reset for new user entry
            else:
                st.error("⚠️ Please fill both password fields before continuing.")

        if login_clicked:
            st.session_state["page"] = "Login"

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    cols = st.columns([2, 6, 7])  # Adjust column widths for spacing

    with cols[0]:  # Left side for Login button
        login_clicked = st.button("Login")

    with cols[2]:  # Right side for Forgot Password and Create Account buttons
        col1, col2 = st.columns(2)  # Two buttons in one row
        with col1:
            forgot_clicked = st.button("Forgot Password?")
        with col2:
            create_clicked = st.button("Create an account")

    # Handle button actions outside columns to prevent layout shifts
    if login_clicked:
        if username in users and password == users[username]["password"]:
            st.success("Login successful!")
            st.session_state.logged_in = True
        else:
            st.error("Invalid username or password.")

    if forgot_clicked:
        st.session_state["page"] = "Forgot Password"

    if create_clicked:
        st.session_state["page"] = "Register"


def forgot_password_page():
    st.title("Reset Password")

    # Initialize tested and last_fail in session state if not already set
    if "tested_passwords" not in st.session_state:
        st.session_state.tested_passwords = []
    if "last_fail" not in st.session_state:
        st.session_state.last_fail = None

    username = st.text_input("Enter your username")
    new_password = st.text_input("Enter new password", type="password")
    new_password_confirm = st.text_input("Confirm new password", type="password")

    cols = st.columns([6, 18, 6])

    with cols[0]:
        reset_clicked = st.button("Reset Password")

    with cols[2]:
        back_clicked = st.button("Back to Login")

    if reset_clicked:
        if username in users:
            if new_password != new_password_confirm:
                st.error("⚠️ Passwords do not match. Please try again.")
                return
            
            if check_password_history(username, new_password):
                st.error("❌ You cannot reuse a recently used password.")
                return
            
            score = check_password_strength(new_password, username, st.session_state.tested_passwords, st.session_state.last_fail)
            
            if isinstance(score, str):  # If a rule failed, score is an error message
                st.session_state.last_fail = new_password[:3]  # Store last failed prefix
                st.error(f"❌ {score}")
                return
            elif score < 4:  # Ensure the password is strong enough
                st.error("❌ Password is too weak. Improve it using the suggestions above.")
                return
            
            update_password_history(username, new_password)
            st.success("✅ Password reset successful. You can now login.")
        else:
            st.error("❌ Username not found.")

    if back_clicked:
        st.session_state["page"] = "Login"



# Manage navigation
if "page" not in st.session_state:
    st.session_state["page"] = "Login"

if st.session_state["page"] == "Login":
    login_page()
elif st.session_state["page"] == "Register":
    register_page()
elif st.session_state["page"] == "Forgot Password":
    forgot_password_page()
