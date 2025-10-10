#!/usr/bin/env python3
"""
Script para iniciar el backend de FastAPI
"""

import subprocess
import sys
import os
from pathlib import Path


def main():
    """Iniciar el servidor FastAPI"""
    project_root = Path(__file__).parent

    # Cambiar al directorio del proyecto
    os.chdir(project_root)

    print("🚀 Iniciando backend FastAPI...")
    print("📍 URL: http://localhost:8000")
    print("📚 Documentación: http://localhost:8000/docs")
    print("🔄 Modo desarrollo activado (auto-reload)")
    print("=" * 50)

    try:
        # Ejecutar uvicorn con auto-reload
        subprocess.run(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "backend.main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
                "--reload",
            ],
            check=True,
        )
    except KeyboardInterrupt:
        print("\n👋 Backend detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error iniciando el backend: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
