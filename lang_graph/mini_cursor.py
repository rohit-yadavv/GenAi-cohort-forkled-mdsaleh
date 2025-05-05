
















config = {
    "version": "v1.1",
    "embedder": {
        "provider": PROVIDER,
        "config": {
            "model":EMBEDDING_MODEL,
            "embedding_dims":768
        }
    },
    "llm": {
        "provider": PROVIDER,
        "config": {
            "model": OLLAMA_LLM_MODEL
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": QDRANT_HOST,
            "port": 6333,
            "embedding_model_dims":768
        }
    },
    "graph_store":{
        "provider":"neo4j",
        "config":{
            "url": NEO4j_URL,
            "username": NEO4J_USERNAME,
            "password": NEO4J_PASSWORD,
        }
    }

}