"""
author: Luis Manuel Torres Trevino
description: Este archivo es el principal para la aplicacion flask
"""
from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
