import json


def configure_summarization_parameters(
    max_summary_length: int = 150,
    summary_window_size: int = 512,
) -> str:
    """Configures constraint parameters and computational sliding windows for text summarization tasks."""
    
    max_len = max(1, int(max_summary_length))
    window_size = max(10, int(summary_window_size))

    # Evaluate computational footprint and chunking ratios
    chunking_density = "High-Density Chunking" if window_size < 256 else "Standard Aggregation Window"
    
    report = {
        "task_paradigm": "Abstractive/Extractive Text Summarization Constraints",
        "parameters": {
            "max_summary_length": max_len,
            "summary_window_size": window_size
        },
        "resolved_pipeline_properties": {
            "token_truncation_bound": max_len,
            "sliding_context_window": window_size,
            "attention_aggregation_mode": chunking_density
        },
        "configuration_applied_successfully": True
    }

    return f"[summarization_config] Summarization pipeline dimensions updated: {json.dumps(report, ensure_ascii=False)}"


SKILLS = [
    {
        "name": "summarization_config",
        "description": "Sets structural constraint targets and computational token window splits for text summarization components.",
        "trigger_phrases": [
            "text summarization parameters",
            "set max summary length",
            "configure summary window size",
            "setup summarization configuration",
            "summarization engine settings",
            "adjust text summary limits",
        ],
        "func": configure_summarization_parameters,
    },
]