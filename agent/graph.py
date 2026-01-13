from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from agent.intent_classifier import classify_intent
from agent.rag import retrieve_knowledge
from agent.tools import mock_lead_capture


# =========================
# STATE
# =========================
class AgentState(TypedDict):
    # routing
    route: Optional[str]

    # conversation
    user_input: Optional[str]
    response: Optional[str]

    # intent + flow
    intent: Optional[str]
    pricing_shown: bool
    collecting_lead: bool
    lead_step: Optional[str]   # name | email | platform

    # lead data
    name: Optional[str]
    email: Optional[str]
    platform: Optional[str]


# =========================
# ROUTER NODE (RETURNS STATE, NOT STRING)
# =========================
def router_node(state: AgentState):
    # If already collecting lead → always go to lead node
    if state["collecting_lead"]:
        state["route"] = "lead"
        return state

    # Otherwise classify intent
    intent = classify_intent(state["user_input"])
    state["intent"] = intent

    if intent == "greeting":
        state["route"] = "greeting"
    elif intent == "product_inquiry":
        state["route"] = "pricing"
    elif intent == "high_intent" and state["pricing_shown"]:
        state["route"] = "lead_start"
    else:
        state["route"] = "general"

    return state


# =========================
# NODES
# =========================
def greeting_node(state: AgentState):
    state["response"] = "Hi! How can I help you today?"
    return state


def pricing_node(state: AgentState):
    state["pricing_shown"] = True
    state["response"] = retrieve_knowledge(state["user_input"])
    return state


def lead_start_node(state: AgentState):
    state["collecting_lead"] = True
    state["lead_step"] = "name"
    state["response"] = "Great! May I know your name?"
    return state


def lead_node(state: AgentState):
    # Name → Email → Platform (STRICT)

    if state["lead_step"] == "name":
        state["name"] = state["user_input"]
        state["lead_step"] = "email"
        state["response"] = "Thanks! Please share your email."
        return state

    if state["lead_step"] == "email":
        state["email"] = state["user_input"]
        state["lead_step"] = "platform"
        state["response"] = "Which platform do you create content on?"
        return state

    if state["lead_step"] == "platform":
        state["platform"] = state["user_input"]

        mock_lead_capture(
            state["name"],
            state["email"],
            state["platform"]
        )

        state["response"] = "You're all set! Our team will contact you soon."
        return state

    return state


def general_node(state: AgentState):
    state["response"] = "Could you please clarify?"
    return state


# =========================
# GRAPH
# =========================
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("greeting", greeting_node)
    graph.add_node("pricing", pricing_node)
    graph.add_node("lead_start", lead_start_node)
    graph.add_node("lead", lead_node)
    graph.add_node("general", general_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {
            "greeting": "greeting",
            "pricing": "pricing",
            "lead_start": "lead_start",
            "lead": "lead",
            "general": "general",
        }
    )

    graph.add_edge("greeting", END)
    graph.add_edge("pricing", END)
    graph.add_edge("lead_start", END)
    graph.add_edge("lead", END)
    graph.add_edge("general", END)

    return graph.compile()
