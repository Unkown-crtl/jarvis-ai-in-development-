"""
Jarvis UI v2 — Clean blue-tile design with voice, code engine, MCP tester,
reasoning display, and modular skill/agent panels.
"""
import os, sys, queue, threading, tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog, filedialog

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.jarvis import Jarvis
from core.voice import VoiceController

# ─── Design Tokens ───────────────────────────────────────────────────────────
BG        = "#050d1a"   # deep navy
BG2       = "#0a1628"   # card bg
TILE      = "#0d1f3c"   # big tile bg
TILE_H    = "#102448"   # tile hover
BORDER    = "#1a3a6b"   # tile border
BLUE1     = "#1565c0"   # primary blue
BLUE2     = "#1976d2"   # medium blue
BLUE3     = "#2196f3"   # bright blue
BLUE4     = "#42a5f5"   # accent blue
CYAN      = "#00e5ff"   # active/voice glow
GREEN     = "#00e676"   # success
AMBER     = "#ffab00"   # warning / thinking
RED       = "#ff1744"   # error
FG        = "#e8f4fd"   # main text
FG2       = "#7eb3d8"   # secondary text
FG3       = "#3d6d9e"   # muted
MONO      = "Consolas"
SANS      = "Segoe UI"
HEAD      = ("Segoe UI", 11, "bold")
MONO_SM   = (MONO, 9)
MONO_MD   = (MONO, 10)
MONO_LG   = (MONO, 11)

def _hex(c): return c

