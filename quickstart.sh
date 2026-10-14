#!/usr/bin/env bash
#
# FlowBeast one-command launcher.
#
# Preflight-checks every dependency that a cold start actually needs, then
# brings up the FastAPI backend and the Streamlit demo together. Ctrl-C stops
# both. Every check fails with an actionable message rather than a stack trace
# from halfway through pipeline execution.
#
# Usage:  ./quickstart.sh [--api-only]
#
set -uo pipefail

cd "$(dirname "$0")"

API_PORT="${API_PORT:-8000}"
UI_PORT="${UI_PORT:-8501}"
UI_ONLY_READY_TIMEOUT=60

C_OK=$'\033[0;32m'; C_ERR=$'\033[0;31m'; C_WARN=$'\033[0;33m'; C_DIM=$'\033[2m'; C_OFF=$'\033[0m'
ok()   { printf '%s  ✓%s %s\n' "$C_OK" "$C_OFF" "$1"; }
bad()  { printf '%s  ✗%s %s\n' "$C_ERR" "$C_OFF" "$1"; }
warn() { printf '%s  !%s %s\n' "$C_WARN" "$C_OFF" "$1"; }
step() { printf '\n%s▸ %s%s\n' "$C_DIM" "$1" "$C_OFF"; }
die()  { bad "$1"; [ $# -gt 1 ] && printf '\n%s\n' "$2"; exit 1; }

API_PID=""; UI_PID=""
cleanup() {
    code=$?
    trap - EXIT INT TERM
    # Nothing to say if we bailed during preflight — no service ever started.
    [ -z "$API_PID$UI_PID" ] && exit "$code"
    printf '\n%s  shutting down…%s\n' "$C_DIM" "$C_OFF"
    # Negative PID kills the whole process group; `setsid` below put each
    # server in its own group so uvicorn's children die with it.
    for pid in "$UI_PID" "$API_PID"; do
        [ -n "$pid" ] && kill -- "-$pid" 2>/dev/null
    done
    wait 2>/dev/null
    printf '%s  stopped.%s\n' "$C_DIM" "$C_OFF"
    exit "$code"
}
# Signals only set the exit code; EXIT does the actual teardown, so an
# interrupt during startup can't fall through and keep launching services.
trap cleanup EXIT
trap 'exit 130' INT TERM

# ---------------------------------------------------------------- preflight

step "Preflight"

command -v uv >/dev/null 2>&1 || die "uv not found." \
"    FlowBeast uses uv, not pip. Install:
      curl -LsSf https://astral.sh/uv/install.sh | sh"
ok "uv $(uv --version 2>/dev/null | awk '{print $2}')"

if [ ! -f .env ]; then
    [ -f .env.example ] || die ".env is missing and .env.example was not found."
    cp .env.example .env
    warn "Created .env from .env.example — you must fill in an API key."
    printf '\n    Edit %s.env%s and set:\n' "$C_DIM" "$C_OFF"
    printf '      ACTIVE_VENDOR=deepseek\n      DEEPSEEK_API_KEY=sk-xxxxxxxx\n\n'
    printf '    Then re-run %s./quickstart.sh%s\n' "$C_DIM" "$C_OFF"
    exit 1
fi
ok ".env found"

# Read a value out of .env without sourcing it (sourcing would let an empty
# assignment clobber the shell env, the same trap config.py has).
# Octal escapes in tr keep this free of nested-quote escaping: \42=" \47='
env_val() { sed -n "s/^[[:space:]]*$1[[:space:]]*=[[:space:]]*//p" .env | tail -1 | tr -d '\42\47\r'; }

VENDOR="$(env_val ACTIVE_VENDOR)"; VENDOR="${VENDOR:-deepseek}"
case "$VENDOR" in
    ollama) KEY_VAR="" ;;
    deepseek) KEY_VAR=DEEPSEEK_API_KEY ;;
    qwen)     KEY_VAR=DASHSCOPE_API_KEY ;;   # qwen reads DASHSCOPE_API_KEY, not QWEN_API_KEY
    openai)   KEY_VAR=OPENAI_API_KEY ;;
    anthropic) KEY_VAR=ANTHROPIC_API_KEY ;;
    gemini)   KEY_VAR=GOOGLE_API_KEY ;;
    glm)      KEY_VAR=GLM_API_KEY ;;
    openrouter) KEY_VAR=OPENROUTER_API_KEY ;;
    *) die "Unknown ACTIVE_VENDOR '$VENDOR' in .env." ;;
esac

if [ -n "$KEY_VAR" ]; then
    KEY="$(env_val "$KEY_VAR")"
    [ -n "$KEY" ] || die "$KEY_VAR is empty in .env (ACTIVE_VENDOR=$VENDOR)." \
"    Get a key, then put it in .env:
      ${KEY_VAR}=sk-xxxxxxxx
    Note: the backend reads .env at import time, so restart it after any edit."
    ok "LLM vendor: $VENDOR (key configured)"
else
    ok "LLM vendor: ollama (no key needed)"
fi

EMBED_VENDOR="$(env_val EMBED_VENDOR)"; EMBED_VENDOR="${EMBED_VENDOR:-ollama}"
if [ "$EMBED_VENDOR" = "ollama" ]; then
    command -v ollama >/dev/null 2>&1 || die "ollama not found, but EMBED_VENDOR=ollama." \
