from ai.ai_engine import AIEngine

def get_ai_summary(data: dict) -> dict:
    engine = AIEngine()
    engine.analyze(data)
    return {
        "risk_score": engine.risk_score,
        "summary": engine.generate_summary(),
        "recommendations": engine.get_recommendations()
    }
