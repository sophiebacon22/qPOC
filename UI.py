# amazon q poc frontend
# source https://github.com/aws-samples/genai-quickstart-pocs/blob/main/genai-quickstart-pocs-python/amazon-bedrock-asynchronous-invocation-poc/app.py

import streamlit as st
import backend

st.set_page_config(page_title="Amazon Q Developer Demo", layout="wide")

st.title("Amazon Q Developer Demo")

col1, col2 = st.columns(2)

with col1:
    task_description = st.text_area("Enter task description", height=200)
    github_link = st.text_input("Enter GitHub repository link")
    
    if st.button("Generate Changes"):
        if task_description and github_link:
            with st.spinner("Generating changes..."):
                try:
                    master_context = backend.create_master_context(github_link)
                    generated_code = backend.generate_code(task_description, master_context)
                    processed_code = backend.apply_post_processing(generated_code)
                    commit_url = backend.commit_and_push_changes(github_link, processed_code)
                    st.success(f"Changes generated and pushed. View commit: {commit_url}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please provide both task description and GitHub link.")

with col2:
    st.subheader("View Changes")
    if 'commit_url' in locals():
        st.markdown(f"[View latest commit]({commit_url})")
    
    # You can add more UI elements here to display the changes,
    # such as a diff view or a code block showing the generated code.

# Add a section for displaying the master context
if st.checkbox("Show Master Context"):
    if 'master_context' in locals():
        st.text_area("Master Context", value=master_context, height=300)
    else:
        st.info("Generate changes to view the master context.")
