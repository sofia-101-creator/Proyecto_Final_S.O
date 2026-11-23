# Proyecto final: infraestructura Docker con proxy inverso y observabilidad

Universidad Autonoma de Occidente  
Asignatura: [Completar]  
Docente: [Completar]  
Integrantes: [Nombres completos de todos]  
Fecha: [Fecha real]  
Entorno: [Windows + Ubuntu WSL2 + Docker Desktop / Linux nativo]  
Repositorio: [URL real]  
Video: [URL real]

> Plantilla: reemplazar campos y pegar capturas reales. Las frases de resultados son orientaciones, no resultados ya obtenidos.

## 1. Introduccion
El proyecto implementa una infraestructura de aplicaciones web contenerizada para estudiar el balanceo de carga y la observabilidad. Se integran tres backends identificables, Nginx, Prometheus, Nginx Prometheus Exporter, cAdvisor y Grafana. Las pruebas de carga se ejecutan desde el host y permiten contrastar la latencia, la tasa de solicitudes y el uso de recursos.

## 2. Objetivos
### General
Implementar y evaluar una infraestructura Docker con balanceo entre tres backends y monitoreo centralizado.
### Especificos
- Construir una imagen backend reproducible e instrumentada.
- Distribuir peticiones mediante Nginx.
- Recolectar metricas de aplicacion, proxy y contenedores.
- Visualizar las metricas en Grafana.
- Comparar dos escenarios de carga y documentar sus resultados reales.

## 3. Entorno de trabajo
Versiones reales de sistema, Docker, Compose y k6: [Completar]. Recursos asignados a Docker y especificaciones del equipo: [Completar].
[E01: versiones] [E02: estructura]

## 4. Arquitectura
El trafico del host ingresa por Nginx en el puerto 8088. Nginx reenvia a app1, app2 y app3 por su puerto interno 5000. Prometheus consulta directamente sus endpoints /metrics, consulta Nginx a traves del exportador y recolecta los recursos expuestos por cAdvisor. Grafana utiliza Prometheus como fuente. Los ocho servicios comparten una red bridge personalizada. Prometheus y Grafana conservan sus datos en volumenes nombrados.
[Insertar diagrama de arquitectura]

## 5. Implementacion y decisiones
### Backend y Dockerfile
La imagen parte de Python 3.12 slim, instala Flask, Gunicorn y prometheus-client, copia la aplicacion y la ejecuta con un usuario no privilegiado. Cada contenedor recibe SERVER_NAME. Se usa un proceso con ocho hilos para compartir correctamente el registro de metricas en ese proceso. Se excluyen /health y /metrics del conteo de usuarios. La ruta principal espera 30 ms y /slow simula 500 ms sin carga intensiva de CPU.
[E03: backend y Dockerfile]
### Compose
Explicar build, environment, healthcheck, depends_on, networks, ports, volumes y labels con ejemplos del archivo entregado. No afirmar que todos los servicios tienen healthcheck: solo backends y Nginx lo incluyen en esta configuracion.
[E04: servicios y red] [E05: estado de despliegue]
### Nginx
El upstream declara tres backends de igual peso; la zona compartida conserva el estado entre workers. Se agregan cabeceras para identificar el destino y reenviar la IP del cliente. stub_status se publica solo internamente en el puerto 8081. La ruta publica /metrics queda bloqueada.
[E06: configuracion y prueba nginx -t]
### Prometheus y exportadores
Se recolectan seis targets cada cinco segundos: tres backends, Nginx exporter, cAdvisor y Prometheus. El exportador convierte stub_status en metricas Prometheus; no proporciona por si solo latencias HTTP. cAdvisor requiere privilegios y acceso al host Docker para leer recursos.
[E09: targets y nginx_up] [E10: metricas cAdvisor]
### Grafana y persistencia
La fuente Prometheus y el dashboard se aprovisionan desde YAML y JSON versionados. Prometheus y Grafana usan volumenes nombrados.
[E11: dashboard] [E16: persistencia]

## 6. Validacion funcional
### Identidad y balanceo
Conteo real de 30 solicitudes: server 1 [ ], server 2 [ ], server 3 [ ].
Las cabeceras X-Backend y X-Upstream [describir lo observado]. No confundir request.remote_addr (IP del proxy vista por Flask) con la IP propia del backend.
[E07: navegador con tres identidades] [E08: conteo, cabeceras y logs]

