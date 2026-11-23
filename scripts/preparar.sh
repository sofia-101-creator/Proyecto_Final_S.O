#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p evidencias resultados
python3 - <<'PY'
from pathlib import Path
import secrets
p = Path('.env')
if not p.exists():
    p.write_text('GRAFANA_ADMIN_PASSWORD=' + secrets.token_urlsafe(24) + '\n')
    p.chmod(0o600)
    print('Archivo .env creado. Consulta la clave solo en privado.')
else:
    print('.env ya existe; no se cambia la clave.')
PY
printf '\nValidando Compose...\n'
docker compose config -q
