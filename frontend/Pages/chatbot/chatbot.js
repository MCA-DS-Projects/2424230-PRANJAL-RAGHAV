(async () => {

  // add html
  document.body.insertAdjacentHTML("beforeend",
    await (await fetch("chatbot/chatbot.html")).text()
);

let css = document.createElement("link");
css.rel="stylesheet";
css.href = "chatbot/chatbot.css";
document.head.appendChild(css);


  const toggler=document.querySelector(".chatbot-toggler");
  const close=document.querySelector(".close-btn");
  const chatbox=document.querySelector(".chatbox");
  const input=document.querySelector(".chat-input textarea");
  const send=document.getElementById("send-btn");

  function add(type,text){
    let li=document.createElement("li");
    li.className="chat "+type;
    li.innerHTML=`<p>${text}</p>`;
    chatbox.appendChild(li);
    chatbox.scrollTop=chatbox.scrollHeight;
  }

  async function callAI(msg){
    let r=await fetch("http://127.0.0.1:5000/api/chat",{
      method:"POST",headers:{"Content-Type":"application/json"},
      body:JSON.stringify({message:msg})
    });
    return (await r.json()).reply;
  }

  async function sendMsg(){
    let msg=input.value.trim();
    if(!msg) return;
    add("outgoing",msg);
    input.value="";
    add("incoming","Thinking...");
    let reply=await callAI(msg);
    chatbox.lastChild.querySelector("p").innerText=reply;
  }

  send.onclick=sendMsg;
  
  // ✅ ADD THIS HERE
  input.addEventListener("keydown", (e)=>{
    if(e.key === "Enter" && !e.shiftKey){
      e.preventDefault();
      sendMsg();
    }
  });

  toggler.onclick=()=>document.body.classList.toggle("show-chatbot");
  close.onclick=()=>document.body.classList.remove("show-chatbot");

})();