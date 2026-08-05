# Descarga SAT CFDI

Aplicación para descargar, procesar y consultar comprobantes fiscales digitales (CFDI) obtenidos desde el SAT.

El objetivo del proyecto es automatizar la recuperación de CFDI, almacenar los paquetes descargados, extraer los XML contenidos y permitir consultas resumidas de los documentos recibidos.

---

# Funcionalidades actuales

## Descargas SAT

La aplicación permite:

- Crear solicitudes de descarga de CFDI al SAT.
- Consultar el estado de solicitudes.
- Descargar paquetes ZIP generados por el SAT.
- Almacenar localmente los paquetes descargados.
- Asociar solicitudes con paquetes descargados.

---

## Procesamiento CFDI

La aplicación procesa los paquetes descargados y realiza:

- Extracción automática de archivos XML contenidos en ZIP.
- Lectura del UUID desde el nodo `TimbreFiscalDigital`.
- Almacenamiento físico de XML individuales.

Información extraída de cada CFDI:

- UUID
- RFC emisor
- Fecha de emisión
- Total del comprobante
- IVA trasladado
- Ruta del archivo XML

Características:

- Evita documentos duplicados utilizando el UUID como identificador único.
- Mantiene la relación entre paquetes descargados y CFDI procesados.
- Permite que un CFDI exista en múltiples paquetes sin duplicar información.

---

# Consultas CFDI

Permite consultar documentos asociados a una descarga.

Información disponible:

- Número de CFDI procesados.
- Total acumulado.
- IVA acumulado.
- Detalle individual de cada comprobante.

Formatos disponibles:

- JSON
- TSV compatible con Excel

---

# Arquitectura actual

```
Cliente / Swagger UI
        |
        |
      FastAPI
        |
        +----------------+
        |                |
 SAT Download      CFDI Processing
 Service           Service
        |                |
        |                |
        +-------+--------+
                |
            PostgreSQL
                |
        +-------+-------+
        |               |
     Database        Storage
                        |
              +---------+---------+
              |                   |
            ZIP SAT             XML
```

---

# Endpoints API

## Health Check

### GET /

Verifica que la aplicación está disponible.

Respuesta:

```json
{
  "status": "ok"
}
```

---

# Descargas

## Crear solicitud de descarga

### POST /downloads

Crea una solicitud de recuperación de CFDI ante el SAT.

Parámetros principales:

- RFC solicitante.
- Fecha inicial.
- Fecha final.
- Tipo de comprobante.
- Dirección del CFDI.

Direcciones soportadas:

- `received`
  - CFDI recibidos.
- `issued`
  - CFDI emitidos.

Ejemplo:

```json
{
  "rfc": "AAAAXXXXXXXXX",
  "start_date": "2026-07-01",
  "end_date": "2026-07-31",
  "direction": "received"
}
```

---

## Consultar solicitudes

### GET /downloads

Lista las solicitudes realizadas.

Información mostrada:

- Identificador interno.
- Estado de solicitud.
- Fecha de creación.
- Datos de respuesta del SAT.

---

## Consultar detalle de descarga

### GET /downloads/{download_id}

Obtiene información detallada de una solicitud.

Incluye:

- Estado actual.
- Paquetes asociados.
- Información generada por SAT.

---

## Procesar paquetes descargados

### POST /downloads/{download_id}/process

Procesa los paquetes ZIP asociados a una descarga.

Proceso realizado:

1. Localiza paquetes descargados.
2. Abre archivos ZIP.
3. Extrae XML CFDI.
4. Obtiene UUID.
5. Guarda XML localmente.
6. Inserta CFDI nuevos.
7. Crea relación paquete-documento.

Respuesta ejemplo:

```json
{
  "packages": 1,
  "documents": 12
}
```

---

# Consultas CFDI

## Resumen JSON

### GET /downloads/{download_id}/summary

Obtiene un resumen de los CFDI asociados a una descarga.

Respuesta ejemplo:

```json
{
  "documents": 12,
  "total": 5000.50,
  "iva": 689.32,
  "rows": [
    {
      "fecha": "2026-07-20",
      "rfc": "SSF810612MK7",
      "uuid": "XXXXXXXX",
      "total": 900.01,
      "iva": 120.95
    }
  ]
}
```

---

## Resumen TSV

### GET /downloads/{download_id}/summary/tsv

Genera un reporte tabular.

Ejemplo:

```
Fecha        RFC             Total     IVA
2026-07-20   SSF810612MK7    900.01    120.95
TOTAL                       900.01    120.95
```

---

# Modelo de datos

## download_requests

Almacena las solicitudes realizadas al SAT.

Contiene información como:

- RFC solicitante.
- Periodo solicitado.
- Dirección del CFDI.
- Estado de solicitud.

---

## download_packages

Representa los paquetes ZIP descargados desde SAT.

Campos principales:

- `package_id`
- `file_path`
- `download_request_id`

---

## cfdi_documents

Catálogo único de comprobantes CFDI.

Campos principales:

- UUID.
- RFC emisor.
- Fecha.
- Total.
- IVA trasladado.
- Archivo XML asociado.

El UUID tiene restricción única para evitar duplicados.

---

## download_package_documents

Tabla de relación entre paquetes y CFDI.

Permite la relación:

```
Paquete ZIP
     |
     |
     +---- CFDI
```

Un mismo CFDI puede aparecer en diferentes paquetes sin duplicar el documento.

---

# Estructura de almacenamiento

```
storage/

packages/

    ZIP descargados del SAT

    xml/

        UUID.xml
        UUID.xml
        UUID.xml
```

---

# Flujo actual de operación

1. Crear solicitud de descarga.

2. Consultar estado hasta que SAT genere paquetes.

3. Descargar paquetes ZIP.

4. Procesar paquetes.

5. Consultar resumen CFDI.

Flujo:

```
Solicitud SAT
      |
      v
Paquete ZIP
      |
      v
Extracción XML
      |
      v
CFDI Database
      |
      v
Consultas / Reportes
```

---

# Próximas mejoras

- Interfaz web.
- Selección visual de dirección CFDI.
- Validación XML contra esquemas SAT.
- Descargas programadas.
- Exportación Excel.
- Búsqueda por RFC.
- Búsqueda por UUID.
- Autenticación y usuarios.
