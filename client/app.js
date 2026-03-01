// DOM elements
const form = document.getElementById("createForm");
const msg = document.getElementById("message");
const tbody = document.getElementById("usersTbody");
const refreshBtn = document.getElementById("refreshBtn");
const searchInput = document.getElementById("search");

let allUsers = [];

// helpers
function setMessage(text, isError = false) {
  msg.textContent = text;
  msg.style.color = isError ? "#ff6b6b" : "#9aa4b2";
}

function escapeHtml(str) {
  return String(str)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderUsers(users) {
  tbody.innerHTML = users.map(u => `
    <tr>
      <td>${u.id}</td>
      <td>${escapeHtml(u.username)}</td>
      <td>${escapeHtml(u.email)}</td>
    </tr>
  `).join("");
}

// load users
async function loadUsers() {
  setMessage("Loading users...");
  try {
    const res = await fetch("/api/users");
    if (!res.ok) throw new Error(`GET /api/users failed: ${res.status}`);
    allUsers = await res.json();
    applyFilter();
    setMessage(`Loaded ${allUsers.length} users.`);
  } catch (e) {
    setMessage(e.message, true);
  }
}

// filter users
function applyFilter() {
  const q = searchInput.value.trim().toLowerCase();
  const filtered = q
    ? allUsers.filter(u =>
        u.username.toLowerCase().includes(q) ||
        u.email.toLowerCase().includes(q) ||
        String(u.id).includes(q)
      )
    : allUsers;

  renderUsers(filtered);
}

// create user
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  setMessage("Creating user...");

  const payload = {
    username: document.getElementById("username").value.trim(),
    email: document.getElementById("email").value.trim(),
    password: document.getElementById("password").value
  };

  try {
    const res = await fetch("/api/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const text = await res.text();
      throw new Error(`POST /api/users failed: ${res.status} ${text}`);
    }

    form.reset();
    setMessage("User created ✅");
    await loadUsers();
  } catch (e) {
    setMessage(e.message, true);
  }
});

// events
refreshBtn.addEventListener("click", loadUsers);
searchInput.addEventListener("input", applyFilter);

// initial load
loadUsers();