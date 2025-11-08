document.addEventListener("DOMContentLoaded", () => {
  const nav = document.getElementById("navMenu");
  if (!nav) return;

  const sessionRaw = localStorage.getItem("userSession");
  const loggedIn = !!sessionRaw;

  let name = "User";
  if (loggedIn) {
    try {
      const s = JSON.parse(sessionRaw);
      name = (s.user?.fullName || s.user?.email || "User").trim();
    } catch (_) {}
  }

  const initials = name.split(/\s+/).map(p => p[0]).slice(0,2).join("").toUpperCase();

  const page = location.pathname.split("/").pop();
  const link = (href, text) => `<a href="${href}" class="nav-link ${page === href ? "active" : ""}">${text}</a>`;

  if (loggedIn) {
    nav.innerHTML = `
      ${link("user_dashboard.html","Dashboard")}
      ${link("food_recommendations.html","Recommendations")}
      ${link("body_type_quiz.html","Take Quiz")}
      ${link("body_type_results.html","My Results")}
      ${link("user_profile_settings.html","Account")}

      <span class="avatar" title="${name}">${initials}</span>

      <button onclick="logout()" class="logout-btn">Logout</button>
    `;
  } else {
    nav.innerHTML = `
      ${link("user_login.html","Sign In")}
      ${link("user_registration.html","Sign Up")}
      ${link("body_type_quiz.html","Take Quiz")}
      ${link("food_recommendations.html","Recommendations")}
    `;
  }
});
