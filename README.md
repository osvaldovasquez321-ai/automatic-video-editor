# Editor automático de videos

Script sencillo y eficiente basado en FFmpeg para preparar videos verticales para TikTok, YouTube Shorts, Instagram Reels y otras plataformas.

## Requisitos

- Python 3.9 o superior
- FFmpeg instalado y disponible en el `PATH`

Comprueba la instalación:

```bash
python --version
ffmpeg -version
```

## Uso rápido

```bash
python video_editor.py entrada.mp4 -o salida.mp4
```

Ejemplo con duración máxima, relación vertical y calidad personalizada:

```bash
python video_editor.py entrada.mp4 -o short.mp4 --max-duration 60 --width 1080 --height 1920 --crf 23
```

El script:

- Recorta el video al centro para adaptarlo al formato vertical 9:16.
- Conserva el audio y lo convierte a AAC compatible.
- Usa codificación H.264 compatible con la mayoría de plataformas.
- Evita sobrescribir archivos accidentalmente, salvo que se use `--overwrite`.
- Procesa el archivo directamente sin crear archivos temporales.

## Opciones

```text
-o, --output       Archivo de salida (obligatorio)
--max-duration     Duración máxima en segundos
--width            Ancho de salida (por defecto: 1080)
--height           Alto de salida (por defecto: 1920)
--crf              Calidad H.264, menor número significa mayor calidad (por defecto: 23)
--preset           Velocidad de codificación: ultrafast, fast, medium, slow (por defecto: medium)
--overwrite        Permite reemplazar el archivo de salida
```

## Notas

El archivo original no se modifica. Para obtener mejores resultados, usa videos con buena resolución y audio claro. El recorte se realiza desde el centro; una versión futura puede añadir detección automática de rostros.
