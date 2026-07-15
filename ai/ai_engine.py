class AIEngine:
    def __init__(self):
        self.risk_score = 0
        self.summary = ""
        self.recommendations = []

    def analyze(self, data: dict):
        # Simple rule-based risk score
        score = 0
        if not data.get("https_enabled"):
            score += 30
        if data.get("missing_security_headers"):
            score += 20
        if data.get("expired_cert"):
            score += 40
        if data.get("weak_tls"):
            score += 15
        # ... more rules
        self.risk_score = min(score, 100)

    def generate_summary(self) -> str:
        if self.risk_score < 30:
            return "Good security posture."
        elif self.risk_score < 60:
            return "Moderate risk; some improvements needed."
        else:
            return "High risk; immediate action recommended."

    def get_recommendations(self) -> list:
        recs = []
        if self.risk_score > 20:
            recs.append("Enable HTTPS and HSTS.")
        if self.risk_score > 40:
            recs.append("Implement Content Security Policy.")
        return recs