# ─── App ─────────────────────────────────────────────────────────────────────
class JarvisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("J·A·R·V·I·S")
        self.configure(bg=BG)
        self.geometry("1280x820")
        self.minsize(1000, 700)
        self._configure_styles()

        self.jarvis = Jarvis(base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.voice  = VoiceController()
        self.q: queue.Queue = queue.Queue()
        self._busy       = False
        self._voice_on   = False
        self._current_tab = "chat"
        self._plan_data  = None
        self._code_buffer = ""

        self._build()
        self._boot()
        self._poll()

    # ── Styles ───────────────────────────────────────────────────────────────
    def _configure_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TNotebook",        background=BG,    borderwidth=0)
        s.configure("TNotebook.Tab",    background=BG2,   foreground=FG2,
                    padding=[14,6],     font=(SANS,9,"bold"))
        s.map("TNotebook.Tab",
              background=[("selected", TILE)],
              foreground=[("selected", CYAN)])
        s.configure("TSeparator",       background=BORDER)
        s.configure("Vertical.TScrollbar",  background=BG2, troughcolor=BG,
                    borderwidth=0, arrowcolor=BLUE3)
        s.configure("Horizontal.TScrollbar", background=BG2, troughcolor=BG,
                    borderwidth=0, arrowcolor=BLUE3)

    # ── Layout ───────────────────────────────────────────────────────────────
    def _build(self):
        # Top bar
        self._top_bar()
        # Body: sidebar + main
        body = tk.Frame(self, bg=BG)
        body.pack(fill=tk.BOTH, expand=True)
        self._sidebar(body)
        self._main(body)

    def _top_bar(self):
        bar = tk.Frame(self, bg=BG2, height=52)
        bar.pack(fill=tk.X, side=tk.TOP)
        bar.pack_propagate(False)

        tk.Label(bar, text="◈ J·A·R·V·I·S", font=("Segoe UI", 15, "bold"),
                 fg=CYAN, bg=BG2, padx=20).pack(side=tk.LEFT, pady=8)
        tk.Label(bar, text="powered by Llama 3.1", font=(SANS, 9),
                 fg=FG3, bg=BG2).pack(side=tk.LEFT)

        # right side controls
        r = tk.Frame(bar, bg=BG2)
        r.pack(side=tk.RIGHT, padx=14)

        self.ollama_lbl = tk.Label(r, text="⬤ Connecting…", font=(SANS,9),
                                   fg=AMBER, bg=BG2)
        self.ollama_lbl.pack(side=tk.LEFT, padx=10)

        self.voice_btn = self._icon_btn(r, "🎤 Voice OFF", self._toggle_voice,
                                        bg=TILE, fg=FG2, width=11)
        self.voice_btn.pack(side=tk.LEFT, padx=4)

        self._icon_btn(r, "⚙ Settings", self._open_settings, bg=TILE, fg=FG2).pack(side=tk.LEFT, padx=4)

    def _sidebar(self, parent):
        sb = tk.Frame(parent, bg=BG2, width=68)
        sb.pack(side=tk.LEFT, fill=tk.Y)
        sb.pack_propagate(False)

        icons = [
            ("💬", "chat",    "Chat"),
            ("🧠", "reason",  "Reason"),
            ("💻", "code",    "Code"),
            ("🔌", "mcp",     "MCP"),
            ("🤖", "agents",  "Agents"),
            ("⚡", "skills",  "Skills"),
            ("📋", "log",     "Log"),
        ]
        self._nav_btns = {}
        for icon, key, tip in icons:
            btn = tk.Button(sb, text=icon, font=("Segoe UI",16),
                            bg=BG2, fg=FG2, relief=tk.FLAT,
                            cursor="hand2", width=3, pady=10,
                            activebackground=TILE, activeforeground=CYAN,
                            command=lambda k=key: self._switch_tab(k))
            btn.pack(fill=tk.X)
            self._nav_btns[key] = btn
            self._tooltip(btn, tip)

        # Spacer
        tk.Frame(sb, bg=BG2).pack(fill=tk.BOTH, expand=True)

        # Voice indicator
        self.voice_dot = tk.Label(sb, text="●", font=("Segoe UI",20),
                                   fg=FG3, bg=BG2)
        self.voice_dot.pack(pady=8)

    def _main(self, parent):
        self.main_frame = tk.Frame(parent, bg=BG)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._tabs = {}
        for key, builder in [
            ("chat",   self._tab_chat),
            ("reason", self._tab_reason),
            ("code",   self._tab_code),
            ("mcp",    self._tab_mcp),
            ("agents", self._tab_agents),
            ("skills", self._tab_skills),
            ("log",    self._tab_log),
        ]:
            f = tk.Frame(self.main_frame, bg=BG)
            builder(f)
            self._tabs[key] = f

        self._switch_tab("chat")

    # ── Navigation ───────────────────────────────────────────────────────────
    def _switch_tab(self, key: str):
        for k, f in self._tabs.items():
            f.pack_forget()
        self._tabs[key].pack(fill=tk.BOTH, expand=True)
        self._current_tab = key
        for k, b in self._nav_btns.items():
            b.config(bg=TILE if k==key else BG2,
                     fg=CYAN if k==key else FG2)
        if key == "agents": self._refresh_agents()
        if key == "skills": self._refresh_skills()

    # ═══════════════════════════════ CHAT TAB ════════════════════════════════
    def _tab_chat(self, f):
        # Quick tile row
        tiles = tk.Frame(f, bg=BG, pady=10)
        tiles.pack(fill=tk.X, padx=16)
        quick_actions = [
            ("📸", "Screenshot",  lambda: self._send_msg("take a screenshot")),
            ("💻", "System Info", lambda: self._send_msg("get system info")),
            ("🕐", "Time",        lambda: self._send_msg("what time is it?")),
            ("🌐", "Web Search",  self._quick_search),
            ("📂", "Open App",    self._quick_open_app),
        ]
        for icon, lbl, cmd in quick_actions:
            self._big_tile(tiles, icon, lbl, cmd).pack(side=tk.LEFT, padx=6, pady=4)

        ttk.Separator(f, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=16)

        # Thinking banner (hidden by default)
        self.think_bar = tk.Frame(f, bg=BLUE1, height=28)
        self.think_lbl = tk.Label(self.think_bar, text="", font=(SANS,9),
                                   fg=FG, bg=BLUE1, padx=12)
        self.think_lbl.pack(side=tk.LEFT)

        # Chat display
        self.chat_out = scrolledtext.ScrolledText(
            f, bg=BG, fg=FG, font=MONO_MD, relief=tk.FLAT,
            padx=18, pady=12, wrap=tk.WORD, state=tk.DISABLED,
            insertbackground=BLUE3, selectbackground=BLUE1,
        )
        self.chat_out.pack(fill=tk.BOTH, expand=True)

        tags = {
            "you":      {"foreground": BLUE4,  "font":(MONO,10,"bold")},
            "jarvis":   {"foreground": CYAN,   "font":(MONO,10,"bold")},
            "text":     {"foreground": FG},
            "think":    {"foreground": AMBER,  "font":(MONO,9,"italic")},
            "action":   {"foreground": GREEN,  "font":(MONO,9)},
            "error":    {"foreground": RED,    "font":(MONO,9)},
            "plan":     {"foreground": BLUE4,  "font":(MONO,9)},
            "dim":      {"foreground": FG3},
        }
        for name, cfg in tags.items():
            self.chat_out.tag_config(name, **cfg)

        # Input row
        inp = tk.Frame(f, bg=BG2, pady=10)
        inp.pack(fill=tk.X)

        self.inp_var = tk.StringVar()
        self.inp_entry = tk.Entry(inp, textvariable=self.inp_var,
                                   bg=TILE, fg=FG, font=MONO_MD,
                                   insertbackground=CYAN, relief=tk.FLAT,
                                   disabledbackground=TILE)
        self.inp_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(16,8), ipady=9)
        self.inp_entry.bind("<Return>", lambda e: self._on_send())

        self.send_btn = tk.Button(inp, text="Send ▶", font=(SANS,9,"bold"),
                                   bg=BLUE2, fg=FG, relief=tk.FLAT,
                                   activebackground=BLUE3, cursor="hand2",
                                   padx=18, pady=6, command=self._on_send)
        self.send_btn.pack(side=tk.RIGHT, padx=(0,16))

        self.reason_btn = tk.Button(inp, text="🧠 Think", font=(SANS,9,"bold"),
                                     bg=TILE, fg=BLUE4, relief=tk.FLAT,
                                     activebackground=BLUE1, cursor="hand2",
                                     padx=10, pady=6,
                                     command=lambda: self._on_send(force_reason=True))
        self.reason_btn.pack(side=tk.RIGHT, padx=4)

        self._chat_append("jarvis", "JARVIS", "")
        self._chat_append("text",   "",
                          "Online and ready. You can type, use quick tiles, or press 🎤 Voice to speak.\n")

    # ═══════════════════════════════ REASON TAB ══════════════════════════════
    def _tab_reason(self, f):
        hdr = tk.Frame(f, bg=BG2, pady=10)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="🧠  Reasoning Engine", font=(SANS,13,"bold"),
                 fg=CYAN, bg=BG2, padx=16).pack(side=tk.LEFT)
        tk.Label(hdr, text="Plan → Reason → Act", font=(SANS,9),
                 fg=FG3, bg=BG2).pack(side=tk.LEFT, padx=8)

        # Plan display
        plan_lbl = tk.Frame(f, bg=BG, padx=16, pady=6)
        plan_lbl.pack(fill=tk.X)
        tk.Label(plan_lbl, text="CURRENT PLAN", font=(SANS,8,"bold"),
                 fg=FG3, bg=BG).pack(anchor=tk.W)

        self.plan_out = scrolledtext.ScrolledText(
            f, bg=BG2, fg=BLUE4, font=MONO_SM, height=8,
            relief=tk.FLAT, padx=12, pady=8, state=tk.DISABLED
        )
        self.plan_out.pack(fill=tk.X, padx=16, pady=(0,4))

        ttk.Separator(f, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=16, pady=4)

        tk.Label(f, text="REASONING TRACE", font=(SANS,8,"bold"),
                 fg=FG3, bg=BG, padx=16).pack(anchor=tk.W)

        self.reason_out = scrolledtext.ScrolledText(
            f, bg=BG, fg=FG, font=MONO_SM, relief=tk.FLAT,
            padx=12, pady=8, state=tk.DISABLED
        )
        self.reason_out.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0,16))

        self.reason_out.tag_config("thinking", foreground=AMBER)
        self.reason_out.tag_config("conclude", foreground=GREEN)
        self.reason_out.tag_config("dim",      foreground=FG3)

    # ═══════════════════════════════ CODE TAB ════════════════════════════════
    def _tab_code(self, f):
        hdr = tk.Frame(f, bg=BG2, pady=8)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="💻  Code Engine", font=(SANS,13,"bold"),
                 fg=CYAN, bg=BG2, padx=16).pack(side=tk.LEFT)

        # Stage buttons (tile row)
        stages = tk.Frame(f, bg=BG, pady=8)
        stages.pack(fill=tk.X, padx=16)
        for icon, lbl, cmd in [
            ("🔍","Review",  lambda: self._run_code_stage("review")),
            ("🐛","Debug",   lambda: self._run_code_stage("debug")),
            ("🔧","Fix",     lambda: self._run_code_stage("fix")),
            ("⬆","Upgrade", lambda: self._run_code_stage("upgrade")),
            ("🚀","Full Run",lambda: self._run_code_stage("full")),
        ]:
            self._big_tile(stages, icon, lbl, cmd).pack(side=tk.LEFT, padx=5)

        ttk.Separator(f, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=16, pady=4)

        paned = tk.PanedWindow(f, orient=tk.HORIZONTAL, bg=BG,
                                sashwidth=6, sashpad=2, sashrelief=tk.FLAT)
        paned.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)

        # Left: code input
        left = tk.Frame(paned, bg=BG)
        paned.add(left, minsize=300)
        top_l = tk.Frame(left, bg=BG)
        top_l.pack(fill=tk.X)
        tk.Label(top_l, text="INPUT CODE", font=(SANS,8,"bold"),
                 fg=FG3, bg=BG).pack(side=tk.LEFT)
        tk.Button(top_l, text="📂 Load File", font=(SANS,8), bg=TILE, fg=FG2,
                  relief=tk.FLAT, cursor="hand2", padx=6,
                  command=self._load_code_file).pack(side=tk.RIGHT, pady=2)
        tk.Button(top_l, text="✂ Clear", font=(SANS,8), bg=TILE, fg=FG2,
                  relief=tk.FLAT, cursor="hand2", padx=6,
                  command=self._clear_code_input).pack(side=tk.RIGHT, padx=4, pady=2)

        self.code_in = tk.Text(left, bg=TILE, fg=FG, font=MONO_MD,
                                insertbackground=CYAN, relief=tk.FLAT,
                                padx=8, pady=8, wrap=tk.NONE)
        self.code_in.pack(fill=tk.BOTH, expand=True, pady=4)
        self.code_in.insert("1.0", "# Paste or type your code here\n\ndef example():\n    x = []\n    print(x[5])  # IndexError!\n")

        # Right: output
        right = tk.Frame(paned, bg=BG)
        paned.add(right, minsize=300)
        tk.Label(right, text="ANALYSIS OUTPUT", font=(SANS,8,"bold"),
                 fg=FG3, bg=BG).pack(anchor=tk.W)

        self.code_out = scrolledtext.ScrolledText(
            right, bg=BG2, fg=FG, font=MONO_SM, relief=tk.FLAT,
            padx=10, pady=8, state=tk.DISABLED
        )
        self.code_out.pack(fill=tk.BOTH, expand=True, pady=4)
        self.code_out.tag_config("stage",   foreground=CYAN,  font=(MONO,9,"bold"))
        self.code_out.tag_config("ok",      foreground=GREEN)
        self.code_out.tag_config("warn",    foreground=AMBER)
        self.code_out.tag_config("err",     foreground=RED)
        self.code_out.tag_config("code",    foreground=BLUE4, font=MONO_SM)

    # ═══════════════════════════════ MCP TAB ═════════════════════════════════
    def _tab_mcp(self, f):
        hdr = tk.Frame(f, bg=BG2, pady=8)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="🔌  MCP Server Tester", font=(SANS,13,"bold"),
                 fg=CYAN, bg=BG2, padx=16).pack(side=tk.LEFT)

        url_row = tk.Frame(f, bg=BG, pady=10)
        url_row.pack(fill=tk.X, padx=16)
        tk.Label(url_row, text="Server URL:", font=(SANS,9), fg=FG2, bg=BG).pack(side=tk.LEFT)
        self.mcp_url_var = tk.StringVar(value="http://localhost:3000")
        tk.Entry(url_row, textvariable=self.mcp_url_var, bg=TILE, fg=FG,
                 font=MONO_MD, insertbackground=CYAN, relief=tk.FLAT,
                 width=40).pack(side=tk.LEFT, padx=8, ipady=6)

        for lbl, cmd in [
            ("▶ Full Test",    lambda: self._run_mcp("test")),
            ("⚡ Ping",        lambda: self._run_mcp("ping")),
            ("📋 List Tools",  lambda: self._run_mcp("list")),
        ]:
            tk.Button(url_row, text=lbl, font=(SANS,9), bg=BLUE1, fg=FG,
                      relief=tk.FLAT, cursor="hand2", padx=10, pady=4,
                      command=cmd).pack(side=tk.LEFT, padx=4)

        # Tool call row
        tool_row = tk.Frame(f, bg=BG, pady=4)
        tool_row.pack(fill=tk.X, padx=16)
        tk.Label(tool_row, text="Tool name:", font=(SANS,9), fg=FG2, bg=BG).pack(side=tk.LEFT)
        self.mcp_tool_var = tk.StringVar()
        tk.Entry(tool_row, textvariable=self.mcp_tool_var, bg=TILE, fg=FG,
                 font=MONO_MD, insertbackground=CYAN, relief=tk.FLAT,
                 width=20).pack(side=tk.LEFT, padx=8, ipady=5)
        tk.Label(tool_row, text="Params (JSON):", font=(SANS,9), fg=FG2, bg=BG).pack(side=tk.LEFT)
        self.mcp_params_var = tk.StringVar(value="{}")
        tk.Entry(tool_row, textvariable=self.mcp_params_var, bg=TILE, fg=FG,
                 font=MONO_MD, insertbackground=CYAN, relief=tk.FLAT,
                 width=26).pack(side=tk.LEFT, padx=8, ipady=5)
        tk.Button(tool_row, text="🔧 Call Tool", font=(SANS,9), bg=BLUE2, fg=FG,
                  relief=tk.FLAT, cursor="hand2", padx=10, pady=4,
                  command=lambda: self._run_mcp("call")).pack(side=tk.LEFT, padx=4)

        ttk.Separator(f, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=16, pady=4)

        self.mcp_out = scrolledtext.ScrolledText(
            f, bg=BG, fg=FG, font=MONO_SM, relief=tk.FLAT,
            padx=14, pady=10, state=tk.DISABLED
        )
        self.mcp_out.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0,16))
        self.mcp_out.tag_config("ok",   foreground=GREEN)
        self.mcp_out.tag_config("err",  foreground=RED)
        self.mcp_out.tag_config("hdr",  foreground=CYAN, font=(MONO,9,"bold"))
        self.mcp_out.tag_config("dim",  foreground=FG3)

    # ═══════════════════════════════ AGENTS TAB ══════════════════════════════
    def _tab_agents(self, f):
        hdr = tk.Frame(f, bg=BG2, pady=8)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="🤖  Agents", font=(SANS,13,"bold"),
                 fg=CYAN, bg=BG2, padx=16).pack(side=tk.LEFT)
        tk.Button(hdr, text="⟳ Refresh", font=(SANS,9), bg=TILE, fg=FG2,
                  relief=tk.FLAT, cursor="hand2", padx=8,
                  command=self._refresh_agents).pack(side=tk.RIGHT, padx=16)
        tk.Button(hdr, text="⟳ Reload", font=(SANS,9), bg=TILE, fg=BLUE4,
                  relief=tk.FLAT, cursor="hand2", padx=8,
                  command=self._reload_agents).pack(side=tk.RIGHT, padx=4)

        canvas = tk.Canvas(f, bg=BG, highlightthickness=0)
        sb_y = ttk.Scrollbar(f, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=sb_y.set)
        sb_y.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)

        self.agents_inner = tk.Frame(canvas, bg=BG)
        self._agents_window = canvas.create_window((0,0), window=self.agents_inner, anchor="nw")
        self.agents_inner.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
            lambda e: canvas.itemconfig(self._agents_window, width=e.width))

    # ═══════════════════════════════ SKILLS TAB ══════════════════════════════
    def _tab_skills(self, f):
        hdr = tk.Frame(f, bg=BG2, pady=8)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="⚡  Skills", font=(SANS,13,"bold"),
                 fg=CYAN, bg=BG2, padx=16).pack(side=tk.LEFT)
        tk.Button(hdr, text="⟳ Reload", font=(SANS,9), bg=TILE, fg=BLUE4,
                  relief=tk.FLAT, cursor="hand2", padx=8,
                  command=self._reload_skills).pack(side=tk.RIGHT, padx=16)
        tk.Button(hdr, text="+ Open Folder", font=(SANS,9), bg=TILE, fg=GREEN,
                  relief=tk.FLAT, cursor="hand2", padx=8,
                  command=self._open_skills_folder).pack(side=tk.RIGHT, padx=4)

        self.skills_out = scrolledtext.ScrolledText(
            f, bg=BG, fg=FG, font=MONO_MD, relief=tk.FLAT,
            padx=16, pady=12, state=tk.DISABLED
        )
        self.skills_out.pack(fill=tk.BOTH, expand=True, padx=16, pady=8)
        self.skills_out.tag_config("name", foreground=CYAN, font=(MONO,10,"bold"))
        self.skills_out.tag_config("desc", foreground=FG2)
        self.skills_out.tag_config("param",foreground=BLUE4)

    # ═══════════════════════════════ LOG TAB ═════════════════════════════════
    def _tab_log(self, f):
        hdr = tk.Frame(f, bg=BG2, pady=8)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text="📋  System Log", font=(SANS,13,"bold"),
                 fg=CYAN, bg=BG2, padx=16).pack(side=tk.LEFT)
        tk.Button(hdr, text="Clear", font=(SANS,9), bg=TILE, fg=FG2,
                  relief=tk.FLAT, cursor="hand2", padx=8,
                  command=self._clear_log).pack(side=tk.RIGHT, padx=16)

        self.log_out = scrolledtext.ScrolledText(
            f, bg=BG, fg=FG3, font=(MONO,9), relief=tk.FLAT,
            padx=14, pady=10, state=tk.DISABLED
        )
        self.log_out.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0,16))
        self.log_out.tag_config("ok",   foreground=GREEN)
        self.log_out.tag_config("warn", foreground=AMBER)
        self.log_out.tag_config("err",  foreground=RED)

    # ── Widgets ──────────────────────────────────────────────────────────────
    def _big_tile(self, parent, icon, label, cmd):
        outer = tk.Frame(parent, bg=TILE, padx=2, pady=2,
                          relief=tk.FLAT, cursor="hand2")
        inner = tk.Frame(outer, bg=TILE, width=100, height=78)
        inner.pack_propagate(False)
        inner.pack()
        tk.Label(inner, text=icon, font=("Segoe UI",22),
                 bg=TILE, fg=FG).pack(pady=(8,2))
        tk.Label(inner, text=label, font=(SANS,8,"bold"),
                 bg=TILE, fg=FG2).pack()

        def _enter(e):
            outer.config(bg=TILE_H); inner.config(bg=TILE_H)
            for w in inner.winfo_children(): w.config(bg=TILE_H)
        def _leave(e):
            outer.config(bg=TILE); inner.config(bg=TILE)
            for w in inner.winfo_children(): w.config(bg=TILE)
        def _click(e): cmd()

        for w in [outer, inner] + list(inner.winfo_children()):
            w.bind("<Enter>", _enter)
            w.bind("<Leave>", _leave)
            w.bind("<Button-1>", _click)
        return outer

    def _icon_btn(self, parent, text, cmd, bg=TILE, fg=FG2, width=None):
        kw = dict(font=(SANS,9), bg=bg, fg=fg, relief=tk.FLAT,
                  cursor="hand2", padx=8, pady=4,
                  activebackground=BLUE1, activeforeground=FG,
                  command=cmd)
        if width:
            kw["width"] = width
        return tk.Button(parent, text=text, **kw)

    def _tooltip(self, widget, text):
        def _show(e):
            tip = tk.Toplevel(self)
            tip.wm_overrideredirect(True)
            tip.wm_geometry(f"+{e.x_root+14}+{e.y_root+8}")
            tk.Label(tip, text=text, font=(SANS,8), bg=TILE, fg=FG2,
                     relief=tk.SOLID, borderwidth=1, padx=6, pady=2).pack()
            widget._tip = tip
        def _hide(e):
            if hasattr(widget, "_tip"):
                widget._tip.destroy()
        widget.bind("<Enter>", _show)
        widget.bind("<Leave>", _hide)

    # ── Boot ─────────────────────────────────────────────────────────────────
    def _boot(self):
        def _init():
            self.jarvis.start()
            status = "online" if self.jarvis.ollama_ok else "offline"
            self.q.put(("ollama_status", status))
            self.q.put(("log", f"[Boot] Ollama: {status}"))
            self.q.put(("log", f"[Boot] Skills: {len(self.jarvis.skill_manager.skills)}"))
            self.q.put(("log", f"[Boot] Agents: {len(self.jarvis.agent_runner.agents)}"))
            self.q.put(("refresh_agents", None))
            self.q.put(("refresh_skills", None))
        threading.Thread(target=_init, daemon=True).start()

    # ── Queue poll ───────────────────────────────────────────────────────────
    def _poll(self):
        try:
            while True:
                kind, data = self.q.get_nowait()

                if kind == "ollama_status":
                    if data == "online":
                        self.ollama_lbl.config(text="⬤ Llama 3.1 Online", fg=GREEN)
                    else:
                        self.ollama_lbl.config(text="⬤ Ollama Offline", fg=RED)

                elif kind == "chat_you":
                    self._chat_append("you", f"\nYOU: ", "")
                    self._chat_append("text", data + "\n", "")
                elif kind == "chat_start":
                    self._chat_append("jarvis", "\nJARVIS: ", "")
                elif kind == "chat_chunk":
                    self._chat_raw(data)
                elif kind == "chat_end":
                    self._chat_raw("\n")
                    self._set_busy(False)

                elif kind == "plan":
                    self._show_plan(data)
                elif kind == "reason_chunk":
                    self._reason_raw(data)
                elif kind == "reason_clear":
                    self._reason_clear()

                elif kind == "think_msg":
                    self._set_thinking(data)

                elif kind == "code_out":
                    self._code_write(data)
                elif kind == "code_clear":
                    self._code_clear()

                elif kind == "mcp_out":
                    self._mcp_write(data)
                elif kind == "mcp_clear":
                    self._mcp_clear()

                elif kind == "log":
                    self._log_write(data)
                elif kind == "refresh_agents":
                    self._refresh_agents()
                elif kind == "refresh_skills":
                    self._refresh_skills()

        except queue.Empty:
            pass
        self.after(40, self._poll)

    # ── Chat logic ───────────────────────────────────────────────────────────
    def _on_send(self, event=None, force_reason=False):
        if self._busy:
            return
        text = self.inp_var.get().strip()
        if not text:
            return
        self.inp_var.set("")
        self._set_busy(True)
        self.q.put(("chat_you", text))

        from core.reasoner import is_complex
        use_reason = force_reason or is_complex(text)

        threading.Thread(target=self._process, args=(text, use_reason), daemon=True).start()

    def _process(self, text: str, use_reason: bool):
        if use_reason and self.jarvis.ollama_ok:
            self._do_reason_pipeline(text)
        else:
            self._do_chat(text)

    def _do_reason_pipeline(self, text: str):
        from core.reasoner import plan, reason_stream

        self.q.put(("think_msg", "⚙ Planning…"))
        self.q.put(("reason_clear", None))
        p = plan(text)
        self.q.put(("plan", p))
        self.q.put(("think_msg", "🧠 Reasoning…"))

        reason_buf = ""
        for chunk in reason_stream(text, p, self.jarvis.skill_manager.get_skill_descriptions()):
            reason_buf += chunk
            self.q.put(("reason_chunk", chunk))

        # Now do actual chat with the reasoning as context hint
        self.q.put(("think_msg", "💬 Responding…"))
        self.q.put(("chat_start", None))
        for chunk in self.jarvis.chat_stream(text):
            self.q.put(("chat_chunk", chunk))
        self.q.put(("chat_end", None))
        self.q.put(("think_msg", ""))

    def _do_chat(self, text: str):
        self.q.put(("think_msg", "⚙ Processing…"))
        self.q.put(("chat_start", None))
        for chunk in self.jarvis.chat_stream(text):
            self.q.put(("chat_chunk", chunk))
        self.q.put(("chat_end", None))
        self.q.put(("think_msg", ""))

    def _send_msg(self, text: str):
        self.inp_var.set(text)
        self._on_send()
        self._switch_tab("chat")

    def _set_busy(self, busy: bool):
        self._busy = busy
        state = tk.DISABLED if busy else tk.NORMAL
        self.send_btn.config(state=state)
        self.reason_btn.config(state=state)
        self.inp_entry.config(state=state)
        if not busy:
            self.inp_entry.focus()

    def _set_thinking(self, msg: str):
        if msg:
            self.think_bar.pack(fill=tk.X, after=self.chat_out)
            self.think_lbl.config(text=msg)
        else:
            self.think_bar.pack_forget()

    # ── Chat text helpers ─────────────────────────────────────────────────────
    def _chat_append(self, tag: str, prefix: str, text: str):
        self.chat_out.config(state=tk.NORMAL)
        if prefix:
            self.chat_out.insert(tk.END, prefix, tag)
        if text:
            self.chat_out.insert(tk.END, text, "text")
        self.chat_out.config(state=tk.DISABLED)
        self.chat_out.see(tk.END)

    def _chat_raw(self, text: str):
        self.chat_out.config(state=tk.NORMAL)
        self.chat_out.insert(tk.END, text, "text")
        self.chat_out.config(state=tk.DISABLED)
        self.chat_out.see(tk.END)

    # ── Reason helpers ───────────────────────────────────────────────────────
    def _show_plan(self, plan_data: dict):
        import json
        self.plan_out.config(state=tk.NORMAL)
        self.plan_out.delete("1.0", tk.END)
        self.plan_out.insert(tk.END, json.dumps(plan_data, indent=2))
        self.plan_out.config(state=tk.DISABLED)
        self._switch_tab("reason")

    def _reason_raw(self, text: str):
        self.reason_out.config(state=tk.NORMAL)
        tag = "thinking" if "THINKING" in text else ("conclude" if "CONCLUSION" in text else "")
        self.reason_out.insert(tk.END, text, tag)
        self.reason_out.config(state=tk.DISABLED)
        self.reason_out.see(tk.END)

    def _reason_clear(self):
        self.reason_out.config(state=tk.NORMAL)
        self.reason_out.delete("1.0", tk.END)
        self.reason_out.config(state=tk.DISABLED)

    # ── Code engine ──────────────────────────────────────────────────────────
    def _run_code_stage(self, stage: str):
        code = self.code_in.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("No Code", "Paste code in the input panel first.")
            return
        self.q.put(("code_clear", None))
        self.q.put(("code_out", f"▶ Running stage: {stage.upper()}\n\n"))

        def _run():
            from skills.code_engine import review_code, debug_code, fix_code, upgrade_code, full_pipeline
            stages = {
                "review":  lambda: review_code(code),
                "debug":   lambda: debug_code(code),
                "fix":     lambda: fix_code(code),
                "upgrade": lambda: upgrade_code(code),
                "full":    lambda: full_pipeline(code),
            }
            fn = stages.get(stage, lambda: "Unknown stage")
            result = fn()
            self.q.put(("code_out", result + "\n"))
        threading.Thread(target=_run, daemon=True).start()

    def _code_write(self, text: str):
        self.code_out.config(state=tk.NORMAL)
        self.code_out.insert(tk.END, text)
        self.code_out.config(state=tk.DISABLED)
        self.code_out.see(tk.END)

    def _code_clear(self):
        self.code_out.config(state=tk.NORMAL)
        self.code_out.delete("1.0", tk.END)
        self.code_out.config(state=tk.DISABLED)

    def _load_code_file(self):
        path = filedialog.askopenfilename(filetypes=[("Python","*.py"),("All","*.*")])
        if path:
            with open(path) as fh:
                content = fh.read()
            self.code_in.delete("1.0", tk.END)
            self.code_in.insert("1.0", content)

    def _clear_code_input(self):
        self.code_in.delete("1.0", tk.END)

    # ── MCP tester ───────────────────────────────────────────────────────────
    def _run_mcp(self, action: str):
        url = self.mcp_url_var.get().strip()
        if not url:
            messagebox.showwarning("MCP", "Enter a server URL first.")
            return
        self.q.put(("mcp_clear", None))
        self.q.put(("mcp_out", f"Testing {url}…\n\n"))

        def _run():
            from skills.mcp_tester import test_mcp_server, ping_mcp, list_mcp_tools, call_mcp_tool
            if action == "test":   result = test_mcp_server(url)
            elif action == "ping": result = ping_mcp(url)
            elif action == "list": result = list_mcp_tools(url)
            elif action == "call":
                tool = self.mcp_tool_var.get().strip()
                params = self.mcp_params_var.get().strip()
                result = call_mcp_tool(url, tool, params)
            else:
                result = "Unknown action"
            self.q.put(("mcp_out", result + "\n"))
        threading.Thread(target=_run, daemon=True).start()

    def _mcp_write(self, text: str):
        self.mcp_out.config(state=tk.NORMAL)
        tag = "ok" if "✓" in text else ("err" if "✗" in text else "")
        self.mcp_out.insert(tk.END, text, tag)
        self.mcp_out.config(state=tk.DISABLED)
        self.mcp_out.see(tk.END)

    def _mcp_clear(self):
        self.mcp_out.config(state=tk.NORMAL)
        self.mcp_out.delete("1.0", tk.END)
        self.mcp_out.config(state=tk.DISABLED)

    # ── Agents panel ─────────────────────────────────────────────────────────
    def _refresh_agents(self):
        for w in self.agents_inner.winfo_children():
            w.destroy()
        agents = self.jarvis.agent_runner.status_all()
        if not agents:
            tk.Label(self.agents_inner,
                     text="No agents loaded.\nAdd .py files to the /agents directory.",
                     font=(SANS,10), fg=FG3, bg=BG).pack(pady=40)
            return
        for a in agents:
            self._agent_card(a)

    def _agent_card(self, a: dict):
        card = tk.Frame(self.agents_inner, bg=TILE, pady=10, padx=14)
        card.pack(fill=tk.X, pady=5)

        top = tk.Frame(card, bg=TILE)
        top.pack(fill=tk.X)
        dot = GREEN if a["enabled"] else FG3
        status_col = AMBER if a["status"] == "running" else (RED if a["status"] == "error" else GREEN)
        tk.Label(top, text=f"⬤  {a['name']}", font=(SANS,10,"bold"),
                 fg=dot, bg=TILE).pack(side=tk.LEFT)
        tk.Label(top, text=f"[{a['status']}]", font=(SANS,8),
                 fg=status_col, bg=TILE).pack(side=tk.LEFT, padx=8)
        interval = f"every {a['interval']}s" if a["interval"] else "one-shot"
        tk.Label(top, text=interval, font=(SANS,8), fg=FG3, bg=TILE).pack(side=tk.LEFT)

        tk.Label(card, text=a["description"], font=(SANS,9),
                 fg=FG2, bg=TILE).pack(anchor=tk.W, pady=(4,0))
        if a["last_output"]:
            tk.Label(card, text=f"↳ {a['last_output'][:100]}",
                     font=(MONO,8), fg=BLUE4, bg=TILE).pack(anchor=tk.W)

        btns = tk.Frame(card, bg=TILE)
        btns.pack(anchor=tk.W, pady=(6,0))
        name = a["name"]
        tk.Button(btns, text="▶ Run", font=(SANS,8), bg=BLUE1, fg=FG,
                  relief=tk.FLAT, cursor="hand2", padx=8, pady=3,
                  command=lambda n=name: self._run_agent(n)).pack(side=tk.LEFT, padx=(0,6))
        tlbl = "Disable" if a["enabled"] else "Enable"
        tk.Button(btns, text=tlbl, font=(SANS,8), bg=TILE, fg=AMBER,
                  relief=tk.FLAT, cursor="hand2", padx=8, pady=3,
                  command=lambda n=name: self._toggle_agent(n)).pack(side=tk.LEFT)

    def _run_agent(self, name: str):
        def _run():
            r = self.jarvis.agent_runner.run_agent_now(name)
            self.q.put(("log", f"[Agent:{name}] {r}"))
            self.q.put(("refresh_agents", None))
        threading.Thread(target=_run, daemon=True).start()

    def _toggle_agent(self, name: str):
        msg = self.jarvis.agent_runner.toggle(name)
        self.q.put(("log", msg))
        self.q.put(("refresh_agents", None))

    # ── Skills panel ─────────────────────────────────────────────────────────
    def _refresh_skills(self):
        self.skills_out.config(state=tk.NORMAL)
        self.skills_out.delete("1.0", tk.END)
        for name, skill in self.jarvis.skill_manager.skills.items():
            self.skills_out.insert(tk.END, f"⚡ {name}\n", "name")
            self.skills_out.insert(tk.END, f"   {skill.description}\n", "desc")
            if skill.params:
                self.skills_out.insert(tk.END, f"   params: {', '.join(skill.params)}\n", "param")
            self.skills_out.insert(tk.END, "\n")
        self.skills_out.config(state=tk.DISABLED)

    # ── Log ──────────────────────────────────────────────────────────────────
    def _log_write(self, msg: str):
        self.log_out.config(state=tk.NORMAL)
        tag = "ok" if "✓" in msg else ("err" if "ERROR" in msg or "✗" in msg else
               "warn" if "WARNING" in msg else "")
        self.log_out.insert(tk.END, msg + "\n", tag)
        self.log_out.config(state=tk.DISABLED)
        self.log_out.see(tk.END)
        # also push to jarvis log
        self.jarvis.log(msg)

    def _clear_log(self):
        self.log_out.config(state=tk.NORMAL)
        self.log_out.delete("1.0", tk.END)
        self.log_out.config(state=tk.DISABLED)

    # ── Voice ─────────────────────────────────────────────────────────────────
    def _toggle_voice(self):
        self._voice_on = not self._voice_on
        if self._voice_on:
            self.voice_btn.config(text="🎤 Voice ON", fg=CYAN)
            self.voice_dot.config(fg=CYAN)
            self.voice.start_listening(
                on_speech=self._on_voice_speech,
                on_status=self._on_voice_status
            )
        else:
            self.voice_btn.config(text="🎤 Voice OFF", fg=FG2)
            self.voice_dot.config(fg=FG3)
            self.voice.stop_listening()

    def _on_voice_speech(self, text: str):
        self.q.put(("log", f"[Voice STT] {text}"))
        self.inp_var.set(text)
        self._on_send()

    def _on_voice_status(self, status: str):
        colors = {"listening": CYAN, "processing": AMBER, "idle": FG3}
        self.voice_dot.config(fg=colors.get(status, FG3))

    # ── Settings ─────────────────────────────────────────────────────────────
    def _open_settings(self):
        win = tk.Toplevel(self)
        win.title("Settings")
        win.configure(bg=BG)
        win.geometry("420x300")

        tk.Label(win, text="Settings", font=(SANS,13,"bold"), fg=CYAN, bg=BG).pack(pady=12)

        btns = [
            ("⟳ Reload Skills",  self._reload_skills),
            ("⟳ Reload Agents",  self._reload_agents),
            ("🗑 Clear Chat History", self._clear_chat),
            ("📂 Open Skills Folder", self._open_skills_folder),
        ]
        for lbl, cmd in btns:
            tk.Button(win, text=lbl, font=(SANS,10), bg=TILE, fg=FG,
                      relief=tk.FLAT, cursor="hand2", padx=12, pady=6,
                      command=cmd).pack(fill=tk.X, padx=40, pady=4)

    # ── Misc actions ─────────────────────────────────────────────────────────
    def _quick_search(self):
        q = simpledialog.askstring("Web Search", "Search for:", parent=self)
        if q:
            self._send_msg(f"search for {q}")

    def _quick_open_app(self):
        app = simpledialog.askstring("Open App", "App name:", parent=self)
        if app:
            self._send_msg(f"open {app}")

    def _reload_skills(self):
        self.jarvis.reload_skills()
        self._refresh_skills()
        self.q.put(("log", "[Jarvis] Skills reloaded."))

    def _reload_agents(self):
        self.jarvis.reload_agents()
        self._refresh_agents()
        self.q.put(("log", "[Jarvis] Agents reloaded."))

    def _clear_chat(self):
        self.jarvis.clear_history()
        self.chat_out.config(state=tk.NORMAL)
        self.chat_out.delete("1.0", tk.END)
        self.chat_out.config(state=tk.DISABLED)
        self._chat_append("jarvis", "\nJARVIS: ", "")
        self._chat_raw("Chat cleared. Ready.\n")

    def _open_skills_folder(self):
        import webbrowser, os
        p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "skills")
        webbrowser.open(f"file://{p}")
