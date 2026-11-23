#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
printf '\n=== Servicios ===\n'
docker compose ps
printf '\n=== Identidad directa de cada backend ===\n'
for app in app1 app2 app3; do
  echo "$app"
  docker compose exec -T "$app" python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:5000/health',timeout=3).read().decode())"
done
printf '\n=== 30 peticiones por Nginx ===\n'
for i in $(seq 1 30); do
  curl -fsS --max-time 10 http://localhost:8088/ | grep -o 'server [123]'
done | sort | uniq -c
printf '\n=== Cabeceras ===\n'
for i in 1 2 3 4 5 6; do
  curl -fsSI --max-time 10 http://localhost:8088/ | grep -iE 'HTTP/|x-backend:|x-upstream:'
  echo '---'
done
printf '\n=== Targets Prometheus ===\n'
curl -fsS http://localhost:9090/api/v1/targets | python3 -c 'import json,sys; d=json.load(sys.stdin); [print(t["labels"].get("job"),t["labels"].get("instance"),t["health"],t.get("lastError","")) for t in d["data"]["activeTargets"]]'
