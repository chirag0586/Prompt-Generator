import streamlit as st
import openai
from typing import Dict

def setup_openai(api_key: str) -> None:
    """Configure OpenAI client with API key."""
    openai.api_key = api_key

def generate_enhanced_prompt(role: str, context: str, task: str) -> str:
    """Use GPT to generate an enhanced prompt."""
    try:
        system_message = """You are a prompt expert. Your task is to take the provided role, context, and task, 
        and generate an enhanced prompt that:
        1. Includes clear formatting instructions
        2. Explicitly asks for clarifying questions before proceeding
        3. Structures the response format
        4. Maintains all the essential information from the original inputs
        
        Return only the enhanced prompt, without any additional explanation."""

        user_message = f"""Please generate an enhanced prompt using these inputs:
        Role: {role}
        Context: {context}
        Task: {task}"""

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating prompt: {str(e)}"

# Streamlit UI
def main():
    st.title("AI Prompt Generator")
    st.write("Generate enhanced prompts using GPT")
    
    # API Key input (with password protection)
    api_key = st.text_input("Enter your OpenAI API Key", type="password")
    
    if api_key:
        setup_openai(api_key)
        
        # Input fields
        role = st.text_area("Role (e.g., 'experienced python developer', 'marketing expert')", height=100)
        context = st.text_area("Context (background information, current situation)", height=100)
        task = st.text_area("Task (what needs to be accomplished)", height=100)
        
        if st.button("Generate Enhanced Prompt"):
            if role and context and task:
                # Show loading spinner while generating prompt
                with st.spinner("Generating enhanced prompt..."):
                    enhanced_prompt = generate_enhanced_prompt(role, context, task)
                
                # Display enhanced prompt
                st.subheader("Enhanced Prompt")
                st.text_area("Generated Prompt", enhanced_prompt, height=300)
            else:
                st.error("Please fill in all fields")

if __name__ == "__main__":
    main()
