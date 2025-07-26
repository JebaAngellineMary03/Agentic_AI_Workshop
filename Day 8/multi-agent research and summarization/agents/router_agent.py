def route_query(state):
    query = state["query"].lower()

    # Keywords for each route
    rag_keywords = ["ai", "artificial intelligence", "machine learning", "deep learning", "langgraph", "gemini"]
    web_keywords = ["latest", "current", "news", "trending", "today", "2025"]

    # Route to Web if any web keyword matches
    if any(word in query for word in web_keywords):
        return {"route": "web_research"}

    # Route to RAG if any RAG keyword matches
    if any(word in query for word in rag_keywords):
        return {"route": "rag"}

    return {"route": "llm"}
