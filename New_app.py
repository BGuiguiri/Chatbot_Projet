import os
import csv
import datetime
import streamlit as st
import json
import urllib.request

st.set_page_config(page_title="ISE, Assistant AI", page_icon="🎓", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #f5f0ea !important;
    font-family: 'DM Sans', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #1a1a18 !important;
    border-right: none !important;
}
section[data-testid="stSidebar"] * {
    color: rgba(255,255,255,0.72) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
}
section[data-testid="stSidebar"] h3 {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.1rem !important;
    font-weight: 500 !important;
    color: rgba(255,255,255,0.9) !important;
    letter-spacing: 0.03em;
}

.stat-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    margin: 0.35rem 0;
    text-align: center;
}
.stat-n {
    font-size: 1.5rem;
    font-weight: 600;
    color: #c8b89a !important;
    font-family: 'Cormorant Garamond', serif !important;
}
.stat-l {
    font-size: 0.67rem;
    color: rgba(255,255,255,0.35) !important;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

/* ── Main container ── */
.block-container {
    max-width: 720px !important;
    padding: 2.5rem 1.5rem 1.5rem !important;
}

/* ── Header ── */
.rh-header {
    text-align: center;
    padding: 2.5rem 1rem 2rem;
    margin-bottom: 0.5rem;
}
.rh-avatar {
    width: 64px;
    height: 64px;
    background: #1a1a18;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.6rem;
    margin: 0 auto 1.2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.12);
}
.rh-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem;
    font-weight: 400;
    color: #1a1a18;
    letter-spacing: 0.01em;
    margin-bottom: 0.4rem;
}
.rh-subtitle {
    font-size: 0.83rem;
    color: #8a8070;
    font-weight: 300;
    letter-spacing: 0.02em;
}
.rh-badge {
    display: inline-block;
    margin-top: 0.8rem;
    background: rgba(26,26,24,0.06);
    color: #6b6155;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── Chat area ── */
.chat-area {
    background: transparent;
    padding: 0.5rem 0;
    min-height: 360px;
    margin-bottom: 1.2rem;
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
    padding: 0.9rem 1.2rem;
    border-radius: 20px 20px 4px 20px;
    max-width: 70%;
    font-size: 0.88rem;
    line-height: 1.6;
    font-weight: 300;
    letter-spacing: 0.01em;
}

.bubble-bot {
    background: #ffffff;
    color: #1a1a18;
    padding: 0.9rem 1.2rem;
    border-radius: 20px 20px 20px 4px;
    max-width: 70%;
    font-size: 0.88rem;
    line-height: 1.6;
    font-weight: 300;
    letter-spacing: 0.01em;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}

.avatar-bot {
    width: 32px;
    height: 32px;
    background: #1a1a18;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.avatar-user {
    width: 32px;
    height: 32px;
    background: #d9d0c4;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
}

.source-tag {
    font-size: 0.67rem;
    color: #a89e90;
    margin-top: 0.3rem;
    padding-left: 0.2rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
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

/* ── Chips / suggestions ── */
.chips-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin: 1.2rem 0 0.6rem;
    justify-content: center;
}
.chip {
    background: rgba(255,255,255,0.8);
    border: 1px solid rgba(26,26,24,0.12);
    color: #4a4438;
    padding: 0.38rem 0.9rem;
    border-radius: 20px;
    font-size: 0.76rem;
    font-weight: 400;
    letter-spacing: 0.01em;
    cursor: pointer;
    transition: all 0.2s;
}
.chip:hover { background: #1a1a18; color: #f0ebe3; }

/* ── Input ── */
.stTextInput > div > div > input {
    background: #ffffff !important;
    border: 1px solid rgba(26,26,24,0.14) !important;
    border-radius: 30px !important;
    color: #1a1a18 !important;
    font-size: 0.88rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 300 !important;
    padding: 0.78rem 1.4rem !important;
    box-shadow: 0 2px 16px rgba(0,0,0,0.06) !important;
    transition: box-shadow 0.2s, border-color 0.2s !important;
}
.stTextInput > div > div > input::placeholder {
    color: #b0a898 !important;
    font-style: italic;
    font-weight: 300 !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(26,26,24,0.35) !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.1) !important;
    outline: none !important;
}

/* ── Send button ── */
.stButton > button {
    background: #1a1a18 !important;
    color: #f0ebe3 !important;
    border: none !important;
    border-radius: 30px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    padding: 0.7rem 1.4rem !important;
    transition: opacity 0.2s !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.15) !important;
}
.stButton > button:hover { opacity: 0.82 !important; }

/* ── Spinner ── */
.stSpinner > div { color: #8a8070 !important; }

/* ── Divider ── */
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
6. Reponds TOUJOURS en francais, de facon chaleureuse et professionnelle.
7. A la fin de ta reponse indique la categorie ainsi : [Source: NomCategorie]"""

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

categories = sorted(set(r["categorie"] for r in faq_data))

with st.sidebar:
    st.markdown("### ISE, Assistant AI")
    st.markdown("---")
    st.markdown(f"""
    <div class="stat-box"><div class="stat-n">{len(faq_data)}</div><div class="stat-l">Questions en base</div></div>
    <div class="stat-box"><div class="stat-n">{st.session_state.total_q}</div><div class="stat-l">Questions posées</div></div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Thèmes disponibles**")
    for cat in categories:
        icon = CAT_ICONS.get(cat, "📌")
        count = sum(1 for r in faq_data if r["categorie"] == cat)
        st.markdown(f"{icon} **{cat}** — {count} entrées")
    st.markdown("---")
    if st.button("Nouvelle conversation"):
        st.session_state.messages = []
        st.session_state.api_history = []
        st.rerun()

# ── Header ──
st.markdown("""
<div class="rh-header">
    <div class="rh-avatar">🎓</div>
    <p class="rh-title">ISE, Assistant AI</p>
    <p class="rh-subtitle">Votre assistant IA dédié au concours ISE — réponses expertes instantanées.</p>
    <span class="rh-badge">⚡ ISE · Assistant AI · CAPESA</span>
</div>
""", unsafe_allow_html=True)

# ── Chat ──
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
            parts = content.split("[Source:")
            content = parts[0].strip()
            cat = parts[1].replace("]", "").strip()
            icon = CAT_ICONS.get(cat, "📌")
            source_tag = f'<div class="source-tag"><span class="cat-badge">{icon} {cat}</span></div>'
        st.markdown(f"""
        <div class="msg-row-bot">
            <div class="avatar-bot">🎓</div>
            <div>
                <div class="bubble-bot">{content}</div>
                {source_tag}
            </div>
        </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "", placeholder="Posez votre question sur le concours ISE…",
        label_visibility="collapsed", key="user_input"
    )
with col2:
    send = st.button("Envoyer ➤", use_container_width=True)

if send and user_input.strip():
    question = user_input.strip()
    
    # Éviter les doublons
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
