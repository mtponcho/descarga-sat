1. Descripción general

El sistema permite:

Autenticarse con un certificado digital del SAT (.cer y .key).
Solicitar descarga masiva de CFDI.
Descargar paquetes generados por el SAT.
Procesar archivos XML.
Extraer información principal de las facturas.
Consultar totales e IVA trasladado.
Obtener una tabla copiable para Excel.
2. Requisitos
Usuario

Debe contar con:

Certificado digital SAT:
Archivo .cer
Archivo .key
Contraseña de la llave privada.
RFC asociado al certificado.
3. Acceso al sistema

El sistema está disponible mediante API REST.

Documentación interactiva:

http://<servidor>:8000/docs

Ejemplo:

http://192.168.100.183:8000/docs
4. Flujo de trabajo

El proceso completo consta de cuatro etapas:

1. Solicitar descarga
        |
        v
2. Esperar procesamiento SAT
        |
        v
3. Descargar paquete ZIP
        |
        v
4. Procesar XML y consultar resultados
5. Solicitar descarga de CFDI

Endpoint:

POST /downloads

Parámetros:

Campo	Descripción
certificate_id	Identificador del certificado cargado
password	Contraseña del certificado
direction	Tipo de CFDI
start_date	Fecha inicial
end_date	Fecha final

Valores de direction:

Valor	Descripción
received	CFDI recibidos
emitted	CFDI emitidos

Ejemplo:

direction=received
start_date=2026-06-01
end_date=2026-06-30

Respuesta exitosa:

{
  "request_id": "0a29893c-ecba-4c9e-a9f1-e24d1f60a67f",
  "sat_response": {
    "CodEstatus": "5000",
    "Mensaje": "Solicitud Aceptada"
  }
}
6. Consultar estado de descarga

Endpoint:

GET /downloads/{id}/status

Ejemplo:

GET /downloads/2/status

Estados posibles:

Estado	Descripción
0	Solicitud pendiente
1	En proceso
3	Disponible

Cuando el SAT termina:

Ejemplo:

{
 "EstadoSolicitud":3,
 "NumeroCFDIs":7,
 "IdsPaquetes":[
   "0A29893C-ECBA-4C9E-A9F1-E24D1F60A67F_01"
 ]
}
7. Descargar paquete SAT

El sistema descarga el paquete ZIP generado por el SAT.

Contenido:

paquete.zip

 ├── factura1.xml
 ├── factura2.xml
 ├── factura3.xml
 ...

Cada XML contiene un CFDI individual.

8. Procesar CFDI

Endpoint:

POST /downloads/{id}/process

Ejemplo:

POST /downloads/2/process

Resultado:

{
 "packages":1,
 "documents":7
}

Significado:

Campo	Descripción
packages	Paquetes procesados
documents	CFDI encontrados
9. Consulta resumen CFDI

Endpoint:

GET /downloads/{id}/summary

Ejemplo:

GET /downloads/2/summary

Respuesta:

{
 "documents":7,
 "total":6769.30,
 "iva":920.98,
 "rows":[
   {
    "fecha":"2026-06-22",
    "rfc":"SCO990422SV5",
    "uuid":"...",
    "total":896.72,
    "iva":120.64
   }
 ]
}

Campos:

Campo	Descripción
fecha	Fecha emisión CFDI
rfc	RFC del emisor
uuid	Folio fiscal SAT
total	Total factura
iva	IVA trasladado
10. Exportar tabla para Excel

Endpoint:

GET /downloads/{id}/summary/tsv

Ejemplo:

GET /downloads/2/summary/tsv

Salida:

Fecha	RFC	Total	IVA
2026-06-22	SCO990422SV5	896.72	120.64
2026-06-25	CAR1509021B4	500.12	67.20
2026-06-24	VEHE9706213V6	914.49	126.14

TOTAL		6769.30	920.98

Uso:

Seleccionar todo el contenido.
Copiar.
Pegar en Excel o LibreOffice Calc.
11. Información almacenada

El sistema almacena:

Solicitudes

Tabla:

download_requests

Contiene:

Solicitud SAT
Dirección
Estado
Paquetes SAT

Tabla:

download_packages

Contiene:

Id paquete SAT
Archivo ZIP
Relación con solicitud
CFDI

Tabla:

cfdi_documents

Contiene:

UUID
RFC emisor
Fecha
Total
IVA trasladado
Ruta XML
12. Limitaciones actuales

Versión 1.0:

No genera PDF.
No genera reportes fiscales.
No procesa cancelaciones.
No tiene autenticación de usuarios.
No tiene interfaz gráfica.
13. Próximas mejoras

Versión futura:

Generación PDF por CFDI.
Exportación Excel.
Dashboard mensual.
Filtros por RFC.
Búsqueda por UUID.
Reportes de IVA acreditable.
Gestión multi-RFC.
