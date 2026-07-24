class AIEngine:
    def __init__(self):
        self.risk_score = 0
        self.summary = ""
        self.recommendations = []
        self.vulnerabilities = []  # ડિટેક્ટ થયેલી બધી જ ક્ષતિઓની યાદી

    def analyze(self, data: dict):
        score = 0
        self.vulnerabilities = []

        # ----------------------------------------------------
        # 1. SSL / HTTPS Critical Check (સૌથી વધુ મહત્વનું)
        # ----------------------------------------------------
        https_enabled = data.get("https_enabled", True)
        ssl_data = data.get("SSL", {})
        
        if not https_enabled:
            score += 40
            self.vulnerabilities.append({
                "severity": "CRITICAL",
                "issue": "Missing HTTPS / Unencrypted Connection",
                "details": "વેબસાઇટ HTTP પર ચાલે છે. ડેટા પ્લેન ટેક્સ્ટમાં ટ્રાન્સફર થાય છે."
            })
        
        if isinstance(ssl_data, dict) and ssl_data.get("expired", False):
            score += 50
            self.vulnerabilities.append({
                "severity": "CRITICAL",
                "issue": "Expired SSL Certificate",
                "details": "SSL સર્ટિફિકેટ એક્સપાયર થઈ ગયું છે, જે બ્રાઉઝર વોર્નિંગ દર્શાવે છે."
            })

        # ----------------------------------------------------
        # 2. Critical Open Ports Check (ડેટાબેઝ/સર્વર એક્સેસ)
        # ----------------------------------------------------
        open_ports = data.get("Open Ports", [])
        dangerous_ports = [21, 22, 23, 3306, 3389, 5432]  # FTP, SSH, Telnet, DB Ports
        found_dangerous = [p for p in open_ports if p in dangerous_ports]
        
        if found_dangerous:
            score += 35
            self.vulnerabilities.append({
                "severity": "HIGH",
                "issue": f"Exposed Critical Ports ({found_dangerous})",
                "details": "સર્વરના મહત્વના એડમિન/ડેટાબેઝ પોર્ટ્સ પબ્લિકલી ખુલ્લા છે."
            })

        # ----------------------------------------------------
        # 3. Security Headers Check (હવે વાજબી પેનલ્ટી સાથે)
        # ----------------------------------------------------
        missing_headers = data.get("missing_security_headers", [])
        if isinstance(missing_headers, list) and len(missing_headers) > 0:
            # હવે દરેક મિસિંગ હેડર માટે ફક્ત ૨ કે ૩ પોઈન્ટ્સ જ ઉમેરાશે (મહત્તમ ૧૨)
            header_penalty = min(len(missing_headers) * 3, 12)
            score += header_penalty
            
            # જો બહુ અગત્યના હેડર્સ મિસિંગ હોય તો જ સિક્યોરિટી એલર્ટ આપો
            important_missing = [h for h in missing_headers if h in ["Strict-Transport-Security", "Content-Security-Policy"]]
            if important_missing:
                self.vulnerabilities.append({
                    "severity": "LOW",
                    "issue": f"Missing Hardening Headers ({', '.join(important_missing)})",
                    "details": "XSS અથવા Clickjacking જેવી સપાટી સામે રક્ષણ આપતા હેડર્સ મિસિંગ છે."
                })

        # ----------------------------------------------------
        # 4. CDN Expose / Real Origin IP Exposure
        # ----------------------------------------------------
        if data.get("CDN") and data.get("Potential Real Origin IP"):
            score += 15
            self.vulnerabilities.append({
                "severity": "MEDIUM",
                "issue": "CDN Origin IP Bypass",
                "details": "Cloudflare/WAF પાછળનો સાચો સર્વર IP જાહેર થઈ ગયો છે."
            })

        # ----------------------------------------------------
        # 5. Outdated TLS Protocols
        # ----------------------------------------------------
        if data.get("weak_tls") or (isinstance(ssl_data, dict) and ssl_data.get("protocol") in ["TLSv1.0", "TLSv1.1"]):
            score += 15
            self.vulnerabilities.append({
                "severity": "MEDIUM",
                "issue": "Weak / Outdated TLS Protocol",
                "details": "જુના અને સુરક્ષિત ન હોય તેવા TLS 1.0/1.1 નો ઉપયોગ થઈ રહ્યો છે."
            })

        # સ્કોરને ૦ થી ૧૦૦ વચ્ચે રાખવો
        self.risk_score = min(max(score, 0), 100)

    def generate_summary(self) -> str:
        if self.risk_score <= 15:
            return f"Low Risk ({self.risk_score}/100): Excellent security posture. Standard enterprise level settings."
        elif self.risk_score <= 40:
            return f"Moderate Risk ({self.risk_score}/100): Minor missing hardening configurations, but overall safe."
        elif self.risk_score <= 70:
            return f"Elevated Risk ({self.risk_score}/100): Significant security gaps identified that require attention."
        else:
            return f"High Critical Risk ({self.risk_score}/100): Dangerous open ports or invalid SSL detected!"

    def get_recommendations(self) -> list:
        recs = []
        for vuln in self.vulnerabilities:
            if vuln["severity"] in ["CRITICAL", "HIGH"]:
                recs.append(f"<b>[Fix Required]</b> {vuln['issue']}: {vuln['details']}")
            else:
                recs.append(f"<b>[Recommendation]</b> {vuln['issue']}")

        if not recs:
            recs.append("No critical vulnerabilities found. Maintain current configuration.")
            
        return recs
