import customtkinter as ctk
import threading
import requests
import os
import json

# GUI Widgets Imports
from gui.widgets import InfoCard, StatusBadge, SectionHeader

# Modules Imports
from modules.url_validator import validate_url
from modules.dns_lookup import DNSLookup
from modules.ip_lookup import IPLookup
from modules.whois_lookup import lookup_whois
from modules.asn_lookup import lookup_asn
from modules.geoip import GeoIP
from modules.ssl_certificate import SSLCertificate
from modules.http_headers import get_headers
from modules.security_headers import check_security_headers
from modules.technologies import TechDetector
from modules.cdn_detector import detect_cdn
from modules.performance import measure_response_time, get_page_size
from modules.robots import get_robots
from modules.sitemap import detect_sitemap
from modules.screenshot import take_screenshot
from modules.advanced_recon import AdvancedRecon

# Utilities Imports
from ai.ai_summary import get_ai_summary
from utils.helper import extract_domain
from utils.export import export_json, export_csv, export_pdf


class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, config):
        super().__init__(parent, fg_color="transparent")
        self.parent = parent
        self.config = config
        self.results = {}
        
        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ==========================================
        # 1. TOP HEADER PANEL (Input & Action Buttons)
        # ==========================================
        header_card = ctk.CTkFrame(
            self, 
            corner_radius=12, 
            fg_color=("#F0F2F5", "#1E1E2E"), 
            border_width=1, 
            border_color=("#D1D5DB", "#313244")
        )
        header_card.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        header_card.grid_columnconfigure(1, weight=1)

        self.url_label = ctk.CTkLabel(header_card, text="🌐 Target URL:", font=("Segoe UI", 13, "bold"))
        self.url_label.grid(row=0, column=0, padx=(15, 5), pady=12)

        self.url_entry = ctk.CTkEntry(
            header_card, 
            placeholder_text="https://example.com", 
            font=("Consolas", 13),
            height=38,
            corner_radius=8
        )
        self.url_entry.grid(row=0, column=1, padx=5, pady=12, sticky="ew")

        # Action Buttons
        self.analyze_btn = ctk.CTkButton(
            header_card, 
            text="🔍 Analyze", 
            font=("Segoe UI", 12, "bold"),
            height=38,
            corner_radius=8,
            fg_color="#3B82F6", 
            hover_color="#2563EB",
            command=self.analyze
        )
        self.analyze_btn.grid(row=0, column=2, padx=5, pady=12)

        self.export_btn = ctk.CTkButton(
            header_card, 
            text="📥 Export All", 
            font=("Segoe UI", 12, "bold"),
            height=38,
            corner_radius=8,
            fg_color="#10B981", 
            hover_color="#059669",
            command=self.export_all
        )
        self.export_btn.grid(row=0, column=3, padx=5, pady=12)
        self.export_btn.configure(state="disabled")

        self.copy_btn = ctk.CTkButton(
            header_card, 
            text="📋 Copy Text", 
            font=("Segoe UI", 12, "bold"),
            height=38,
            corner_radius=8,
            fg_color="#6B7280", 
            hover_color="#4B5563",
            command=self.copy_text_to_clipboard
        )
        self.copy_btn.grid(row=0, column=4, padx=(5, 15), pady=12)

        # Progress Bar
        self.progress = ctk.CTkProgressBar(header_card, height=6, corner_radius=3, progress_color="#3B82F6")
        self.progress.grid(row=1, column=0, columnspan=5, padx=15, pady=(0, 12), sticky="ew")
        self.progress.set(0)

        # ==========================================
        # 2. MAIN CONTENT AREA (Cards & Terminal Output)
        # ==========================================
        content_container = ctk.CTkFrame(self, fg_color="transparent")
        content_container.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        content_container.grid_columnconfigure(0, weight=1)
        content_container.grid_rowconfigure(2, weight=1)

        # 📌 Section Header 1: Quick Summary Cards
        self.sec1_header = SectionHeader(content_container, title="Quick Overview", icon="📊")
        self.sec1_header.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        # Cards Frame (Row of InfoCards & StatusBadge)
        self.cards_frame = ctk.CTkFrame(content_container, fg_color="transparent")
        self.cards_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.card_ip = InfoCard(self.cards_frame, title="Target IP", value="N/A", icon="💻")
        self.card_ip.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="ew")

        self.card_status = InfoCard(self.cards_frame, title="Scan Status", value="Idle", icon="⚡")
        self.card_status.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.card_cdn = InfoCard(self.cards_frame, title="CDN / WAF", value="Unknown", icon="🛡️")
        self.card_cdn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.card_ssl = InfoCard(self.cards_frame, title="SSL State", value="Checking...", icon="🔒")
        self.card_ssl.grid(row=0, column=3, padx=(5, 0), pady=5, sticky="ew")

        # 📌 Section Header 2: Detailed Terminal Output
        self.sec2_header = SectionHeader(content_container, title="Detailed Intelligence Report", icon="📝")
        self.sec2_header.grid(row=2, column=0, sticky="ew", pady=(5, 8))

        # Detailed Text Console Box
        result_card = ctk.CTkFrame(
            content_container, 
            corner_radius=12, 
            fg_color=("#F0F2F5", "#1E1E2E"), 
            border_width=1, 
            border_color=("#D1D5DB", "#313244")
        )
        result_card.grid(row=3, column=0, sticky="nsew", pady=(0, 5))
        result_card.grid_columnconfigure(0, weight=1)
        result_card.grid_rowconfigure(0, weight=1)

        self.result_text = ctk.CTkTextbox(
            result_card, 
            wrap="word", 
            font=("Consolas", 12),
            corner_radius=8,
            border_width=0
        )
        self.result_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # ==========================================
    # HELPER & ACTION FUNCTIONS
    # ==========================================
    def copy_text_to_clipboard(self):
        """ક્લિપબોર્ડમાં લખાણ કોપી કરવા માટે"""
        content = self.result_text.get("0.0", "end").strip()
        if content:
            self.clipboard_clear()
            self.clipboard_append(content)
            self.update()
            self.copy_btn.configure(text="✅ Copied!")
            self.after(2000, lambda: self.copy_btn.configure(text="📋 Copy Text"))

    def update_status(self, msg, progress_val=0.0):
        """સ્કેનિંગ પ્રગતિ અને સ્ટેટસ અપડેટ કરશે"""
        self.progress.set(progress_val)
        self.card_status.update_value(msg)
        self.result_text.insert("end", f"  ⏳ [Checking] {msg}...\n")
        self.result_text.see("end")
        self.update_idletasks()

    def analyze(self):
        """સ્કેન શરુ કરવા માટેનું મુખ્ય બટન ફંક્શન"""
        url = self.url_entry.get().strip()
        if not url:
            url = self.url_entry.cget("placeholder_text")
            
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            
        if not validate_url(url):
            self.result_text.delete("0.0", "end")
            self.result_text.insert("0.0", "❌ Invalid URL format.\n")
            return

        self.analyze_btn.configure(state="disabled")
        self.export_btn.configure(state="disabled")
        self.progress.set(0.05)
        self.result_text.delete("0.0", "end")
        self.result_text.insert("0.0", "🚀 Starting Advanced Recon Analysis...\n")

        # Background thread માં સ્કેનર ચલાવશે
        thread = threading.Thread(target=self._run_analysis, args=(url,))
        thread.daemon = True
        thread.start()

    def _run_analysis(self, url):
        """બેકગ્રાઉન્ડ થ્રેડમાં બધી તપાસ પ્રક્રિયા કરશે"""
        try:
            domain = extract_domain(url)
            self.results["URL"] = url
            self.results["Domain"] = domain

            # Step 1: DNS Lookup
            self.update_status("DNS Lookup", 0.1)
            dns = DNSLookup(domain)
            dns_results = dns.all_lookups()
            self.results["DNS"] = dns_results

            # IP મેળવો
            ip = None
            if dns_results.get("A") and not dns_results["A"][0].startswith("Error"):
                ip = dns_results["A"][0]
                self.results["IP"] = ip
                self.card_ip.update_value(ip)

            # Step 2: Advanced OSINT Recon
            self.update_status("Subdomains & Real IP Finder", 0.25)
            try:
                recon = AdvancedRecon(domain)
                recon_data = recon.run_all(current_ip=ip)
                self.results["Subdomains"] = recon_data.get("Subdomains Found", [])
                self.results["Potential Real Origin IP"] = recon_data.get("Potential Real Origin IPs", [])
                self.results["Open Ports"] = recon_data.get("Open Services & Ports", [])
            except Exception as e:
                self.results["Advanced Recon"] = f"Error: {str(e)}"

            # Step 3: WHOIS
            self.update_status("WHOIS Lookup", 0.35)
            whois_data = lookup_whois(domain)
            self.results["WHOIS"] = whois_data

            # Step 4: IP Location & ASN
            if ip:
                self.update_status("IP GeoIP & ASN", 0.45)
                ip_info = IPLookup(ip).get_info()
                self.results["IP Info"] = ip_info
                asn_data = lookup_asn(ip)
                self.results["ASN"] = asn_data
                geo_data = GeoIP(ip).get_location()
                self.results["GeoIP"] = geo_data

            # Step 5: SSL Certificate
            self.update_status("SSL Certificate Check", 0.55)
            ssl = SSLCertificate(domain)
            ssl_data = ssl.get_cert_info()
            self.results["SSL"] = ssl_data
            ssl_valid = "valid_from" in ssl_data
            self.results["https_enabled"] = ssl_valid
            self.card_ssl.update_value("Valid SSL" if ssl_valid else "No/Expired SSL")

            # Step 6: HTTP Headers
            self.update_status("HTTP Headers", 0.65)
            headers = get_headers(url)
            self.results["HTTP Headers"] = headers
            if "error" not in headers:
                sec_headers = check_security_headers(headers)
                self.results["Security Headers"] = sec_headers
                self.results["missing_security_headers"] = sec_headers.get("missing", [])

            # Step 7: Technologies & CDN
            self.update_status("Technology & CDN Detection", 0.75)
            html = ""
            try:
                resp = requests.get(url, timeout=10)
                html = resp.text
            except:
                pass
            tech = TechDetector(url, html).detect()
            self.results["Technologies"] = tech

            cdn = detect_cdn(url)
            self.results["CDN"] = cdn
            self.card_cdn.update_value(cdn if cdn else "Direct / None")

            # Step 8: Performance & Robots
            self.update_status("Performance & Robots.txt", 0.85)
            self.results["Response Time (s)"] = measure_response_time(url)
            self.results["Page Size (bytes)"] = get_page_size(url)
            robots = get_robots(url)
            self.results["robots.txt"] = robots[:500] if isinstance(robots, str) else "Error"
            self.results["sitemap.xml"] = "Present" if detect_sitemap(url) else "Not found"

            # Step 9: Screenshot
            self.update_status("Taking Screenshot", 0.92)
            try:
                screenshot_path = take_screenshot(url, domain)
                self.results["Screenshot"] = screenshot_path
            except Exception as e:
                self.results["Screenshot"] = f"Error: {str(e)}"

            # Step 10: AI Summary
            self.update_status("Generating AI Summary", 0.98)
            ai = get_ai_summary(self.results)
            self.results["AI Summary"] = ai

            # 🏁 Complete Display
            self.display_results()
            self.progress.set(1.0)
            self.card_status.update_value("Completed")
            self.analyze_btn.configure(state="normal")
            self.export_btn.configure(state="normal")

        except Exception as e:
            self.result_text.delete("0.0", "end")
            self.result_text.insert("0.0", f"❌ Error during analysis: {str(e)}")
            self.card_status.update_value("Failed")
            self.analyze_btn.configure(state="normal")

    def display_results(self):
        """પરિણામોને કન્સોલમાં સુંદર રીતે ફોર્મેટ કરીને દર્શાવશે"""
        self.result_text.delete("0.0", "end")
        for key, value in self.results.items():
            self.result_text.insert("end", f"\n{'='*22} {key} {'='*22}\n")
            if isinstance(value, dict):
                for k, v in value.items():
                    self.result_text.insert("end", f"  • {k}: {v}\n")
            elif isinstance(value, list):
                for item in value:
                    self.result_text.insert("end", f"  • {item}\n")
            else:
                self.result_text.insert("end", f"  {value}\n")
        self.result_text.see("end")

    def export_all(self):
        """બધા જ રિપોર્ટ્સ ડાઉનલોડ/સેવ કરવા માટે"""
        if not self.results:
            return
        filename = self.results.get("Domain", "report")
        json_path = export_json(self.results, filename)
        csv_path = export_csv(self.results, filename)
        pdf_path = export_pdf("CyberScope Report", self.results, filename)
        self.result_text.insert(
            "end", 
            f"\n\n📂 Reports Saved Successfully:\n  • JSON: {json_path}\n  • CSV: {csv_path}\n  • PDF: {pdf_path}\n"
        )
