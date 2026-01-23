# Automatización de Subida de Reels a Instagram

Este script automatiza la subida de Reels a Instagram usando la biblioteca `instagrapi`.

## 📍 Ubicación del Script

El script está ubicado en: `_doctools/upload_instagram_reel.py`

## 🔐 Dónde se Almacenan las Credenciales y Sesiones

### Archivo de Sesión (insta_session.json)

Después del primer inicio de sesión exitoso, el script crea un archivo de sesión:

- **Ubicación predeterminada**: `insta_session.json` en el directorio actual
- **Contenido**: Tokens de autenticación, cookies, información del dispositivo
- **Propósito**: Evitar tener que iniciar sesión en cada ejecución

**⚠️ Importante:**
- Este archivo contiene información sensible
- **NO** lo subas a GitHub o sistemas de control de versiones
- Añádelo a tu `.gitignore`
- Protege el archivo con permisos restrictivos: `chmod 600 insta_session.json`

### Variables de Entorno (Recomendado)

Las credenciales pueden almacenarse de forma segura en variables de entorno:

```bash
export IG_USERNAME="tu_usuario_instagram"
export IG_PASSWORD="tu_contraseña"
export IG_CAPTION="¡Contenido creado con IA! 🚀"
export IG_SESSION_FILE="ruta/personalizada/session.json"
```

Para hacerlas permanentes, agrégalas a tu archivo de perfil de shell:
- Bash: `~/.bashrc` o `~/.bash_profile`
- Zsh: `~/.zshrc`

## 📊 Cómo Ver Tu Contenido Diario

### 1. Ver Contenido Subido

Después de cada subida exitosa, puedes ver tu contenido:

- **App de Instagram**: Abre Instagram → Tu perfil → Pestaña de Reels
- **Navegador Web**: Visita `https://www.instagram.com/TU_USUARIO/`
- **Revisar Logs**: El script registra cada subida con fecha, hora y ID del Reel

### 2. Sistema de Logs Diarios

El script muestra logs como:

```
2026-01-23 10:30:15 INFO: Sesión cargada desde insta_session.json
2026-01-23 10:30:16 INFO: Sesión válida para mi_cuenta
2026-01-23 10:30:16 INFO: Subiendo Reel...
2026-01-23 10:32:45 INFO: ¡Éxito! Reel publicado. ID: 1234567890123456789
```

**Guardar logs en archivos para revisión diaria:**

```bash
python _doctools/upload_instagram_reel.py --video mi_video.mp4 2>&1 | tee logs/subida_$(date +%Y%m%d).txt
```

### 3. Script de Seguimiento Diario

Crea un script para facilitar el seguimiento:

```bash
#!/bin/bash
# subida_diaria.sh

FECHA=$(date +%Y-%m-%d)
DIR_LOGS="./logs_instagram"
mkdir -p $DIR_LOGS

echo "=== Subida de contenido para $FECHA ===" | tee -a "$DIR_LOGS/registro_$FECHA.log"

python _doctools/upload_instagram_reel.py \
  --video "$1" \
  --caption "Contenido diario $FECHA 🎬 #ContenidoDiario #IA" \
  2>&1 | tee -a "$DIR_LOGS/registro_$FECHA.log"

echo "✅ Log guardado en: $DIR_LOGS/registro_$FECHA.log"
```

Uso:
```bash
chmod +x subida_diaria.sh
./subida_diaria.sh videos/mi_reel.mp4
```

### 4. Ver Registro de Todas las Subidas

Para revisar todas tus subidas anteriores:

```bash
# Ver todos los logs
ls -lt logs_instagram/

# Ver el contenido del log más reciente
cat logs_instagram/$(ls -t logs_instagram/ | head -1)

# Buscar todas las subidas exitosas
grep "¡Éxito!" logs_instagram/*.log
```

## 🚀 Uso Rápido

### Instalación

```bash
pip install instagrapi
```

### Subida Simple

```bash
python _doctools/upload_instagram_reel.py \
  --username mi_usuario \
  --video videos/mi_reel.mp4
```

### Con Variables de Entorno (Más Seguro)

```bash
export IG_USERNAME="mi_usuario"
export IG_PASSWORD="mi_contraseña"

python _doctools/upload_instagram_reel.py --video videos/mi_reel.mp4
```

### Con Portada Personalizada

```bash
python _doctools/upload_instagram_reel.py \
  --video mi_reel.mp4 \
  --thumbnail portada.jpg \
  --caption "¡Nuevo contenido! 🎥 #Reel"
```

## 📋 Opciones Disponibles

- `--username` / `-u`: Usuario de Instagram (o usa `IG_USERNAME`)
- `--password` / `-p`: Contraseña (o usa `IG_PASSWORD`)
- `--video` / `-v`: Ruta al video (.mp4) - **Obligatorio**
- `--thumbnail` / `-t`: Imagen de portada (.jpg/.png) - Opcional
- `--caption` / `-c`: Texto del caption (o usa `IG_CAPTION`)
- `--session-file` / `-s`: Ruta al archivo de sesión

## 🔒 Seguridad

1. **Nunca** incluyas credenciales directamente en el código
2. Usa variables de entorno para las credenciales
3. Protege tu archivo de sesión: `chmod 600 insta_session.json`
4. Añade archivos de sesión a `.gitignore`:
   ```
   insta_session.json
   *.session.json
   logs_instagram/
   ```

## 📖 Documentación Completa

Para documentación completa en inglés, consulta:
`docs/code/cookbook/instagram-automation.md`

## 🔧 Integración con n8n

Este script puede integrarse con workflows de n8n para automatización completa:

1. Usa el nodo **Execute Command** para ejecutar el script
2. Programa subidas con el nodo **Cron**
3. Almacena credenciales en el sistema de credenciales de n8n
4. Encadena con otros nodos para flujos de trabajo completos

Ejemplo de flujo:
```
Cron → Generar Video con IA → Subir a Instagram → Notificación
```

## ❓ Solución de Problemas

### Error "Bad Password"
- Verifica usuario y contraseña
- Aprueba el inicio de sesión desde la app de Instagram

### Error "Challenge Required"
- Instagram requiere verificación adicional
- Inicia sesión desde la app primero
- Completa verificaciones de seguridad pendientes

### Sesión Expirada
- Elimina el archivo `insta_session.json`
- Ejecuta el script nuevamente para crear una nueva sesión

## 📞 Soporte

Para más información sobre n8n y automatización de workflows:
- [Documentación de n8n](https://docs.n8n.io/)
- [Comunidad de n8n](https://community.n8n.io/)
