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

st.set_page_config(page_title="🔴 Pokémon Reken-Gym Pro", page_icon="🔴", layout="centered")

# Custom CSS voor perfecte leesbaarheid en Pokémon-stijl
st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        color: #ffffff;
    }
    .pokeball-card {
        background-color: #ffffff !important;
        border: 4px solid #facc15;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.6);
        color: #000000 !important;
        margin-bottom: 25px;
    }
    .level-badge {
        background-color: #ef4444;
        color: #ffffff;
        font-weight: bold;
        padding: 6px 18px;
        border-radius: 50px;
        font-size: 1.2rem;
        display: inline-block;
        margin-bottom: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .som-card {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        border: 4px solid #facc15;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: #ffffff !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    .impostor-box {
        background-color: #ffffff;
        color: #000000;
        border: 3px solid #ef4444;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
    }
    .stButton>button, .stFormSubmitButton>button {
        background: linear-gradient(90deg, #dc2626 0%, #991b1b 100%) !important;
        color: #ffffff !important;
        font-size: 1.4rem !important;
        font-weight: bold !important;
        border-radius: 14px !important;
        border: 3px solid #facc15 !important;
        padding: 12px 20px !important;
        box-shadow: 0 6px 0px #7f1d1d;
        width: 100% !important;
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

# AUTOMATISCHE GEMENGDE SOM-GENERATOR
def genereer_gemengde_som(level):
    keuze = random.choice(["maal", "deel", "plusmin"])
    
    if keuze == "maal":
        if level == 1:
            n1, n2 = random.randint(6, 12), random.randint(4, 12)
        elif level == 2:
            n1, n2 = random.randint(11, 15), random.randint(6, 12)
        elif level == 3:
            n1, n2 = random.randint(12, 20), random.randint(8, 15)
        else:
            n1, n2 = random.randint(15, 25), random.randint(12, 20)
        return f"{n1} × {n2}", n1 * n2

    elif keuze == "plusmin":
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

    else: # Delen
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
if "huidige_som" not in st.session_state:
    st.session_state.huidige_som = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "ingelogd" not in st.session_state:
    st.session_state.ingelogd = False
if "speler_naam" not in st.session_state:
    st.session_state.speler_naam = ""
if "modus" not in st.session_state:
    st.session_state.modus = "normaal"

# ---------------- ADMIN SIDEBAR ----------------
st.sidebar.title("👑 Gym Leader Admin")
if not st.session_state.is_admin:
    u = st.sidebar.text_input("Admin Name", key="au")
    p = st.sidebar.text_input("Passcode", type="password", key="ap")
    if st.sidebar.button("Inloggen als Admin"):
        if u == "admin" and p == "admin123":
            st.session_state.is_admin = True
            st.sidebar.success("Welkom Admin!")
            st.rerun()
        else:
            st.sidebar.error("Foute Passcode!")
else:
    st.sidebar.success("Ingelogd als Admin")
    if st.sidebar.button("Uitloggen Admin"):
        st.session_state.is_admin = False
        st.rerun()

st.title("🔴 POKÉMON REKEN-GYM ⚡")

# ---------------- INLOG- & REGISTRATIESCHERM ----------------
if not st.session_state.ingelogd:
    st.subheader("🎒 Trainer Inloggen / Registreren")
    
    inlog_naam = st.text_input("Wat is je Trainer Naam?").strip().lower()
    inlog_code = st.text_input("Vul een geheime 4-cijferige Pincode in:", type="password", max_chars=4)

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 INLOGGEN", use_container_width=True):
            if inlog_naam and inlog_code:
                try:
                    res = supabase.table("players").select("*").eq("naam", inlog_naam).execute()
                    if res.data:
                        speler_data = res.data[0]
                        if str(speler_data["pincode"]) == str(inlog_code):
                            st.session_state.speler_naam = inlog_naam
                            st.session_state.xp = speler_data["xp"]
                            st.session_state.ingelogd = True
                            st.success(f"Welkom terug {inlog_naam.capitalize()}!")
                            st.rerun()
                        else:
                            st.error("Onjuiste pincode voor deze trainer!")
                    else:
                        st.warning("Trainer niet gevonden. Klik op 'Nieuw Account Maken'.")
                except Exception as e:
                    st.error(f"Fout bij inloggen: {e}")
            else:
                st.warning("Vul zowel een naam als pincode in.")

    with col2:
        if st.button("✨ NIEUW ACCOUNT MAKEN", use_container_width=True):
            if inlog_naam and inlog_code:
                try:
                    res = supabase.table("players").select("*").eq("naam", inlog_naam).execute()
                    if res.data:
                        st.error("Deze naam bestaat al! Kies een andere naam of log in.")
                    else:
                        supabase.table("players").insert({
                            "naam": inlog_naam,
                            "pincode": str(inlog_code),
                            "xp": 0
                        }).execute()
                        st.session_state.speler_naam = inlog_naam
                        st.session_state.xp = 0
                        st.session_state.ingelogd = True
                        st.success("Account aangemaakt! Veel succes met je training!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Fout bij maken account: {e}")
            else:
                st.warning("Vul een naam en 4-cijferige pincode in.")

# ---------------- SPEELSCHERM ----------------
else:
    huidige_lvl, volgende_lvl = bereken_level_info(st.session_state.xp)

    # Bovensectie met spelersstatus
    st.markdown(f"""
    <div class="pokeball-card">
        <div class="level-badge">GYM LEVEL {huidige_lvl['level']}</div>
        <h2 style="margin: 8px 0; font-size: 2rem; color: #000000;">{huidige_lvl['avatar']} {huidige_lvl['naam']}</h2>
        <h3 style="margin: 0; color: #dc2626; font-size: 1.4rem;">🔴 Trainer: <b>{st.session_state.speler_naam.capitalize()}</b> | Totaal XP: <b>{st.session_state.xp} XP</b></h3>
    </div>
    """, unsafe_allow_html=True)

    # Schakelen tussen Normale Modus en Impostor-Puzzel
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        if st.button("⚔️ Normale Battle", use_container_width=True):
            st.session_state.modus = "normaal"
            st.rerun()
    with col_m2:
        if st.button("🕵️ Ontmasker de Impostor!", use_container_width=True):
            st.session_state.modus = "impostor"
            st.rerun()

    st.divider()

    # ---------------- MODUS 1: NORMAAL REKENEN ----------------
    if st.session_state.modus == "normaal":
        # Genereer automatisch een gemengde som
        if st.session_state.huidige_som is None:
            st.session_state.huidige_som = genereer_gemengde_som(huidige_lvl['level'])

        som_tekst, juist_ans = st.session_state.huidige_som
        st.markdown(f'<div class="som-card">{som_tekst} = ?</div>', unsafe_allow_html=True)

        with st.form(key=f"reken_form_{st.session_state.xp}", clear_on_submit=True):
            ans_invoer = st.number_input("Typ je antwoord (en druk op Enter):", step=1, value=None)
            submitted = st.form_submit_button("💥 GEBRUIK REKEN-AANVAL! ⚡")

            if submitted:
                if ans_invoer is not None:
                    oude_lvl = huidige_lvl['level']
                    
                    if ans_invoer == juist_ans:
                        st.session_state.xp += 1  # 1 XP per goed antwoord!
                        st.toast("⚡ AANVAL GESLAAGD! +1 XP opgeslagen! 🔴", icon="⭐")
                        
                        try:
                            supabase.table("players").update({"xp": st.session_state.xp}).eq("naam", st.session_state.speler_naam).execute()
                        except Exception:
                            pass

                        nieuwe_lvl, _ = bereken_level_info(st.session_state.xp)
                        if nieuwe_lvl['level'] > oude_lvl:
                            st.balloons()
                            st.snow()
                            st.toast(f"🎉 EVOLUTIE! Je bent geëvolueerd naar Level {nieuwe_lvl['level']} ({nieuwe_lvl['naam']})!", icon="🔴")
                    else:
                        st.toast(f"❌ AANVAL GEMIST! Het juiste antwoord was {juist_ans}.", icon="💡")

                    st.session_state.huidige_som = None
                    st.rerun()

    # ---------------- MODUS 2: IMPOSTOR PUZZEL (PICO-CODE) ----------------
    else:
        st.subheader("🕵️ ONTMASKER DE IMPOSTOR!")
        st.write("Bereken de waarden van de Pokémon en vind het antwoord dat de **IMPOSTOR** is!")

        # Vaste getallen per Pokémon
        pika = 12
        chari = 25
        blast = 8
        mew = 50

        st.markdown("""
        <div class="impostor-box">
            <h4>📜 Pokémon Waarden Kaart:</h4>
            <b>⚡ Pikachu</b> = 12 &nbsp;&nbsp;|&nbsp;&nbsp; 
            <b>🔥 Charizard</b> = 25 &nbsp;&nbsp;|&nbsp;&nbsp; 
            <b>🌊 Blastoise</b> = 8 &nbsp;&nbsp;|&nbsp;&nbsp; 
            <b>🔮 Mewtwo</b> = 50
        </div>
        """, unsafe_allow_html=True)

        st.write("### ❓ Los de Puzzels op:")
        
        # Puzzel 1: Pikachu + Charizard
        ans1 = st.number_input("1) ⚡ Pikachu + 🔥 Charizard = ?", step=1, key="imp_1")
        # Puzzel 2: Mewtwo - Blastoise
        ans2 = st.number_input("2) 🔮 Mewtwo - 🌊 Blastoise = ?", step=1, key="imp_2")
        # Puzzel 3: Charizard × Blastoise
        ans3 = st.number_input("3) 🔥 Charizard × 🌊 Blastoise = ?", step=1, key="imp_3")

        st.write("---")
        impostor_keuze = st.number_input("🚨 Welke van de bovenstaande uitkomsten is gelijk aan 42? (De Impostor)", step=1, key="imp_ans")

        if st.button("🔥 CONTROLEER IMPOSTOR PUZZEL", use_container_width=True):
            corr1 = pika + chari  # 37
            corr2 = mew - blast   # 42  <-- Impostor!
            corr3 = chari * blast # 200

            if ans1 == corr1 and ans2 == corr2 and ans3 == corr3 and impostor_keuze == 42:
                st.balloons()
                st.session_state.xp += 5
                try:
                    supabase.table("players").update({"xp": st.session_state.xp}).eq("naam", st.session_state.speler_naam).execute()
                except Exception:
                    pass
                st.success("🎉 GEWELDIG! Je hebt alle rekenpuzzels én de Impostor ontmaskerd! **+5 BONUS XP!** 🔴")
            else:
                st.error("❌ Oeps! Niet alle antwoorden waren juist. Kijk goed naar de Pokémon-waarden en reken opnieuw uit!")

    st.divider()
    if st.button("🚪 Uitloggen & Voortgang Bewaren"):
        st.session_state.ingelogd = False
        st.session_state.huidige_som = None
        st.session_state.modus = "normaal"
        st.rerun()

# ---------------- ADMIN DASHBOARD ----------------
if st.session_state.is_admin:
    st.divider()
    st.subheader("📊 Gym Leader Admin Dashboard (Alle Spelers)")
    try:
        res = supabase.table("players").select("id, naam, xp, pincode").order("xp", desc=True).execute()
        if res.data:
            st.dataframe(res.data, use_container_width=True)
            if st.button("🗑️ Wis Alle Spelers & Voortgang"):
                supabase.table("players").delete().neq("id", 0).execute()
                st.success("Alle scores gewist!")
                st.rerun()
        else:
            st.info("Nog geen geregistreerde spelers in de database.")
    except Exception as e:
        st.error(f"Fout bij ophalen spelers: {e}")
