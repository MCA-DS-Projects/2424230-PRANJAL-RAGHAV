// auth.js - frontend guard
console.log("AUTH JS LOADED ✅");

function checkAuth() {
    const session = localStorage.getItem("userSession");
    if (!session) {
        window.location.href = "sign_in.html";
    }
}

function saveAuth(user, token) {
    localStorage.setItem("userSession", JSON.stringify({ user, token }));
}

function getToken() {
    const s = localStorage.getItem("userSession");
    if (!s) return null;
    return JSON.parse(s).token;
}

function logout() {
    localStorage.removeItem("userSession");
     window.location.href = "user_login.html";
}

document.addEventListener("DOMContentLoaded", () => {
    const header = document.querySelector("header");
    if (header) {
        header.style.backgroundColor = localStorage.getItem("userSession")
            ? "#d7f7d7"   // logged in = light green
            : "#f7d7d7";  // not logged in = light red
    }
});
