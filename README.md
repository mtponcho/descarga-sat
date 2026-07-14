# descarga-sat
descarga multiple de CFDI SAT 2026


# Descarga SAT

## Estado actual

Fecha: 2026-07-10

## Completado

- [x] FastAPI
- [x] Docker
- [x] PostgreSQL
- [x] Upload .cer/.key
- [x] Lectura certificado .cer

## En progreso

- [ ] Persistencia de certificados
- [ ] Validación e.firma

## Próximo commit

feat: persist certificates metadata



API:

http://localhost:8000

Swagger:

http://localhost:8000/docs
Endpoints actuales
Health
GET /health
Cargar certificado
POST /certificates
