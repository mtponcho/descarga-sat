from satcfdi.models import Signer
from satcfdi.pacs.sat import SAT

from app.models.download_request import DownloadRequest
from app.models.certificate import Certificate


class DownloadStatusService:

    def __init__(self, db):
        self.db = db


    def get_status(
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


        with open(certificate.cer_file, "rb") as f:
            cer = f.read()

        with open(certificate.key_file, "rb") as f:
            key = f.read()


        signer = Signer.load(
            certificate=cer,
            key=key,
            password=password,
        )


        sat = SAT(
            signer=signer
        )


        response = sat.recover_comprobante_status(
            download.request_id
        )


        return {
            "download_id": download.id,
            "request_id": download.request_id,
            "sat_response": response,
        }
