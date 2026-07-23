
class AIEngine:
    def __init__(self):
        self.risk_score = 0
        self.summary = ""
        self.recommendations = []
        self.detected_issues = []

    def analyze(self, data: dict):
        score = 0
        self.detected_issues = []

        # 1. HTTPS / SSL Check
        # https_enabled ફ્લેગ અથવા SSL ડિક્શનરીમાંથી ચેક કરો
        https_enabled = data.get("https_enabled", True)
        ssl_data = data.get("SSL", {})
        
        if not https_enabled:
            score += 35
            self.detected_issues.append("HTTPS is disabled or unavailable.")
        
        # Expired or Invalid Certificate Check
        if isinstance(ssl_data, dict) and ssl_data.get("expired", False):
            score += 40
            self.detected_issues.append("SSL Certificate has expired.")

        # 2. Security Headers Check (Missing count પર આધારિત)
        missing_headers = data.get("missing_security_headers", [])
        if isinstance(missing_headers, list) and len(missing_headers) > 0:
            # પ્રત્યેક મિસિંગ હેડર માટે 5 પોઈન્ટ્સ (મહત્તમ 25)
            header_penalty = min(len(missing_headers) * 5, 25)
            score += header_penalty
            self.detected_issues.append(f"Missing {len(missing_headers)} critical security headers.")

        # 3. Open Critical Ports Check
        open_ports = data.get("Open Ports", [])
        dangerous_ports = [21, 22, 23, 3306, 3389, 5432]  # FTP, SSH, Telnet, DB Ports
        found_dangerous = [p for p in open_ports if p in dangerous_ports]
        
        if found_dangerous:
            score += 25
            self.detected_issues.append(f"Critical service ports exposed: {found_dangerous}")

        # 4. CDN Expose / Real Origin IP Exposure
        if data.get("CDN") and data.get("Potential Real Origin IP"):
            score += 20
            self.detected_issues.append("Origin IP exposed behind CDN/WAF.")

        # 5. Weak TLS Protocol Check
        if data.get("weak_tls") or (isinstance(ssl_data, dict) and ssl_data.get("protocol") in ["TLSv1.0", "TLSv1.1"]):
            score += 15
            self.detected_issues.append("Outdated/Weak TLS protocol in use.")

        # સ્કોરને 0 થી 100 ની વચ્ચે મર્યાદિત રાખવો
        self.risk_score = min(max(score, 0), 100)

    def generate_summary(self) -> str:
        if self.risk_score < 30:
            return f"Low Risk ({self.risk_score}/100): Security posture is good. Minimal vulnerabilities found."
        elif self.risk_score < 60:
            return f"Moderate Risk ({self.risk_score}/100): Several security gaps identified that should be addressed."
        else:
            return f"High Risk ({self.risk_score}/100): Critical security issues detected! Immediate remediation required."

    def get_recommendations(self) -> list:
        recs = []

        # ડાયગ્નોસ થયેલા ઈશ્યુઝના આધારે ચોક્કસ સલાહ આપો
        for issue in self.detected_issues:
            if "HTTPS" in issue or "SSL" in issue:
                recs.append("Install and enforce a valid SSL/TLS certificate with auto-renewal.")
            elif "security headers" in issue:
                recs.append("Configure essential HTTP Security Headers (CSP, HSTS, X-Frame-Options, X-Content-Type-Options).")
            elif "ports" in issue:
                recs.append("Close unnecessary public ports or restrict access using a firewall/VPN.")
            elif "CDN" in issue:
                recs.append("Restrict direct access to origin IP using firewall rules (allow only CDN IPs).")
            elif "TLS" in issue:
                recs.append("Disable weak protocols (TLS 1.0/1.1) and enforce TLS 1.2 or TLS 1.3.")

        if not recs:
            recs.append("Maintain regular updates and keep monitoring server configuration.")

        return recs
