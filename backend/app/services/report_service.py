import time

from app.services.download_service import DownloadService
from app.services.download_status_service import DownloadStatusService
from app.services.package_service import PackageService
from app.services.cfdi_service import CfdiService
from pprint import pprint


class ReportService:

    def __init__(self, db):
        self.db = db

    def generate_iva_report(
        self,
        certificate_id: int,
        password: str,
        start_date,
        end_date,
    ):

        download_service = DownloadService(
            self.db
        )

        print("1. Creando solicitud")

        download = download_service.create(
            certificate_id=certificate_id,
            password=password,
            direction="received",
            start_date=start_date,
            end_date=end_date,
        )

        print("2. Solicitud creada:", download)

        print("3. Esperando SAT")

        self._wait_until_ready(
            download["id"],
            password,
        )

        print("4. SAT listo")

        package_service = PackageService(
            self.db
        )

        for intento in range(12):

            print(
                f"5. Descargando paquetes (intento {intento + 1})"
            )

            packages = package_service.download_all(
                download["id"],
                password,
            )

            print("6. Paquetes:", packages)

            if packages["packages"]:
                break

            time.sleep(10)

        else:
            raise TimeoutError(
                "El SAT aún no publicó los paquetes."
            )

        cfdi_service = CfdiService(
            self.db
        )

        print("7. Procesando XML")

        cfdi_service.process(
            download["id"]
        )

        from app.services.cfdi_query_service import (
            CfdiQueryService,
        )

        query = CfdiQueryService(
            self.db
        )

        print("8. Generando resumen")

        return query.summary_tsv(
            download["id"]
        )

    def _wait_until_ready(
        self,
        download_id: int,
        password: str,
        timeout: int = 1800,
        interval: int = 600,
    ):

        service = DownloadStatusService(
            self.db
        )

        elapsed = 0

        while elapsed < timeout:

            status = service.get_status(
                download_id,
                password,
            )

            sat = status["sat_response"]

            print(
                f"[{elapsed:03d}s] "
                f"CodEstatus={sat.get('CodEstatus')} "
                f"EstadoSolicitud={sat.get('EstadoSolicitud')} "
                f"Mensaje={sat.get('Mensaje')} "
                f"IdsPaquetes={sat.get('IdsPaquetes')}"
            )
            pprint(sat)

            if sat.get("CodEstatus") != "5000":
                raise ValueError(
                    f"SAT rechazó la solicitud: "
                    f"{sat.get('Mensaje')}"
                )

            if sat.get("EstadoSolicitud") == 3:
                return status

            time.sleep(interval)
            elapsed += interval

        raise TimeoutError(
            "SAT no terminó la descarga dentro del tiempo esperado."
        )
