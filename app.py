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

# Custom CSS voor leesbaarheid en Pokémon-stijl
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

# POKÉMON AFBEELDINGEN URLs
POKEMON_IMG = {
    "Pikachu": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
    "Charizard": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png",
    "Blastoise": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/9.png",
    "Mewtwo": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/150.png"
}

# LEVEL-DREMPELS
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

# GEMENGDE SOM-GENERATOR
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

# IMPOSTOR PUZZEL GENERATOR
def genereer_impostor_puzzel(level):
    pika = random.randint(10, 25)
    chari = random.randint(15, 30)
    blast = random.randint(6, 15)
    
    ans1 = pika + chari
    ans2 = chari * blast
    ans3 = (chari + pika) - blast
    
    impostor = ans2
    return pika, chari, blast, ans1, ans2, ans3, impostor

# Sessie variabelen
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "sommen_teller" not in st.session_state:
    st.session_state.sommen_teller = 0
if "vraag_id" not in st.session_state:
    st.session_state.vraag_id = 0
if "huidige_som" not in st.session_state:
    st.session_state.huidige_som = None
if "huidige_impostor" not in st.session_state:
    st.session_state.huidige_impostor = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "ingelogd" not in st.session_state:
    st.session_state.ingelogd = False
if "speler_naam" not in st.session_state:
    st.session_state.speler_naam = ""

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

    # Bovensectie met spelersstatus & Pokémon-afbeelding
    c_img, c_info = st.columns([1, 3])
    with c_img:
        st.image(huidige_lvl["img"], width=100)
    with c_info:
        st.markdown(f"### GYM LEVEL {huidige_lvl['level']}: {huidige_lvl['naam']}")
        st.markdown(f"🔴 Trainer: **{st.session_state.speler_naam.capitalize()}** | Totaal XP: **{st.session_state.xp} XP**")

    # Voortgangsbalk naar volgend level
    if huidige_lvl['level'] < 5:
        xp_in_dit_level = st.session_state.xp - huidige_lvl['xp_nodig']
        xp_nodig_in_dit_level = volgende_lvl['xp_nodig'] - huidige_lvl['xp_nodig']
        voortgang = min(max(xp_in_dit_level / xp_nodig_in_dit_level, 0.0), 1.0)
        st.progress(voortgang)
        st.caption(f"Nog {volgende_lvl['xp_nodig'] - st.session_state.xp} XP nodig voor Level {volgende_lvl['level']}!")
    else:
        st.success("🎉 Je bent de absolute Pokémon Champion!")

    st.divider()

    # ---------------- NA ELKE 10 SOMMEN: VERPLICHTE VISUELE IMPOSTOR PUZZEL ----------------
    if st.session_state.sommen_teller >= 10:
        st.subheader("🕵️ VERPLICHTE CHALLENGE: ONTMASKER DE IMPOSTOR!")
        st.write("Los de Pokémon-afbeeldingen puzzel op om weer door te gaan!")

        if st.session_state.huidige_impostor is None:
            st.session_state.huidige_impostor = genereer_impostor_puzzel(huidige_lvl['level'])

        pika, chari, blast, c1, c2, c3, imp_juist = st.session_state.huidige_impostor

        st.markdown("### 📜 Pokémon Waarden Kaart:")
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            st.image(POKEMON_IMG["Pikachu"], width=60)
            st.write(f"**Pikachu = {pika}**")
        with col_p2:
            st.image(POKEMON_IMG["Charizard"], width=60)
            st.write(f"**Charizard = {chari}**")
        with col_p3:
            st.image(POKEMON_IMG["Blastoise"], width=60)
            st.write(f"**Blastoise = {blast}**")

        st.divider()

        with st.form(key=f"imp_form_{st.session_state.vraag_id}", clear_on_submit=True):
            a1 = st.number_input(f"1) Pikachu ({pika}) + Charizard ({chari}) = ?", step=1)
            a2 = st.number_input(f"2) Charizard ({chari}) × Blastoise ({blast}) = ?", step=1)
            a3 = st.number_input(f"3) (Charizard + Pikachu) - Blastoise = ?", step=1)
            imp_gekozen = st.number_input("🚨 Welke uitkomst is de GROOTSTE (De Impostor)?", step=1)

            if st.form_submit_button("🔥 ONTMASKER EN GA DOOR!"):
                if a1 == c1 and a2 == c2 and a3 == c3 and imp_gekozen == imp_juist:
                    st.balloons()
                    st.session_state.xp += 2
                    st.session_state.sommen_teller = 0
                    st.session_state.huidige_impostor = None
                    st.session_state.vraag_id += 1
                    
                    try:
                        supabase.table("players").update({"xp": st.session_state.xp}).eq("naam", st.session_state.speler_naam).execute()
                    except Exception:
                        pass

                    st.toast("🎉 GEWELDIG! Puzzel opgelost! +2 XP verdiend! 🔴", icon="⭐")
                    st.rerun()
                else:
                    st.toast("❌ Niet alle antwoorden kloppen nog! Reken goed na.", icon="💡")

    # ---------------- REGULIERE GEMENGDE SOMMEN (10 STUKS) ----------------
    else:
        st.write(f"**Ronde Voortgang: Vraag {st.session_state.sommen_teller + 1} van 10**")
        st.progress((st.session_state.sommen_teller + 1) / 10)

        if st.session_state.huidige_som is None:
            st.session_state.huidige_som = genereer_gemengde_som(huidige_lvl['level'])

        som_tekst, juist_ans = st.session_state.huidige_som
        st.markdown(f'<div class="som-card">{som_tekst} = ?</div>', unsafe_allow_html=True)

        # HET GEHEIM VOOR DIRECTE FOCUS: EEN UNIEKE KEY PER VRAAG
        with st.form(key=f"reken_form_{st.session_state.vraag_id}", clear_on_submit=True):
            ans_invoer = st.number_input(
                "Typ je antwoord (en druk op Enter):", 
                step=1, 
                value=None, 
                key=f"input_box_{st.session_state.vraag_id}"
            )
            submitted = st.form_submit_button("💥 GEBRUIK REKEN-AANVAL! ⚡")

            if submitted:
                if ans_invoer is not None:
                    oude_lvl = huidige_lvl['level']
                    
                    if ans_invoer == juist_ans:
                        st.session_state.xp += 1
                        st.session_state.sommen_teller += 1
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

                    # Verhoog de vraag_id zodat Streamlit het volgende invoerveld direct focust
                    st.session_state.vraag_id += 1
                    st.session_state.huidige_som = None
                    st.rerun()

    st.divider()
    if st.button("🚪 Uitloggen & Voortgang Bewaren"):
        st.session_state.ingelogd = False
        st.session_state.huidige_som = None
        st.session_state.huidige_impostor = None
        st.session_state.sommen_teller = 0
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
                st.success("Alle spelers gewist!")
                st.rerun()
        else:
            st.info("Nog geen geregistreerde spelers in de database.")
    except Exception as e:
        st.error(f"Fout bij ophalen spelers: {e}")
