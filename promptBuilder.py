def build_prompt(question, results):
    
    prompt = (
        "You are a helpful AI assistant.\n\n"
        "Use ONLY the information below to answer the user's question.\n\n"
        "Context:\n\n"
    )

    for index, result in enumerate(results, start=1):

        chunk = result["chunk"]

        prompt += (
            f"[{index}]\n"
            f"{chunk['content']}\n\n"
        )

    prompt += (
        f"Question:\n{question}\n\n"
        "If the answer cannot be found in the context,\n"
        "reply with:\n"
        "\"Bu konuda yeterli bilgi bulunamadı.\"\n\n"
        "Answer:"
    )

    return prompt