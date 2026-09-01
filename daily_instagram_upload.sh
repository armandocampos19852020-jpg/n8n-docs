#!/bin/bash
# Script de ejemplo para subida diaria de Reels a Instagram
# Usage: ./daily_instagram_upload.sh path/to/video.mp4

set -e

# Configuración
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="./logs_instagram"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Crear directorio de logs si no existe
mkdir -p "$LOG_DIR"

# Verificar que se proporcionó un video
if [ -z "$1" ]; then
    echo "❌ Error: Debes proporcionar la ruta al video"
    echo "Uso: $0 path/to/video.mp4 [thumbnail.jpg] [caption]"
    exit 1
fi

VIDEO_PATH="$1"
THUMBNAIL_PATH="${2:-}"
CAPTION="${3:-Contenido diario para $DATE 🎬 #ContenidoDiario #IA #Automation}"

# Verificar que el video existe
if [ ! -f "$VIDEO_PATH" ]; then
    echo "❌ Error: El video no existe: $VIDEO_PATH"
    exit 1
fi

# Verificar que las variables de entorno están configuradas
if [ -z "$IG_USERNAME" ]; then
    echo "⚠️  Advertencia: IG_USERNAME no está configurado"
    echo "Configura tus credenciales con:"
    echo "  export IG_USERNAME='tu_usuario'"
    echo "  export IG_PASSWORD='tu_contraseña'"
fi

echo "=================================================="
echo "  SUBIDA DE REEL A INSTAGRAM - $DATE"
echo "=================================================="
echo "Video: $VIDEO_PATH"
echo "Thumbnail: ${THUMBNAIL_PATH:-Ninguno}"
echo "Caption: $CAPTION"
echo "=================================================="

# Ejecutar el script de Python
if [ -n "$THUMBNAIL_PATH" ] && [ -f "$THUMBNAIL_PATH" ]; then
    python "$SCRIPT_DIR/_doctools/upload_instagram_reel.py" \
        --video "$VIDEO_PATH" \
        --thumbnail "$THUMBNAIL_PATH" \
        --caption "$CAPTION" \
        2>&1 | tee "$LOG_DIR/upload_${TIMESTAMP}.log"
else
    python "$SCRIPT_DIR/_doctools/upload_instagram_reel.py" \
        --video "$VIDEO_PATH" \
        --caption "$CAPTION" \
        2>&1 | tee "$LOG_DIR/upload_${TIMESTAMP}.log"
fi

# Verificar el resultado
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo "✅ ¡Subida completada exitosamente!"
    echo "📋 Log guardado en: $LOG_DIR/upload_${TIMESTAMP}.log"
    echo "📱 Revisa tu contenido en: https://www.instagram.com/$IG_USERNAME/"
    
    # Extraer el ID del Reel del log si es posible
    REEL_ID=$(grep -oP 'ID: \K[0-9]+' "$LOG_DIR/upload_${TIMESTAMP}.log" | tail -1)
    if [ -n "$REEL_ID" ]; then
        echo "🆔 ID del Reel: $REEL_ID"
    fi
else
    echo ""
    echo "❌ Error durante la subida"
    echo "📋 Revisa el log para más detalles: $LOG_DIR/upload_${TIMESTAMP}.log"
    exit 1
fi

echo "=================================================="
