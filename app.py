import streamlit as st
import random
from supabase import create_client

# -------------------------------------------------------------
# JOUW UNIEKE SUPABASE CLOUD GEGEVENS
# -------------------------------------------------------------
SUPABASE_URL = "https://iwootoqaieisilkylotg.supabase.co"
SUPABASE_KEY = "sb_publishable_dAOMuXRA6lUMrPbieCpcVA_VMWQCSs-"

# Initialiseer de database
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="⚡ Pokémon Reken-Gym", page_icon="🔴", layout="centered")

# Custom CSS voor een echte Pokémon Battle & Gym sfeer
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #111827 0%, #1f2937 50%, #111827 100%);
        color: #ffffff;
    }
    .pokeball-card {
        background: linear-gradient(180deg, #ef4444 0%, #dc2626 48%, #111827 48%, #111827 52%, #f9fafb 52%, #f3f4f6 100%);
        border: 4px solid #facc15;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        color: #111827;
        margin-bottom: 20px;
    }
    .level-badge {
        background-color: #facc15;
        color: #000000;
        font-weight: bold;
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 1.2rem;
        display: inline-block;
        margin-bottom: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .som-card {
        background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%);
        border: 4px solid #facc15;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        font-size: 3.2rem;
        font-weight: bold;
        color: #ffffff;
        box-shadow: 0 8px 16px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ef4444 0%, #b91c1c 100%) !important;
        color: #ffffff !important;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        border-radius: 14px !important;
        border: 3px solid #facc15 !important;
        padding: 12px 20px !important;
        box-shadow: 0 6px 0px #7f1d1d;
    }
    .stButton>button:active {
        transform: translateY(4px);
        box-shadow: 0 2px 0px #7f1d1d;
    }
    </style>
""", unsafe_allow_html=True)

# Pokémon Rangen & Level Drempels
LEVELS = [
    {"level": 1, "naam": "⚡ Pikachu Trainer", "xp_nodig": 0, "avatar": "⚡"},
    {"level": 2, "naam": "🔥 Charmeleon Gym-Uitdager", "xp_nodig": 20, "avatar": "🦎"},
    {"level": 3, "naam": "🌊 Blastoise Reken-Master", "xp_nodig": 50, "avatar": "🐢"},
    {"level": 4, "naam": "🐉 Dragonite Elite Four", "xp_nodig": 100, "avatar": "🐉"},
    {"level": 5, "naam": "👑 Mewtwo Reken-Champion", "xp_nodig": 200, "avatar": "🔮"}
]

def bereken_level_info(totale_xp):
    huidige_lvl = LEVELS[0]
    volgende_lvl = LEVELS[1]
    
    for i in range(len(LEVELS) - 1):
        if totale_xp >= LEVELS[i]["xp_nodig"]:
            huidige_lvl = LEVELS[i]
            volgende_lvl = LEVELS[i + 1] if (i + 1) < len(LEVELS) else LEVELS[i]
            
    if totale_xp >= LEVELS[-1]["xp_nodig"]:
        huidige_lvl = LEVELS[-1]
        volgende_lvl = LEVELS[-1]
        
    return huidige_lvl, volgende_lvl

# UITDAGENDE SOM-GENERATOR (10-JARIGEN)
def genereer_uitdagende_som(modus, level):
    if modus == "⚡ Pikachu Battle (Tafels Pro)":
        if level == 1:
            n1, n2 = random.randint(6, 12), random.randint(4, 12)
        elif level == 2:
            n1, n2 = random.randint(11, 15), random.randint(6, 12)
        elif level == 3:
            n1, n2 = random.randint(12, 20), random.randint(8, 15)
        else:
            n1, n2 = random.randint(15, 25), random.randint(12, 20)
        return f"{n1} × {n2}", n1 * n2

    elif modus == "🔥 Charizard Attack (Complex Plus & Min)":
        if level == 1:
            n1, n2 = random.randint(25, 80), random.randint(15, 60)
            return f"{n1} + {n2}", n1 + n2
        elif level == 2:
            n1, n2, n3 = random.randint(40, 150), random.randint(20, 90), random.randint(10, 50)
            return f"{n1} + {n2} - {n3}", n1 + n2 - n3
        elif level == 3:
            n1, n2 = random.randint(100, 300), random.randint(50, 200)
            return f"{n1} + {n2}", n1 + n2
        else:
            n1, n2, n3 = random.randint(150, 500), random.randint(100, 350), random.randint(50, 200)
            return f"{n1} + {n2} - {n3}", n1 + n2 - n3

    else:  # 🌊 Blastoise Delingen
        if level == 1:
            ans, n2 = random.randint(6, 12), random.randint(4, 12)
        elif level == 2:
            ans, n2 = random.randint(10, 15), random.randint(6, 12)
        else:
            ans, n2 = random.randint(12, 25), random.randint(8, 15)
        return f"{ans * n2} ÷ {n2}", ans

# Sessie variabelen
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "juiste_antwoorden" not in st.session_state:
    st.session_state.juiste_antwoorden = 0
if "totale_vragen" not in st.session_state:
    st.session_state.totale_vragen = 0
if "huidige_som" not in st.session_state:
    st.session_state.huidige_som = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "gestart" not in st.session_state:
    st.session_state.gestart = False

# ---------------- ADMIN SIDEBAR ----------------
st.sidebar.title("👑 Gym Leader Admin")
if not st.session_state.is_admin:
    u = st.sidebar.text_input("Trainer Name", key="au")
    p = st.sidebar.text_input("Passcode", type="password", key="ap")
    if st.sidebar.button("Inloggen als Gym Leader"):
        if u == "admin" and p == "admin123":
            st.session_state.is_admin = True
            st.sidebar.success("Welkom Gym Leader!")
            st.rerun()
        else:
            st.sidebar.error("Foute Passcode!")
else:
    st.sidebar.success("Ingelogd als Gym Leader")
    if st.sidebar.button("Uitloggen"):
        st.session_state.is_admin = False
        st.rerun()

st.title("🔴 POKÉMON REKEN-GYM ⚡")

# ---------------- BEREKEN & TONEN LEVEL STATUS ----------------
huidige_lvl, volgende_lvl = bereken_level_info(st.session_state.xp)

st.markdown(f"""
<div class="pokeball-card">
    <div class="level-badge">LEVEL {huidige_lvl['level']} BADGE</div>
    <h2 style="margin: 5px 0; font-size: 1.8rem; color: #111827;">{huidige_lvl['avatar']} {huidige_lvl['naam']}</h2>
    <h3 style="margin: 0; color: #dc2626;">🔴 Verdiende Pokéballen: <b>{st.session_state.xp} XP</b></h3>
</div>
""", unsafe_allow_html=True)

# Voortgangsbalk naar volgend level
if huidige_lvl['level'] < 5:
    xp_in_dit_level = st.session_state.xp - huidige_lvl['xp_nodig']
    xp_nodig_in_dit_level = meervoud = volgende_lvl['xp_nodig'] - huidige_lvl['xp_nodig']
    voortgang = min(max(xp_in_dit_level / xp_nodig_in_dit_level, 0.0), 1.0)
    st.write(f"**Evolutie-Voortgang naar Level {volgende_lvl['level']} ({volgende_lvl['naam']}):**")
    st.progress(voortgang)
    st.caption(f"Nog {volgende_lvl['xp_nodig'] - st.session_state.xp} Pokéballen (XP) nodig voor de volgende Evolutie!")
else:
    st.success("🎉 GEEVENAARD! Je bent de absolute Pokémon Champion van de Reken-Gym!")

st.divider()

# ---------------- STARTSCHERM ----------------
if not st.session_state.gestart:
    st.subheader("🎒 Kies je Trainer-Uitdaging:")
    naam = st.text_input("Wat is je Trainer Naam?", value="Ash Ketchum")
    modus = st.selectbox("Welke Battle kies je?", [
        "⚡ Pikachu Battle (Tafels Pro)", 
        "🔥 Charizard Attack (Complex Plus & Min)", 
        "🌊 Blastoise Delingen"
    ])
    
    if st.button("🔴 KIES JOUW POKÉMON & START BATTLE!", use_container_width=True):
        st.session_state.speler_naam = naam
        st.session_state.gekozen_modus = modus
        st.session_state.gestart = True
        st.rerun()

# ---------------- SPEELSCHERM ----------------
else:
    st.subheader(f"🧢 Trainer: {st.session_state.speler_naam} | ⚔️ Gym Level {huidige_lvl['level']}")
    
    # Genereer som op basis van HUIDIGE LEVEL
    if st.session_state.huidige_som is None:
        modus = st.session_state.get("gekozen_modus", "⚡ Pikachu Battle (Tafels Pro)")
        st.session_state.huidige_som = genereer_uitdagende_som(modus, huidige_lvl['level'])

    som_tekst, juist_ans = st.session_state.huidige_som
    st.markdown(f'<div class="som-card">{som_tekst} = ?</div>', unsafe_allowed_html=True)

    ans_invoer = st.number_input("Typ je antwoord en val aan:", step=1, value=None, key=f"q_{st.session_state.totale_vragen}")

    if st.button("💥 GEBRUIK REKEN-AANVAL! ⚡", use_container_width=True):
        if ans_invoer is not None:
            st.session_state.totale_vragen += 1
            oude_lvl = huidige_lvl['level']
            
            if ans_invoer == juist_ans:
                st.session_state.juiste_antwoorden += 1
                st.session_state.xp += 1  # 1 Pokéball per goed antwoord!
                
                # Check voor Level Up / Evolutie!
                nieuwe_lvl, _ = bereken_level_info(st.session_state.xp)
                if nieuwe_lvl['level'] > oude_lvl:
                    st.balloons()
                    st.snow()
                    st.toast(f"🎉 EVOLUTIE! Je bent geëvolueerd naar Level {nieuwe_lvl['level']} ({nieuwe_lvl['naam']})!", icon="🔴")
                else:
                    st.toast("⚡ AANVAL GESLAAGD! +1 Pokéball gevangen! 🔴", icon="⭐")
            else:
                st.toast(f"❌ AANVAL GEMIST! Het juiste antwoord was {juist_ans}.", icon="💡")

            # Cloud Opslag in Supabase
            try:
                supabase.table("scores").insert({
                    "naam": st.session_state.speler_naam,
                    "score": st.session_state.xp,
                    "totaal": st.session_state.totale_vragen,
                    "modus": st.session_state.gekozen_modus
                }).execute()
            except Exception:
                pass

            st.session_state.huidige_som = None
            st.rerun()

    if st.button("🛑 Stop & Sla Battle op"):
        st.session_state.gestart = False
        st.rerun()

# ---------------- ADMIN DASHBOARD ----------------
if st.session_state.is_admin:
    st.divider()
    st.subheader("📊 Gym Leader Dashboard (Live Trainer Scores)")
    try:
        res = supabase.table("scores").select("id, created_at, naam, score, totaal, modus").order("id", desc=True).execute()
        if res.data:
            st.dataframe(res.data, use_container_width=True)
            if st.button("🗑️ Wis Alle Trainer Scores"):
                supabase.table("scores").delete().neq("id", 0).execute()
                st.success("Alle scores gewist!")
                st.rerun()
        else:
            st.info("Nog geen scores in de database.")
    except Exception as e:
        st.error(f"Fout bij het ophalen van gegevens: {e}")
