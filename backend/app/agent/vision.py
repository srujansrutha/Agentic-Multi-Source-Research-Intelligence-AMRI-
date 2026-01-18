from app.agent.state import AgentState
from app.services.llm_factory import llm
from langchain_core.messages import HumanMessage
from app.core.config import settings

def vision_node(state: AgentState):
    """
    Multi-Modal Layer: Analyzes images found during search.
    Uses GPT-4o Vision to describe charts/diagrams.
    """
    # 1. Extract potential image URLs from search results
    # (In a real scenario, we'd parse the search_results or use Tavily's image field)
    # For this implementation, let's look for specific image keys if available, 
    # or just assume we might have passed them in state["search_results"] if we parsed differently.
    
    # However, Tavily python client 'search' with include_images=True returns an 'images' key.
    # We need to ensure search_web_node extracted them.
    
    image_urls = state.get("images", []) 
    if not image_urls:
        return {"visual_data": []}

    # Limit to top 1-2 images to save tokens/time
    target_images = image_urls[:2]
    descriptions = []

    print(f"--- 👁️ ANALYZING {len(target_images)} IMAGES ---")

    for url in target_images:
        try:
            # Prepare message for GPT-4o
            message = HumanMessage(
                content=[
                    {"type": "text", "text": "Describe this image in detail, focusing on any charts, data, or key visual information relevant to a research report."},
                    {"type": "image_url", "image_url": {"url": url}}
                ]
            )
            
            # Use the LLM (Must be GPT-4o or Vision capable)
            # We assume llm created by factory is capable (e.g. ChatOpenAI(model="gpt-4o"))
            response = llm.invoke([message])
            desc = f"Image Source: {url}\nAnalysis: {response.content}"
            descriptions.append(desc)
            
        except Exception as e:
            print(f"Vision analysis failed for {url}: {e}")
            
    return {"visual_data": descriptions}
