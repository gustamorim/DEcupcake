"""Confere os assets públicos antes do deploy, sem conectar ao banco."""
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    for name in ("css/style.css", "css/shop.css", "js/main.js"):
        path = root / "public" / "static" / name
        if not path.is_file():
            raise RuntimeError(f"Arquivo público ausente: {name}")
    print("CSS e JavaScript conferidos em public/static/.")


if __name__ == "__main__":
    main()
