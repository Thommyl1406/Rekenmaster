import streamlit as st
import random
from supabase import create_client

# -------------------------------------------------------------
# JOUW UNIEKE SUPABASE CLOUD GEGEVENS
# -------------------------------------------------------------
SUPABASE_URL = "https://iwootoqaieisilkylotg.supabase.co"
SUPABASE_KEY = "sb_publishable_dAOMuXRA6lUMrPbieCpcVA_VMWQCSs-"

# Initialiseer de cloud-database
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="RekenMaster Arcade Cloud", page_icon="🎮", layout="centered")

# Sessie-variabelen instellen
if "score" not in st.session_state:
    st.session_state.score = 0
if "vraag_index" not in st.session_state:
    st.session_state.vraag_index = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "huidige_som" not in st.session_state:
    st.session_state.huidige_som = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# ---------------- ZIJBALK: ADMIN LOGIN ----------------
st.sidebar.title("👑 Beheerderspaneel")

if not st.session_state.is_admin:
    st.sidebar.subheader("Admin Login")
    admin_user = st.sidebar.text_input("Gebruikersnaam", key="admin_u")
    admin_pass = st.sidebar.text_input("Wachtwoord", type="password", key="admin_p")
    
    if st.sidebar.button("Inloggen als Admin"):
        # INSTELBAAR WACHTWOORD EN GEBRUIKERSNAAM:
        if admin_user == "admin" and admin_pass == "admin123":
            st.session_state.is_admin = True
            st.sidebar.success("Succesvol ingelogd!")
            st.rerun()
        else:
            st.sidebar.error("Onjuiste gegevens!")
else:
    st.sidebar.success("🔑 Ingelogd als Admin")
    if st.sidebar.button("Uitloggen"):
        st.session_state.is_admin = False
        st.rerun()

st.title("🎮 RekenMaster Arcade Online")

# ---------------- SCHERM 1: INSTELLINGEN ----------------
if st.session_state.vraag_index == 0 and not st.session_state.game_over:
    st.subheader("Welkom! Stel je quiz in:")
    naam = st.text_input("Vul je naam in:", value="Alex")
    modus = st.selectbox("Kies een oefening:", [
        "Maaltafels (t/m 100)", 
        "Optellen & Aftrekken", 
        "Deeltafels (t/m 100)"
    ])
    totaal_vragen = st.radio("Aantal vragen:", [10, 20, 50], index=0, horizontal=True)

    if st.button("🚀 START QUIZ", use_container_width=True):
        st.session_state.speler_naam = naam
        st.session_state.gekozen_modus = modus
        st.session_state.totaal_vragen = totaal_vragen
        st.session_state.vraag_index = 1
        st.session_state.score = 0
        st.rerun()

# ---------------- SCHERM 2: SPEELSCHERM ----------------
elif st.session_state.vraag_index > 0 and not st.session_state.game_over:
    totaal = st.session_state.totaal_vragen
    huidige = st.session_state.vraag_index
    modus = st.session_state.gekozen_modus

    st.write(f"**Vraag {huidige} van {totaal}**")
    st.progress(huidige / totaal)

    # Som genereren
    if st.session_state.huidige_som is None:
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
    st.header(f"{som_tekst} = ?")

    antwoord_invoer = st.number_input("Jouw antwoord:", step=1, value=None, key=f"q_{huidige}")

    if st.button("BEVESTIG ANTWOORD ➔", use_container_width=True):
        if antwoord_invoer is not None:
            if antwoord_invoer == juist_ans:
                st.session_state.score += 1
                st.success("Goed zo! 🎉")
            else:
                st.error(f"Helaas! Het juiste antwoord was {juist_ans}.")

            st.session_state.huidige_som = None
            if huidige < totaal:
                st.session_state.vraag_index += 1
            else:
                st.session_state.game_over = True
            st.rerun()

# ---------------- SCHERM 3: EINDRESULTAAT & CLOUD OPSLAG ----------------
elif st.session_state.game_over:
    st.balloons()
    score = st.session_state.score
    totaal = st.session_state.totaal_vragen
    pct = round((score / totaal) * 100)

    st.subheader(f"🏆 Challenge Voltooid! Score: {score} / {totaal} ({pct}%)")

    # Eenmalig opslaan in Supabase Cloud
    if "opgeslagen" not in st.session_state:
        try:
            supabase.table("scores").insert({
                "naam": st.session_state.speler_naam,
                "score": score,
                "totaal": totaal,
                "modus": st.session_state.gekozen_modus
            }).execute()
            st.session_state.opgeslagen = True
            st.success("Je resultaat is opgeslagen in de cloud! ☁️")
        except Exception:
            st.warning("Let op: Zorg dat de tabel 'scores' aanwezig is in Supabase.")

    if st.button("Opnieuw Spelen 🔄", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# ---------------- EXCLUSIEF ADMIN DASHBOARD ----------------
st.divider()

if st.session_state.is_admin:
    st.subheader("📊 Admin Live Cloud Dashboard")
    try:
        res = supabase.table("scores").select("id, created_at, naam, score, totaal, modus").order("id", desc=True).execute()
        if res.data:
            st.dataframe(res.data, use_container_width=True)
            
            # Mogelijkheid om de database te wissen als Admin
            if st.button("🗑️ Wis Alle Scores uit Cloud"):
                supabase.table("scores").delete().neq("id", 0).execute()
                st.success("Alle scores zijn gewist!")
                st.rerun()
        else:
            st.info("Er staan momenteel geen scores in de database.")
    except Exception as e:
        st.error(f"Fout bij het ophalen van gegevens: {e}")
else:
    st.info("🔒 Log in via de linkerzijbalk als Admin om de volledige live scorelijst te bekijken.")
