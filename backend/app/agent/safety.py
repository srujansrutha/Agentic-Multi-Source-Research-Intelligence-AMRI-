from app.agent.state import AgentState
from app.services.llm_factory import llm
from langchain_core.messages import HumanMessage

def guardrail_node(state: AgentState):
    """
    Safety Layer: Checks output for toxicity, hallucinations, and PII.
    Acts as a 'Responsible AI' gatekeeper.
    """
    report = state.get("final_report")
    if not report:
        return {}

    # Simple Layout for Guardrail Prompt (Lite version of LlamaGuard)
    prompt = f"""
    You are a Safety & Compliance Officer. Review the following report for:
    1. Toxicity/Harmful Content
    2. PII (Personally Identifiable Information) leaks
    3. Severe Hallucinations (making up facts not likely in a research context)

    Report:
    {report}

    If SAFE, return "SAFE".
    If UNSAFE, return "UNSAFE: <reason>".
    """

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    result = response.content.strip()

    if "UNSAFE" in result:
        # Fallback mechanism: Rewrite or Block
        print(f"--- 🛡️ GUARDRAIL TRIGGERED: {result} ---")
        return {
            "final_report": f"⚠️ **Safety Alert**: The generated report was flagged by our safety guardrails.\n\nReason: {result}",
            "critique_comments": "Safety Violation Triggered"
        }
    
    print("--- 🛡️ GUARDRAIL PASSED ---")
    return {}
