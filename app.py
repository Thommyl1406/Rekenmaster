<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🔴 Pokémon Reken-Gym Pro</title>
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
  <style>
    :root {
      --bg: #0f172a;
      --panel: #ffffff;
      --card-bg: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
      --accent: #facc15;
      --danger: #dc2626;
      --text-dark: #0f172a;
      --text-light: #ffffff;
    }

    * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    body {
      background-color: var(--bg);
      color: var(--text-light);
      margin: 0;
      padding: 20px;
      display: flex;
      justify-content: center;
      min-height: 100vh;
    }

    .container {
      width: 100%;
      max-width: 650px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .header-card {
      background: var(--panel);
      color: var(--text-dark);
      border: 4px solid var(--accent);
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      position: relative;
    }

    .top-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }

    .level-badge {
      background: var(--danger);
      color: white;
      font-weight: bold;
      padding: 6px 16px;
      border-radius: 50px;
      font-size: 0.95rem;
      text-transform: uppercase;
    }

    .player-info {
      font-size: 1.1rem;
      font-weight: 700;
      color: #334155;
    }

    .trainer-profile {
      display: flex;
      align-items: center;
      gap: 15px;
    }

    .trainer-avatar {
      width: 80px;
      height: 80px;
      object-fit: contain;
      filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));
    }

    .progress-outer {
      background: #e2e8f0;
      border-radius: 10px;
      height: 16px;
      overflow: hidden;
      margin-top: 10px;
    }
    .progress-inner {
      background: linear-gradient(90deg, #10b981, #059669);
      height: 100%;
      width: 0%;
      transition: width 0.3s ease;
    }

    .som-card {
      background: var(--card-bg);
      border: 4px solid var(--accent);
      border-radius: 20px;
      padding: 30px 20px;
      text-align: center;
      font-size: 3.5rem;
      font-weight: 900;
      letter-spacing: 2px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.5);
      text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }

    .action-card {
      background: rgba(30, 41, 59, 0.7);
      border-radius: 20px;
      padding: 20px;
      border: 1px solid rgba(255,255,255,0.1);
    }

    .input-group {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    input[type="text"], input[type="password"] {
      width: 100%;
      padding: 16px;
      font-size: 1.6rem;
      border-radius: 14px;
      border: 3px solid var(--accent);
      background: #ffffff;
      color: #0f172a;
      font-weight: bold;
      text-align: center;
      outline: none;
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    input[type="text"]:focus, input[type="password"]:focus {
      border-color: #38bdf8;
      box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.4);
    }

    .btn {
      background: linear-gradient(90deg, #dc2626 0%, #991b1b 100%);
      color: white;
      font-size: 1.3rem;
      font-weight: 800;
      border-radius: 14px;
      border: 3px solid var(--accent);
      padding: 14px;
      cursor: pointer;
      box-shadow: 0 6px 0px #7f1d1d;
      transition: transform 0.05s ease;
      width: 100%;
    }
    .btn:active {
      transform: translateY(4px);
      box-shadow: 0 2px 0px #7f1d1d;
    }
    .btn-secondary {
      background: #475569;
      box-shadow: 0 4px 0px #1e293b;
      font-size: 1rem;
      border: none;
      padding: 10px;
      margin-top: 10px;
    }

    .toast {
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%) translateY(100px);
      padding: 14px 24px;
      border-radius: 50px;
      font-weight: bold;
      font-size: 1.1rem;
      color: white;
      box-shadow: 0 10px 25px rgba(0,0,0,0.4);
      transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      z-index: 1000;
    }
    .toast.show { transform: translateX(-50%) translateY(0); }
    .toast.success { background: #10b981; }
    .toast.error { background: #ef4444; }

    .impostor-box {
      background: white;
      color: #0f172a;
      border-radius: 16px;
      padding: 20px;
      border: 4px solid var(--danger);
    }
    .impostor-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin-bottom: 15px;
      text-align: center;
    }
    .impostor-item {
      background: #f1f5f9;
      border-radius: 12px;
      padding: 10px;
    }
    .impostor-item img { width: 50px; height: 50px; object-fit: contain; }
    .impostor-inputs input {
      font-size: 1.1rem;
      padding: 8px;
      margin-bottom: 8px;
      border-width: 2px;
    }

    .hidden { display: none !important; }
  </style>
</head>
<body>

  <div class="container">
    
    <!-- AUTH SCREEN -->
    <div id="auth-screen" class="action-card">
      <h2 style="text-align: center; color: var(--accent); margin-top: 0;">🔴 POKÉMON REKEN-GYM</h2>
      <p style="text-align: center; color: #94a3b8;">Log in of maak een account om voortgang op te slaan!</p>
      
      <div class="input-group">
        <input type="text" id="auth-name" placeholder="Trainer Naam" autocomplete="off" autocorrect="off" spellcheck="false">
        <input type="password" id="auth-pin" placeholder="4-cijferige Pincode" maxlength="4" inputmode="numeric">
        <button class="btn" id="btn-login">🚀 INLOGGEN</button>
        <button class="btn btn-secondary" id="btn-register">✨ NIEUW ACCOUNT MAKEN</button>
      </div>
    </div>

    <!-- GAME SCREEN -->
    <div id="game-screen" class="hidden">
      
      <!-- HEADER STATUS -->
      <div class="header-card">
        <div class="top-bar">
          <span class="level-badge" id="lvl-badge">GYM LEVEL 1</span>
          <div class="player-info">🔴 <span id="player-name">Ash</span> | <span id="player-xp">0</span> XP</div>
        </div>
        <div class="trainer-profile">
          <img id="lvl-img" class="trainer-avatar" src="" alt="Pokemon">
          <div style="flex-grow: 1;">
            <h3 id="lvl-title" style="margin: 0 0 6px 0;">Pikachu Trainer</h3>
            <div style="font-size: 0.85rem; color: #64748b;" id="lvl-sub">Nog 50 XP tot het volgende level</div>
            <div class="progress-outer"><div id="lvl-progress" class="progress-inner"></div></div>
          </div>
        </div>
      </div>

      <!-- REGULAR MATH MODE -->
      <div id="math-mode">
        <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 8px; text-align: center;" id="round-counter">Ronde Voortgang: Vraag 1 van 10</div>
        <div class="som-card" id="som-display">12 × 8 = ?</div>
        <br>
        <form id="math-form" class="action-card">
          <div class="input-group">
            <input type="text" id="answer-input" placeholder="Typ je antwoord..." autocomplete="off" autocorrect="off" spellcheck="false" inputmode="numeric">
            <button type="submit" class="btn">💥 GEBRUIK REKEN-AANVAL!</button>
          </div>
        </form>
      </div>

      <!-- IMPOSTOR CHALLENGE MODE -->
      <div id="impostor-mode" class="hidden">
        <div class="impostor-box">
          <h3 style="margin-top: 0; color: var(--danger); text-align: center;">🕵️ ONTMASKER DE IMPOSTOR!</h3>
          <p style="font-size: 0.9rem; margin-bottom: 12px; text-align: center;">Los de puzzel op om verder te kunnen spelen!</p>
          
          <div class="impostor-grid">
            <div class="impostor-item">
              <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png" alt="Pikachu">
              <div id="imp-val1"><b>Pikachu = 12</b></div>
            </div>
            <div class="impostor-item">
              <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png" alt="Charizard">
              <div id="imp-val2"><b>Charizard = 20</b></div>
            </div>
            <div class="impostor-item">
              <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/9.png" alt="Blastoise">
              <div id="imp-val3"><b>Blastoise = 5</b></div>
            </div>
          </div>

          <form id="impostor-form" class="impostor-inputs">
            <label style="font-size: 0.85rem; font-weight: bold;" id="lbl-imp1">1) Pikachu + Charizard = ?</label>
            <input type="text" id="imp-ans1" autocomplete="off" inputmode="numeric">
            
            <label style="font-size: 0.85rem; font-weight: bold;" id="lbl-imp2">2) Charizard × Blastoise = ?</label>
            <input type="text" id="imp-ans2" autocomplete="off" inputmode="numeric">
            
            <label style="font-size: 0.85rem; font-weight: bold;" id="lbl-imp3">3) (Charizard + Pikachu) - Blastoise = ?</label>
            <input type="text" id="imp-ans3" autocomplete="off" inputmode="numeric">
            
            <label style="font-size: 0.85rem; font-weight: bold; color: var(--danger);">🚨 Welke uitkomst is de GROOTSTE (De Impostor)?</label>
            <input type="text" id="imp-ans-final" autocomplete="off" inputmode="numeric">
            
            <button type="submit" class="btn" style="margin-top: 10px;">🔥 ONTMASKER EN GA DOOR!</button>
          </form>
        </div>
      </div>

      <button class="btn btn-secondary" id="btn-logout">🚪 Uitloggen & Voortgang Bewaren</button>
    </div>

  </div>

  <div id="toast" class="toast"></div>

  <script>
    // SUPABASE CONFIGURATIE
    const SUPABASE_URL = "https://iwootoqaieisilkylotg.supabase.co";
    const SUPABASE_KEY = "sb_publishable_dAOMuXRA6lUMrPbieCpcVA_VMWQCSs-";
    const supabase = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY) : null;

    // GAME CONFIG
    const LEVELS = [
      { level: 1, name: "Pikachu Trainer", xpNeeded: 0, img: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png" },
      { level: 2, name: "Charmeleon Gym-Uitdager", xpNeeded: 50, img: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png" },
      { level: 3, name: "Blastoise Reken-Master", xpNeeded: 120, img: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/9.png" },
      { level: 4, name: "Dragonite Elite Four", xpNeeded: 250, img: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/149.png" },
      { level: 5, name: "Mewtwo Reken-Champion", xpNeeded: 500, img: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/150.png" }
    ];

    let player = { name: "", xp: 0 };
    let currentSom = { text: "", answer: 0 };
    let roundProgress = 0;
    let currentImpostor = null;

    // DOM ELEMENTS
    const authScreen = document.getElementById("auth-screen");
    const gameScreen = document.getElementById("game-screen");
    const mathMode = document.getElementById("math-mode");
    const impostorMode = document.getElementById("impostor-mode");
    const answerInput = document.getElementById("answer-input");

    // NOTIFICATIES
    function showToast(msg, isSuccess = true) {
      const toast = document.getElementById("toast");
      toast.textContent = msg;
      toast.className = `toast show ${isSuccess ? 'success' : 'error'}`;
      setTimeout(() => toast.className = 'toast', 2200);
    }

    // FOCUS HERSTEL (VOORKOMT HAPEREN BIJ ENTER)
    function keepFocus() {
      requestAnimationFrame(() => {
        if (!impostorMode.classList.contains("hidden")) {
          document.getElementById("imp-ans1").focus();
        } else {
          answerInput.focus();
        }
      });
    }

    // LEVEL PROGRESSIE
    function getLevelInfo(xp) {
      let current = LEVELS[0];
      let next = LEVELS[1];
      for (let i = 0; i < LEVELS.length - 1; i++) {
        if (xp >= LEVELS[i].xpNeeded) {
          current = LEVELS[i];
          next = LEVELS[i + 1] || LEVELS[i];
        }
      }
      if (xp >= LEVELS[LEVELS.length - 1].xpNeeded) {
        current = LEVELS[LEVELS.length - 1];
        next = current;
      }
      return { current, next };
    }

    function updateUI() {
      const { current, next } = getLevelInfo(player.xp);
      document.getElementById("player-name").textContent = player.name.charAt(0).toUpperCase() + player.name.slice(1);
      document.getElementById("player-xp").textContent = player.xp;
      document.getElementById("lvl-badge").textContent = `GYM LEVEL ${current.level}`;
      document.getElementById("lvl-title").textContent = current.name;
      document.getElementById("lvl-img").src = current.img;

      if (current.level < 5) {
        const xpInLvl = player.xp - current.xpNeeded;
        const xpSpan = next.xpNeeded - current.xpNeeded;
        const pct = Math.min(Math.max((xpInLvl / xpSpan) * 100, 0), 100);
        document.getElementById("lvl-progress").style.width = `${pct}%`;
        document.getElementById("lvl-sub").textContent = `Nog ${next.xpNeeded - player.xp} XP tot Level ${next.level}!`;
      } else {
        document.getElementById("lvl-progress").style.width = "100%";
        document.getElementById("lvl-sub").textContent = "Maximum Level Behaald!";
      }

      document.getElementById("round-counter").textContent = `Ronde Voortgang: Vraag ${roundProgress + 1} van 10`;
    }

    // GEMENGDE SOM-GENERATOR
    function nextQuestion() {
      const { current } = getLevelInfo(player.xp);
      const level = current.level;
      const types = ["maal", "plusmin", "deel"];
      const type = types[Math.floor(Math.random() * types.length)];

      let text = "", ans = 0;
      if (type === "maal") {
        let n1 = level === 1 ? rand(6, 12) : level === 2 ? rand(11, 15) : rand(12, 20);
        let n2 = rand(4, 12);
        text = `${n1} × ${n2}`;
        ans = n1 * n2;
      } else if (type === "plusmin") {
        if (level === 1) {
          let n1 = rand(25, 80), n2 = rand(15, 60);
          text = `${n1} + ${n2}`;
          ans = n1 + n2;
        } else {
          let n1 = rand(40, 150), n2 = rand(20, 90), n3 = rand(10, 50);
          text = `${n1} + ${n2} - ${n3}`;
          ans = n1 + n2 - n3;
        }
      } else {
        let n2 = rand(4, 12);
        let target = rand(6, 15);
        text = `${target * n2} ÷ ${n2}`;
        ans = target;
      }

      currentSom = { text, answer: ans };
      document.getElementById("som-display").textContent = `${text} = ?`;
      answerInput.value = "";
      keepFocus();
    }

    function rand(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }

    // IMPOSTOR GENERATOR
    function generateImpostor() {
      let pika = rand(10, 25), chari = rand(15, 30), blast = rand(6, 15);
      let c1 = pika + chari;
      let c2 = chari * blast;
      let c3 = (chari + pika) - blast;
      let imp = c2; // Grootste waarde

      currentImpostor = { pika, chari, blast, c1, c2, c3, imp };

      document.getElementById("imp-val1").innerHTML = `<b>Pikachu = ${pika}</b>`;
      document.getElementById("imp-val2").innerHTML = `<b>Charizard = ${chari}</b>`;
      document.getElementById("imp-val3").innerHTML = `<b>Blastoise = ${blast}</b>`;

      document.getElementById("lbl-imp1").textContent = `1) Pikachu (${pika}) + Charizard (${chari}) = ?`;
      document.getElementById("lbl-imp2").textContent = `2) Charizard (${chari}) × Blastoise (${blast}) = ?`;
      document.getElementById("lbl-imp3").textContent = `3) (Charizard + Pikachu) - Blastoise = ?`;

      document.getElementById("imp-ans1").value = "";
      document.getElementById("imp-ans2").value = "";
      document.getElementById("imp-ans3").value = "";
      document.getElementById("imp-ans-final").value = "";

      mathMode.classList.add("hidden");
      impostorMode.classList.remove("hidden");
      keepFocus();
    }

    // CLOUD SYNC
    async function saveXP() {
      if (supabase && player.name) {
        try {
          await supabase.from("players").update({ xp: player.xp }).eq("naam", player.name);
        } catch (e) {}
      }
    }

    // EVENT HANDLERS
    document.getElementById("btn-login").onclick = async () => {
      const name = document.getElementById("auth-name").value.trim().toLowerCase();
      const pin = document.getElementById("auth-pin").value.trim();

      if (!name || !pin) return showToast("Vul een naam en pincode in!", false);

      if (supabase) {
        const { data } = await supabase.from("players").select("*").eq("naam", name);
        if (data && data.length > 0) {
          if (data[0].pincode === pin) {
            player = { name: name, xp: data[0].xp || 0 };
            startSession();
          } else {
            showToast("Onjuiste pincode!", false);
          }
        } else {
          showToast("Trainer niet gevonden. Maak eerst een account aan!", false);
        }
      }
    };

    document.getElementById("btn-register").onclick = async () => {
      const name = document.getElementById("auth-name").value.trim().toLowerCase();
      const pin = document.getElementById("auth-pin").value.trim();

      if (!name || !pin) return showToast("Vul een naam en 4-cijferige pincode in!", false);

      if (supabase) {
        const { data } = await supabase.from("players").select("*").eq("naam", name);
        if (data && data.length > 0) {
          showToast("Deze naam bestaat al!", false);
        } else {
          await supabase.from("players").insert([{ naam: name, pincode: pin, xp: 0 }]);
          player = { name: name, xp: 0 };
          startSession();
        }
      }
    };

    function startSession() {
      authScreen.classList.add("hidden");
      gameScreen.classList.remove("hidden");
      roundProgress = 0;
      updateUI();
      nextQuestion();
    }

    document.getElementById("math-form").onsubmit = (e) => {
      e.preventDefault();
      const val = parseInt(answerInput.value.trim());
      if (isNaN(val)) return;

      const oldInfo = getLevelInfo(player.xp);
      if (val === currentSom.answer) {
        player.xp += 1;
        roundProgress += 1;
        saveXP();
        showToast("⚡ AANVAL GESLAAGD! +1 XP 🔴", true);

        const newInfo = getLevelInfo(player.xp);
        if (newInfo.current.level > oldInfo.current.level) {
          confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
          showToast(`🎉 EVOLUTIE! Level ${newInfo.current.level}!`, true);
        }
      } else {
        showToast(`❌ GEMIST! Antwoord was ${currentSom.answer}`, false);
      }

      updateUI();

      if (roundProgress >= 10) {
        generateImpostor();
      } else {
        nextQuestion();
      }
    };

    document.getElementById("impostor-form").onsubmit = (e) => {
      e.preventDefault();
      const a1 = parseInt(document.getElementById("imp-ans1").value);
      const a2 = parseInt(document.getElementById("imp-ans2").value);
      const a3 = parseInt(document.getElementById("imp-ans3").value);
      const finalAns = parseInt(document.getElementById("imp-ans-final").value);

      if (a1 === currentImpostor.c1 && a2 === currentImpostor.c2 && a3 === currentImpostor.c3 && finalAns === currentImpostor.imp) {
        confetti({ particleCount: 150, spread: 90 });
        player.xp += 2;
        roundProgress = 0;
        saveXP();
        showToast("🎉 IMPOSTOR ONTMASKERD! +2 BONUS XP! 🔴", true);
        
        impostorMode.classList.add("hidden");
        mathMode.classList.remove("hidden");
        updateUI();
        nextQuestion();
      } else {
        showToast("❌ Reken alles nog eens goed na!", false);
      }
    };

    document.getElementById("btn-logout").onclick = () => {
      gameScreen.classList.add("hidden");
      authScreen.classList.remove("hidden");
    };
  </script>
</body>
</html>
