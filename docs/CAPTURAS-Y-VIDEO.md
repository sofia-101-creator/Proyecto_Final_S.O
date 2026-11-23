# Capturas y entrega

Guardar capturas con el codigo E01, E02, etc. en evidencias/ y pegarlas en el informe. Capturar comando y salida sin recortar errores relevantes; mostrar fecha/hora cuando sea posible. Nunca mostrar .env ni la clave Grafana.

| Codigo | Momento exacto | Contenido | Texto orientativo (adaptar a lo observado) |
|---|---|---|---|
| E01 | Antes de crear contenedores | docker --version, docker compose version, k6 version, fecha | Se verificaron las herramientas del host. |
| E02 | Tras extraer el proyecto | tree -a -I .git | Estructura separada del laboratorio anterior. |
| E03 | Antes del build | app.py y Dockerfile en editor, dos capturas si hace falta | Backend instrumentado con identidad y metricas. |
| E04 | Antes del despliegue | Compose, prometheus.yml y nginx.conf, capturas separadas | Servicios, targets y red definidos como codigo. |
| E05 | Tras estabilizar arranque | docker compose ps con ocho servicios | Registrar estados reales; solo cuatro servicios tienen healthcheck. |
| E06 | Tras validar Nginx | nginx -t y upstream con tres backends | Configuracion valida y backends de igual peso. |
| E07 | Antes de generar carga | Tres vistas del navegador con server 1, 2 y 3 | Tres instancias identificables a traves del mismo proxy. |
| E08 | Sin navegador refrescando | Conteo de 30 peticiones, seis cabeceras y logs | Indicar conteos reales y destinos X-Upstream. |
| E09 | Tras al menos 30 segundos | /targets y consulta nginx_up | Seis targets UP y exportador leyendo Nginx. |
| E10 | Antes de pruebas | Consultas CPU, memoria, red y disco en Prometheus, varias capturas | cAdvisor expone recursos; anotar ausencias sin ocultarlas. |
| E11 | Al abrir Grafana | Dashboard con fuente aprovisionada | Dashboard disponible sin creacion manual. |
| E12 | Al terminar prueba normal | Resumen k6 completo | Registrar p95, p99, tasa y errores reales. |
| E13 | Durante normal, etapa 20-40 usuarios | Dashboard recursos y latencia | Comportamiento bajo carga normal. |
| E14 | Al terminar prueba slow | Resumen k6 completo | Registrar datos incluso si fallan umbrales. |
| E15 | Durante slow, etapa 20-40 usuarios | Dashboard recursos y latencia | Comparar con escenario normal. |
| E16 | Tras reiniciar Prometheus y Grafana | Grafana mostrando historial previo y dashboard | Volumenes conservan datos tras reinicio. |
| E17 | Tras push a GitHub | Repo con README renderizado y archivos | Codigo y documentacion disponibles, sin secretos. |

# Video: guion de 9 minutos (maximo permitido: 10)
- 0:00-1:00: integrantes, objetivo y entorno.
- 1:00-2:00: arquitectura y Compose.
- 2:00-3:00: backend, Dockerfile y /metrics.
- 3:00-4:00: balanceo real, conteo y cabeceras.
- 4:00-5:00: seis targets y nginx_up.
- 5:00-6:30: dashboard CPU, memoria, red, disco, latencia y tasa.
- 6:30-8:00: resultados k6 normal y slow; mostrar resumenes guardados.
- 8:00-9:00: conclusiones, limitaciones, GitHub y README.

Cada integrante debe aparecer visible al menos un minuto. Si hay muchos integrantes, pueden aparecer simultaneamente con sus camaras. No es obligatorio ejecutar dos pruebas completas en vivo dentro del video: mostrar archivos y evidencia reales previamente obtenidos. Comprobar audio y que las terminales se lean.

# Entrega individual
Cada integrante entrega: informe PDF con todos los nombres, enlace GitHub y enlace del video. Probar los enlaces en ventana privada y conceder acceso al docente cuando corresponda. No limpiar volumenes hasta tener PDF, capturas, repositorio y video verificados.
