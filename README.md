# Relay — Personal AI Assistant

Relay is a personal AI assistant that lives in a single chat window and actually *does things* — checks your calendar, reads and replies to email, manages your tasks, jots down notes, and tracks your expenses. The conversational frontend is a standalone HTML app; all the real work happens in an [n8n](https://n8n.io) workflow behind a webhook, powered by an AI Agent with tool access to your Google services.

> One line in, the right task out.

<img width="955" height="441" alt="Screenshot 2026-07-18 005432" src="https://github.com/user-attachments/assets/3639fff9-50e2-48f5-93a0-66333002429c" />


---

## ✨ What it can do

| Capability | Description |
|---|---|
| 🗓️ **Calendar** | Check upcoming events, get a single event's details, create new events |
| ✉️ **Mail** | Send emails, delete messages, summarize your inbox |
| ✅ **Tasks** | Create, fetch, update, and delete to-dos |
| 📝 **Notes / Docs** | Create, read, and update notes stored as Google Docs |
| 💰 **Budget** | Log expenses to a Google Sheet, remove entries, run quick calculations |
| 🔎 **General Q&A** | Ask anything else — general knowledge, web lookups via Google Search |

Every message is routed automatically — you don't pick a mode, you just talk.

---

## 🧠 How it works

```
You type a message
        │
        ▼
 Frontend (index.html)
        │  POST { message, capability, sessionId, timestamp }
        ▼
   n8n Webhook (trigger)
        │
        ▼
     AI Agent  ──── Simple Memory (conversation history per session)
        │      ──── Groq Chat Model (LLM reasoning)
        │      ──── Tools (see breakdown below)
        ▼
 Respond to Webhook
        │  { "output": "..." }
        ▼
 Frontend renders the reply
```

The frontend does a lightweight **client-side keyword match** (e.g. "meeting," "spend," "note") purely to light up the matching icon in the UI while the request is in flight — the actual decision of *which tool to use* is made by the AI Agent itself inside n8n, using the tools connected to it.

### The n8n workflow

<img width="514" height="269" alt="Screenshot 2026-07-18 003351" src="https://github.com/user-attachments/assets/21c3ec23-e193-4b77-b566-528fba708910" />


The workflow is built around a single **AI Agent** node that has:

- **Simple Memory** — keeps conversation context per session, so Relay remembers what you just asked.
- **Groq Chat Model** — the LLM powering the agent's reasoning and responses.
- **Tool groups**, each wired in as callable tools the agent can choose from on its own:

| Tool group | Nodes | What it lets the agent do |
|---|---|---|
| **Google Calendar** | `Get_Many`, `Event_Creation`, `Get_Single_Event` | Look up events, create events, fetch a specific event |
| **Gmail** | `Send_Message`, `Delete_Message` | Send and delete emails |
| **Google Docs** | `Get_Docs`, `Update_Docs`, `Create_Docs` | Read, edit, and create notes/documents |
| **Google Tasks** | `Create_Tasks`, `Get_Tasks`, `GetMany_Tasks`, `Update_Tasks`, `Delete_Tasks` | Full to-do list management |
| **Expense Tracker** | `Append in Google Sheets`, `Append in Google Sheets1`, `Deletion in Google Sheets1`, `Calculator` | Log expenses to a spreadsheet, remove entries, and do quick math |
| **Google Search** | `Google search in SerpApi` | Answer general questions that need a live web lookup |

The **Webhook** node feeds the AI Agent, and a **Respond to Webhook** node sends the agent's final answer back to the frontend as JSON:
> ⚠️ **Important:** the Webhook (trigger) node's **"Respond"** setting must be set to **"Using 'Respond to Webhook' Node"** — not "Immediately." If it's left on "Immediately," you'll get a `200 OK` with an empty body every time, because n8n replies before the AI Agent has finished thinking.

---

## 🖥️ The frontend

A single self-contained HTML file — no build step, no framework. Open it in any browser.

- Left rail shows the six capabilities as connected nodes; the matching node lights up and a small animated packet "flies" into the chat when a message is routed.
- Chat bubbles show which capability handled each reply (`via Calendar`, `via Tasks`, etc).
- Quick-start chips let you try common requests with one click.
- Runs in a **preview/demo mode** with canned responses if no webhook is configured yet, so you can show it off before wiring up the backend.

---

## 🚀 Setup

### 1. Import the workflow into n8n
Import the workflow JSON (exported from n8n: **Workflow → Download**) into your own n8n instance, or rebuild it following the tool breakdown above.

### 2. Connect your credentials
You'll need OAuth/API credentials set up in n8n for:
- Google Calendar
- Gmail
- Google Docs
- Google Tasks
- Google Sheets
- SerpApi (for Google Search)
- Groq (for the chat model)

### 3. Configure the Webhook node
- Set **Respond** to `Using 'Respond to Webhook' Node`.
- Copy the **Production** webhook URL (not the test URL) once you're ready to go live.

### 4. Activate the workflow
Toggle the workflow to **Active** in the top-right of the n8n editor — production webhooks only listen while the workflow is active.

### 5. Connect the frontend
Open `index.html` and find this near the top of the `<script>` section:

```js
const WEBHOOK_URL = "";
```

Paste your production webhook URL between the quotes:

```js
const WEBHOOK_URL = "https://your-instance.app.n8n.cloud/webhook/your-id";
```

### 6. Open it and start chatting
Just open `index.html` in a browser. No server required.

---

## ⚠️ Notes & limitations

- **CORS:** if your n8n instance doesn't send `Access-Control-Allow-Origin` headers, browser requests from the frontend will be blocked. Set the **Allowed Origins (CORS)** option on the Webhook node, or set the `N8N_CORS_ORIGIN` environment variable on your n8n instance.
- **localhost webhooks:** if you're running n8n locally (e.g. `http://localhost:5678/webhook/...`), the frontend must be opened on the same machine, and CORS still applies.
- **Memory:** conversation memory is scoped per `sessionId`, generated fresh each time the frontend loads — it isn't persisted across browser sessions.

---

## 🛠️ Built with

- [n8n](https://n8n.io) — workflow automation & AI Agent orchestration
- [Groq](https://groq.com) — LLM inference for the agent
- Google Calendar, Gmail, Docs, Tasks, and Sheets APIs
- [SerpApi](https://serpapi.com) — web search tool
- Plain HTML / CSS / JavaScript — no frontend framework or build step

---

## Develper
- Yash Raj
