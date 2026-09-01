#!/usr/bin/env python3
"""
Sube un Reel a Instagram usando instagrapi.

Mejoras incluidas:
- Uso de variables de entorno o entrada segura para credenciales
- Guardado/recuperación de sesión para evitar re-login frecuente
- Soporte básico para 2FA
- Parámetros CLI: video, thumbnail (opcional), caption
- Logs y manejo de errores más robusto
"""

import os
import argparse
import logging
import sys
from getpass import getpass
from instagrapi import Client
from instagrapi.exceptions import TwoFactorRequired, BadPassword, ChallengeRequired

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

SESSION_FILE = os.environ.get("IG_SESSION_FILE", "insta_session.json")

def two_factor_handler(username):
    code = input("Introduce el código 2FA recibido: ").strip()
    return code

def load_session(cl, session_file):
    if os.path.exists(session_file):
        try:
            cl.load_settings(session_file)
            logger.info("Sesión cargada desde %s", session_file)
            return True
        except Exception as e:
            logger.warning("No se pudo cargar la sesión: %s", e)
    return False

def save_session(cl, session_file):
    try:
        cl.dump_settings(session_file)
        logger.info("Sesión guardada en %s", session_file)
    except Exception as e:
        logger.warning("Error al guardar la sesión: %s", e)

def login_client(username, password, session_file):
    cl = Client()
    cl.two_factor_handler = lambda: two_factor_handler(username)

    # Intentar cargar sesión previa
    if load_session(cl, session_file):
        try:
            # Verificar que la sesión funciona solicitando info del usuario
            cl.user_info_by_username(username)
            logger.info("Sesión válida para %s", username)
            return cl
        except Exception:
            logger.info("La sesión cargada no es válida, intentando login con credenciales...")

    try:
        logger.info("Iniciando sesión como %s", username)
        cl.login(username, password)
        save_session(cl, session_file)
        return cl
    except TwoFactorRequired:
        logger.error("Se requiere 2FA.")
        code = two_factor_handler(username)
        cl.two_factor_login(code)
        save_session(cl, session_file)
        return cl
    except BadPassword:
        logger.error("Contraseña incorrecta.")
        raise
    except ChallengeRequired as e:
        logger.error("Se requiere resolver un challenge/ verificación adicional: %s", e)
        raise
    except Exception as e:
        logger.error("Error al iniciar sesión: %s", e)
        raise

def upload_reel(cl, video_path, caption, thumbnail_path=None):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video no encontrado: {video_path}")

    if thumbnail_path and not os.path.exists(thumbnail_path):
        logger.warning("Portada no encontrada, se ignorará thumbnail: %s", thumbnail_path)
        thumbnail_path = None

    logger.info("Subiendo Reel... (esto puede tardar dependiendo del tamaño)")
    try:
        reel = cl.clip_upload(
            video_path,
            caption=caption,
            thumbnail=thumbnail_path
        )
        logger.info("¡Éxito! Reel publicado. ID: %s", getattr(reel, "pk", "unknown"))
        return reel
    except Exception as e:
        logger.error("Error subiendo el Reel: %s", e)
        raise

def parse_args():
    p = argparse.ArgumentParser(description="Subir un Reel a Instagram con instagrapi")
    p.add_argument("--username", "-u", default=os.environ.get("IG_USERNAME"), help="Usuario de Instagram (o IG_USERNAME env)")
    p.add_argument("--password", "-p", help="Contraseña de Instagram (recomendado usar IG_PASSWORD env)")
    p.add_argument("--video", "-v", required=True, help="Ruta al archivo de video (.mp4)")
    p.add_argument("--thumbnail", "-t", help="Ruta al archivo de portada (.jpg/.png) (opcional)")
    p.add_argument("--caption", "-c", default=os.environ.get("IG_CAPTION", "¡Contenido creado con mi IA! 🚀 #IA #Automation #ContentCreation"), help="Texto del caption")
    p.add_argument("--session-file", "-s", default=SESSION_FILE, help="Archivo para guardar la sesión")
    return p.parse_args()

def main():
    args = parse_args()

    username = args.username
    password = args.password or os.environ.get("IG_PASSWORD")

    if not username:
        logger.error("Usuario no proporcionado. Usa --username o la variable IG_USERNAME.")
        sys.exit(1)
    if not password:
        # usar getpass si no hay password en env ni en argumento
        password = getpass(f"Contraseña para {username}: ")

    try:
        cl = login_client(username, password, args.session_file)
        upload_reel(cl, args.video, args.caption, args.thumbnail)
    except Exception as e:
        logger.error("Proceso finalizado con errores: %s", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
