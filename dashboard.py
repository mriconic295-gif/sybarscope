import customtkinter as ctk
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
from ai.ai_summary import get_ai_summary
from utils.helper import extract_domain
from utils.export import export_json, export_csv, export_pdf
import requests, threading, os, json

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.parent = parent
        self.config = config
        self.results = {}
        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Top frame
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        top_frame.grid_columnconfigure(1, weight=1)

        self.url_label = ctk.CTkLabel(top_frame, text="Enter URL:")
        self.url_label.grid(row=0, column=0, padx=5, pady=5)

        self.url_entry = ctk.CTkEntry(top_frame)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.url_entry.insert(0, "https://example.com")

        self.analyze_btn = ctk.CTkButton(top_frame, text="Analyze", command=self.analyze)
        self.analyze_btn.grid(row=0, column=2, padx=5, pady=5)

        self.export_btn = ctk.CTkButton(top_frame, text="Export All", command=self.export_all)
        self.export_btn.grid(row=0, column=3, padx=5, pady=5)
        self.export_btn.configure(state="disabled")

        self.progress = ctk.CTkProgressBar(self)
        self.progress.grid(row=0, column=0, padx=10, pady=(0,10), sticky="ew")
        self.progress.set(0)

        # Result text area
        self.result_text = ctk.CTkTextbox(self, wrap="word", font=("Consolas", 12))
        self.result_text.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

    def analyze(self):
        url = self.url_entry.get().strip()
        if not url:
            self.result_text.delete("0.0", "end")
            self.result_text.insert("0.0", "Please enter a URL.\n")
            return
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        if not validate_url(url):
            self.result_text.delete("0.0", "end")
            self.result_text.insert("0.0", "Invalid URL format.\n")
            return

        self.analyze_btn.configure(state="disabled")
        self.export_btn.configure(state="disabled")
        self.progress.set(0)
        self.result_text.delete("0.0", "end")
        self.result_text.insert("0.0", "Analyzing...\n")

        # Run in thread to keep GUI responsive
        thread = threading.Thread(target=self._run_analysis, args=(url,))
        thread.daemon = True
        thread.start()

    def _run_analysis(self, url):
        try:
            domain = extract_domain(url)
            self.results["URL"] = url
            self.results["Domain"] = domain

            # Step 1: DNS Lookup
            self.update_status("DNS Lookup...")
            dns = DNSLookup(domain)
            dns_results = dns.all_lookups()
            self.results["DNS"] = dns_results

            # Get IP from A record
            ip = None
            if dns_results["A"] and not dns_results["A"][0].startswith("Error"):
                ip = dns_results["A"][0]
                self.results["IP"] = ip

            # Step 2: WHOIS
            self.update_status("WHOIS Lookup...")
            whois_data = lookup_whois(domain)
            self.results["WHOIS"] = whois_data

            # Step 3: IP based lookups (if IP available)
            if ip:
                self.update_status("IP Lookup / ASN / GeoIP...")
                ip_info = IPLookup(ip).get_info()
                self.results["IP Info"] = ip_info
                asn_data = lookup_asn(ip)
                self.results["ASN"] = asn_data
                geo_data = GeoIP(ip).get_location()
                self.results["GeoIP"] = geo_data

            # Step 4: SSL Certificate
            self.update_status("SSL Certificate...")
            ssl = SSLCertificate(domain)
            ssl_data = ssl.get_cert_info()
            self.results["SSL"] = ssl_data
            self.results["https_enabled"] = "valid_from" in ssl_data

            # Step 5: HTTP Headers & Security Headers
            self.update_status("HTTP Headers...")
            headers = get_headers(url)
            self.results["HTTP Headers"] = headers
            if "error" not in headers:
                sec_headers = check_security_headers(headers)
                self.results["Security Headers"] = sec_headers
                self.results["missing_security_headers"] = sec_headers.get("missing", [])
            else:
                self.results["Security Headers"] = {}

            # Step 6: Technology Detection
            self.update_status("Technologies...")
            html = ""
            try:
                resp = requests.get(url, timeout=10)
                html = resp.text
            except:
                pass
            tech = TechDetector(url, html).detect()
            self.results["Technologies"] = tech

            # Step 7: CDN Detection
            self.update_status("CDN Detection...")
            cdn = detect_cdn(url)
            self.results["CDN"] = cdn

            # Step 8: Performance
            self.update_status("Performance...")
            response_time = measure_response_time(url)
            page_size = get_page_size(url)
            self.results["Response Time (s)"] = response_time
            self.results["Page Size (bytes)"] = page_size

            # Step 9: robots.txt & sitemap
            self.update_status("robots.txt & sitemap...")
            robots = get_robots(url)
            self.results["robots.txt"] = robots[:500] if isinstance(robots, str) else "Error"
            has_sitemap = detect_sitemap(url)
            self.results["sitemap.xml"] = "Present" if has_sitemap else "Not found"

            # Step 10: Screenshot (optional)
            self.update_status("Screenshot...")
            try:
                screenshot_path = take_screenshot(url, domain)
                self.results["Screenshot"] = screenshot_path
            except Exception as e:
                self.results["Screenshot"] = f"Error: {str(e)}"

            # Step 11: AI Summary
            self.update_status("AI Analysis...")
            ai = get_ai_summary(self.results)
            self.results["AI Summary"] = ai

            # Display results
            self.display_results()
            self.progress.set(1)
            self.analyze_btn.configure(state="normal")
            self.export_btn.configure(state="normal")

        except Exception as e:
            self.result_text.delete("0.0", "end")
            self.result_text.insert("0.0", f"Error during analysis: {str(e)}")
            self.analyze_btn.configure(state="normal")

    def update_status(self, msg):
        self.result_text.insert("end", f"  {msg}...\n")
        self.result_text.see("end")
        self.update_idletasks()

    def display_results(self):
        self.result_text.delete("0.0", "end")
        for key, value in self.results.items():
            self.result_text.insert("end", f"\n{'='*20} {key} {'='*20}\n")
            if isinstance(value, dict):
                for k, v in value.items():
                    self.result_text.insert("end", f"  {k}: {v}\n")
            elif isinstance(value, list):
                for item in value:
                    self.result_text.insert("end", f"  {item}\n")
            else:
                self.result_text.insert("end", f"  {value}\n")
        self.result_text.see("end")

    def export_all(self):
        if not self.results:
            return
        filename = self.results.get("Domain", "report")
        json_path = export_json(self.results, filename)
        csv_path = export_csv(self.results, filename)
        pdf_path = export_pdf("CyberScope Report", self.results, filename)
        self.result_text.insert("end", f"\nReports saved:\n  JSON: {json_path}\n  CSV: {csv_path}\n  PDF: {pdf_path}\n")
