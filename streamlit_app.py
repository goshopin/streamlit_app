import streamlit as st
#from langchain_openai import ChatOpenAI
import os
import requests

# To run this module use : streamlit run filename.py

st.set_page_config(layout='wide')

col1, col2, col3 = st.columns([2,7,1])
# Set page title

with col1:

    assistant_type = st.radio('Select the type of assistant you want to operate with',
             key='assistant type',
             options = ['QnA', 'KnowledgeVA', 'search', 'Task']
             )
    
    model_option = st.selectbox('Select the Model',
                         ('gpt2',
                        'gpt4',
                        'llama2',
                        'llama4',
                         ),
                        placeholder='gpt2')
    st.write('Your selected model : ', model_option)
    task_option = None
    if assistant_type == 'Task':
        with st.spinner(f'Loading tasks .. '):
            task_option = st.selectbox('What do you want to do ?',
                         ('Praphrase',
                         'Summary',
                         'Shop',
                         'Blog',
                         'Compose Email'))
            st.write('Your selected action : ', task_option)


with col2:
    st.title("GOASSIST")

    # Initialize session state for chat history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role):
            st.markdown(content)

    # OpenAI API key input
    #api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")
    #if api_key:
    #    os.environ["OPENAI_API_KEY"] = api_key

    # User input
    user_input = st.chat_input("Ask something...")

    if user_input: # and api_key:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Display assistant thinking indicator
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            # Initialize LLM
            # llm = ChatOpenAI(model="gpt-3.5-turbo")
            
            # Get response from LLM
            try:

            
                #response = llm.invoke(user_input) # Call GPT function here
                data = {'prompt': user_input, 'stream': True, 'model_name' : model_option, 'assistant_type':assistant_type} 
                
                url = 'http://localhost:8000/chatapp/chat'
                response = requests.get(url,
                                params=data)
                
                print('llm response', response.text)
                
                assistant_response = response.text # response.content
                
                # Update assistant message
                message_placeholder.markdown(assistant_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            except Exception as e:
                message_placeholder.markdown(f"Error: {str(e)}")
    elif user_input:
        st.warning("Please enter your OpenAI API key in the sidebar.")
