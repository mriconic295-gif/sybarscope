import customtkinter as ctk
import logging

logger = logging.getLogger("CyberScope.Dashboard")

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, config=None, *args, **kwargs):
        self.config = config or {}
        super().__init__(parent, *args, **kwargs)
        
        self.pack(fill="both", expand=True, padx=15, pady=15)
        self.current_scan_data = {}
        
        self.setup_ui()

    def setup_ui(self):
        # Configure Grid Rows & Columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) # Results box will scale properly

        # ==========================================
        # 1. HEADER SECTION
        # ==========================================
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="🛡️ CyberScope - Security Assessment & Risk Analysis", 
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        )
        self.title_label.pack(side="left", anchor="w")

        # ==========================================
        # 2. SEARCH / TARGET INPUT BAR (નવું ઉમેરેલું)
        # ==========================================
        self.search_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1e1e2e")
        self.search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15), ipady=5)
        self.search_frame.grid_columnconfigure(0, weight=1)

        self.url_entry = ctk.CTkEntry(
            self.search_frame, 
            placeholder_text="Enter Domain or URL (e.g. example.com or https://example.com)...",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            height=40,
            corner_radius=8
        )
        self.url_entry.grid(row=0, column=0, padx=(15, 10), pady=10, sticky="ew")

        self.scan_btn = ctk.CTkButton(
            self.search_frame,
            text="🚀 Start Scan",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=40,
            corner_radius=8,
            fg_color="#3B82F6",
            hover_color="#1D4ED8",
            command=self.start_scan_action
        )
        self.scan_btn.grid(row=0, column=1, padx=(0, 15), pady=10)

        # ==========================================
        # 3. EXECUTIVE RISK SCORE CARD
        # ==========================================
        self.card_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="#1e1e2e")
        self.card_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15), ipady=5)
        self.card_frame.grid_columnconfigure(0, weight=1)

        self.score_title = ctk.CTkLabel(
            self.card_frame, 
            text="OVERALL RISK SCORE", 
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#a6adc8"
        )
        self.score_title.grid(row=0, column=0, sticky="w", padx=15, pady=(8, 0))

        self.score_display = ctk.CTkLabel(
            self.card_frame, 
            text="-- / 100 (Awaiting Scan)", 
            font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"),
            text_color="#89b4fa"
        )
        self.score_display.grid(row=1, column=0, sticky="w", padx=15, pady=(2, 5))

        self.progress_bar = ctk.CTkProgressBar(self.card_frame, height=8, corner_radius=4)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 8))

        # ==========================================
        # 4. DETAILED BREAKDOWN & RESULTS PANEL
        # ==========================================
        self.details_frame = ctk.CTkFrame(self, corner_radius=10)
        self.details_frame.grid(row=3, column=0, sticky="nsew")
        self.details_frame.grid_columnconfigure(0, weight=1)
        self.details_frame.grid_rowconfigure(1, weight=1)

        self.details_title = ctk.CTkLabel(
            self.details_frame, 
            text="🔍 Security Vulnerabilities & Findings", 
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        )
        self.details_title.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 5))

        self.summary_text = ctk.CTkTextbox(
            self.details_frame, 
            font=ctk.CTkFont(family="Consolas", size=13),
            corner_radius=8,
            wrap="word",
            fg_color="#181825",
            text_color="#cdd6f4"
        )
        self.summary_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        self.summary_text.insert("1.0", "📌 Enter a URL above and click 'Start Scan' to analyze the target.")

    def start_scan_action(self):
        """ઉપરના સર્ચ બારમાંથી Target લઈને સ્કેન પ્રક્રિયા શરૂ કરવા માટે"""
        target = self.url_entry.get().strip()
        if not target:
            self.summary_text.delete("1.0", "end")
            self.summary_text.insert("1.0", "⚠️ Error: Please enter a target domain or URL first!")
            return

        self.summary_text.delete("1.0", "end")
        self.summary_text.insert("1.0", f"🔄 Scanning target: {target}...\nPlease wait, running modules...")
        
        # NOTE: જો તમારી પાસે backend સ્કેનર કૉલ કરવાનું ફંક્શન હોય, તો તેને અહીં કૉલ કરવું.

    def update_dashboard(self, scan_results: dict, ai_summary_data: dict = None):
        """સ્કેન પૂરું થયા પછી ડેટા દર્શાવવા માટે"""
        self.current_scan_data = scan_results

        if not ai_summary_data:
            try:
                from ai.ai_summary import get_ai_summary
                ai_summary_data = get_ai_summary(scan_results)
            except Exception as e:
                logger.error(f"Error loading AI summary: {e}")
                ai_summary_data = {
                    "risk_score": 0,
                    "summary": "AI Assessment unavailable.",
                    "vulnerabilities": [],
                    "recommendations": []
                }

        score = ai_summary_data.get("risk_score", 0)
        summary_msg = ai_summary_data.get("summary", "")
        vulnerabilities = ai_summary_data.get("vulnerabilities", [])
        recommendations = ai_summary_data.get("recommendations", [])

        if score <= 20:
            color = "#a6e3a1"
            status = "LOW RISK"
        elif score <= 50:
            color = "#f9e2af"
            status = "MODERATE RISK"
        else:
            color = "#f38ba8"
            status = "HIGH / CRITICAL RISK"

        self.score_display.configure(text=f"{score} / 100 — {status}", text_color=color)
        self.progress_bar.configure(progress_color=color)
        self.progress_bar.set(score / 100.0)

        self.summary_text.delete("1.0", "end")
        
        self.summary_text.insert("end", f"📌 EXECUTIVE SUMMARY\n{summary_msg}\n\n")
        
        self.summary_text.insert("end", "⚠️ DETECTED VULNERABILITIES\n")
        if vulnerabilities:
            for idx, item in enumerate(vulnerabilities, 1):
                if isinstance(item, dict):
                    self.summary_text.insert("end", f"{idx}. [{item.get('severity')}] {item.get('issue')}\n   ↳ Details: {item.get('details')}\n")
                else:
                    self.summary_text.insert("end", f"{idx}. {item}\n")
        else:
            self.summary_text.insert("end", " ✔ No vulnerabilities detected.\n")

        self.summary_text.insert("end", "\n💡 RECOMMENDED ACTIONS\n")
        if recommendations:
            for rec in recommendations:
                clean_rec = str(rec).replace("<b>", "").replace("</b>", "")
                self.summary_text.insert("end", f" • {clean_rec}\n")
        else:
            self.summary_text.insert("end", " • Maintain current configurations.\n")
