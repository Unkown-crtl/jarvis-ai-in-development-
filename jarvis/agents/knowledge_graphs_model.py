import json


def configure_knowledge_graph_model(
    entity_disambiguation: bool = True,
    relation_extraction: str = "triplet",
) -> str:
    """Configures processing constraints for text-to-graph extraction models, targeting entity and relationship discovery."""
    
    relation_mode = relation_extraction.strip().lower()
    
    if relation_mode not in ["triplet", "graph_neural_network", "matrix_dependency"]:
        return f"[kg_model_config] Error: Unsupported relation extraction mapping mechanism: '{relation_extraction}'."

    # Map architectural feature capabilities across graph generation parameters
    structural_capabilities = {
        "entity_resolution_layer": "Contextual Cross-Encoder (Disambiguation Enabled)" if entity_disambiguation else "Exact Match Native Filtering",
        "relationship_representation_format": relation_mode.upper(),
        "graph_node_schema_variant": "Subject-Predicate-Object (SPO Matrix)" if relation_mode == "triplet" else "Dense Continuous Embeddings"
    }

    report = {
        "model_paradigm": "Knowledge Graph Enhanced Language Model Setup",
        "extraction_flags": {
            "entity_disambiguation_active": entity_disambiguation,
            "relation_extraction_strategy": relation_mode
        },
        "resolved_graph_architecture": structural_capabilities,
        "pipeline_state": "Ready for unstructured knowledge ingestion"
    }

    return f"[kg_model_config] Knowledge graph alignment layer configured: {json.dumps(report, ensure_ascii=False)}"


SKILLS = [
    {
        "name": "kg_model_config",
        "description": "Configures parsing settings for knowledge-graph-based architectures, defining entity resolution behaviors and extraction paradigms.",
        "trigger_phrases": [
            "knowledge graph based models",
            "configure entity disambiguation",
            "set relation extraction mode",
            "setup graph model parsing",
            "knowledge graph model configuration",
            "enable entity disambiguation setting",
        ],
        "func": configure_knowledge_graph_model,
    },
]