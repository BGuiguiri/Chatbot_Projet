import os
import csv
import datetime
import streamlit as st
import json
import urllib.request

st.set_page_config(page_title="ISE, Assistant AI", page_icon="🎓", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #f0efed !important;
    font-family: 'DM Sans', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
button[kind="header"] { display: none !important; }
.st-emotion-cache-1egp75f { display: none !important; }

/* ── Main container ── */
.block-container {
    max-width: 740px !important;
    padding: 0 1.5rem 1.5rem !important;
    margin: 0 auto !important;
}

/* ── Logo zone (replaces "Obtenir Pro") ── */
.ise-logo-bar {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 2.2rem 0 0;
    margin-bottom: 0;
}
.ise-logo-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(0,0,0,0.09);
    border-radius: 999px;
    padding: 0.32rem 1rem 0.32rem 0.55rem;
    font-size: 0.78rem;
    font-weight: 500;
    color: #3a3530;
    letter-spacing: 0.02em;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    cursor: default;
}
.ise-logo-icon {
    width: 24px;
    height: 24px;
    background: #1a1a18;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    flex-shrink: 0;
}

/* ── Hero title ── */
.ise-hero {
    text-align: center;
    padding: 2.6rem 1rem 2rem;
}
.ise-hero-title {
    font-family: 'Instrument Serif', serif;
    font-size: 2.75rem;
    font-weight: 400;
    color: #1a1a18;
    letter-spacing: -0.01em;
    line-height: 1.15;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    flex-wrap: wrap;
}
.ise-hero-icon {
    color: #c0392b;
    font-size: 2.4rem;
    display: inline-block;
    animation: spin-slow 8s linear infinite;
}
@keyframes spin-slow {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

/* ── Chat input card ── */
.chat-card-wrap {
    background: #ffffff;
    border: 1px solid rgba(0,0,0,0.1);
    border-radius: 18px;
    padding: 1rem 1rem 0.7rem;
    box-shadow: 0 2px 16px rgba(0,0,0,0.05);
    margin-bottom: 1.6rem;
}

/* ── Input override ── */
.stTextInput > div > div > input {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    color: #1a1a18 !important;
    font-size: 0.95rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 400 !important;
    padding: 0.2rem 0.4rem !important;
    box-shadow: none !important;
}
.stTextInput > div > div > input::placeholder {
    color: #b0a898 !important;
    font-style: normal;
    font-weight: 300 !important;
}
.stTextInput > div > div > input:focus {
    outline: none !important;
    box-shadow: none !important;
    border: none !important;
}
.stTextInput > div > div {
    border: none !important;
    box-shadow: none !important;
}

/* ── Send button ── */
.stButton > button {
    background: #c0392b !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 999px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    padding: 0.52rem 1.3rem !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 2px 10px rgba(192,57,43,0.25) !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Card footer row ── */
.card-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 0.6rem;
    padding-top: 0.5rem;
    border-top: 1px solid rgba(0,0,0,0.06);
}
.card-footer-left {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.card-footer-add {
    width: 28px;
    height: 28px;
    background: rgba(0,0,0,0.05);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    color: #7a7268;
    cursor: pointer;
}
.card-model-badge {
    font-size: 0.72rem;
    color: #8a8070;
    font-weight: 400;
    letter-spacing: 0.01em;
}

/* ── Chat area ── */
.chat-area {
    padding: 0.5rem 0;
    min-height: 0;
    margin-bottom: 0.8rem;
}

/* ── Messages ── */
.msg-row-user {
    display: flex;
    justify-content: flex-end;
    margin: 1rem 0;
    align-items: flex-end;
    gap: 0.6rem;
}
.msg-row-bot {
    display: flex;
    justify-content: flex-start;
    margin: 1rem 0;
    align-items: flex-end;
    gap: 0.6rem;
}
.bubble-user {
    background: #1a1a18;
    color: #f0ebe3;
    padding: 0.85rem 1.1rem;
    border-radius: 18px 18px 4px 18px;
    max-width: 70%;
    font-size: 0.88rem;
    line-height: 1.6;
    font-weight: 300;
}
.bubble-bot {
    background: #ffffff;
    color: #1a1a18;
    padding: 0.85rem 1.1rem;
    border-radius: 18px 18px 18px 4px;
    max-width: 72%;
    font-size: 0.88rem;
    line-height: 1.6;
    font-weight: 300;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.avatar-bot {
    width: 30px;
    height: 30px;
    background: #1a1a18;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.82rem;
    flex-shrink: 0;
}
.avatar-user {
    width: 30px;
    height: 30px;
    background: #d9d0c4;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.82rem;
    flex-shrink: 0;
}

/* ── Source tag ── */
.source-tag {
    font-size: 0.67rem;
    color: #a89e90;
    margin-top: 0.3rem;
    padding-left: 0.2rem;
}
.cat-badge {
    display: inline-block;
    background: rgba(26,26,24,0.05);
    color: #7a6e62;
    border: 1px solid rgba(26,26,24,0.1);
    padding: 0.1rem 0.5rem;
    border-radius: 6px;
    font-size: 0.66rem;
    font-weight: 500;
}

/* ── Chips ── */
.chips-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin: 1.4rem 0 0.8rem;
    justify-content: center;
}
.chip {
    background: rgba(255,255,255,0.85);
    border: 1px solid rgba(26,26,24,0.1);
    color: #4a4438;
    padding: 0.34rem 0.85rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 400;
    cursor: pointer;
    transition: all 0.18s;
}
.chip:hover { background: #1a1a18; color: #f0ebe3; }

/* ── Spinner ── */
.stSpinner > div { color: #8a8070 !important; }
hr { border-color: rgba(26,26,24,0.08) !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_faq():
    data = []
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "faq_ise.csv")
    with open(path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            data.append(row)
    return data

faq_data = load_faq()

def build_faq_context():
    lines = []
    for i, row in enumerate(faq_data):
        lines.append(f"[{i+1}] Categorie: {row['categorie']}")
        lines.append(f"Q: {row['question']}")
        lines.append(f"R: {row['answer']}")
        lines.append("")
    return "\n".join(lines)

FAQ_CONTEXT = build_faq_context()

def ask_openrouter(user_question, conversation_history):
    api_key = st.secrets.get("OPENROUTER_API_KEY", "")
    if not api_key:
        return "Erreur : clé API manquante. Ajoutez OPENROUTER_API_KEY dans les secrets Streamlit."

    system_prompt = f"""Tu es ISE, Assistant AI — un assistant expert qui guide les candidats 
sur les processus du concours ISE organisé par le CAPESA en Afrique.
Tu dois te présenter sous le nom "ISE, Assistant AI" et repondre aux questions de maniere claire, precise et professionnelle en francais.

Voici la base de connaissances sur le concours ISE :
{FAQ_CONTEXT}

INSTRUCTIONS :
1. Utilise la base de connaissances pour repondre avec precision.
2. Reformule naturellement, ne copie pas mot pour mot.
3. Si la question n est pas dans la FAQ mais reste liee au concours ISE, reponds avec tes connaissances.
4. Sois precis, cite des dates et delais quand c est pertinent.
5. Propose toujours une question connexe a la fin.
6. Reponds TOUJOURS en francais, de facon chaleureuse et professionnelle."""

    messages = [{"role": "system", "content": system_prompt}]
    for msg in conversation_history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_question})

    payload = json.dumps({
        "model": "openrouter/auto",
        "max_tokens": 1000,
        "messages": messages,
        "temperature": 0.7
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://streamlit.app",
            "X-Title": "ISE, Assistant AI"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return f"Erreur HTTP {e.code}: {body}"
    except Exception as e:
        return f"Erreur : {str(e)}"

CAT_ICONS = {
    "Conges": "🏖️", "Congés": "🏖️", "Paie": "💰", "Avantages": "🎁",
    "Formation": "📚", "Carriere": "🚀", "Carrière": "🚀",
    "Teletravail": "💻", "Télétravail": "💻", "Droits": "⚖️",
    "Representation": "🤝", "Représentation": "🤝"
}

if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_history" not in st.session_state:
    st.session_state.api_history = []
if "total_q" not in st.session_state:
    st.session_state.total_q = 0

# ── Logo bar (replaces "Obtenir Pro") ──
st.markdown("""
<div class="ise-logo-bar">
    <div class="ise-logo-pill">
        <div class="ise-logo-icon">🎓</div>
        ISE · Assistant AI · CAPESA
    </div>
</div>
""", unsafe_allow_html=True)

# ── Hero title ──
st.markdown("""
<div class="ise-hero">
    <div class="ise-hero-title">
        Qu'est-ce que tu veux savoir sur ISE ?
    </div>
</div>
""", unsafe_allow_html=True)

# ── Chat area ──
st.markdown('<div class="chat-area">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="msg-row-bot">
        <div class="avatar-bot">🎓</div>
        <div>
            <div class="bubble-bot">
                Bonjour ! Je suis <strong>ISE, Assistant AI</strong>, votre assistant intelligent dédié au concours ISE organisé par le CAPESA.<br><br>
                Je peux répondre à vos questions sur les <strong>conditions d'inscription</strong>, 
                les <strong>épreuves</strong>, les <strong>délais</strong> et bien plus encore.<br><br>
                Comment puis-je vous aider aujourd'hui ?
            </div>
        </div>
    </div>
    <div class="chips-wrap">
        <span class="chip">📋 Conditions d'inscription</span>
        <span class="chip">📅 Dates du concours</span>
        <span class="chip">📝 Épreuves et coefficients</span>
        <span class="chip">📁 Documents requis</span>
        <span class="chip">🎓 Débouchés après ISE</span>
        <span class="chip">💡 Conseils de préparation</span>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-row-user">
            <div class="bubble-user">{msg["content"]}</div>
            <div class="avatar-user">👤</div>
        </div>""", unsafe_allow_html=True)
    else:
        content = msg["content"]
        source_tag = ""
        if "[Source:" in content:
            content = content.split("[Source:")[0].strip()
        st.markdown(f"""
        <div class="msg-row-bot">
            <div class="avatar-bot">🎓</div>
            <div>
                <div class="bubble-bot">{content}</div>
                {source_tag}
            </div>
        </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Chat input card ──
st.markdown('<div class="chat-card-wrap">', unsafe_allow_html=True)

user_input = st.text_input(
    "", placeholder="Posez votre question sur le concours ISE…",
    label_visibility="collapsed", key="user_input"
)

st.markdown("""
<div class="card-footer">
    <div class="card-footer-left">
        <div class="card-footer-add">+</div>
        <span class="card-model-badge">ISE · Assistant AI</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

send = st.button("Envoyer ➤", use_container_width=False)

if send and user_input.strip():
    question = user_input.strip()

    if not st.session_state.messages or st.session_state.messages[-1].get("content") != question:
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.api_history.append({"role": "user", "content": question})
        st.session_state.total_q += 1

        with st.spinner("L'assistant réfléchit…"):
            answer = ask_openrouter(question, st.session_state.api_history[:-1])

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.api_history.append({"role": "assistant", "content": answer})

        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chat_log.csv")
        file_exists = os.path.exists(log_path)
        with open(log_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Question", "Reponse"])
            writer.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), question, answer])

    st.rerun()
