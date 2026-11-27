#!/usr/bin/env python
"""Script para iniciar el servidor API REST."""

import argparse
from auditoria.api import create_app


def main():
    parser = argparse.ArgumentParser(
        description="Inicia servidor API REST de Auditoría"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help=(
            "Host en el que escuchar (default: 127.0.0.1). La API no tiene "
            "autenticación: usar 0.0.0.0 la expone a toda la red."
        ),
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Puerto en el que escuchar (default: 5000)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Modo debug activado",
    )
    parser.add_argument(
        "--db-path",
        default="auditoria.db",
        help="Ruta de la base de datos",
    )
    parser.add_argument(
        "--webhooks-path",
        default="webhooks.json",
        help="Ruta del archivo de webhooks",
    )

    args = parser.parse_args()

    app = create_app(
        db_path=args.db_path,
        webhooks_path=args.webhooks_path,
    )

    print(f"🚀 Servidor API iniciado en http://{args.host}:{args.port}")
    print(f"📊 Documentación: API.md")
    print(f"💾 Base de datos: {args.db_path}")
    print(f"🔗 Webhooks: {args.webhooks_path}")

    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug,
    )


if __name__ == "__main__":
    main()
