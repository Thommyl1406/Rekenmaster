import streamlit as st
import random
from supabase import create_client

# -------------------------------------------------------------
# JOUW UNIEKE SUPABASE CLOUD GEGEVENS
# -------------------------------------------------------------
SUPABASE_URL = "https://iwootoqaieisilkylotg.supabase.co"
SUPABASE_KEY = "sb_publishable_dAOMuXRA6lUMrPbieCpcVA_VMWQCSs-"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="🗺️ Reken-Expeditie", page_icon="🗺️", layout="centered")

# Custom CSS voor een kleurrijke avonturensfeer
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #ffffff;
    }
    .map-container {
        background: rgba(255, 255, 255, 0.05);
        border: 3px dashed #facc15;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .map-step {
        display: inline-block;
        font-size: 2rem;
        padding: 10px;
        margin: 5px;
        border-radius: 12px;
        background-color: #334155;
    }
    .active-step {
        background-color: #22c55e !important;
        border: 3px solid #facc15;
        transform: scale(1.15);
    }
    .som-card {
        background: linear-gradient(90deg, #4338ca 0%, #3730a3 100%);
        border: 4px solid #38bdf8;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        font-size: 3.2rem;
        font-weight: bold;
        color: #ffffff;
        box-shadow: 0 8px 16px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #eab308 0%, #ca8a04 100%) !important;
        color: #000000 !important;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
    }
    </style>
""", unsafe_allowed_html=True)

# Sessie variabelen
if "positie" not in st.session_state:
    st.session_state.positie = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "huidige_som" not in st.session_state:
    st.session_state.huidige_som = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# De halten op de avonturenkaart
KAART_STAPPEN = [
    {"naam": "Starteiland", "icoon": "🏝️"},
    {"naam": "Toverbos", "icoon": "🌲"},
    {"naam": "Ridderslot", "icoon": "🏰"},
    {"naam": "Vulkanenvallei", "icoon": "🌋"},
    {"naam": "Diamanteiland", "icoon": "💎"},
    {"naam": "SCHATKIST!", "icoon": "🏆"}
]
MAX_STAPPEN = len(KAART_STAPPEN) - 1

# Admin sidebar
st.sidebar.title("👑 Admin Login")
if not st.session_state.is_admin:
    u = st.sidebar.text_input("User", key="au")
    p = st.sidebar.text_input("Pass", type="password", key="ap")
    if st.sidebar.button("Inloggen"):
        if u == "admin" and p == "admin123":
            st.session_state.is_admin = True
            st.rerun()
else:
    st.sidebar.success("Ingelogd als Admin")
    if st.sidebar.button("Uitloggen"):
        st.session_state.is_admin = False
        st.rerun()

st.title("🗺️ REKEN-EXPEDITIE 🏆")

# ---------------- TEKEN DE VISUELE KAART ----------------
st.markdown("### 📜 Jouw Avonturenkaart:")
cols = st.columns(len(KAART_STAPPEN))

for idx, stap in enumerate(KAART_STAPPEN):
    with cols[idx]:
        if idx == st.session_state.positie:
            st.markdown(f"<div style='text-align: center; font-size: 2.2rem; background: #22c55e; border-radius: 50%; padding: 10px; border: 3px solid #facc15;'>🏃‍➡️<br>{stap['icoon']}</div>", unsafe_allowed_html=True)
            st.caption(f"**{stap['naam']}**")
        elif idx < st.session_state.positie:
            st.markdown(f"<div style='text-align: center; font-size: 1.8rem; opacity: 0.6;'>✅<br>{stap['icoon']}</div>", unsafe_allowed_html=True)
            st.caption(stap['naam'])
        else:
            st.markdown(f"<div style='text-align: center; font-size: 1.8rem; opacity: 0.3;'>🔒<br>{stap['icoon']}</div>", unsafe_allowed_html=True)
            st.caption(stap['naam'])

st.divider()

# ---------------- STARTSCHERM ----------------
if st.session_state.positie == 0 and "speler_naam" not in st.session_state:
    st.subheader("🎯 Begin je expeditie!")
    naam = st.text_input("Wat is je heldennaam?", value="Alex")
    modus = st.selectbox("Welke route neem je?", ["Maaltafels (t/m 100)", "Optellen & Aftrekken", "Deeltafels (t/m 100)"])
    
    if st.button("🚀 START DE REIS!", use_container_width=True):
        st.session_state.speler_naam = naam
        st.session_state.gekozen_modus = modus
        st.session_state.positie = 0
        st.rerun()

# ---------------- HET SPEL / VRAGEN ----------------
elif st.session_state.positie < MAX_STAPPEN:
    huidige_halte = KAART_STAPPEN[st.session_state.positie]
    st.subheader(f"📍 Huidige locatie: {huidige_halte['icoon']} {huidige_halte['naam']}")
    st.write(f"Los de som goed op om 1 stap vooruit te springen op de kaart!")

    # Som genereren
    if st.session_state.huidige_som is None:
        modus = st.session_state.get("gekozen_modus", "Maaltafels (t/m 100)")
        if modus == "Maaltafels (t/m 100)":
            n1, n2 = random.randint(1, 10), random.randint(1, 10)
            st.session_state.huidige_som = (f"{n1} × {n2}", n1 * n2)
        elif modus == "Deeltafels (t/m 100)":
            ans = random.randint(1, 10)
            n2 = random.randint(1, 10)
            st.session_state.huidige_som = (f"{ans * n2} ÷ {n2}", ans)
        else:
            n1, n2 = random.randint(1, 30), random.randint(1, 30)
            st.session_state.huidige_som = (f"{n1} + {n2}", n1 + n2)

    som_tekst, juist_ans = st.session_state.huidige_som
    st.markdown(f'<div class="som-card">{som_tekst} = ?</div>', unsafe_allowed_html=True)

    ans_invoer = st.number_input("Typ je antwoord in:", step=1, value=None, key=f"p_{st.session_state.positie}")

    if st.button("🏃 VOORUIT SPRINGEN ➔", use_container_width=True):
        if ans_invoer is not None:
            if ans_invoer == juist_ans:
                st.session_state.positie += 1
                st.session_state.score += 10
                st.toast("🎉 Goed zo! Je springt 1 stap vooruit op de kaart!", icon="🗺️")
            else:
                st.toast(f"❌ Oeps! Het juiste antwoord was {juist_ans}. Probeer de volgende som!", icon="🧟")

            st.session_state.huidige_som = None
            st.rerun()

# ---------------- GEWONNEN / SCHATKIST BEREIKT ----------------
else:
    st.balloons()
    st.snow()
    st.markdown(f"## 🏆 GEFELICITEERD, {st.session_state.speler_naam.upper()}! 🏆")
    st.markdown("### Je hebt de Schatkist bereikt en de expedition voltooid! 💎✨")

    # Cloud opslag
    if "opgeslagen" not in st.session_state:
        try:
            supabase.table("scores").insert({
                "naam": st.session_state.speler_naam,
                "score": st.session_state.score,
                "totaal": MAX_STAPPEN,
                "modus": st.session_state.get("gekozen_modus", "Expeditie")
            }).execute()
            st.session_state.opgeslagen = True
            st.success("Je behaalde schat staat opgeslagen op de muur! ☁️")
