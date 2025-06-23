import sys
import re
import ollama

# Allowed topics
ALLOWED_TOPICS = {
    "basic math": ["math", "add", "subtract", "multiply", "divide", "average", "sum", "number"],
    "health-eyes": ["eye", "eyestrain", "vision", "blink", "screen", "dry", "strain"],
    "system usage": ["install", "pip", "github", "cli", "terminal", "command", "push", "package"],
}

# tokenize the ask from user, to filter/process
def tokenize(text):
    # return text.split(" ")
    tokens = re.findall(r'\b\w+\b', text.lower())
    # print(tokens)
    return tokens


def is_topic_allowed(tokens):
    flat_keywords = [kw for keywords in ALLOWED_TOPICS.values() for kw in keywords]
    math_expr_pattern = r"^\s*\d+\s*[\+\-\*/]\s*\d+\s*$"
    text = " ".join(tokens)
    return any(kw in tokens for kw in flat_keywords) or bool(re.match(math_expr_pattern, text))

def extract_action_and_topic(tokens):
    actions = [w for w in tokens if w in {
        # specific to allowed topics
        "install", "add", "calculate", "reduce", "fix", "relieve", "push", "configure", "create", "build", "use"
    }]
    topics = [w for w in tokens if w in [kw for kws in ALLOWED_TOPICS.values() for kw in kws]]
    return actions, topics

def build_summary(actions, topics):
    a = ", ".join(actions) if actions else "perform a task"
    t = ", ".join(topics) if topics else "a general topic"
    return f"You are asked to **{a}** related to **{t}**.\n"

# create the prompt
def build_prompt(user_input, summary=""):
    return f"""{summary}
You are a helpful assistant.

## Task:
"{user_input}"

Respond in this format, keep it short:

### Steps (Max 5 steps)
Give numbered steps (1–5 only). Be brief and clear.

### Pros (Max 3 points)
Give 2–3 short bullet points on what's good about the process.

### Cons (Max 3 points)
Give 2–3 short bullet points on possible downsides.

Avoid repeating or over-explaining. Do not skip any section.
"""


# Ask model via Ollama
def ask_ai(prompt):
    response = ollama.chat(
        model="phi3:mini",
        messages=[{"role": "user", "content": prompt}],
        options={"num_predict": 300}
    )
    return response['message']['content']

def main():
    if len(sys.argv) < 2:
        print("Usage: python ai_flow_assistant.py \"your question here\"")
        return

    question = sys.argv[1]
    tokens = tokenize(question)

    if not is_topic_allowed(tokens):
        print("Err: XXX This topic is not allowed by admin policy.")
        return

    actions, topics = extract_action_and_topic(tokens)
    summary = build_summary(actions, topics)
    prompt = build_prompt(question, summary)
    answer = ask_ai(prompt)

    print(answer)
    print("\n---")
    print(f"Action: {actions or 'unknown'}\nTopic: {topics or 'unknown'}")

if __name__ == "__main__":
    main()

