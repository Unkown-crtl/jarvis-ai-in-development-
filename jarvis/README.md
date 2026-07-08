# J.A.R.V.I.S.
**Just A Rather Very Intelligent System** — local AI desktop assistant powered by **Llama 3.1** via Ollama.

---

## Quick Start

### 1. Install Ollama + Llama 3.1
```bash
# Install Ollama (https://ollama.com)
curl -fsSL https://ollama.com/install.sh | sh

# Pull Llama 3.1
ollama pull llama3.1

# Start Ollama (runs in background)
ollama serve
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Jarvis
```bash
python main.py          # GUI mode
python main.py --cli    # CLI mode
```

---

## Project Structure

```
jarvis/
├── main.py               # Entry point
├── requirements.txt
│
├── core/
│   ├── brain.py          # Ollama/Llama 3.1 interface
│   ├── jarvis.py         # Orchestrator
│   ├── skill_manager.py  # Dynamic skill loader
│   └── agent_runner.py   # Background agent scheduler
│
├── skills/               # ← Add your skill .py files here
│   ├── desktop.py        # Built-in: open apps, screenshot, shell, etc.
│   └── _template.py      # Copy this to add new skills
│
├── agents/               # ← Add your agent .py files here
│   ├── system_monitor.py # Built-in: CPU/RAM monitor
│   ├── reminder.py       # Built-in: reminder checker
│   └── _template.py      # Copy this to add new agents
│
└── ui/
    └── app.py            # Tkinter GUI
```

---

## Adding Skills

1. Copy `skills/_template.py` to a new file, e.g. `skills/spotify.py`
2. Write your Python function(s)
3. Add them to the `SKILLS` list in the file
4. Click **⟳ Reload Skills** in the sidebar (no restart needed)

Jarvis will automatically tell Llama 3.1 about your new skill, so you can ask naturally:

> "Play some lo-fi music on Spotify"

And it will call your skill.

---

## Adding Agents

Agents run **automatically in the background** at a set interval.

1. Copy `agents/_template.py` to a new file
2. Write a function that returns a string result
3. Add it to the `AGENTS` list with an `interval` in seconds
4. Click **⟳ Reload Agents** or restart

---

## Built-in Skills

| Skill | Description |
|-------|-------------|
| `open_app` | Open any desktop application |
| `take_screenshot` | Capture the screen |
| `search_web` | Google search in browser |
| `run_command` | Execute shell commands |
| `get_system_info` | CPU, RAM, disk stats |
| `get_time` | Current date and time |
| `open_url` | Open any URL |
| `write_file` | Write content to a file |
| `read_file` | Read a file's content |

---

## Built-in Agents

| Agent | Interval | Description |
|-------|----------|-------------|
| `system_monitor` | 60s | Alerts when CPU > 85% or RAM > 90% |
| `reminder` | 30s | Fires reminders from `reminders.json` |

---

## Adding Reminders

Create/edit `reminders.json` in the project root:

```json
[
  {
    "message": "Take a break!",
    "due": "2025-01-01T15:00:00"
  }
]
```
