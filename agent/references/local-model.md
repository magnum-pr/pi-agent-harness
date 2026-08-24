# Local model — Mobile LLM + Qwen

## What it is
`~/projects/mobile-llm` — a menu-bar app that starts/stops the llama.cpp
server and a pi session. Manages RAM/battery, benchmarks tokens/s,
low-power mode (16k context).

- Server binary: `~/.local/llama/llama-b10444/llama-server`
- Model: `~/models/qwen2.5-coder-7b-instruct-q4_k_m.gguf`
- Port 8080

## pi integration
`~/.pi/agent/models.json` defines a "local" provider:
- baseUrl `http://127.0.0.1:8080/v1`, api `openai-completions`, dummy key
- compat: `supportsDeveloperRole:false`, `supportsReasoningEffort:false`
- model id `qwen2.5-coder-7b-instruct-q4_k_m`

## Switch
- In chat: `/model` → "Qwen2.5-Coder 7B (Local)" (back to DeepSeek anytime)
- New window: Mobile LLM menu → Open Pi Session
- Lifecycle: menu-bar dot (gray=off, amber=starting, green=on)

## Honest limits
7B local is far weaker than DeepSeek for long agent work. Use for light
Q&A/notes/mechanical edits; keep the paid model for builds/debugging.

## Server start (manual, if menu bar is off)
`nohup ~/.local/llama/llama-b10444/llama-server --model ~/models/qwen2.5-coder-7b-instruct-q4_k_m.gguf --host 127.0.0.1 --port 8080 -ngl 999 -c 32768 --jinja > ~/.local/llama/server.log 2>&1 &`
