// auth.js - frontend authentication & session handling
console.log("AUTH JS LOADED ✅");

// --------------------------------------
// CHECK IF USER IS LOGGED IN
// --------------------------------------
function checkAuth() {
    const session = localStorage.getItem("userSession");
    if (!session) {
        window.location.href = "user_login.html";   // FIXED
    }
}

// --------------------------------------
// SAVE LOGIN SESSION
// --------------------------------------
function saveAuth(user, token) {
    localStorage.setItem("userSession", JSON.stringify({ user, token }));
}

// --------------------------------------
// GET TOKEN FOR AUTHORIZED API CALLS
// --------------------------------------
function getToken() {
    const session = localStorage.getItem("userSession");
    if (!session) return null;
    return JSON.parse(session).token;
}

// --------------------------------------
// LOGOUT USER
// --------------------------------------
function logout() {
    localStorage.removeItem("userSession");
    window.location.href = "user_login.html";   // FIXED
}

// --------------------------------------
// HEADER COLOR (OPTIONAL)
// --------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    const header = document.querySelector("header");
    if (!header) return;

    if (localStorage.getItem("userSession")) {
        header.style.backgroundColor = "#d7f7d7"; // logged in
    } else {
        header.style.backgroundColor = "#f7d7d7"; // not logged in
    }
});
