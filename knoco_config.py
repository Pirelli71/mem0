# Knoco Configuration File for connecting mem0 to Supabase

from mem0 import Memory
from mem0.configs.base import MemoryConfig

# Supabase configuration
supabase_config = {
    "connection_string": "YOUR_SUPABASE_CONNECTION_STRING",  # Replace with your actual connection string
    "collection_name": "knoco_memories",
    "embedding_model_dims": 1536,  # Default for OpenAI embeddings
    "index_method": "hnsw",        # Using hnsw which requires less memory than ivfflat
    "index_measure": "cosine_distance"  # Use cosine distance for similarity comparison
}

# Memory configuration for Knoco
memory_config = MemoryConfig(
    # Vector store configuration
    vector_store={
        "provider": "supabase",
        "config": supabase_config
    },
    
    # Embedding model configuration
    embedder={
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small",
            "api_key": "YOUR_OPENAI_API_KEY"  # Will use environment variable if not set
        }
    },
    
    # LLM configuration
    llm={
        "provider": "openai",
        "config": {
            "model": "gpt-4o",
            "temperature": 0.2,
            "max_tokens": 2000,
            "api_key": "YOUR_OPENAI_API_KEY"  # Will use environment variable if not set
        }
    },
    
    # Custom prompts for consultant-specific memory extraction
    custom_prompt="""
    You are a professional consultant memory system designed to extract valuable information from conversations. 
    Your task is to identify and extract key information that consultants would need to reference later.

    Pay special attention to the following types of information:

    1. DECISIONS: Key decisions made, with their rationale and alternatives
    2. ISSUES: Problems, challenges, or questions that arise
    3. ACTIONS: Tasks, commitments, or next steps agreed upon
    4. CLIENT_CONTEXT: Information about the client's preferences, constraints, or requirements
    5. PROJECT_CONTEXT: Background information about the project scope, timeline, or objectives
    6. REFERENCES: Important documents, sources, or best practices mentioned
    7. LEARNINGS: Insights or lessons that could be applied to future work

    For each memory you identify, extract the core content as a clear, concise statement.
    Include the type of information (e.g., DECISION, ACTION) at the beginning of each statement.

    If you don't find any relevant information to extract, return an empty array: {\"facts\": []}

    For example:
    Input: We decided to use AWS instead of Azure for the cloud infrastructure because of the client's existing AWS expertise.
    Output: {\"facts\": [\"DECISION: The team decided to use AWS over Azure for cloud infrastructure due to client's existing AWS expertise.\"]}

    Input: The client mentioned they need the final report by next Friday and it must include a detailed cost breakdown.
    Output: {\"facts\": [\"CLIENT_CONTEXT: Client requires final report by next Friday with detailed cost breakdown.\"]}

    Format your response as a JSON object with a \"facts\" array containing strings.

    Here are some few shot examples:
    Input: We should probably schedule a meeting with the finance team to discuss budget implications.
    Output: {\"facts\": [\"ACTION: Schedule a meeting with finance team to discuss budget implications.\"]}

    Input: The client doesn't like our proposed solution because they had a negative experience with a similar approach last year.
    Output: {\"facts\": [\"CLIENT_CONTEXT: Client dislikes proposed solution due to negative experience with similar approach last year.\"]}

    Input: After analyzing three options, we've decided to implement the microservice architecture because it offers better scalability and maintainability.
    Output: {\"facts\": [\"DECISION: Implement microservice architecture because it offers better scalability and maintainability.\"]}

    IMPORTANT: Return the facts as simple strings in an array, not as complex objects. The format must be exactly as shown in the examples above.
    """,
    
    # Set the API version to the latest
    version="v1.1"
)

# Create the memory instance with the configuration
def create_memory():
    return Memory(config=memory_config)

# Example usage
if __name__ == "__main__":
    # Set your OpenAI API key in the environment variable
    import os
    os.environ["OPENAI_API_KEY"] = "your-api-key-here"
    
    # Create memory instance
    memory = create_memory()
    
    # Add a test memory
    result = memory.add(
        "We decided to use AWS for cloud infrastructure due to the client's existing expertise.",
        user_id="test-user"
    )
    
    print("Added memory:", result)
    
    # Search for memories
    search_result = memory.search("cloud infrastructure", user_id="test-user")
    print("Search results:", search_result)
