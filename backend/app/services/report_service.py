import time

from app.services.download_service import DownloadService
from app.services.download_status_service import DownloadStatusService
from app.services.package_service import PackageService
from app.services.cfdi_service import CfdiService


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

        download = download_service.create(
            certificate_id=certificate_id,
            password=password,
            direction="received",
            start_date=start_date,
            end_date=end_date,
        )

        status = self._wait_until_ready(
            download["id"],
            password,
        )

        package_service = PackageService(
            self.db
        )

        packages = package_service.download_all(
            download["id"],
            password,
        )

        cfdi_service = CfdiService(
            self.db
        )

        process = cfdi_service.process(
            download["id"]
        )

        return {
            "download_id": download["id"],
            "request_id": download["request_id"],
            "status": status,
            "packages": packages,
            "process": process,
        }

    def _wait_until_ready(
        self,
        download_id: int,
        password: str,
        timeout: int = 300,
        interval: int = 10,
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

            if sat.get("EstadoSolicitud") == 3:
                return status

            time.sleep(interval)
            elapsed += interval

        raise TimeoutError(
            "SAT no terminó la descarga dentro del tiempo esperado."
        )
