#!/usr/bin/env python3
"""Prepara videos para formatos verticales usando FFmpeg."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def positive_int(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("debe ser un entero mayor que cero")
    return number


def non_negative_float(value: str) -> float:
    number = float(value)
    if number < 0:
        raise argparse.ArgumentTypeError("debe ser cero o un número positivo")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convierte un video al formato vertical para TikTok, Shorts y Reels."
    )
    parser.add_argument("input", type=Path, help="ruta del video de entrada")
    parser.add_argument("-o", "--output", type=Path, required=True, help="ruta del video de salida")
    parser.add_argument("--max-duration", type=non_negative_float, help="duración máxima en segundos")
    parser.add_argument("--width", type=positive_int, default=1080, help="ancho de salida (por defecto: 1080)")
    parser.add_argument("--height", type=positive_int, default=1920, help="alto de salida (por defecto: 1920)")
    parser.add_argument("--crf", type=int, choices=range(18, 32), default=23, help="calidad H.264 entre 18 y 31")
    parser.add_argument(
        "--preset",
        choices=("ultrafast", "fast", "medium", "slow"),
        default="medium",
        help="velocidad/calidad de codificación (por defecto: medium)",
    )
    parser.add_argument("--overwrite", action="store_true", help="reemplaza la salida si ya existe")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if shutil.which("ffmpeg") is None:
        print("Error: FFmpeg no está instalado o no está disponible en PATH.", file=sys.stderr)
        return 1
    if not args.input.is_file():
        print(f"Error: no existe el archivo de entrada: {args.input}", file=sys.stderr)
        return 1
    if args.input.resolve() == args.output.resolve():
        print("Error: la entrada y la salida deben ser archivos diferentes.", file=sys.stderr)
        return 1
    if args.output.exists() and not args.overwrite:
        print(f"Error: la salida ya existe: {args.output}. Usa --overwrite para reemplazarla.", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    filter_complex = (
        f"scale={args.width}:{args.height}:force_original_aspect_ratio=increase,"
        f"crop={args.width}:{args.height}"
    )
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-y" if args.overwrite else "-n",
        "-i",
        str(args.input),
        "-vf",
        filter_complex,
        "-c:v",
        "libx264",
        "-preset",
        args.preset,
        "-crf",
        str(args.crf),
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
    ]
    if args.max_duration is not None:
        command.extend(["-t", str(args.max_duration)])
    command.append(str(args.output))

    print(f"Procesando: {args.input} -> {args.output}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as error:
        print(f"Error: FFmpeg terminó con código {error.returncode}.", file=sys.stderr)
        return error.returncode or 1
    print("Video creado correctamente.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
