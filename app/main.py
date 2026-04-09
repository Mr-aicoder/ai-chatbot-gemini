from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

try:
    # Works when running as module: uvicorn app.main:app
    from app.llm import get_response
except ModuleNotFoundError:
    # Works when running file directly: python app/main.py
    from llm import get_response

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "AI Chatbot is running 🚀"}

@app.get("/chat-ui", response_class=HTMLResponse)
def chat_ui():
    return """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>AI Chatbot</title>
        <style>
          body { font-family: Arial, sans-serif; max-width: 760px; margin: 24px auto; padding: 0 12px; }
          h1 { margin-bottom: 8px; }
          #chat { border: 1px solid #ddd; border-radius: 8px; padding: 12px; height: 360px; overflow-y: auto; background: #fafafa; }
          .msg { margin: 8px 0; white-space: pre-wrap; }
          .user { color: #1f4aa8; }
          .bot { color: #12824a; }
          .row { display: flex; gap: 8px; margin-top: 12px; }
          input { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 6px; }
          button { padding: 10px 14px; border: none; border-radius: 6px; background: #111; color: white; cursor: pointer; }
          button:disabled { opacity: 0.6; cursor: not-allowed; }
        </style>
      </head>
      <body>
        <h1>AI Chatbot</h1>
        <p>Send a message to test your Gemini-backed API.</p>
        <div id="chat"></div>
        <div class="row">
          <input id="message" placeholder="Type your message..." />
          <button id="sendBtn">Send</button>
        </div>

        <script>
          const chat = document.getElementById("chat");
          const messageInput = document.getElementById("message");
          const sendBtn = document.getElementById("sendBtn");

          function addMessage(role, text) {
            const div = document.createElement("div");
            div.className = "msg " + role;
            div.textContent = (role === "user" ? "You: " : "Bot: ") + text;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
          }

          async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;

            addMessage("user", message);
            messageInput.value = "";
            sendBtn.disabled = true;

            try {
              const res = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message }),
              });
              const data = await res.json();
              addMessage("bot", data.response || "No response");
            } catch (err) {
              addMessage("bot", "Error: unable to reach server.");
            } finally {
              sendBtn.disabled = false;
              messageInput.focus();
            }
          }

          sendBtn.addEventListener("click", sendMessage);
          messageInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter") sendMessage();
          });
        </script>
      </body>
    </html>
    """

@app.post("/chat")
def chat(req: ChatRequest):
    reply = get_response(req.message)
    return {"response": reply}
