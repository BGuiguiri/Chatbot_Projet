import os
import csv
import datetime
import streamlit as st
import json
import urllib.request

st.set_page_config(page_title="Assistant RH", page_icon="🏢", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');
* { font-family: 'Plus Jakarta Sans', sans-serif; box-sizing: border-box; }
.stApp { background: #f0f4f8; }
#MainMenu, footer, header { visibility: hidden; }
.rh-header { background: linear-gradient(135deg, #1e3a5f 0%, #2d6a9f 100%); border-radius: 20px; padding: 2rem; margin-bottom: 1.5rem; display: flex; align-items: center; gap: 1rem; box-shadow: 0 10px 40px rgba(30,58,95,0.2); }
.rh-logo { width: 56px; height: 56px; background: rgba(255,255,255,0.15); border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; }
.rh-title { color: white; font-size: 1.5rem; font-weight: 700; margin: 0; }
.rh-subtitle { color: rgba(255,255,255,0.65); font-size: 0.82rem; margin: 0; }
.rh-badge { margin-left: auto; background: rgba(255,255,255,0.15); color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.72rem; font-weight: 600; border: 1px solid rgba(255,255,255,0.2); }
.chat-area { background: white; border-radius: 20px; padding: 1.5rem; min-height: 420px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); margin-bottom: 1rem; }
.msg-row-user { display: flex; justify-content: flex-end; margin: 0.8rem 0; align-items: flex-end; gap: 0.5rem; }
.msg-row-bot { display: flex; justify-content: flex-start; margin: 0.8rem 0; align-items: flex-end; gap: 0.5rem; }
.bubble-user { background: linear-gradient(135deg, #1e3a5f, #2d6a9f); color: white; padding: 0.8rem 1.1rem; border-radius: 18px 18px 4px 18px; max-width: 72%; font-size: 0.9rem; line-height: 1.55; }
.bubble-bot { background: #f8fafc; border: 1px solid #e2e8f0; color: #1e293b; padding: 0.8rem 1.1rem; border-radius: 18px 18px 18px 4px; max-width: 72%; font-size: 0.9rem; line-height: 1.55; }
.avatar-bot { width: 34px; height: 34px; background: linear-gradient(135deg, #1e3a5f, #2d6a9f); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; }
.avatar-user { width: 34px; height: 34px; background: #e2e8f0; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0; }
.source-tag { font-size: 0.7rem; color: #94a3b8; margin-top: 0.35rem; padding-left: 0.2rem; }
.cat-badge { display: inline-block; background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; padding: 0.15rem 0.5rem; border-radius: 6px; font-size: 0.68rem; font-weight: 600; }
.chips-wrap { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0 0.5rem; }
.chip { background: white; border: 1px solid #cbd5e1; color: #475569; padding: 0.4rem 0.85rem; border-radius: 20px; font-size: 0.78rem; }
.stTextInput > div > div > input { background: white !important; border: 2px solid #e2e8f0 !important; border-radius: 12px !important; color: #1e293b !important; font-size: 0.92rem !important; padding: 0.75rem 1rem !important; }
.stTextInput > div > div > input:focus { border-color: #2d6a9f !important; box-shadow: 0 0 0 3px rgba(45,106,159,0.1) !important; }
.stButton > button { background: linear-gradient(135deg, #1e3a5f, #2d6a9f) !important; color: white !important; border: none !important; border-radius: 10px !important; font-weight: 600 !important; }
section[data-testid="stSidebar"] { background: #1e3a5f !important; }
section[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }
.stat-box { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12); border-radius: 12px; padding: 0.75rem 1rem; margin: 0.4rem 0; text-align: center; }
.stat-n { font-size: 1.6rem; font-weight: 700; color: #60a5fa; }
.stat-l { font-size: 0.7rem; color: rgba(255,255,255,0.45); text-transform: uppercase; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_faq():
    data = []
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "faq_rh.csv")
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

    system_prompt = f"""Tu es un assistant RH expert et bienveillant pour une entreprise francaise.
Tu dois repondre aux questions des employes de maniere claire, precise et professionnelle en francais.

Voici la base de connaissances RH de l entreprise :
{FAQ_CONTEXT}

INSTRUCTIONS :
1. Utilise la base de connaissances pour repondre avec precision.
2. Reformule naturellement, ne copie pas mot pour mot.
3. Si la question n est pas dans la FAQ mais reste un sujet RH, reponds avec tes connaissances du droit du travail francais.
4. Sois precis, cite des chiffres et delais quand c est pertinent.
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
            "X-Title": "Assistant RH"
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
    st.markdown("### 🏢 Assistant RH")
    st.markdown("---")
    st.markdown(f"""
    <div class="stat-box"><div class="stat-n">{len(faq_data)}</div><div class="stat-l">Questions en base</div></div>
    <div class="stat-box"><div class="stat-n">{st.session_state.total_q}</div><div class="stat-l">Questions posées</div></div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**📂 Thèmes disponibles**")
    for cat in categories:
        icon = CAT_ICONS.get(cat, "📌")
        count = sum(1 for r in faq_data if r["categorie"] == cat)
        st.markdown(f"{icon} **{cat}** — {count} entrées")
    st.markdown("---")
    if st.button("🗑️ Nouvelle conversation"):
        st.session_state.messages = []
        st.session_state.api_history = []
        st.rerun()

st.markdown("""
<div class="rh-header">
    <div class="rh-logo">🏢</div>
    <div>
        <p class="rh-title">Assistant RH</p>
        <p class="rh-subtitle">Vos questions RH — réponses expertes instantanées</p>
    </div>
    <div class="rh-badge">⚡ OpenRouter · Mistral 7B</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-area">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="msg-row-bot">
        <div class="avatar-bot">🤖</div>
        <div>
            <div class="bubble-bot">
                Bonjour ! Je suis votre assistant RH intelligent. Je peux répondre à toutes vos questions sur 
                les <strong>congés</strong>, la <strong>paie</strong>, le <strong>télétravail</strong>, 
                vos <strong>droits</strong>, la <strong>formation</strong> et bien plus encore.<br><br>
                Comment puis-je vous aider aujourd'hui ?
            </div>
        </div>
    </div>
    <div class="chips-wrap">
        <span class="chip">🏖️ Mes congés payés</span>
        <span class="chip">💰 Ma fiche de paie</span>
        <span class="chip">💻 Indemnité télétravail</span>
        <span class="chip">📚 Utiliser mon CPF</span>
        <span class="chip">⚖️ Rupture conventionnelle</span>
        <span class="chip">🚀 Demander une augmentation</span>
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
            <div class="avatar-bot">🤖</div>
            <div>
                <div class="bubble-bot">{content}</div>
                {source_tag}
            </div>
        </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "", placeholder="Ex: Comment poser un congé ? Qu'est-ce que le CPF ?",
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

        with st.spinner("🤔 L'assistant réfléchit..."):
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
