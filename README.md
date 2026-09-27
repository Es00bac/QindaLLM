# QindaLLM

qinda's local coding-model server, packaged as `sci-ml/qinda-llm-server` in
the QindaGentoo overlay (models: `sci-ml/gguf-coding-models`, runtime:
::guru's `sci-misc/llama-cpp[vulkan]`).

| File | Installed as | What it does |
| --- | --- | --- |
| `systemd/qinda-llm.service` | unit | `llama-server` in router mode over `/etc/qinda-llm/models.ini`, API key from `/etc/qinda-llm/api-key`, `--metrics` on |
| `systemd/qinda-llm-server.target` | unit | **LLM Server mode**: multi-user + the server + the console, no SDDM or desktop |
| `systemd/qinda-llm-monitor.service` | unit | `qinda-llm-top --console` on tty1 in that mode (Alt+F2 for a login) |
| `monitor/qinda-llm-top` | `/usr/bin` | live console: model and placement, tokens/s, slots, requests, CPU/RAM/GPU/network |
| `config/models.ini`, `config/server.env` | `/etc/qinda-llm/` | model presets and the listen address |
| `boot/50-llm-server.conf` | `/usr/share/qinda-boot/modes.d/` | the "LLM Server" row of the QindaQt boot menu (`sys-boot/qinda-boot`) |

## Using it

- Boot **LLM Server** from the boot menu, or from the desktop:
  `systemctl isolate qinda-llm-server.target` (stops the desktop). Next boot
  returns to the menu's default.
- Alongside the desktop: `systemctl start qinda-llm.service`; watch it with
  `sudo qinda-llm-top` (or `qinda-llm-top` with the key in
  `~/.config/qinda-llm/api-key`).
- Clients send `"model": "ornith"` or `"qwen3.6"` (the sections of
  `models.ini`); the router loads the requested model and unloads the other.
  OpenAI (`/v1/chat/completions`, `/v1/responses`) and Anthropic
  (`/v1/messages`) APIs are both served.

GPU/CPU placement is left to llama-server's `--fit`: every layer on the GPU,
and as many MoE expert tensors in system RAM as needed to keep 1 GiB of VRAM
free, measured at load time.

## qinda-llm-top

Reads `/models`, `/props`, `/slots` and `/metrics` from the server once a
second, the service journal for completed-request timings and load facts, and
`/proc` and amdgpu sysfs for the machine. Live speeds are deltas of each
slot's prompt and generated token counters. Keys: `m` load the other model,
`u` unload, `r` restart the service, `l` log view, `q` quit. `--once` prints a
plain snapshot; `--console` sets a Terminus font sized to the framebuffer and
the QindaQt palette for the Linux console.

```sh
make test
```
