import streamlit as st
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import Chroma

st.set_page_config(page_title="The Game Codex", page_icon="🎲")

DISPLAY_NAMES = {
    "uno": "UNO",
    "monopoly": "Monopoly",
    "catan": "Catan",
    "monopoly_deal": "Monopoly Deal",
    "root": "Root",
    "betrayal": "Betrayal at House on the Hill",
    "sushi_go": "Sushi Go!",
    "pandemic": "Pandemic",
    "ticket_to_ride": "Ticket to Ride",
    "risk": "Risk"
}

# Use your own model and embedding here.
# Make sure the embedding matches the one you used to create the vector database.
OLLAMA_CHAT_MODEL = "phi3:mini"
OLLAMA_EMBED_MODEL = "nomic-embed-text"

# DO NOT EDIT BELOW UNLESS YOU KNOW WHAT YOU'RE DOING - this is the core logic of the app that connects everything together. 
# If you want to change how the prompt is built or how the response is cleaned, this is where to do it.
def format_chat_history(messages, max_turns=4):
    recent_messages = messages[-(max_turns * 2):]
    lines = []
    for msg in recent_messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        lines.append(f"{role}: {msg['content']}")
    return "\n".join(lines)


def build_prompt(chat_history, context, question, selected_display_name):
    return f"""
You are The Game Codex, a friendly and reliable board game rules assistant.

Your job is to answer questions using the provided rulebook context for {selected_display_name}.

Guidelines:
- Be conversational, natural, and helpful.
- Do not sound robotic, abrupt, or defensive.
- If the answer is straightforward, answer directly.
- If the user asks a follow-up, use the chat history to continue naturally.
- Avoid copying the rulebook text word-for-word unless necessary.
- Only answer from the provided rulebook context.
- If the context does not clearly answer the question, say:
  "I’m not fully sure from the rules I have here."
- Match the scope of the user's question.
- If the question is narrow, keep the answer narrow.
- Do not add unrelated gameplay rules unless necessary.
- If earlier assistant replies seem inconsistent with the rulebook context, prefer the rulebook context and correct the earlier mistake clearly.

Chat history:
{chat_history if chat_history else "No prior conversation."}

Rulebook context:
{context}

User question:
{question}

Answer:
""".strip()


def clean_response(text: str) -> str:
    cleaned = text.strip()

    stop_markers = [
        "\nUser Question:",
        "\nAnswer:",
        "\nUser:",
        "\nAssistant:",
        "\nQuestion:",
        "\nExample scenario"
    ]
    for marker in stop_markers:
        if marker in cleaned:
            cleaned = cleaned.split(marker)[0].strip()

    if cleaned.startswith("No,"):
        cleaned = cleaned.replace("No,", "No —", 1)
    elif cleaned.startswith("Yes,"):
        cleaned = cleaned.replace("Yes,", "Yes —", 1)

    return cleaned


@st.cache_resource
def load_resources():
    llm = OllamaLLM(model=OLLAMA_CHAT_MODEL, temperature=0)
    embeddings = OllamaEmbeddings(model=OLLAMA_EMBED_MODEL)
    vectordb = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    return llm, vectordb


llm, vectordb = load_resources()

st.title("🎲 The Game Codex")
st.caption("Ask board game rules questions naturally.")

st.sidebar.header("Game Settings")
selected_display_name = st.sidebar.selectbox(
    "Select the game you are playing:",
    options=list(DISPLAY_NAMES.values())
)

current_game_id = [
    gid for gid, name in DISPLAY_NAMES.items()
    if name == selected_display_name
][0]

if "messages_by_game" not in st.session_state:
    st.session_state.messages_by_game = {
        game_id: [] for game_id in DISPLAY_NAMES.keys()
    }

messages = st.session_state.messages_by_game[current_game_id]

if st.sidebar.button("Clear Chat History"):
    st.session_state.messages_by_game[current_game_id] = []
    st.rerun()

for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input(f"Ask a question about {selected_display_name}..."):
    messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.status(f"🔍 Checking the {selected_display_name} rules...", expanded=False) as status:
                search_query = f"{selected_display_name} rulebook rules {prompt}"

                docs = vectordb.max_marginal_relevance_search(
                    search_query,
                    k=3,
                    fetch_k=8,
                    lambda_mult=0.7,
                    filter={"game": current_game_id}
                )

                if not docs:
                    status.update(label="⚠️ I couldn’t find a clear rule match.", state="complete")
                    context = "No specific rule passages were found for this question."
                else:
                    status.update(label="✅ Found relevant rule sections", state="complete")
                    context = "\n\n---\n\n".join([doc.page_content for doc in docs])

            chat_history = format_chat_history(messages[:-1], max_turns=4)
            full_prompt = build_prompt(
                chat_history=chat_history,
                context=context,
                question=prompt,
                selected_display_name=selected_display_name
            )

            raw_answer = llm.invoke(full_prompt)
            full_response = clean_response(raw_answer if isinstance(raw_answer, str) else str(raw_answer))

            if not full_response:
                full_response = "I’m not fully sure from the rules I have here."

            st.markdown(full_response)

        except Exception as e:
            full_response = f"I ran into an issue while checking the rules: {str(e)}"
            st.error(full_response)

        if "docs" in locals() and docs:
            with st.expander("📚 Rulebook Context Used"):
                for doc in docs:
                    st.write(doc.page_content)
                    st.divider()

    messages.append({"role": "assistant", "content": full_response})