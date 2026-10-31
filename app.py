import streamlit as st
import random
from supabase import create_client

# -------------------------------------------------------------
# SUPABASE CLOUD GEGEVENS
# -------------------------------------------------------------
SUPABASE_URL = "https://iwootoqaieisilkylotg.supabase.co"
SUPABASE_KEY = "sb_publishable_dAOMuXRA6lUMrPbieCpcVA_VMWQCSs-"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="🔴 Pokémon Reken-Gym Pro", page_icon="🔴", layout="centered")

# Custom CSS
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
        background-color: #ef4444; color: #ffffff; font-weight: bold;
        padding: 6px 18px; border-radius: 50px; font-size: 1.2rem;
        display: inline-block; margin-bottom: 10px;
    }
    .som-card {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        border: 4px solid #facc15; border-radius: 20px; padding: 25px;
        text-align: center; font-size: 3.5rem; font-weight: bold;
        color: #ffffff !important; box-shadow: 0 8px 20px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    .hint-box {
        background-color: #1e293b;
        border: 2px dashed #facc15;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        text-align: center;
        font-size: 1.2rem;
    }
    
    .stForm label, div[data-testid="stForm"] p {
        color: #ffffff !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
    }

    div[data-testid="stChatInput"] textarea,
    div[data-testid="stChatInput"] input,
    .stTextInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-size: 1.8rem !important;
        font-weight: 900 !important;
        border: 3px solid #facc15 !important;
        border-radius: 14px !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder,
    .stTextInput input::placeholder {
        color: #64748b !important;
        -webkit-text-fill-color: #64748b !important;
        font-size: 1.2rem !important;
        font-weight: normal !important;
    }

    div[data-testid="stToast"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 2px solid #facc15 !important;
        border-radius: 12px !important;
    }
    div[data-testid="stToast"] p, div[data-testid="stToast"] div {
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #dc2626 0%, #991b1b 100%) !important;
        color: #ffffff !important; font-size: 1.4rem !important;
        font-weight: bold !important; border-radius: 14px !important;
        border: 3px solid #facc15 !important; padding: 12px 20px !important;
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

POKEMON_IMG = {
    "Pikachu": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
    "Charizard": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png",
    "Blastoise": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/9.png",
    "Mewtwo": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/150.png"
}

LEVELS = [
    {"level": 1, "naam": "Pikachu Trainer", "xp_nodig": 0, "img": POKEMON_IMG["Pikachu"]},
    {"level": 2, "naam": "Charmeleon Gym-Uitdager", "xp_nodig": 50, "img": POKEMON_IMG["Charizard"]},
    {"level": 3, "naam": "Blastoise Reken-Master", "xp_nodig": 120, "img": POKEMON_IMG["Blastoise"]},
    {"level": 4, "naam": "Dragonite Elite Four", "xp_nodig": 250, "img": POKEMON_IMG["Charizard"]},
    {"level": 5, "naam": "Mewtwo Reken-Champion", "xp_nodig": 500, "img": POKEMON_IMG["Mewtwo"]}
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

# INCLUSIEF TIENTALLEN EN HONDERDTALLEN (X10, X100, :10, :100)
def genereer_gemengde_som(level):
    keuze = random.choice(["maal", "deel", "plusmin", "breuk", "tientallen"])
    
    if keuze == "maal":
        n1 = random.randint(2, 9) if level == 1 else random.randint(3, 10) if level == 2 else random.randint(6, 12)
        n2 = random.randint(2, 9) if level == 1 else random.randint(3, 10)
        hint = f"💡 Denk aan: {n1} groepen van {n2}"
        return f"{n1} × {n2}", n1 * n2, "maal", hint

    elif keuze == "plusmin":
        if level == 1:
            n1, n2 = random.randint(15, 50), random.randint(10, 40)
            return f"{n1} + {n2}", n1 + n2, "plusmin", f"💡 Tel eerst de tientallen op, dan de eenheden!"
        else:
            n1 = random.randint(40, 90)
            n2 = random.randint(15, 35)
            return f"{n1} - {n2}", n1 - n2, "plusmin", f"💡 Trek er eerst {n2 - (n2%10)} af, daarna de rest!"

    elif keuze == "deel":
        ans, n2 = random.randint(2, 8), random.randint(2, 5) if level == 1 else random.randint(2, 8)
        hint = f"💡 Welk getal × {n2} is gelijk aan {ans * n2}?"
        return f"{ans * n2} ÷ {n2}", ans, "deel", hint

    elif keuze == "breuk":
        opties = [("1/2", 2), ("1/4", 4), ("3/4", 4), ("1/3", 3), ("2/3", 3)]
        breuk_tekst, noemer = random.choice(opties)
        factor = random.randint(2, 8)
        totaal_getal = noemer * factor
        
        if breuk_tekst == "1/2": ans = totaal_getal // 2
        elif breuk_tekst == "1/4": ans = totaal_getal // 4
        elif breuk_tekst == "3/4": ans = (totaal_getal // 4) * 3
        elif breuk_tekst == "1/3": ans = totaal_getal // 3
        elif breuk_tekst == "2/3": ans = (totaal_getal // 3) * 2

        hint = f"💡 Verdeel {totaal_getal} eerst in {noemer} gelijke delen (elk deel is {totaal_getal // noemer})"
        return f"{breuk_tekst} van {totaal_getal}", ans, "breuk", hint

    else: # TIENTALLEN EN HONDERDTALLEN (x10, x100, :10, :100)
        sub_type = random.choice(["maal10", "maal100", "deel10", "deel100"])
        
        if sub_type == "maal10":
            n1 = random.randint(3, 45)
            return f"{n1} × 10", n1 * 10, "tientallen", "💡 Vermenigvuldigen met 10? Plak er een 0 achteraan!"
        elif sub_type == "maal100":
            n1 = random.randint(2, 9)
            return f"{n1} × 100", n1 * 100, "tientallen", "💡 Vermenigvuldigen met 100? Plak er twee nullen achteraan!"
        elif sub_type == "deel10":
            ans = random.randint(3, 50)
            return f"{ans * 10} ÷ 10", ans, "tientallen", "💡 Delen door 10? Haal er één 0 vanaf!"
        else: # deel100
            ans = random.randint(2, 9)
            return f"{ans * 100} ÷ 100", ans, "tientallen", "💡 Delen door 100? Haal er twee nullen vanaf!"

def genereer_impostor_puzzel(level):
    pika = random.randint(4, 10)
    chari = random.randint(5, 10)
    blast = random.randint(2, 6)
    c1 = pika + chari
    c2 = chari * blast
    c3 = (chari + pika) - blast
    imp_juist = max(c1, c2, c3)
    return pika, chari, blast, c1, c2, c3, imp_juist

# SESSIE VARIABELEN
if "xp" not in st.session_state: st.session_state.xp = 0
if "fouten" not in st.session_state or st.session_state.fouten is None: st.session_state.fouten = 0
if "sommen_teller" not in st.session_state: st.session_state.sommen_teller = 0
if "huidige_som" not in st.session_state: st.session_state.huidige_som = None
if "huidige_impostor" not in st.session_state: st.session_state.huidige_impostor = None
if "ingelogd" not in st.session_state: st.session_state.ingelogd = False
if "speler_naam" not in st.session_state: st.session_state.speler_naam = ""
if "is_admin" not in st.session_state: st.session_state.is_admin = False
if "fouten_per_type" not in st.session_state: st.session_state.fouten_per_type = {"maal": 0, "deel": 0, "plusmin": 0, "breuk": 0, "tientallen": 0}
if "toon_hint" not in st.session_state: st.session_state.toon_hint = False

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

# ---------------- INLOGSCHERM ----------------
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
                    if res.data and str(res.data[0]["pincode"]) == str(inlog_code):
                        d = res.data[0]
                        st.session_state.speler_naam = inlog_naam
                        st.session_state.xp = d.get("xp") or 0
                        st.session_state.fouten = d.get("fouten") or 0
                        st.session_state.ingelogd = True
                        st.rerun()
                    else: st.error("Onjuiste gegevens!")
                except Exception: st.error("Fout bij inloggen!")
    with col2:
        if st.button("✨ NIEUW ACCOUNT MAKEN", use_container_width=True):
            if inlog_naam and inlog_code:
                try:
                    supabase.table("players").insert({"naam": inlog_naam, "pincode": str(inlog_code), "xp": 0, "fouten": 0}).execute()
                    st.session_state.speler_naam = inlog_naam
                    st.session_state.xp = 0
                    st.session_state.fouten = 0
                    st.session_state.ingelogd = True
                    st.rerun()
                except Exception: st.error("Naam bestaat al!")

# ---------------- SPEELSCHERM ----------------
else:
    huidige_lvl, volgende_lvl = bereken_level_info(st.session_state.xp)

    tab_game, tab_board = st.tabs(["⚔️ Reken Battle", "🏆 Highscores"])

    with tab_game:
        c_img, c_info = st.columns([1, 3])
        with c_img: st.image(huidige_lvl["img"], width=100)
        with c_info:
            st.markdown(f"### GYM LEVEL {huidige_lvl['level']}: {huidige_lvl['naam']}")
            st.markdown(f"🔴 Trainer: **{st.session_state.speler_naam.capitalize()}** | Totaal XP: **{st.session_state.xp} XP**")

        if huidige_lvl['level'] < 5:
            xp_in_dit_level = st.session_state.xp - huidige_lvl['xp_nodig']
            xp_nodig_in_dit_level = volgende_lvl['xp_nodig'] - huidige_lvl['xp_nodig']
            st.progress(min(max(xp_in_dit_level / xp_nodig_in_dit_level, 0.0), 1.0))
            st.caption(f"Nog {volgende_lvl['xp_nodig'] - st.session_state.xp} XP nodig voor Level {volgende_lvl['level']}!")

        st.divider()

        # IMPOSTOR PUZZEL
        if st.session_state.sommen_teller >= 10:
            st.subheader("🕵️ VERPLICHTE CHALLENGE: ONTMASKER DE IMPOSTOR!")
            if st.session_state.huidige_impostor is None:
                st.session_state.huidige_impostor = genereer_impostor_puzzel(huidige_lvl['level'])

            pika, chari, blast, c1, c2, c3, imp_juist = st.session_state.huidige_impostor

            col_p1, col_p2, col_p3 = st.columns(3)
            with col_p1: st.image(POKEMON_IMG["Pikachu"], width=60); st.write(f"**Pikachu = {pika}**")
            with col_p2: st.image(POKEMON_IMG["Charizard"], width=60); st.write(f"**Charizard = {chari}**")
            with col_p3: st.image(POKEMON_IMG["Blastoise"], width=60); st.write(f"**Blastoise = {blast}**")

            with st.form(key="imp_form", clear_on_submit=True):
                a1 = st.text_input(f"1) Pikachu ({pika}) + Charizard ({chari}) = ?")
                a2 = st.text_input(f"2) Charizard ({chari}) × Blastoise ({blast}) = ?")
                a3 = st.text_input(f"3) (Charizard + Pikachu) - Blastoise = ?")
                imp_g = st.text_input("🚨 Welke uitkomst is de GROOTSTE (De Impostor)?")

                if st.form_submit_button("🔥 ONTMASKER EN GA DOOR!"):
                    try:
                        if int(a1)==c1 and int(a2)==c2 and int(a3)==c3 and int(imp_g)==imp_juist:
                            st.balloons()
                            st.session_state.xp += 2
                            st.session_state.sommen_teller = 0
                            st.session_state.huidige_impostor = None
                            supabase.table("players").update({"xp": st.session_state.xp}).eq("naam", st.session_state.speler_naam).execute()
                            st.toast("🎉 Puzzel opgelost! +2 XP verdiend!", icon="⭐")
                            st.rerun()
                        else: 
                            st.session_state.fouten = (st.session_state.fouten or 0) + 1
                            supabase.table("players").update({"fouten": st.session_state.fouten}).eq("naam", st.session_state.speler_naam).execute()
                            st.toast("❌ Niet alles klopt!", icon="💡")
                    except Exception: pass

        # REGULIERE REKENVRAGEN
        else:
            st.write(f"**Ronde Voortgang: Vraag {st.session_state.sommen_teller + 1} van 10**")
            st.progress((st.session_state.sommen_teller + 1) / 10)

            if st.session_state.huidige_som is None:
                st.session_state.huidige_som = genereer_gemengde_som(huidige_lvl['level'])

            som_tekst, juist_ans, s_type, hint_txt = st.session_state.huidige_som
            st.markdown(f'<div class="som-card">{som_tekst} = ?</div>', unsafe_allow_html=True)

            if st.session_state.toon_hint:
                st.markdown(f'<div class="hint-box">{hint_txt}</div>', unsafe_allow_html=True)
            else:
                if st.button("💡 Gebruik Hint"):
                    st.session_state.toon_hint = True
                    st.rerun()

            invoer_antwoord = st.chat_input("Typ je antwoord hier en druk op Enter...")

            if invoer_antwoord:
                try:
                    ans_invoer = int(invoer_antwoord.strip())
                    if ans_invoer == juist_ans:
                        st.session_state.xp += 1
                        st.session_state.sommen_teller += 1
                        supabase.table("players").update({"xp": st.session_state.xp}).eq("naam", st.session_state.speler_naam).execute()
                        st.toast("⚡ AANVAL GESLAAGD! +1 XP! 🔴", icon="⭐")
                    else:
                        st.session_state.fouten = (st.session_state.fouten or 0) + 1
                        st.session_state.fouten_per_type[s_type] = st.session_state.fouten_per_type.get(s_type, 0) + 1
                        supabase.table("players").update({"fouten": st.session_state.fouten}).eq("naam", st.session_state.speler_naam).execute()
                        st.toast(f"❌ GEMIST! Het antwoord was {juist_ans}.", icon="💡")

                    st.session_state.huidige_som = None
                    st.session_state.toon_hint = False
                    st.rerun()
                except ValueError:
                    st.toast("⚠️ Typ een geldig getal!", icon="⚠️")

    with tab_board:
        st.subheader("🏆 Reken-Gym Ranglijst (Top Trainers)")
        try:
            res_lb = supabase.table("players").select("naam, xp").order("xp", desc=True).limit(10).execute()
            if res_lb.data:
                for rank, speler in enumerate(res_lb.data, start=1):
                    medaille = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
                    st.markdown(f"#### {medaille} **{speler['naam'].capitalize()}** — ⭐ {speler['xp']} XP")
        except Exception:
            st.info("Ranglijst laden...")

    st.divider()
    if st.button("🚪 Uitloggen & Voortgang Bewaren"):
        st.session_state.ingelogd = False
        st.session_state.huidige_som = None
        st.session_state.sommen_teller = 0
        st.rerun()

# ---------------- ADMIN DASHBOARD ----------------
if st.session_state.is_admin:
    st.divider()
    st.subheader("📊 Gym Leader Admin Dashboard")
    try:
        res = supabase.table("players").select("id, naam, xp, fouten, pincode").order("xp", desc=True).execute()
        if res.data:
            st.dataframe(res.data, use_container_width=True)

            st.write("### 📈 Analyse Fouten per Somtype (Sessie)")
            st.json(st.session_state.fouten_per_type)

            st.write("### ⚙️ Beheer per Speler")
            spelers_lijst = [sp["naam"] for sp in res.data]
            gekozen_speler = st.selectbox("Selecteer een speler om te beheren:", spelers_lijst)

            col_res1, col_res2 = st.columns(2)
            with col_res1:
                if st.button(f"🔄 Reset Voortgang van '{gekozen_speler.capitalize()}'"):
                    supabase.table("players").update({"xp": 0, "fouten": 0}).eq("naam", gekozen_speler).execute()
                    st.success("Gereset!")
                    st.rerun()

            with col_res2:
                if st.button(f"❌ Verwijder Account '{gekozen_speler.capitalize()}'"):
                    supabase.table("players").delete().eq("naam", gekozen_speler).execute()
                    st.success("Account gewist!")
                    st.rerun()
    except Exception as e:
        st.error(f"Fout bij ophalen spelers: {e}")
