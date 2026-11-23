# Proyecto final: proxy inverso y observabilidad

## Integrantes
- [Nombre completo 1]
- [Nombre completo 2]
- [Completar todos los integrantes]

## Objetivo y arquitectura
Tres backends Flask identificables, Nginx con Round Robin, Prometheus, Nginx Prometheus Exporter, cAdvisor y Grafana: ocho contenedores en una red bridge personalizada. El cliente entra a Nginx; Prometheus recolecta cada backend directamente, el exportador de Nginx y cAdvisor. Grafana consulta a Prometheus. Los backends no publican puertos.

## Requisitos
Docker con Compose v2, contenedores Linux, Bash, Python 3, curl, Git. Para las pruebas: k6 instalado en el host (Ubuntu/WSL o Windows), no como servicio de Compose. En Docker Desktop, habilitar integracion WSL para Ubuntu. cAdvisor depende de acceso a los cgroups y al daemon Linux de Docker; validar las metricas reales antes de dar por terminado el proyecto.

## Inicio
```bash
bash scripts/preparar.sh
docker compose config -q
docker compose up -d --build
docker compose ps
bash scripts/verificar.sh
```

## Accesos locales
- Nginx: http://localhost:8088
- Prometheus: http://localhost:9090
- Targets: http://localhost:9090/targets
- Grafana: http://localhost:3000 (usuario admin, clave en .env)
- Dashboard: http://localhost:3000/d/proyecto-final
- cAdvisor: http://localhost:8089

No subir `.env` a GitHub. Preparar el archivo antes de ejecutar Compose. Para consultar la clave en privado: `grep GRAFANA_ADMIN_PASSWORD .env`. La variable de entorno inicializa la clave de Grafana solo al crear su base de datos: no cambia automaticamente una clave ya guardada.

## Rutas de la aplicacion
`/`: identidad y pausa de 30 ms; `/health`: estado; `/headers`: cabeceras; `/slow?ms=500`: pausa controlada; `/metrics`: metricas internas Prometheus. Nginx bloquea la ruta publica `/metrics`; Prometheus accede directamente a app1:5000, app2:5000 y app3:5000.

## Balanceo
```bash
for i in $(seq 1 30); do curl -fsS http://localhost:8088/ | grep -o 'server [123]'; done | sort | uniq -c
```
Con los tres backends disponibles y sin otro trafico, esperar alrededor de 10/10/10. La zona compartida de Nginx mantiene el estado del upstream entre workers. No confundir el nombre de respuesta con la IP: X-Upstream identifica el destino y /headers muestra la IP del proxy vista por Flask.

## Monitoreo
Dashboard y datasource se aprovisionan desde archivos. Deben aparecer seis targets UP: tres backends, Nginx exporter, cAdvisor y Prometheus. `up{job="nginx"}=1` prueba el scrape del exportador; `nginx_up=1` prueba que este puede leer Nginx.

Metricas propias: `backend_http_requests_total` (Counter), `backend_http_request_duration_seconds` (Histogram). Se excluyen `/metrics` y `/health` para no contabilizar el monitoreo como trafico de usuarios. Cada backend usa un proceso Gunicorn y ocho hilos para conservar un registro compartido entre hilos sin configurar el modo multiproceso de prometheus-client. No aumentar workers sin implementar ese modo.

Nginx stub_status aporta conexiones y solicitudes globales, no latencia ni desglose de codigos HTTP. La latencia proviene de Flask; la experiencia extremo a extremo proviene de k6. No son mediciones identicas.

cAdvisor proporciona CPU, memoria, red y disco. Los paneles filtran la etiqueta `monitoring_group=proyecto-final` y agrupan por servicio Compose. CPU se expresa como porcentaje de un nucleo: puede superar 100%. No interpretar No data como cero. En Docker Desktop, cAdvisor observa la VM Linux de Docker, no todos los procesos Windows. Algunas combinaciones de cgroups/storage driver no exponen todas las series de disco: comprobarlo y documentar limitaciones reales.

## Pruebas de carga desde el host
```bash
mkdir -p resultados
set -o pipefail
k6 run --summary-export resultados/normal.json tests/carga.js 2>&1 | tee resultados/normal.txt
# Esperar 60 s antes de la segunda prueba.
k6 run -e MODE=slow --summary-export resultados/slow.json tests/carga.js 2>&1 | tee resultados/slow.txt
```
Cada prueba dura unos 3 minutos y emplea etapas de 5, 20 y 40 usuarios virtuales concurrentes. No son tasas fijas de solicitudes por segundo. Umbrales: menos de 1% de errores y p95 menor de 2000 ms. Un umbral fallido es un resultado que se debe analizar, no ocultar. Registrar p95, p99, solicitudes/s, fallos y recursos de ambas pruebas. Con 3 x 8 hilos y 0,5 s de espera, el techo idealizado de /slow es aproximadamente 48 solicitudes/s, sin incluir otros costes. Este calculo no garantiza el resultado real.

## Persistencia
Prometheus y Grafana usan volumenes nombrados. `docker compose down` conserva esos volumenes. `docker compose down -v` borra datos: NO usar antes de terminar evidencias y entrega. Probar reinicio con `docker compose restart prometheus grafana`.

## Configuracion y versiones
Las imagenes tienen etiquetas explicitas; Python 3.12 y Nginx 1.28-alpine siguen actualizaciones de su linea. Guardar las versiones e image digests usados mediante `docker compose images` y `docker image inspect`. Las versiones fijadas son una base de laboratorio, no una garantia de actualizacion de seguridad para produccion.

## Seguridad y limitaciones
Puertos ligados a 127.0.0.1; metricas y backends internos; credenciales fuera del repositorio; backend sin root. cAdvisor ejecuta privilegiado y tiene acceso a informacion sensible del host Docker: usar solo en el equipo de laboratorio de confianza. La red bridge compartida no es aislamiento de alta seguridad. No se implementa TLS ni alta disponibilidad del proxy. Para produccion: actualizar versiones, aplicar parches, TLS, autenticacion, secretos gestionados, backups y revisar privilegios.

## Diagnostico
```bash
docker compose logs --tail 50 app1 app2 app3 nginx nginx-exporter prometheus grafana cadvisor
docker compose exec nginx nginx -t
docker compose exec nginx nginx -T
docker compose exec prometheus promtool check config /etc/prometheus/prometheus.yml
```
Si falta reparto, contrastar identidad directa con `bash scripts/verificar.sh`, cabeceras X-Upstream y logs. No afirmar que pesos 3:1 explican por si solos un resultado 20:0. Tras recrear backends, validar y recargar Nginx para renovar resolucion DNS: `docker compose exec nginx nginx -t && docker compose exec nginx nginx -s reload`.

## Detener sin borrar datos
```bash
docker compose down
```

## Resultados, informe y video
Completar `docs/INFORME-PLANTILLA.md` con resultados reales. Exportar el informe final a PDF con todos los integrantes. Video de maximo 10 minutos, cada integrante visible al menos un minuto. Cada integrante entrega PDF, enlace GitHub y enlace del video.
