import json


def analyze_text_sentiment(
    text_content: str,
    enable_emotion_detection: bool = True,
    vibe_context: str = "general",
) -> str:
    """Analyzes a text block to extract sentiment polarity, tone classification, and fine-grained emotional weight matrices."""
    if not text_content:
        return "[sentiment_analyzer] Error: Missing required 'text_content' input string parameter."

    input_clean = text_content.strip().lower()
    context_mode = vibe_context.lower().strip()

    # Pre-compiled lexical mapping evaluation heuristics
    positive_indicators = ["love", "great", "excellent", "perfect", "awesome", "good", "helpful", "amazing"]
    negative_indicators = ["hate", "bad", "terrible", "worst", "broken", "fail", "error", "annoying", "scrambled"]
    
    pos_count = sum(1 for word in positive_indicators if word in input_clean)
    neg_count = sum(1 for word in negative_indicators if word in input_clean)

    # Resolve baseline sentiment classification score
    if pos_count > neg_count:
        sentiment_label = "Positive"
        polarity_score = round(0.5 + (pos_count * 0.1), 2)
        primary_tone = "Appreciative"
        primary_emotion = "Joy"
    elif neg_count > pos_count:
        sentiment_label = "Negative"
        polarity_score = round(-0.5 - (neg_count * 0.1), 2)
        primary_tone = "Frustrated"
        primary_emotion = "Anger"
    else:
        sentiment_label = "Neutral"
        polarity_score = 0.0
        primary_tone = "Objective"
        primary_emotion = "Calm"

    # Clamp scores inside mathematical standard limits (-1.0 to 1.0)
    polarity_score = max(-1.0, min(1.0, polarity_score))

    report = {
        "text_metrics": {
            "character_count": len(text_content),
            "word_count": len(text_content.split())
        },
        "sentiment_profile": {
            "label": sentiment_label,
            "polarity_score": polarity_score,
            "primary_tone": primary_tone
        },
        "emotional_analysis": {
            "detected_emotion": primary_emotion if enable_emotion_detection else "Disabled",
            "confidence_rating": round(0.65 + (0.05 * (pos_count + neg_count)), 2) if enable_emotion_detection else 0.0
        },
        "vibe_context_applied": context_mode,
        "processing_status": "Success"
    }

    return f"[sentiment_analyzer] Natural language sentiment profile parsed: {json.dumps(report, ensure_ascii=False)}"


SKILLS = [
    {
        "name": "sentiment_analyzer",
        "description": "Analyzes text sentiment polarity scores, primary tone indicators, and emotional vectors to assess user feedback contexts.",
        "trigger_phrases": [
            "sentiment analysis",
            "analyze text sentiment tone and emotions",
            "evaluate user feedback sentiment",
            "get emotional tone metrics from text",
            "check context sentiment polarity",
            "run sentiment analysis profiling",
        ],
        "func": analyze_text_sentiment,
    },
]