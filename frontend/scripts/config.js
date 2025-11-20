// Detect host automatically (IP or domain)
const HOST = location.hostname;

// Backend port (only change here)
const BACKEND_PORT = 5000;

// Central API base
window.API_BASE_URL = `https://${HOST}:${BACKEND_PORT}`;