"    Embeddings run locally via Ollama (no API key needed):
      https://ollama.com/download
    Or switch EMBED_VENDOR in .env to a vendor that serves embeddings."
    if ! curl -sf -m 5 http://localhost:11434/api/tags >/dev/null 2>&1; then
        die "Ollama is installed but not responding on :11434." \
"    Start it:  ollama serve"
    fi
    if ! curl -sf -m 5 http://localhost:11434/api/tags | grep -q 'nomic-embed-text'; then
        printf '%s  …%s pulling nomic-embed-text (first run only)\n' "$C_DIM" "$C_OFF"
        ollama pull nomic-embed-text || die "Failed to pull nomic-embed-text."
    fi
    ok "embeddings: ollama / nomic-embed-text"
else
    ok "embeddings: $EMBED_VENDOR"
fi

for spec in "$API_PORT:API" "$UI_PORT:UI"; do
    port="${spec%%:*}"
    if curl -sf -m 2 -o /dev/null "http://localhost:$port" 2>/dev/null; then
        die "Port $port is already serving something (${spec##*:} would bind here)." \
"    Stop it first:   fuser -k ${port}/tcp"
    fi
done
ok "ports $API_PORT and $UI_PORT are free"

# ------------------------------------------------------------- dependencies

step "Dependencies"
uv sync --quiet || die "uv sync failed."
ok "dependencies in sync"

# ------------------------------------------------------------------- FP3

step "FP3 viral memory"
FP3_INDEX="flowbeast/data/outputs/vector_store/fp3/fp3.index"
if [ -f "$FP3_INDEX" ]; then
    ok "index present ($(du -h "$FP3_INDEX" | cut -f1))"
else
    printf '%s  …%s building index from seed data (first run only)\n' "$C_DIM" "$C_OFF"
    uv run python -m flowbeast.fp3.seed_data >/dev/null 2>&1 \
        || die "FP3 seeding failed." "    Run it directly to see why:
      uv run python -m flowbeast.fp3.seed_data"
    ok "index built"
fi

# ------------------------------------------------------------------ launch

step "Starting services"
setsid uv run uvicorn flowbeast.api.main:app --host 0.0.0.0 --port "$API_PORT" \
    >/tmp/flowbeast_api.log 2>&1 &
API_PID=$!

printf '%s  …%s waiting for API on :%s\n' "$C_DIM" "$C_OFF" "$API_PORT"
for _ in $(seq "$UI_ONLY_READY_TIMEOUT"); do
    curl -sf -m 2 -o /dev/null "http://localhost:$API_PORT/health" 2>/dev/null && break
    kill -0 "$API_PID" 2>/dev/null || die "API process exited during startup." \
"    Last lines of /tmp/flowbeast_api.log:
$(tail -15 /tmp/flowbeast_api.log | sed 's/^/      /')"
    sleep 1
done
curl -sf -m 2 -o /dev/null "http://localhost:$API_PORT/health" \
    || die "API did not become healthy in ${UI_ONLY_READY_TIMEOUT}s." \
"    Check /tmp/flowbeast_api.log"
ok "API   → http://localhost:$API_PORT      (log: /tmp/flowbeast_api.log)"

if [ "${1:-}" = "--api-only" ]; then
    printf '\n%s  API-only mode. Ctrl-C to stop.%s\n\n' "$C_DIM" "$C_OFF"
    wait "$API_PID"
    exit 0
fi

setsid uv run streamlit run flowbeast/demo/app.py \
    --server.port "$UI_PORT" --server.headless true \
    >/tmp/flowbeast_ui.log 2>&1 &
UI_PID=$!

printf '%s  …%s waiting for UI on :%s\n' "$C_DIM" "$C_OFF" "$UI_PORT"
for _ in $(seq "$UI_ONLY_READY_TIMEOUT"); do
    curl -sf -m 2 -o /dev/null "http://localhost:$UI_PORT" 2>/dev/null && break
    kill -0 "$UI_PID" 2>/dev/null || die "UI process exited during startup." \
"    Last lines of /tmp/flowbeast_ui.log:
$(tail -15 /tmp/flowbeast_ui.log | sed 's/^/      /')"
    sleep 1
done
curl -sf -m 2 -o /dev/null "http://localhost:$UI_PORT" \
    || die "UI did not become healthy in ${UI_ONLY_READY_TIMEOUT}s." \
"    Check /tmp/flowbeast_ui.log"
ok "UI    → http://localhost:$UI_PORT      (log: /tmp/flowbeast_ui.log)"

printf '\n%s──────────────────────────────────────────────%s\n' "$C_DIM" "$C_OFF"
printf '  %s🌊 FlowBeast is up.%s  Open %shttp://localhost:%s%s\n' \
    "$C_OK" "$C_OFF" "$C_DIM" "$UI_PORT" "$C_OFF"
printf '  Pick a recommended topic, hit Generate, ~2-4 min per run.\n'
printf '  Ctrl-C to stop both services.\n'
printf '%s──────────────────────────────────────────────%s\n\n' "$C_DIM" "$C_OFF"

# Exit as soon as either service dies, so the trap cleans up the other.
while kill -0 "$API_PID" 2>/dev/null && kill -0 "$UI_PID" 2>/dev/null; do
    sleep 1
done
# Ctrl-C exits from the signal trap, so reaching here means a service crashed.
warn "A service exited unexpectedly — shutting the other one down."
exit 1
