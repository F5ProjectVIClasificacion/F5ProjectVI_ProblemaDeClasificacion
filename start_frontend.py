#!/usr/bin/env python3
"""
Script para iniciar el frontend de Streamlit
"""

import subprocess
import sys
import os
from pathlib import Path


def main():
    """Iniciar el servidor Streamlit"""
    project_root = Path(__file__).parent

    # Cambiar al directorio del proyecto
    os.chdir(project_root)

    print("🎨 Iniciando frontend Streamlit...")
    print("📍 URL: http://localhost:8501")
    print("🔄 Modo desarrollo activado")
    print("=" * 50)

    try:
        # Ejecutar streamlit
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "frontend/app.py",
                "--server.port",
                "8501",
                "--server.address",
                "0.0.0.0",
            ],
            check=True,
        )
    except KeyboardInterrupt:
        print("\n👋 Frontend detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error iniciando el frontend: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
