const BACKEND = "http://127.0.0.1:5001";

let secretWord = "";
let currentRow = 0;
let currentGuess = "";
let gameOver = false;

// Build the 6x5 board
function buildBoard() {
  const board = document.getElementById("board");
  for (let r = 0; r < 6; r++) {
    const row = document.createElement("div");
    row.classList.add("row");
    for (let c = 0; c < 5; c++) {
      const tile = document.createElement("div");
      tile.classList.add("tile");
      tile.id = `tile-${r}-${c}`;
      row.appendChild(tile);
    }
    board.appendChild(row);
  }
}

// Build the on-screen keyboard
function buildKeyboard() {
  const rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"];
  const keyboard = document.getElementById("keyboard");
  rows.forEach(rowLetters => {
    const row = document.createElement("div");
    row.classList.add("key-row");
    rowLetters.split("").forEach(letter => {
      const key = document.createElement("button");
      key.textContent = letter.toUpperCase();
      key.id = `key-${letter}`;
      key.classList.add("key");
      key.addEventListener("click", () => handleKey(letter));
      row.appendChild(key);
    });
    keyboard.appendChild(row);
  });

  // Enter and Backspace
  const lastRow = keyboard.lastChild;

  const enterKey = document.createElement("button");
  enterKey.textContent = "ENTER";
  enterKey.classList.add("key", "wide-key");
  enterKey.addEventListener("click", submitGuess);
  lastRow.prepend(enterKey);

  const backKey = document.createElement("button");
  backKey.textContent = "⌫";
  backKey.classList.add("key", "wide-key");
  backKey.addEventListener("click", () => handleKey("Backspace"));
  lastRow.appendChild(backKey);
}

// Fetch the secret word from backend
async function fetchWord() {
  const res = await fetch(`${BACKEND}/word`);
  const data = await res.json();
  secretWord = data.word;
}

// Handle physical keyboard
document.addEventListener("keydown", (e) => {
  if (gameOver) return;
  if (e.key === "Enter") submitGuess();
  else if (e.key === "Backspace") handleKey("Backspace");
  else if (/^[a-zA-Z]$/.test(e.key)) handleKey(e.key.toLowerCase());
});

function handleKey(key) {
  if (gameOver) return;
  if (key === "Backspace") {
    currentGuess = currentGuess.slice(0, -1);
  } else if (currentGuess.length < 5) {
    currentGuess += key;
  }
  updateRow();
}

function updateRow() {
  for (let c = 0; c < 5; c++) {
    const tile = document.getElementById(`tile-${currentRow}-${c}`);
    tile.textContent = currentGuess[c] ? currentGuess[c].toUpperCase() : "";
  }
}

async function submitGuess() {
// Validate word
  const validateRes = await fetch(`${BACKEND}/validate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ word: currentGuess })
  });
  const validateData = await validateRes.json();
  if (!validateData.valid) {
    const row = document.querySelector(`#board .row:nth-child(${currentRow + 1})`);
    row.classList.add("shake");
    row.addEventListener("animationend", () => row.classList.remove("shake"), { once: true });
    showMessage("Not a valid word!");
    return;
  }
  if (currentGuess.length !== 5) {
    const row = document.querySelector(`#board .row:nth-child(${currentRow + 1})`);
    row.classList.add("shake");
    row.addEventListener("animationend", () => row.classList.remove("shake"), { once: true });
    showMessage("Not enough letters!");
    return;
  }

  const res = await fetch(`${BACKEND}/guess`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ guess: currentGuess })
  });

  const data = await res.json();

  data.result.forEach((item, c) => {
    const tile = document.getElementById(`tile-${currentRow}-${c}`);
    setTimeout(() => {
      tile.classList.add("flip");
      setTimeout(() => {
        tile.classList.add(item.status);
      }, 250);
    }, c * 150);

    setTimeout(() => {
      const key = document.getElementById(`key-${item.letter}`);
      if (key && !key.classList.contains("correct")) {
        key.classList.remove("present", "absent");
        key.classList.add(item.status);
      }
    }, c * 150 + 500);
  });

  const totalDelay = 5 * 150 + 500;

  setTimeout(() => {
    if (data.result.every(item => item.status === "correct")) {
      showMessage("You got it! 🎉");
      gameOver = true;
      saveStats(true);
      return;
    }

    currentRow++;
    currentGuess = "";

    if (currentRow === 6) {
      showMessage(`Game over! The word was ${secretWord.toUpperCase()}`);
      gameOver = true;
      saveStats(false);
    }
  }, totalDelay);
}

function showMessage(msg) {
  document.getElementById("message").textContent = msg;
}

// Start the game
buildBoard();
buildKeyboard();
fetchWord();

// Stats functions
function loadStats() {
  return JSON.parse(localStorage.getItem("wordleStats")) || {
    played: 0,
    wins: 0,
    streak: 0,
    bestStreak: 0,
    distribution: [0, 0, 0, 0, 0, 0]
  };
}

function saveStats(won) {
  const stats = loadStats();
  stats.played++;
  if (won) {
    stats.wins++;
    stats.streak++;
    stats.bestStreak = Math.max(stats.bestStreak, stats.streak);
    stats.distribution[currentRow]++;
  } else {
    stats.streak = 0;
  }
  localStorage.setItem("wordleStats", JSON.stringify(stats));
  showStats(stats);
}

function showStats(stats) {
  const winPct = stats.played ? Math.round((stats.wins / stats.played) * 100) : 0;
  const dist = stats.distribution
    .map((n, i) => `${i + 1}: ${"█".repeat(n)} ${n}`)
    .join("\n");
  document.getElementById("message").innerHTML = `
    <div class="stats">
      <div class="stat"><span>${stats.played}</span>Played</div>
      <div class="stat"><span>${winPct}%</span>Win %</div>
      <div class="stat"><span>${stats.streak}</span>Streak</div>
      <div class="stat"><span>${stats.bestStreak}</span>Best</div>
    </div>
  `;
}