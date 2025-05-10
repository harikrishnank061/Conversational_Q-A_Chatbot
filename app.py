import streamlit as st
import cohere

# === SETUP COHERE CLIENT ===
cohere_api_key = "vzSUUNFPnI6IBHil4qwn0rQxVDegkZaHL9cZNNiR"  # Replace with your actual key
co = cohere.Client(cohere_api_key)

# === STREAMLIT PAGE CONFIG ===
st.set_page_config(page_title="Conversational Q&A Chatbot")
st.header("🎭 Comedian Cohere Bot - Ready to Roast and Respond!")

# === SESSION STATE TO STORE CONVO FLOW ===
if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        {"role": "system", "content": "You're a hilarious AI comedian who answers questions with wit and sass."}
    ]

# === FUNCTION TO GET COHERE RESPONSE ===
def get_chatmodel_response(user_input):
    # Build the full conversation history as a prompt
    prompt = ""
    for msg in st.session_state['flowmessages']:
        if msg["role"] == "system":
            prompt += f"[System Instruction]: {msg['content']}\n"
        elif msg["role"] == "user":
            prompt += f"[User]: {msg['content']}\n"
        elif msg["role"] == "assistant":
            prompt += f"[AI]: {msg['content']}\n"

    prompt += f"[User]: {user_input}\n[AI]:"

    # Get Cohere response
    response = co.generate(
        model='command',
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )

    ai_reply = response.generations[0].text.strip()
    
    # Save convo
    st.session_state['flowmessages'].append({"role": "user", "content": user_input})
    st.session_state['flowmessages'].append({"role": "assistant", "content": ai_reply})
    
    return ai_reply

# === INPUT UI ===
user_input = st.text_input("Type your question, wise human 👇", key="input")
submit = st.button("Ask the question")

if submit and user_input:
    reply = get_chatmodel_response(user_input)
    st.subheader("🤖 AI Says:")
    st.write(reply)
