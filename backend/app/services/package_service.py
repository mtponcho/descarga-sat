import base64
from pathlib import Path

from satcfdi.models import Signer
from satcfdi.pacs.sat import SAT

from app.models.download_request import DownloadRequest
from app.models.certificate import Certificate
from app.models.download_package import DownloadPackage


STORAGE = Path("/app/app/storage/packages")
STORAGE.mkdir(parents=True, exist_ok=True)


class PackageService:

    def __init__(self, db):
        self.db = db


    def download_all(
        self,
        download_id: int,
        password: str,
    ):

        download = (
            self.db.query(DownloadRequest)
            .filter(
                DownloadRequest.id == download_id
            )
            .first()
        )

        if not download:
            raise ValueError(
                "Download request not found"
            )


        certificate = (
            self.db.query(Certificate)
            .filter(
                Certificate.id == download.certificate_id
            )
            .first()
        )

        if not certificate:
            raise ValueError(
                "Certificate not found"
            )


        with open(
            certificate.cer_file,
            "rb"
        ) as f:
            cer = f.read()


        with open(
            certificate.key_file,
            "rb"
        ) as f:
            key = f.read()


        signer = Signer.load(
            certificate=cer,
            key=key,
            password=password,
        )


        sat = SAT(
            signer=signer
        )


        # Consultar estado para obtener paquetes
        status = (
            sat.recover_comprobante_status(
                download.request_id
            )
        )


        packages = status.get(
            "IdsPaquetes",
            []
        )


        if not packages:
            return {
                "download_id": download.id,
                "packages": [],
                "sat_status": status,
            }


        result = []


        for package_id in packages:

            response, content = (
                sat.recover_comprobante_download(
                    package_id
                )
            )


            if response.get(
                "CodEstatus"
            ) != "5000":

                result.append(
                    {
                        "package_id": package_id,
                        "error": response,
                    }
                )

                continue


            zip_data = base64.b64decode(
                content
            )


            zip_path = (
                STORAGE /
                f"{package_id}.zip"
            )


            zip_path.write_bytes(
                zip_data
            )


            package = DownloadPackage(
                download_request_id=download.id,
                package_id=package_id,
                file_path=str(zip_path),
            )


            self.db.add(
                package
            )


            result.append(
                {
                    "package_id": package_id,
                    "file": str(zip_path),
                }
            )


        self.db.commit()


        return {
            "download_id": download.id,
            "packages": result,
            "sat_status": status,
        }
