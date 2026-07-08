"""
Jarvis UI — Tkinter-based GUI
"""
import os
import sys
import queue
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.jarvis import Jarvis


BG        = "#0d1117"
BG2       = "#161b22"
BG3       = "#21262d"
ACCENT    = "#58a6ff"
ACCENT2   = "#3fb950"
WARN      = "#f0883e"
FG        = "#e6edf3"
FG2       = "#8b949e"
RED       = "#f85149"
FONT_MAIN = ("Courier New", 11)
FONT_HEAD = ("Courier New", 13, "bold")
FONT_SMALL= ("Courier New", 9)


class JarvisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("J.A.R.V.I.S.")
        self.configure(bg=BG)
        self.geometry("1100x750")
        self.minsize(800, 600)

        self.jarvis = Jarvis(base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.queue: queue.Queue = queue.Queue()
        self._thinking = False

        self._build_ui()
        self._start_jarvis()
        self._poll_queue()

    def _build_ui(self):
        sidebar = tk.Frame(self, bg=BG2, width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0,1))
        sidebar.pack_propagate(False)
        self._build_sidebar(sidebar)
        main = tk.Frame(self, bg=BG)
        main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=BG3, foreground=FG2,
                        padding=[12, 5], font=FONT_SMALL)
        style.map("TNotebook.Tab",
                  background=[("selected", BG)],
                  foreground=[("selected", ACCENT)])

        self.notebook = ttk.Notebook(main)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self._build_chat_tab()
        self._build_agents_tab()
        self._build_skills_tab()
        self._build_log_tab()

    def _build_sidebar(self, parent):
        logo = tk.Label(parent, text="◈ JARVIS", font=("Courier New", 16, "bold"),
                        fg=ACCENT, bg=BG2, pady=20)
        logo.pack()

        tk.Label(parent, text="powered by Llama 3.1", font=FONT_SMALL,
                 fg=FG2, bg=BG2).pack()

        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        self.status_dot = tk.Label(parent, text="⬤ Checking...", font=FONT_SMALL,
                                   fg=WARN, bg=BG2)
        self.status_dot.pack(pady=4)

        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        tk.Label(parent, text="QUICK ACTIONS", font=FONT_SMALL,
                 fg=FG2, bg=BG2).pack(pady=(0,6))

        for label, cmd in [
            ("📸 Screenshot", lambda: self._quick("take a screenshot")),
            ("🔍 Web Search", self._quick_search),
            ("💻 System Info", lambda: self._quick("get system info")),
            ("🕐 What time is it?", lambda: self._quick("what time is it?")),
            ("🗑 Clear Chat", self._clear_chat),
        ]:
            btn = tk.Button(parent, text=label, font=FONT_SMALL,
                            bg=BG3, fg=FG, activebackground=ACCENT,
                            activeforeground=BG, relief=tk.FLAT,
                            cursor="hand2", padx=8, pady=6,
                            command=cmd)
            btn.pack(fill=tk.X, padx=10, pady=2)

        ttk.Separator(parent, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        tk.Button(parent, text="⟳ Reload Skills", font=FONT_SMALL,
                  bg=BG3, fg=ACCENT2, relief=tk.FLAT, cursor="hand2",
                  padx=8, pady=5,
                  command=self._reload_skills).pack(fill=tk.X, padx=10, pady=2)

        tk.Button(parent, text="⟳ Reload Agents", font=FONT_SMALL,
                  bg=BG3, fg=ACCENT2, relief=tk.FLAT, cursor="hand2",
                  padx=8, pady=5,
                  command=self._reload_agents).pack(fill=tk.X, padx=10, pady=2)


    def _build_chat_tab(self):
        frame = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(frame, text="  💬 Chat  ")

        self.chat_display = scrolledtext.ScrolledText(
            frame, bg=BG, fg=FG, font=FONT_MAIN,
            insertbackground=ACCENT, state=tk.DISABLED,
            relief=tk.FLAT, padx=16, pady=12, wrap=tk.WORD,
            selectbackground=BG3
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        self.chat_display.tag_config("user",    foreground=ACCENT,  font=("Courier New", 11, "bold"))
        self.chat_display.tag_config("jarvis",  foreground=ACCENT2, font=("Courier New", 11, "bold"))
        self.chat_display.tag_config("text",    foreground=FG)
        self.chat_display.tag_config("action",  foreground=WARN)
        self.chat_display.tag_config("system",  foreground=FG2)

        input_bar = tk.Frame(frame, bg=BG2, pady=10)
        input_bar.pack(fill=tk.X, padx=0)

        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(
            input_bar, textvariable=self.input_var,
            bg=BG3, fg=FG, font=FONT_MAIN,
            insertbackground=ACCENT, relief=tk.FLAT,
            disabledbackground=BG3
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(16,8), ipady=8)
        self.input_entry.bind("<Return>", self._on_send)

        self.send_btn = tk.Button(
            input_bar, text="Send ▶", font=FONT_SMALL,
            bg=ACCENT, fg=BG, activebackground=ACCENT2,
            activeforeground=BG, relief=tk.FLAT, cursor="hand2",
            padx=16, pady=6, command=self._on_send
        )
        self.send_btn.pack(side=tk.RIGHT, padx=(0,16))

        self._chat_append("JARVIS", "Online. How can I assist?\n", "jarvis")


    def _build_agents_tab(self):
        frame = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(frame, text="  🤖 Agents  ")

        header = tk.Frame(frame, bg=BG2, pady=8)
        header.pack(fill=tk.X)
        tk.Label(header, text="Autonomous Agents", font=FONT_HEAD,
                 fg=ACCENT, bg=BG2, padx=16).pack(side=tk.LEFT)
        tk.Button(header, text="⟳ Refresh", font=FONT_SMALL,
                  bg=BG3, fg=FG2, relief=tk.FLAT, cursor="hand2",
                  padx=8, command=self._refresh_agents).pack(side=tk.RIGHT, padx=16)

        self.agents_frame = tk.Frame(frame, bg=BG)
        self.agents_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)

    def _build_skills_tab(self):
        frame = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(frame, text="  ⚡ Skills  ")

        header = tk.Frame(frame, bg=BG2, pady=8)
        header.pack(fill=tk.X)
        tk.Label(header, text="Available Skills", font=FONT_HEAD,
                 fg=ACCENT, bg=BG2, padx=16).pack(side=tk.LEFT)
        tk.Button(header, text="+ Add Skill", font=FONT_SMALL,
                  bg=ACCENT2, fg=BG, relief=tk.FLAT, cursor="hand2",
                  padx=8, command=self._open_skill_dir).pack(side=tk.RIGHT, padx=16)

        self.skills_text = scrolledtext.ScrolledText(
            frame, bg=BG, fg=FG, font=FONT_MAIN,
            state=tk.DISABLED, relief=tk.FLAT, padx=16, pady=12
        )
        self.skills_text.pack(fill=tk.BOTH, expand=True)

    def _build_log_tab(self):
        frame = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(frame, text="  📋 Log  ")

        self.log_display = scrolledtext.ScrolledText(
            frame, bg=BG, fg=FG2, font=FONT_SMALL,
            state=tk.DISABLED, relief=tk.FLAT, padx=16, pady=12
        )
        self.log_display.pack(fill=tk.BOTH, expand=True)


    def _start_jarvis(self):
        def _init():
            self.jarvis.start()
            if self.jarvis.ollama_ok:
                self.queue.put(("status", "online"))
                self.queue.put(("log", "[Jarvis] Ollama connected ✓"))
            else:
                self.queue.put(("status", "offline"))
                self.queue.put(("log", "[Jarvis] Ollama offline — skills still available"))
            self.queue.put(("refresh_agents", None))
            self.queue.put(("refresh_skills", None))

        threading.Thread(target=_init, daemon=True).start()

    def _on_send(self, event=None):
        if self._thinking:
            return
        text = self.input_var.get().strip()
        if not text:
            return
        self.input_var.set("")
        self._chat_append("YOU", text + "\n", "user")
        self._thinking = True
        self.send_btn.config(state=tk.DISABLED, text="...")
        self.input_entry.config(state=tk.DISABLED)
        threading.Thread(target=self._stream_response, args=(text,), daemon=True).start()

    def _stream_response(self, text: str):
        self.queue.put(("chat_start", "JARVIS"))
        full = ""
        for chunk in self.jarvis.chat_stream(text):
            full += chunk
            self.queue.put(("chat_chunk", chunk))
        self.queue.put(("chat_end", None))
        self.queue.put(("refresh_agents", None))

    def _poll_queue(self):
        try:
            while True:
                item = self.queue.get_nowait()
                kind, data = item

                if kind == "chat_start":
                    self._chat_append(data, "", "jarvis")
                elif kind == "chat_chunk":
                    self._chat_chunk(data)
                elif kind == "chat_end":
                    self._chat_nl()
                    self._thinking = False
                    self.send_btn.config(state=tk.NORMAL, text="Send ▶")
                    self.input_entry.config(state=tk.NORMAL)
                    self.input_entry.focus()
                elif kind == "status":
                    if data == "online":
                        self.status_dot.config(text="⬤ Llama 3.1 Online", fg=ACCENT2)
                    else:
                        self.status_dot.config(text="⬤ Ollama Offline", fg=RED)
                elif kind == "log":
                    self._log(data)
                elif kind == "refresh_agents":
                    self._refresh_agents()
                elif kind == "refresh_skills":
                    self._refresh_skills()

        except queue.Empty:
            pass
        self.after(50, self._poll_queue)


    def _chat_append(self, speaker: str, text: str, tag: str):
        self.chat_display.config(state=tk.NORMAL)
        if speaker:
            self.chat_display.insert(tk.END, f"\n{speaker}: ", tag)
        if text:
            self.chat_display.insert(tk.END, text, "text")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _chat_chunk(self, chunk: str):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, chunk, "text")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _chat_nl(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _log(self, msg: str):
        self.log_display.config(state=tk.NORMAL)
        self.log_display.insert(tk.END, msg + "\n")
        self.log_display.config(state=tk.DISABLED)
        self.log_display.see(tk.END)


    def _refresh_agents(self):
        for w in self.agents_frame.winfo_children():
            w.destroy()

        agents = self.jarvis.agent_runner.status_all()
        if not agents:
            tk.Label(self.agents_frame, text="No agents loaded.\nAdd .py files to the /agents directory.",
                     font=FONT_MAIN, fg=FG2, bg=BG).pack(pady=40)
            return

        for a in agents:
            card = tk.Frame(self.agents_frame, bg=BG2, pady=8, padx=12)
            card.pack(fill=tk.X, pady=4)

            dot_color = ACCENT2 if a["enabled"] else FG2
            status_color = WARN if a["status"] == "running" else (RED if a["status"] == "error" else ACCENT2)

            top = tk.Frame(card, bg=BG2)
            top.pack(fill=tk.X)
            tk.Label(top, text=f"⬤ {a['name']}", font=FONT_MAIN,
                     fg=dot_color, bg=BG2).pack(side=tk.LEFT)
            tk.Label(top, text=f"[{a['status']}]", font=FONT_SMALL,
                     fg=status_color, bg=BG2).pack(side=tk.LEFT, padx=8)
            interval_txt = f"every {a['interval']}s" if a["interval"] > 0 else "one-shot"
            tk.Label(top, text=interval_txt, font=FONT_SMALL,
                     fg=FG2, bg=BG2).pack(side=tk.LEFT)

            name = a["name"]
            btn_frame = tk.Frame(card, bg=BG2)
            btn_frame.pack(fill=tk.X, pady=(4, 0))
            tk.Button(btn_frame, text="▶ Run Now", font=FONT_SMALL,
                      bg=BG3, fg=ACCENT, relief=tk.FLAT, cursor="hand2", padx=6,
                      command=lambda n=name: self._run_agent(n)).pack(side=tk.LEFT, padx=(0,6))
            toggle_lbl = "⏸ Disable" if a["enabled"] else "▶ Enable"
            tk.Button(btn_frame, text=toggle_lbl, font=FONT_SMALL,
                      bg=BG3, fg=WARN, relief=tk.FLAT, cursor="hand2", padx=6,
                      command=lambda n=name: self._toggle_agent(n)).pack(side=tk.LEFT)

            tk.Label(card, text=a["description"], font=FONT_SMALL,
                     fg=FG2, bg=BG2).pack(anchor=tk.W)
            if a["last_output"]:
                tk.Label(card, text=f"↳ {a['last_output'][:120]}", font=FONT_SMALL,
                         fg=FG, bg=BG2).pack(anchor=tk.W)

    def _refresh_skills(self):
        self.skills_text.config(state=tk.NORMAL)
        self.skills_text.delete("1.0", tk.END)
        desc = self.jarvis.skill_manager.get_skill_descriptions()
        self.skills_text.insert(tk.END, desc)
        self.skills_text.config(state=tk.DISABLED)

    def _run_agent(self, name: str):
        def _run():
            result = self.jarvis.agent_runner.run_agent_now(name)
            self.queue.put(("log", f"[Agent:{name}] {result}"))
            self.queue.put(("refresh_agents", None))
        threading.Thread(target=_run, daemon=True).start()

    def _toggle_agent(self, name: str):
        msg = self.jarvis.agent_runner.toggle(name)
        self.queue.put(("log", msg))
        self.queue.put(("refresh_agents", None))


    def _quick(self, text: str):
        self.input_var.set(text)
        self._on_send()
        self.notebook.select(0)

    def _quick_search(self):
        q = simpledialog.askstring("Search", "Search the web for:", parent=self)
        if q:
            self._quick(f"search for {q}")

    def _clear_chat(self):
        self.jarvis.clear_history()
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self._chat_append("JARVIS", "Chat cleared. How can I assist?\n", "jarvis")

    def _reload_skills(self):
        self.jarvis.reload_skills()
        self._refresh_skills()
        self._log("[Jarvis] Skills reloaded.")

    def _reload_agents(self):
        self.jarvis.reload_agents()
        self._refresh_agents()
        self._log("[Jarvis] Agents reloaded.")

    def _open_skill_dir(self):
        import webbrowser, os
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills")
        webbrowser.open(f"file://{path}")
