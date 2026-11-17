from pathlib import Path

from dotenv import load_dotenv

# O Neon grava as conexões em .env.local. Variáveis do servidor têm prioridade.
load_dotenv(Path(__file__).resolve().parent / ".env.local")
load_dotenv(Path(__file__).resolve().parent / ".env")

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
