import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import logging

# Logger Setup
logger = logging.getLogger("CyberScope.Dashboard")

class SecurityDashboard(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Main Layout Setup
        self.pack(fill="both", expand=True, padx=15, pady=15)
        
        # State Data
        self.current_scan_data = {}
        
        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        """
        Builds a modern, clean, and user-friendly GUI for CyberScope Dashboard
        """
        # Configure Grid Weights so UI expands properly
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

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
        # 2. EXECUTIVE RISK SCORE CARD (Top Widget)
        # ==========================================
        self.card_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="#1e1e2e")
        self.card_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15), ipady=8)

        self.card_frame.grid_columnconfigure(0, weight=1)

        self.score_title = ctk.CTkLabel(
            self.card_frame, 
            text="OVERALL RISK SCORE", 
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color="#a6adc8"
        )
        self.score_title.grid(row=0, column=0, sticky="w", padx=20, pady=(10, 0))

        # Big Dynamic Score Display
        self.score_display = ctk.CTkLabel(
            self.card_frame, 
            text="-- / 100 (Awaiting Scan)", 
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color="#89b4fa"
        )
        self.score_display.grid(row=1, column=0, sticky="w", padx=20, pady=(2, 5))

        # Dynamic Colored Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self.card_frame, height=10, corner_radius=5)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 10))

        # ==========================================
        # 3. DETAILED BREAKDOWN & AI INSIGHTS PANEL
        # ==========================================
        self.details_frame = ctk.CTkFrame(self, corner_radius=12)
        self.details_frame.grid(row=2, column=0, sticky="nsew")

        self.details_frame.grid_columnconfigure(0, weight=1)
        self.details_frame.grid_rowconfigure(1, weight=1)

        self.details_title = ctk.CTkLabel(
            self.details_frame, 
            text="🔍 Security Vulnerabilities & Findings", 
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold")
        )
        self.details_title.grid(row=0, column=0, sticky="w", padx=15, pady=(12, 8))

        # Modern Scrollable Text Box for Clear Reading
        self.summary_text = ctk.CTkTextbox(
            self.details_frame, 
            font=ctk.CTkFont(family="Consolas", size=13),
            corner_radius=8,
            wrap="word",
            fg_color="#181825",
            text_color="#cdd6f4"
        )
        self.summary_text.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))

        # Initial Placeholder Text
        self.summary_text.insert("1.0", "📌 Welcome to CyberScope Security Dashboard.\n\nRun a domain scan to view threat intelligence, risk scores, and detailed vulnerability breakdowns here.")

    # ==========================================
    # 4. LOGIC TO UPDATE DASHBOARD DATA
    # ==========================================
    def update_dashboard(self, scan_results: dict, ai_summary_data: dict = None):
        """
        Call this method to update the GUI after scanning a target.
        Accepts raw scan results and processed AI summary data.
        """
        self.current_scan_data = scan_results

        # Fallback if ai_summary_data is not directly passed
        if not ai_summary_data:
            from ai.ai_summary import get_ai_summary
            try:
                ai_summary_data = get_ai_summary(scan_results)
            except Exception as e:
                logger.error(f"Error calling AI summary: {e}")
                ai_summary_data = {
                    "risk_score": 0,
                    "summary": "Could not generate AI summary.",
                    "vulnerabilities": [],
                    "recommendations": ["Ensure scanner engines are running correctly."]
                }

        # Extract values
        score = ai_summary_data.get("risk_score", 0)
        summary_msg = ai_summary_data.get("summary", "N/A")
        vulnerabilities = ai_summary_data.get("vulnerabilities", [])
        recommendations = ai_summary_data.get("recommendations", [])

        # Set Colors & Status according to Risk Score
        if score <= 20:
            color = "#a6e3a1"  # Soft Green (Low Risk)
            status = "LOW RISK"
        elif score <= 50:
            color = "#f9e2af"  # Soft Yellow/Orange (Moderate Risk)
            status = "MODERATE RISK"
        else:
            color = "#f38ba8"  # Soft Red (High Risk)
            status = "HIGH / CRITICAL RISK"

        # Update Top Score Display & Progress Bar
        self.score_display.configure(text=f"{score} / 100 — {status}", text_color=color)
        self.progress_bar.configure(progress_color=color)
        self.progress_bar.set(score / 100.0)

        # Clear previous text
        self.summary_text.delete("1.0", "end")

        # --------------------------------------------------
        # Render Structured & Clean Text Format
        # --------------------------------------------------
        # Section 1: Executive Summary
        self.summary_text.insert("end", "======================================================\n")
        self.summary_text.insert("end", "📌 EXECUTIVE SUMMARY\n")
        self.summary_text.insert("end", "======================================================\n")
        self.summary_text.insert("end", f"{summary_msg}\n\n")

        # Section 2: Vulnerability List
        self.summary_text.insert("end", "======================================================\n")
        self.summary_text.insert("end", "⚠️ DETECTED VULNERABILITIES & SECURITY GAPS\n")
        self.summary_text.insert("end", "======================================================\n")
        
        if vulnerabilities:
            for idx, item in enumerate(vulnerabilities, 1):
                if isinstance(item, dict):
                    sev = item.get("severity", "INFO")
                    issue = item.get("issue", "Unknown Security Issue")
                    details = item.get("details", "")
                    self.summary_text.insert("end", f"{idx}. [{sev}] {issue}\n")
                    if details:
                        self.summary_text.insert("end", f"   ↳ Details: {details}\n")
                else:
                    self.summary_text.insert("end", f"{idx}. {item}\n")
                self.summary_text.insert("end", "\n")
        else:
            self.summary_text.insert("end", " ✔ No critical vulnerabilities found during basic analysis.\n\n")

        # Section 3: Actionable Recommendations
        self.summary_text.insert("end", "======================================================\n")
        self.summary_text.insert("end", "💡 RECOMMENDED REMEDIATION STEPS\n")
        self.summary_text.insert("end", "======================================================\n")
        
        if recommendations:
            for rec in recommendations:
                clean_rec = str(rec).replace("<b>", "").replace("</b>", "")
                self.summary_text.insert("end", f" • {clean_rec}\n")
        else:
            self.summary_text.insert("end", " • Maintain current server hardening policies.\n")

        # Section 4: Key Infrastructure Snapshot
        self.summary_text.insert("end", "\n======================================================\n")
        self.summary_text.insert("end", "🌐 TARGET INFRASTRUCTURE SNAPSHOT\n")
        self.summary_text.insert("end", "======================================================\n")
        self.summary_text.insert("end", f" • Domain/Target : {scan_results.get('domain', 'N/A')}\n")
        self.summary_text.insert("end", f" • IP Address    : {scan_results.get('ip', 'N/A')}\n")
        self.summary_text.insert("end", f" • HTTPS Enabled : {'Yes' if scan_results.get('https_enabled') else 'No'}\n")
        self.summary_text.insert("end", f" • Open Ports    : {scan_results.get('Open Ports', 'None detected')}\n")

    def reset_dashboard(self):
        """
        Resets the dashboard to initial clean state
        """
        self.score_display.configure(text="-- / 100 (Awaiting Scan)", text_color="#89b4fa")
        self.progress_bar.set(0)
        self.summary_text.delete("1.0", "end")
        self.summary_text.insert("1.0", "📌 Dashboard reset. Enter a target and start a scan.")
