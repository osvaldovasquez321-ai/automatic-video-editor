#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Uso: ./run_editor.sh entrada.mp4 salida.mp4 [duración-máxima]"
  exit 1
fi

INPUT="$1"
OUTPUT="$2"
DURATION="${3:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARGS=("$INPUT" --output "$OUTPUT")
if [[ -n "$DURATION" ]]; then
  ARGS+=(--max-duration "$DURATION")
fi

python3 "$SCRIPT_DIR/video_editor.py" "${ARGS[@]}"
