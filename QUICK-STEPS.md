Obtener IVA trasladado del último mes
Abrir Swagger:
http://<servidor>:8000/docs
Solicitar descarga de CFDI:
POST /downloads

Datos:

certificate_id = <id certificado>
password = <contraseña>
direction = received
start_date = YYYY-MM-01
end_date = YYYY-MM-30/31

Guardar el download_id y request_id de la respuesta.

Esperar que SAT termine:
GET /downloads/{download_id}/status

Continuar cuando:

EstadoSolicitud = 3

y aparezca:

IdsPaquetes
Descargar el paquete ZIP del SAT.
Procesar XML:
POST /downloads/{download_id}/process

Ejemplo:

POST /downloads/2/process

Debe responder:

documents: N
Obtener IVA trasladado:

Opción tabla para Excel:

GET /downloads/{download_id}/summary/tsv

Copiar resultado y pegar en Excel.

La última línea muestra:

TOTAL        IVA

Ese es el IVA trasladado del periodo.
