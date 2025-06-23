# AI Flow Assistant (CLI)

This tool runs a local AI model (via [Ollama](https://ollama.com)) to help generate:

- Step-by-step guides for a given task  
- Pros and cons of the process  
- Works only on **allowed topics** (e.g., basic math, eye health, CLI tasks)

---

## Requirements

- Python 3.8+
- [Ollama](https://ollama.com/download) (for running local LLM)
- ~4 GB RAM minimum  
- Internet (only during model pull)

---

## LLM Used

- Model: `phi3:mini`
- Source: https://ollama.com/library/phi3
- Size: ~1.8GB
- Runs fully locally on CPU

---

## Setup Instructions

### 1. Install Ollama

Follow [Ollama install instructions](https://ollama.com/download) for your OS.

#### Ubuntu/Debian:

```bash
curl -fsSL https://ollama.com/install.sh | sh

Then start Ollama:
ollama serve &
```

### 2.  Pull the LLM Model
```bash
ollama pull phi3:mini
```

### 3. Create Python Environment (Optional but Recommended)
```bash
python3 -m venv .ai_pyenv
source .ai_pyenv/bin/activate
pip install --upgrade pip
pip install ollama
```

### 4. Run It
```bash
python ai_flow_assistant.py "how to calculate average of 3 numbers"
```


### Admin-Allowed Topics
Only questions from the following categories will be processed:
- Basic math: add, subtract, multiply, divide, average, etc.
- Eye health: strain, blink, dry eyes, screen fatigue
- CLI/system tasks: pip install, push to git, terminal commands

Everything else will be blocked with:

```bash
Err: XXX This topic is not allowed by admin policy.
```


### Customize Topics
Topics are defined inside the Python script:
```bash
ALLOWED_TOPICS = {
  "basic math": [...],
  "health-eyes": [...],
  "system usage": [...]
}
```
You can add more keywords there to expand allowed prompts.

### Example Prompts
```bash
python ai_flow_assistant.py "how to calculate average of 3 numbers"
python ai_flow_assistant.py "how to calculate weighted average of marks from different subjects"

python ai_flow_assistant.py "how to adapt lighting and screen settings to reduce blue light impact on eyes"
python ai_flow_assistant.py "how to prevent dry eyes during long hours of computer usage"
python ai_flow_assistant.py "how to relieve eye strain"

python ai_flow_assistant.py "how to install a package using pip"
python ai_flow_assistant.py "how to update all Python packages in a virtual environment using CLI"

```
