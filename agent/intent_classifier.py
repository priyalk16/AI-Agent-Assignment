def classify_intent(user_input: str) -> str:
    text = user_input.lower().strip()

   
    if any(x in text for x in [
        "i want to try",
        "i want to use",
        "i want to sign up",
        "sign me up",
        "get started",
        "start using",
        "subscribe",
        "buy",
    ]):
        return "high_intent"

    
    if text in ["hi", "hello", "hey"]:
        return "greeting"

    
    if any(x in text for x in ["price", "pricing", "cost", "plans"]):
        return "product_inquiry"

    return "general"
