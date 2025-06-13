import streamlit as st
import os
from pathlib import Path

st.title("API Settings")

# Initialize session state for provider if not exists
if "current_provider" not in st.session_state:
    # Read current provider from secrets
    current_provider = "OpenAI"  # default
    if os.path.exists(".streamlit/secrets.toml"):
        with open(".streamlit/secrets.toml", "r") as f:
            secrets_content = f.read()
            if "SELECTED_LLM =" in secrets_content:
                import re
                match = re.search(r'SELECTED_LLM = "([^"]+)"', secrets_content)
                if match:
                    current_provider = match.group(1)
    st.session_state["current_provider"] = current_provider

def update_provider(provider):
    st.session_state["current_provider"] = provider

# Create columns for the provider selection buttons
col1, col2 = st.columns(2)

# Create styled buttons for provider selection
with col1:
    st.button(
        "OpenAI",
        use_container_width=True,
        on_click=update_provider,
        args=("OpenAI",),
        type="primary" if st.session_state["current_provider"] == "OpenAI" else "secondary"
    )

with col2:
    st.button(
        "Anthropic",
        use_container_width=True,
        on_click=update_provider,
        args=("Anthropic",),
        type="primary" if st.session_state["current_provider"] == "Anthropic" else "secondary"
    )

# Create a form for API key management
with st.form("api_settings_form"):
    st.markdown("---")
    
    # API Key input with icon
    anthropic_api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        help="Enter your API key here. It will be stored securely.",
        disabled=st.session_state["current_provider"] == "OpenAI"
    )
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Enter your API key here. It will be stored securely.",
        disabled=st.session_state["current_provider"] == "Anthropic"
    )
    
    # Submit button with icon
    submitted = st.form_submit_button("💾 Save Settings", use_container_width=True)
    
    if submitted:
        # Get the path to secrets.toml
        secrets_path = Path(".streamlit/secrets.toml")
        
        # Read existing secrets
        secrets_content = ""
        if secrets_path.exists():
            with open(secrets_path, "r") as f:
                secrets_content = f.read()
        
        # Update or add the API key and selected LLM
        if st.session_state["current_provider"] == "OpenAI":
            key_name = "OPENAI_API_KEY"
        else:
            key_name = "CLAUDE_API_KEY"
            
        # Update the secrets content
        if f"{key_name} =" in secrets_content:
            # Replace existing key
            import re
            secrets_content = re.sub(
                f"{key_name} = .*",
                f'{key_name} = "{api_key}"',
                secrets_content
            )
        else:
            # Add new key
            secrets_content += f'\n{key_name} = "{api_key}"'
            
        # Update selected LLM
        if "SELECTED_LLM =" in secrets_content:
            secrets_content = re.sub(
                r'SELECTED_LLM = "[^"]+"',
                f'SELECTED_LLM = "{st.session_state["current_provider"]}"',
                secrets_content
            )
        else:
            secrets_content += f'\nSELECTED_LLM = "{st.session_state["current_provider"]}"'
        
        # Write back to secrets.toml
        with open(secrets_path, "w") as f:
            f.write(secrets_content)
            
        st.success("✨ Settings saved successfully!")

# Display current settings
st.markdown("---")
st.subheader("📋 Current Settings")
if os.path.exists(".streamlit/secrets.toml"):
    with open(".streamlit/secrets.toml", "r") as f:
        secrets = f.read()
        st.code(secrets, language="toml")
else:
    st.info("No API keys configured yet.")