## 7. Metricas y dashboards
- Counter: respuestas HTTP de la aplicacion por instancia, metodo, ruta y estado.
- Histogram: distribucion de duraciones del backend, usada para estimar p95.
- Nginx: solicitudes globales y conexiones activas.
- cAdvisor: CPU, memoria working set, red y disco por contenedor/servicio.
- up: resultado del scrape; nginx_up: acceso del exportador a Nginx.
CPU se presenta como porcentaje de un nucleo. La latencia Flask no incluye toda la experiencia del cliente. Las metricas ausentes no equivalen a cero. Documentar las series de disco realmente disponibles y cualquier limitacion del entorno.

## 8. Pruebas de carga
Se utilizo k6 desde [Ubuntu WSL en el host / Windows / Linux]. Se aplicaron etapas de 30 s hacia 5 usuarios, 60 s hacia 20, 60 s hacia 40 y 30 s hacia cero. Se compararon / y /slow?ms=500 con los mismos parametros. Es una prueba de concurrencia, no de tasa fija de llegada. Cada usuario espera 100 ms entre iteraciones.

| Indicador | Normal | Slow |
|---|---|---|
| Peticiones totales | [ ] | [ ] |
| Peticiones/s | [ ] | [ ] |
| p95 cliente, ms | [ ] | [ ] |
| p99 cliente, ms | [ ] | [ ] |
| Fallos HTTP, % | [ ] | [ ] |
| Checks fallidos | [ ] | [ ] |
| CPU observada y servicio | [ ] | [ ] |
| Memoria observada y servicio | [ ] | [ ] |
| Resultado de umbrales | [ ] | [ ] |

[E12: k6 normal] [E13: dashboard durante normal] [E14: k6 slow] [E15: dashboard durante slow]

### Analisis
El p95 cambio de [ ] a [ ] ms. La tasa cambio de [ ] a [ ] solicitudes/s. Los errores [aumentaron/no aumentaron, con datos]. El servicio de mayor consumo fue [ ] segun [panel/captura]. Con tres backends de ocho hilos y una espera de 0,5 s, el limite idealizado es 24/0,5 = 48 solicitudes/s; el valor real incorpora costes adicionales. La carga lenta simula espera, por lo que una CPU baja no descarta colas ni saturacion. Si no hubo saturacion, indicarlo expresamente: no se alcanzo un punto de quiebre en el rango probado.

## 9. Problemas y soluciones
| Problema real | Evidencia/diagnostico | Cambio realizado | Verificacion |
|---|---|---|---|
| [Completar solo lo ocurrido] | [ ] | [ ] | [ ] |

## 10. Seguridad y limitaciones
Puertos publicados solo en loopback; credenciales locales fuera de Git; backends sin root. cAdvisor es privilegiado, por lo que no debe tratarse como una configuracion endurecida de produccion. No se configura TLS ni redundancia de Nginx. En Docker Desktop, las metricas describen los contenedores y su entorno Linux virtualizado, no todo Windows. Describir cualquier metrica no disponible y su causa investigada. Recomendaciones: HTTPS, secretos gestionados, actualizacion de dependencias, backups, revision de privilegios y redundancia del proxy.

## 11. Conclusiones
Redactar con evidencia:
1. Se verifico el balanceo entre [ ] instancias mediante [conteos y cabeceras].
2. Prometheus recolecto [ ] targets y Grafana permitio observar [ ].
3. El escenario lento produjo [comparacion numerica real].
4. La limitacion principal observada fue [ ].

## 12. Reproducibilidad y anexos
Incluir enlace GitHub, comandos de inicio/parada, URLs, tablas de metricas, capturas E01-E17 y enlace del video. El README contiene los pasos de ejecucion. No adjuntar contrasenas ni .env.

## 13. Fuentes tecnicas
Consultar documentacion oficial de Docker Compose, Nginx Prometheus Exporter, Prometheus, prometheus-client para Python, cAdvisor, Grafana provisioning y k6. Registrar las URL y fechas reales de consulta usadas por el grupo.
