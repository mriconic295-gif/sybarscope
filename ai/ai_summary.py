from ai.ai_engine import AIEngine

def calculate_exact_risk(data: dict) -> tuple:
    """
    સ્કેન ડેટાના આધારે ફેક્ટ-બેઝ્ડ (Rule-Based) રિસ્ક સ્કોર ગણશે.
    આનાથી AI ની ખોટી ગણતરીઓ (Hallucination) અટકશે.
    """
    score = 0
    reasons = []

    # 1. SSL/HTTPS સિક્યોરિટી ચેક
    if not data.get("https_enabled", True):
        score += 30
        reasons.append("Invalid or Missing SSL Certificate")

    # 2. મિસિંગ સિક્યોરિટી હેડર્સ ચેક
    missing_headers = data.get("missing_security_headers", [])
    if missing_headers:
        header_penalty = min(len(missing_headers) * 5, 25)
        score += header_penalty
        reasons.append(f"Missing {len(missing_headers)} Security Headers")

    # 3. ઓપન પોર્ટ્સ (Open Ports) ચેક
    open_ports = data.get("Open Ports", [])
    dangerous_ports = [21, 22, 23, 3306, 3389, 5432] # FTP, SSH, Telnet, DB Ports
    found_dangerous = [p for p in open_ports if p in dangerous_ports]
    if found_dangerous:
        score += 25
        reasons.append(f"Exposed Critical Ports: {found_dangerous}")

    # 4. CDN અને Origin IP Exposure ચેક
    if data.get("CDN") and data.get("Potential Real Origin IP"):
        score += 20
        reasons.append("CDN Origin IP Exposed/Bypassed")

    # રિસ્ક સ્કોરને 100 ની મર્યાદામાં રાખવો
    final_score = min(score, 100)
    return final_score, reasons


def get_ai_summary(data: dict) -> dict:
    """
    ચોક્કસ રિસ્ક સ્કોર અને AI સમરી રિટર્ન કરશે.
    """
    # 1. રૂલ્સ આધારે સાચો Risk Score ગણો
    calculated_score, risk_reasons = calculate_exact_risk(data)

    # 2. AI Engine માં ચોક્કસ ડેટા મોકલો
    engine = AIEngine()
    
    # AI Engine ને ગણેલો સાચો સ્કોર પાસ કરો
    data["calculated_risk_score"] = calculated_score
    data["risk_reasons"] = risk_reasons
    
    try:
        engine.analyze(data)
        
        # જો AIEngine નો પોતાનો સ્કોર ખોટો હોય, તો આપણી સાચી ગણતરી વાપરો
        risk_score = calculated_score if calculated_score > 0 else getattr(engine, "risk_score", calculated_score)
        
        summary = engine.generate_summary()
        recommendations = engine.get_recommendations()

    except Exception as e:
        # જો AI API અથવા Engine ફેલ થાય તો Fallback રિપોર્ટ
        risk_score = calculated_score
        summary = f"Analysis based on scanned parameters. Identified risks: {', '.join(risk_reasons) if risk_reasons else 'No critical issues found.'}"
        recommendations = [
            "Install valid SSL certificate" if "Invalid or Missing SSL Certificate" in risk_reasons else "Ensure SSL renewal is set to auto",
            "Configure missing HTTP Security Headers (CSP, HSTS, X-Frame-Options)",
            "Restrict public access to administrative or database ports"
        ]

    return {
        "risk_score": risk_score,
        "summary": summary,
        "recommendations": recommendations
    }
