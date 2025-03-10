import streamlit as st
import string
import random
from password_strength import PasswordStats

# Set page config with theme colors
st.set_page_config(
    page_title=" Password Generator Pro",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for purple/off-white theme
purple_theme = """
<style>
:root {
    --primary: #6A1B9A;
    --background:rgb(252, 143, 0);
    --secondary: #E1BEE7;
}

/* Main container */
.stApp {
    background-color: var(--background);
}

/* Headers */
h1, h2, h3 {
    color: var(--primary) !important;
}

/* Buttons */
.stButton>button {
    background-color: var(--primary) !important;
    color: white !important;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    border: none;
}

/* Sliders */
.stSlider .st-ax {
    background-color: var(--secondary);
}
.stSlider .st-az {
    background-color: var(--primary);
}

/* Checkboxes */
.stCheckbox>label>div:first-child {
    background-color: var(--secondary) !important;
}

/* Password strength meter */
.strength-meter {
    height: 8px;
    border-radius: 4px;
    margin: 10px 0;
    background: #eee;
}
.strength-bar {
    height: 100%;
    border-radius: 4px;
    transition: width 0.3s;
}

/* Password cards */
.password-card {
    padding: 1rem;
    background: white;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(48, 5, 97, 0.97);
    margin: 10px 0;
    border-left: 4px solid var(--primary);
}

</style>
"""
st.markdown(purple_theme, unsafe_allow_html=True)

# Password generator function with improved logic
def generate_password(length, include_lowercase, include_uppercase, include_digits, 
                     include_punctuation, exclude_similar):
    character_sets = {
        'lower': string.ascii_lowercase if include_lowercase else '',
        'upper': string.ascii_uppercase if include_uppercase else '',
        'digits': string.digits if include_digits else '',
        'symbols': string.punctuation if include_punctuation else ''
    }
    
    # Exclude similar characters
    if exclude_similar:
        similar_chars = 'l1IoO0'
        for key in character_sets:
            character_sets[key] = ''.join([c for c in character_sets[key] if c not in similar_chars])
    
    all_chars = ''.join(character_sets.values())
    
    if not all_chars:
        return "Error: Select at least one character type"
    
    # Ensure at least one character from each selected set
    password = []
    for chars in character_sets.values():
        if chars:
            password.append(random.choice(chars))
    
    # Fill the rest with random characters
    password += random.choices(all_chars, k=length - len(password))
    random.shuffle(password)
    return ''.join(password)

# Password strength calculator
def get_password_strength(password):
    stats = PasswordStats(password)
    return min(100, int(stats.strength() * 100))

# UI Design
st.title(" Password Generator By Maryam")
st.markdown("Create **strong**, **secure** passwords with enterprise-grade features")

with st.expander("⚙️ Configuration", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        length = st.slider("Password Length", 8, 64, 16,
                          help="Longer passwords are more secure")
    with col2:
        num_passwords = st.number_input("Number of Passwords", 1, 20, 3,
                                       help="Generate multiple passwords at once")

    st.markdown("**Character Settings**")
    col1, col2, col3 = st.columns(3)
    with col1:
        include_lowercase = st.checkbox("Lowercase (a-z)", True)
        include_uppercase = st.checkbox("Uppercase (A-Z)", True)
    with col2:
        include_digits = st.checkbox("Digits (0-9)", True)
        include_punctuation = st.checkbox("Special Characters", False)
    with col3:
        exclude_similar = st.checkbox("Exclude Similar Characters", True,
                                     help="Exclude characters like 'l', '1', 'O', etc.")

# Generate passwords
if st.button(" Generate Secure Passwords"):
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    passwords = []
    for _ in range(num_passwords):
        pwd = generate_password(length, include_lowercase, include_uppercase,
                                include_digits, include_punctuation, exclude_similar)
        passwords.append(pwd)
    
    # Update history (keep last 10)
    st.session_state.history = (passwords + st.session_state.history)[:10]
    
    # Display results
    st.subheader("🔑 Generated Passwords")
    for pwd in passwords:
        strength = get_password_strength(pwd)
        strength_color = "#4CAF50" if strength > 75 else "#FFC107" if strength > 50 else "#F44336"
        
        st.markdown(f"""
        <div class="password-card">
            <div style="display: flex; justify-content: space-between; align-items: center">
                <code style="font-size: 1.2rem">{pwd}</code>
                <button onclick="navigator.clipboard.writeText('{pwd}')" 
                        style="border: none; background: {strength_color}; color: white; padding: 5px 10px; border-radius: 5px">
                    📋 Copy
                </button>
            </div>
            <div class="strength-meter">
                <div class="strength-bar" style="width: {strength}%; background: {strength_color}"></div>
            </div>
            <div style="color: {strength_color}; font-weight: bold">{strength}% Strength</div>
        </div>
        """, unsafe_allow_html=True)

# Password history section
if 'history' in st.session_state and st.session_state.history:
    st.subheader("✅ Recent Passwords")
    cols = st.columns(3)
    for idx, pwd in enumerate(st.session_state.history):
        with cols[idx % 3]:
            st.code(pwd, language="text")

# Hide Streamlit branding
st.markdown("""
<style>
    [data-testid="stToolbar"] { display: none; }
    .reportview-container .main .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)   