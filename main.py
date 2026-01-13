from agent.graph import build_graph

# Build LangGraph
graph = build_graph()

# -------------------------
# INITIAL STATE
# -------------------------
state = {
    "route": None,

    "user_input": None,
    "response": None,

    "intent": None,
    "pricing_shown": False,
    "collecting_lead": False,
    "lead_step": None,

    "name": None,
    "email": None,
    "platform": None,
}

print("AutoStream Agent started. Type 'exit' to quit.\n")

# -------------------------
# MAIN LOOP
# -------------------------
while True:
    user_input = input("User: ").strip()

    if user_input.lower() == "exit":
        break

    state["user_input"] = user_input

    # Invoke LangGraph
    state = graph.invoke(state)

    print("Agent:", state["response"])
