(async () => {

  // Load chatbot HTML
  document.body.insertAdjacentHTML(
    "beforeend",
    await (await fetch("chatbot/chatbot.html")).text()
  );

  // Load CSS
  const css = document.createElement("link");
  css.rel = "stylesheet";
  css.href = "chatbot/chatbot.css";
  document.head.appendChild(css);

  const toggler = document.querySelector(".chatbot-toggler");
  const closeBtn = document.querySelector(".close-btn");
  const chatbox = document.querySelector(".chatbox");
  const input = document.querySelector(".chat-input textarea");
  const sendBtn = document.getElementById("send-btn");

  // Add message to UI
  function addMessage(type, text) {
    let li = document.createElement("li");
    li.className = "chat " + type;
    li.innerHTML = `<p>${text}</p>`;
    chatbox.appendChild(li);
    chatbox.scrollTop = chatbox.scrollHeight;
  }

  async function callAI(msg) {
    let r = await fetch(`${window.API_BASE_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg })
    });

    let data = await r.json();
    return data.reply;
  }

  async function sendMsg() {
    let msg = input.value.trim();
    if (!msg) return;

    addMessage("outgoing", msg);
    input.value = "";

    addMessage("incoming", "Thinking...");

    let reply = await callAI(msg);
    chatbox.lastChild.querySelector("p").innerText = reply;
  }

  // Button click
  sendBtn.onclick = sendMsg;

  // ENTER key support (Shift+Enter → new line)
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMsg();
    }
  });

  // Toggle chat UI
  toggler.onclick = () => document.body.classList.toggle("show-chatbot");
  closeBtn.onclick = () => document.body.classList.remove("show-chatbot");

})();
