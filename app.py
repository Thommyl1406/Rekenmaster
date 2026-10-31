<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔴 Pokémon Reken-Gym Pro ⚡</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800;900&display=swap" rel="stylesheet">
    <!-- Canvas Confetti -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <!-- Supabase JS Client -->
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <style>
        body {
            font-family: 'Outfit', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            min-height: 100vh;
            color: #ffffff;
        }

        .pokeball-card {
            background-color: #ffffff !important;
            border: 4px solid #facc15;
            border-radius: 24px;
            box-shadow: 0 15px 30px rgba(0,0,0,0.5);
            color: #0f172a !important;
        }

        .som-card {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            border: 4px solid #facc15;
            border-radius: 24px;
            box-shadow: 0 10px 25px rgba(37, 99, 235, 0.4);
        }

        .poke-btn {
            background: linear-gradient(180deg, #ef4444 0%, #dc2626 100%);
            border: 3px solid #facc15;
            box-shadow: 0 6px 0px #7f1d1d;
            transition: all 0.1s ease;
        }

        .poke-btn:hover {
            background: linear-gradient(180deg, #f87171 0%, #ef4444 100%);
            transform: translateY(-2px);
            box-shadow: 0 8px 0px #7f1d1d;
        }

        .poke-btn:active {
            transform: translateY(4px);
            box-shadow: 0 2px 0px #7f1d1d;
        }

        @keyframes slideIn {
            from { transform: translateY(-100%); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        .toast-animate {
            animation: slideIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        }

        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0f172a;
        }
        ::-webkit-scrollbar-thumb {
            background: #ef4444;
            border-radius: 4px;
        }
    </style>
</head>
<body class="flex flex-col items-center justify-start p-4 md:p-6 min-h-screen">

    <!-- Toast Meldingen Container -->
    <div id="toast-container" class="fixed top-5 z-50 flex flex-col items-center gap-2 pointer-events-none w-full max-w-md px-4"></div>

    <!-- Header Title -->
    <header class="text-center my-4">
        <h1 class="text-3xl md:text-5xl font-black tracking-wider text-yellow-400 drop-shadow-[0_4px_4px_rgba(0,0,0,0.8)] flex items-center justify-center gap-3">
            <span class="text-red-500 animate-bounce">🔴</span> POKÉMON REKEN-GYM <span class="text-yellow-400">⚡</span>
        </h1>
    </header>

    <!-- INLOG- / REGISTRATIESCHERM -->
    <main id="auth-screen" class="w-full max-w-md my-auto">
        <div class="pokeball-card p-6 md:p-8 text-center">
            <div class="inline-block bg-red-500 text-white font-bold px-4 py-1.5 rounded-full text-sm mb-4 shadow">
                🎒 TRAINER TOEGANG
            </div>
            <h2 class="text-2xl font-black text-slate-900 mb-2">Welkom Trainer!</h2>
            <p class="text-slate-600 font-medium mb-6 text-sm">Vul je Trainer Naam en een geheime 4-cijferige pincode in om je voortgang te bewaren.</p>

            <form id="auth-form" onsubmit="handleAuth(event)" class="space-y-4">
                <div>
                    <label class="block text-left text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Trainer Naam</label>
                    <input type="text" id="trainer-name" required placeholder="bijv. Ash Ketchum" autocomplete="off" class="w-full px-4 py-3 border-2 border-slate-300 rounded-xl focus:outline-none focus:border-red-500 font-bold text-slate-800 text-lg shadow-sm">
                </div>
                <div>
                    <label class="block text-left text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">4-Cijferige Pincode</label>
                    <input type="password" id="trainer-pin" maxlength="4" pattern="\d{4}" required placeholder="****" autocomplete="off" class="w-full px-4 py-3 border-2 border-slate-300 rounded-xl focus:outline-none focus:border-red-500 font-bold text-slate-800 text-lg tracking-widest text-center shadow-sm">
                </div>

                <div class="grid grid-cols-2 gap-3 pt-2">
                    <button type="submit" onclick="authAction = 'login'" class="poke-btn text-white font-black py-3 px-4 rounded-xl text-lg flex items-center justify-center gap-2">
                        <i class="fa-solid fa-right-to-bracket"></i> Inloggen
                    </button>
                    <button type="submit" onclick="authAction = 'register'" class="bg-yellow-400 hover:bg-yellow-300 text-slate-900 border-2 border-yellow-600 font-black py-3 px-4 rounded-xl text-lg shadow-[0_6px_0px_#ca8a04] active:translate-y-1 active:shadow-none transition-all flex items-center justify-center gap-2">
                        <i class="fa-solid fa-user-plus"></i> Nieuw
                    </button>
                </div>
            </form>
        </div>
    </main>

    <!-- SPEELSCHERM (REKEN-GYM) -->
    <main id="game-screen" class="w-full max-w-xl hidden space-y-6 my-auto">

        <!-- Trainer Profile / Level Status Card -->
        <div class="pokeball-card p-5 relative overflow-hidden">
            <div class="flex items-center gap-4">
                <div class="relative bg-slate-100 p-2 rounded-2xl border-2 border-yellow-400 shadow-inner">
                    <img id="poke-avatar" src="" alt="Pokemon Avatar" class="w-20 h-20 object-contain">
                </div>
                <div class="flex-1 min-w-0">
                    <div class="inline-block bg-red-500 text-white text-xs font-extrabold px-3 py-1 rounded-full uppercase tracking-wider mb-1 shadow">
                        Gym Level <span id="lbl-level-num">1</span>
                    </div>
                    <h2 id="lbl-level-name" class="text-xl md:text-2xl font-black text-slate-900 truncate">Pikachu Trainer</h2>
                    <p class="text-sm font-bold text-slate-600 flex items-center gap-2 mt-0.5">
                        <i class="fa-solid fa-user-ninja text-red-500"></i> Trainer: <span id="lbl-trainer-name" class="text-slate-900 capitalize">...</span>
                    </p>
                </div>
                <div class="text-right">
                    <div class="text-xs font-bold text-slate-500 uppercase">Totaal XP</div>
                    <div class="text-2xl md:text-3xl font-black text-red-600 flex items-center justify-end gap-1">
                        <span id="lbl-xp">0</span> <span class="text-lg">🔴</span>
                    </div>
                </div>
            </div>

            <!-- Voortgangsbalk -->
            <div class="mt-4 pt-3 border-t border-slate-100">
                <div class="flex justify-between text-xs font-bold text-slate-600 mb-1">
                    <span>Level Voortgang</span>
                    <span id="lbl-xp-needed">Nog ... XP tot volgend level</span>
                </div>
                <div class="w-full bg-slate-200 h-3.5 rounded-full overflow-hidden p-0.5 border border-slate-300">
                    <div id="progress-bar" class="bg-gradient-to-r from-red-500 to-yellow-400 h-full rounded-full transition-all duration-300" style="width: 0%"></div>
                </div>
            </div>
        </div>

        <!-- REKEN-ARENA (REGULIERE SOMMEN) -->
        <div id="regular-arena" class="space-y-4">
            <!-- Progressie binnen ronde (10 sommen) -->
            <div class="flex items-center justify-between text-sm font-bold text-slate-300 px-2">
                <span class="flex items-center gap-2"><i class="fa-solid fa-flag-checkered text-yellow-400"></i> Ronde Voortgang: Vraag <span id="lbl-question-count">1</span> van 10</span>
                <button onclick="logout()" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1.5 rounded-lg border border-slate-700 transition">
                    <i class="fa-solid fa-right-from-bracket"></i> Uitloggen
                </button>
            </div>
            
            <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden border border-slate-700">
                <div id="round-progress-bar" class="bg-yellow-400 h-full transition-all duration-200" style="width: 10%"></div>
            </div>

            <!-- Som Display Card -->
            <div class="som-card p-6 md:p-8 text-center text-white">
                <div class="text-xs font-bold text-yellow-300 uppercase tracking-widest mb-2 flex items-center justify-center gap-2">
                    <i class="fa-solid fa-bolt"></i> Reken-Aanval Klaarzetten
                </div>
                <div id="som-display" class="text-4xl md:text-6xl font-black tracking-tight text-white drop-shadow-md">
                    12 × 5 = ?
                </div>
            </div>

            <!-- Invoer Formulier -->
            <form id="answer-form" onsubmit="submitAnswer(event)" class="space-y-3">
                <div>
                    <input type="text" id="answer-input" pattern="-?\d*" inputmode="numeric" required autocomplete="off" placeholder="Typ je antwoord..." class="w-full text-center py-4 px-6 rounded-2xl bg-white text-slate-900 text-3xl font-black border-4 border-yellow-400 shadow-xl focus:outline-none focus:ring-4 focus:ring-red-500 transition">
                </div>
                <button type="submit" class="poke-btn w-full text-white font-black text-xl py-4 rounded-2xl flex items-center justify-center gap-3">
                    <i class="fa-solid fa-fire text-yellow-300"></i> BEVESTIG ANTWOORD [ENTER]
                </button>
            </form>
        </div>

        <!-- IMPOSTOR ARENA (VERPLICHTE VISUELE PUZZEL NA 10 SOMMEN) -->
        <div id="impostor-arena" class="hidden pokeball-card p-6 border-4 border-red-500">
            <div class="text-center mb-4">
                <span class="bg-red-500 text-white text-xs font-black px-4 py-1.5 rounded-full uppercase tracking-widest shadow">
                    🕵️ SPECIAL CHALLENGE
                </span>
                <h3 class="text-2xl font-black text-slate-900 mt-2">Ontmasker de Impostor!</h3>
                <p class="text-xs text-slate-600 font-bold">Reken de Pokémon-waarden uit en vind de GROOTSTE uitkomst (de Impostor)!</p>
            </div>

            <!-- Legende Kaart -->
            <div class="bg-slate-100 rounded-2xl p-4 border-2 border-slate-200 mb-5">
                <div class="text-xs font-bold text-slate-500 uppercase text-center mb-3">📜 Pokémon Waarden Sleutel</div>
                <div class="grid grid-cols-3 gap-2 text-center">
                    <div class="bg-white p-2 rounded-xl border border-slate-200 shadow-sm flex flex-col items-center">
                        <img id="imp-img-pika" src="" class="w-12 h-12 object-contain">
                        <span class="text-xs font-bold text-slate-700">Pikachu</span>
                        <span id="imp-val-pika" class="text-lg font-black text-red-600">12</span>
                    </div>
                    <div class="bg-white p-2 rounded-xl border border-slate-200 shadow-sm flex flex-col items-center">
                        <img id="imp-img-chari" src="" class="w-12 h-12 object-contain">
                        <span class="text-xs font-bold text-slate-700">Charizard</span>
                        <span id="imp-val-chari" class="text-lg font-black text-red-600">25</span>
                    </div>
                    <div class="bg-white p-2 rounded-xl border border-slate-200 shadow-sm flex flex-col items-center">
                        <img id="imp-img-blast" src="" class="w-12 h-12 object-contain">
                        <span class="text-xs font-bold text-slate-700">Blastoise</span>
                        <span id="imp-val-blast" class="text-lg font-black text-red-600">8</span>
                    </div>
                </div>
            </div>

            <!-- Impostor Vragen Formulier -->
            <form id="impostor-form" onsubmit="submitImpostor(event)" class="space-y-4">
                <div class="space-y-3">
                    <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
                        <label id="lbl-imp-q1" class="block text-sm font-bold text-slate-800 mb-1">1) Pikachu + Charizard = ?</label>
                        <input type="text" id="imp-ans-1" pattern="-?\d*" inputmode="numeric" required autocomplete="off" placeholder="Antwoord 1" class="w-full px-3 py-2 border-2 border-slate-300 rounded-lg font-bold text-slate-900 focus:outline-none focus:border-red-500">
                    </div>
                    <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
                        <label id="lbl-imp-q2" class="block text-sm font-bold text-slate-800 mb-1">2) Charizard × Blastoise = ?</label>
                        <input type="text" id="imp-ans-2" pattern="-?\d*" inputmode="numeric" required autocomplete="off" placeholder="Antwoord 2" class="w-full px-3 py-2 border-2 border-slate-300 rounded-lg font-bold text-slate-900 focus:outline-none focus:border-red-500">
                    </div>
                    <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
                        <label id="lbl-imp-q3" class="block text-sm font-bold text-slate-800 mb-1">3) (Charizard + Pikachu) - Blastoise = ?</label>
                        <input type="text" id="imp-ans-3" pattern="-?\d*" inputmode="numeric" required autocomplete="off" placeholder="Antwoord 3" class="w-full px-3 py-2 border-2 border-slate-300 rounded-lg font-bold text-slate-900 focus:outline-none focus:border-red-500">
                    </div>
                    <div class="bg-red-50 p-3 rounded-xl border-2 border-red-300">
                        <label class="block text-sm font-black text-red-700 mb-1">🚨 Wat is de GROOTSTE uitkomst (de Impostor)?</label>
                        <input type="text" id="imp-ans-final" pattern="-?\d*" inputmode="numeric" required autocomplete="off" placeholder="Vul de grootste uitkomst in..." class="w-full px-3 py-2 border-2 border-red-400 rounded-lg font-black text-red-900 focus:outline-none focus:border-red-600">
                    </div>
                </div>

                <button type="submit" class="poke-btn w-full text-white font-black text-lg py-3 rounded-xl shadow-lg flex items-center justify-center gap-2">
                    <i class="fa-solid fa-mask"></i> ONTMASKER EN VERDIEN +2 XP!
                </button>
            </form>
        </div>
    </main>

    <!-- JavaScript Logica -->
    <script>
        // Supabase Database Koppeling
        const SUPABASE_URL = "https://iwootoqaieisilkylotg.supabase.co";
        const SUPABASE_KEY = "sb_publishable_dAOMuXRA6lUMrPbieCpcVA_VMWQCSs-";
        const supabaseClient = window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY) : null;

        // Officiële Pokémon API Sprites
        const POKEMON_SPRITES = {
            Pikachu: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
            Charmeleon: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/5.png",
            Charizard: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png",
            Blastoise: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/9.png",
            Mewtwo: "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/150.png"
        };

        // Level Configuratie & Moeilijkheid
        const LEVELS = [
            { level: 1, name: "Pikachu Trainer", xpNeeded: 0, sprite: POKEMON_SPRITES.Pikachu },
            { level: 2, name: "Charmeleon Gym-Uitdager", xpNeeded: 50, sprite: POKEMON_SPRITES.Charmeleon },
            { level: 3, name: "Blastoise Reken-Master", xpNeeded: 120, sprite: POKEMON_SPRITES.Blastoise },
            { level: 4, name: "Dragonite Elite Four", xpNeeded: 250, sprite: POKEMON_SPRITES.Charizard },
            { level: 5, name: "Mewtwo Reken-Champion", xpNeeded: 500, sprite: POKEMON_SPRITES.Mewtwo }
        ];

        // App State
        let currentUser = null;
        let authAction = 'login';
        let currentProblem = null;
        let currentImpostorPuzzle = null;
        let questionCounter = 0;

        // Initialisatie
        window.onload = () => {
            const savedSession = localStorage.getItem('poke_gym_current_session');
            if (savedSession) {
                const userData = localStorage.getItem(`poke_gym_user_${savedSession}`);
                if (userData) {
                    currentUser = JSON.parse(userData);
                    loadGameScreen();
                    return;
                }
            }
            showAuthScreen();
        };

        // --- AUTHENTICATIE MET SUPABASE + FALLBACK LOCALSTORAGE ---
        async function handleAuth(e) {
            e.preventDefault();
            const nameInput = document.getElementById('trainer-name').value.trim().toLowerCase();
            const pinInput = document.getElementById('trainer-pin').value.trim();

            if (!nameInput || pinInput.length !== 4) {
                showToast('❌ Vul een geldige naam en 4-cijferige pincode in!', 'error');
                return;
            }

            if (authAction === 'register') {
                if (supabaseClient) {
                    try {
                        const { data: existing } = await supabaseClient.from('players').select('*').eq('naam', nameInput);
                        if (existing && existing.length > 0) {
                            showToast('⚠️ Deze trainer bestaat al! Kies Inloggen.', 'error');
                            return;
                        }
                        await supabaseClient.from('players').insert([{ naam: nameInput, pincode: pinInput, xp: 0 }]);
                    } catch (err) {
                        console.warn('Supabase offline, local fallback used.', err);
                    }
                }
                
                currentUser = { name: nameInput, pin: pinInput, xp: 0 };
                saveUserData();
                localStorage.setItem('poke_gym_current_session', nameInput);
                showToast('✨ Trainer account succesvol aangemaakt!', 'success');
                loadGameScreen();
            } else {
                let fetchedUser = null;
                if (supabaseClient) {
                    try {
                        const { data } = await supabaseClient.from('players').select('*').eq('naam', nameInput);
                        if (data && data.length > 0) {
                            fetchedUser = { name: data[0].naam, pin: String(data[0].pincode), xp: data[0].xp || 0 };
                        }
                    } catch (err) {
                        console.warn('Supabase check fallback.', err);
                    }
                }

                if (!fetchedUser) {
                    const localData = localStorage.getItem(`poke_gym_user_${nameInput}`);
                    if (localData) fetchedUser = JSON.parse(localData);
                }

                if (!fetchedUser) {
                    showToast('❌ Trainer niet gevonden! Maak eerst een nieuw account aan.', 'error');
                    return;
                }
                if (fetchedUser.pin !== pinInput) {
                    showToast('🔒 Onjuiste pincode voor deze trainer!', 'error');
                    return;
                }

                currentUser = fetchedUser;
                saveUserData();
                localStorage.setItem('poke_gym_current_session', nameInput);
                showToast(`⚡ Welkom terug, ${currentUser.name.toUpperCase()}!`, 'success');
                loadGameScreen();
            }
        }

        function logout() {
            localStorage.removeItem('poke_gym_current_session');
            currentUser = null;
            document.getElementById('auth-form').reset();
            showAuthScreen();
            showToast('👋 Succesvol uitgelogd. Tot de volgende battle!', 'info');
        }

        function showAuthScreen() {
            document.getElementById('auth-screen').classList.remove('hidden');
            document.getElementById('game-screen').classList.add('hidden');
        }

        function loadGameScreen() {
            document.getElementById('auth-screen').classList.add('hidden');
            document.getElementById('game-screen').classList.remove('hidden');
            document.getElementById('lbl-trainer-name').innerText = currentUser.name;
            
            questionCounter = 0;
            updateUserUI();
            nextQuestion();
        }

        async function saveUserData() {
            if (!currentUser) return;
            localStorage.setItem(`poke_gym_user_${currentUser.name}`, JSON.stringify(currentUser));

            if (supabaseClient) {
                try {
                    await supabaseClient.from('players').update({ xp: currentUser.xp }).eq('naam', currentUser.name);
                } catch (err) {
                    console.warn('Supabase sync error', err);
                }
            }
        }

        // --- LEVEL LOGICA ---
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
                next = LEVELS[LEVELS.length - 1];
            }
            return { current, next };
        }

        function updateUserUI() {
            const { current, next } = getLevelInfo(currentUser.xp);
            
            document.getElementById('lbl-level-num').innerText = current.level;
            document.getElementById('lbl-level-name').innerText = current.name;
            document.getElementById('poke-avatar').src = current.sprite;
            document.getElementById('lbl-xp').innerText = currentUser.xp;

            if (current.level < 5) {
                const currentLevelXP = currentUser.xp - current.xpNeeded;
                const neededForNext = next.xpNeeded - current.xpNeeded;
                const pct = Math.min(Math.max((currentLevelXP / neededForNext) * 100, 0), 100);
                
                document.getElementById('progress-bar').style.width = `${pct}%`;
                document.getElementById('lbl-xp-needed').innerText = `Nog ${next.xpNeeded - currentUser.xp} XP tot Level ${next.level}`;
            } else {
                document.getElementById('progress-bar').style.width = `100%`;
                document.getElementById('lbl-xp-needed').innerText = `MAX LEVEL ERREIKT! 🏆`;
            }
        }

        // --- DYNAMISCHE SOMMEN GENERATOR ---
        function generateProblem(level) {
            const types = ['multiply', 'divide', 'plusminus'];
            const chosenType = types[Math.floor(Math.random() * types.length)];

            let num1, num2, num3, answer, questionText;

            if (chosenType === 'multiply') {
                if (level === 1) { num1 = rand(6, 12); num2 = rand(4, 10); }
                else if (level === 2) { num1 = rand(11, 15); num2 = rand(6, 12); }
                else if (level === 3) { num1 = rand(12, 18); num2 = rand(8, 14); }
                else { num1 = rand(14, 25); num2 = rand(12, 20); }
                
                answer = num1 * num2;
                questionText = `${num1} × ${num2}`;
            } else if (chosenType === 'divide') {
                if (level === 1) { answer = rand(6, 12); num2 = rand(4, 10); }
                else if (level === 2) { answer = rand(10, 15); num2 = rand(6, 12); }
                else { answer = rand(12, 22); num2 = rand(8, 15); }

                num1 = answer * num2;
                questionText = `${num1} ÷ ${num2}`;
            } else {
                if (level === 1) {
                    num1 = rand(25, 80); num2 = rand(15, 60);
                    answer = num1 + num2;
                    questionText = `${num1} + ${num2}`;
                } else if (level === 2) {
                    num1 = rand(40, 120); num2 = rand(20, 80); num3 = rand(10, 40);
                    answer = num1 + num2 - num3;
                    questionText = `${num1} + ${num2} - ${num3}`;
                } else {
                    num1 = rand(100, 350); num2 = rand(50, 200); num3 = rand(30, 150);
                    answer = num1 + num2 - num3;
                    questionText = `${num1} + ${num2} - ${num3}`;
                }
            }

            return { questionText, answer };
        }

        function rand(min, max) {
            return Math.floor(Math.random() * (max - min + 1)) + min;
        }

        // --- VOLGENDE VRAAG ENGINE EN AUTOMATISCHE FOCUS ---
        function nextQuestion() {
            if (questionCounter >= 10) {
                showImpostorArena();
                return;
            }

            document.getElementById('regular-arena').classList.remove('hidden');
            document.getElementById('impostor-arena').classList.add('hidden');

            const { current } = getLevelInfo(currentUser.xp);
            currentProblem = generateProblem(current.level);

            document.getElementById('som-display').innerText = `${currentProblem.questionText} = ?`;
            document.getElementById('lbl-question-count').innerText = questionCounter + 1;
            document.getElementById('round-progress-bar').style.width = `${((questionCounter + 1) / 10) * 100}%`;

            const inputField = document.getElementById('answer-input');
            inputField.value = '';
            
            requestAnimationFrame(() => {
                inputField.focus();
            });
        }

        function submitAnswer(e) {
            e.preventDefault();
            const inputField = document.getElementById('answer-input');
            const val = parseInt(inputField.value.trim(), 10);

            if (isNaN(val)) return;

            const oldLevel = getLevelInfo(currentUser.xp).current.level;

            if (val === currentProblem.answer) {
                currentUser.xp += 1;
                questionCounter += 1;
                saveUserData();
                updateUserUI();

                const newLevel = getLevelInfo(currentUser.xp).current.level;
                if (newLevel > oldLevel) {
                    confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
                    showToast(`🎉 EVOLUTIE! Je bent geëvolueerd naar Gym Level ${newLevel}!`, 'success');
                } else {
                    showToast('⚡ AANVAL GESLAAGD! +1 XP verdiend! 🔴', 'success');
                }
            } else {
                showToast(`❌ OEPS! Het juiste antwoord was ${currentProblem.answer}.`, 'error');
            }

            nextQuestion();
        }

        // --- IMPOSTOR PUZZEL LOGICA ---
        function showImpostorArena() {
            document.getElementById('regular-arena').classList.add('hidden');
            document.getElementById('impostor-arena').classList.remove('hidden');

            const pika = rand(10, 25);
            const chari = rand(15, 30);
            const blast = rand(6, 15);

            const ans1 = pika + chari;
            const ans2 = chari * blast;
            const ans3 = (chari + pika) - blast;

            currentImpostorPuzzle = { pika, chari, blast, ans1, ans2, ans3, correctImpostor: ans2 };

            document.getElementById('imp-img-pika').src = POKEMON_SPRITES.Pikachu;
            document.getElementById('imp-img-chari').src = POKEMON_SPRITES.Charizard;
            document.getElementById('imp-img-blast').src = POKEMON_SPRITES.Blastoise;

            document.getElementById('imp-val-pika').innerText = pika;
            document.getElementById('imp-val-chari').innerText = chari;
            document.getElementById('imp-val-blast').innerText = blast;

            document.getElementById('lbl-imp-q1').innerText = `1) Pikachu (${pika}) + Charizard (${chari}) = ?`;
            document.getElementById('lbl-imp-q2').innerText = `2) Charizard (${chari}) × Blastoise (${blast}) = ?`;
            document.getElementById('lbl-imp-q3').innerText = `3) (Charizard + Pikachu) - Blastoise = ?`;

            document.getElementById('impostor-form').reset();
            
            requestAnimationFrame(() => {
                document.getElementById('imp-ans-1').focus();
            });
        }

        function submitImpostor(e) {
            e.preventDefault();
            const a1 = parseInt(document.getElementById('imp-ans-1').value.trim(), 10);
            const a2 = parseInt(document.getElementById('imp-ans-2').value.trim(), 10);
            const a3 = parseInt(document.getElementById('imp-ans-3').value.trim(), 10);
            const finalImp = parseInt(document.getElementById('imp-ans-final').value.trim(), 10);

            const { ans1, ans2, ans3, correctImpostor } = currentImpostorPuzzle;

            if (a1 === ans1 && a2 === ans2 && a3 === ans3 && finalImp === correctImpostor) {
                confetti({ particleCount: 150, spread: 90, origin: { y: 0.5 } });
                currentUser.xp += 2;
                saveUserData();
                updateUserUI();
                
                showToast('🕵️ GEWELDIG! Puzzel opgelost & Impostor ontmaskerd! +2 XP! 🔴', 'success');
                questionCounter = 0;
                nextQuestion();
            } else {
                showToast('❌ Niet alle antwoorden klopen nog! Kijk goed naar de Pokémon waarden en reken opnieuw.', 'error');
            }
        }

        // --- TOAST MELDINGEN ---
        function showToast(message, type = 'info') {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            
            let bgClass = 'bg-slate-900 border-slate-700 text-white';
            if (type === 'success') bgClass = 'bg-emerald-600 border-emerald-400 text-white';
            if (type === 'error') bgClass = 'bg-red-600 border-red-400 text-white';

            toast.className = `toast-animate px-5 py-3 rounded-2xl border-2 font-bold text-sm shadow-xl flex items-center justify-center text-center ${bgClass}`;
            toast.innerText = message;

            container.appendChild(toast);

            setTimeout(() => {
                toast.style.opacity = '0';
                toast.style.transition = 'opacity 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }, 3000);
        }
    </script>
</body>
</html>
