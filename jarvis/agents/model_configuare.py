import json


def configure_model_parameters(
    model_name_or_path: str,
    config_name: str = "default",
) -> str:
    """Configures architectural hyperparameters and setup paths for loading deep learning foundations."""
    if not model_name_or_path:
        return "[model_configurator] Error: Parameter 'model_name_or_path' is required."

    model_target = model_name_or_path.strip()
    config_target = config_name.strip()

    # Pre-compiled lookup matrix containing foundational hyperparameter configurations
    base_configurations = {
        "llama 3.1": {
            "context_window": 131072,
            "hidden_size": 4096,
            "num_attention_heads": 32,
            "tensor_parallel_size": 1,
        },
        "bert-base-uncased": {
            "context_window": 512,
            "hidden_size": 768,
            "num_attention_heads": 12,
            "tensor_parallel_size": 1,
        }
    }

    model_key = model_target.lower()
    if model_key in base_configurations:
        structural_specs = base_configurations[model_key].copy()
    else:
        # Fallback profile generating standard architectural dimensions for unindexed paths
        structural_specs = {
            "context_window": 2048,
            "hidden_size": 2048,
            "num_attention_heads": 16,
            "tensor_parallel_size": 1,
        }

    # Override configurations if custom variations are passed
    if config_target != "default":
        structural_specs["custom_configuration_profile"] = config_target
        structural_specs["quantization_mode"] = "int8" if "quantized" in config_target.lower() else "fp16"

    report = {
        "selected_model_identifier": model_target,
        "configuration_profile_applied": config_target,
        "resolved_model_hyperparameters": structural_specs,
        "initialization_ready_flag": True
    }

    return f"[model_configurator] Configuration mapping phase complete: {json.dumps(report, ensure_ascii=False)}"


SKILLS = [
    {
        "name": "model_configurator",
        "description": "Sets up model path allocations, contextual matrix adjustments, and architectural initialization profiles.",
        "trigger_phrases": [
            "model configuration",
            "configure model parameters",
            "set model name or path",
            "apply model config profile",
            "initialize llama configuration",
            "setup model hyperparameters",
        ],
        "func": configure_model_parameters,
    },
]