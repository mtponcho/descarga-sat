from datetime import datetime

from satcfdi.models import Signer
from satcfdi.pacs.sat import SAT, EstadoComprobante

from app.models.certificate import Certificate
from app.models.download_request import DownloadRequest


class DownloadService:

    def __init__(self, db):
        self.db = db


    def create(
        self,
        certificate_id: int,
        password: str,
        direction: str,
        start_date,
        end_date,
    ):

        certificate = (
            self.db.query(Certificate)
            .filter(
                Certificate.id == certificate_id
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


        if direction == "received":

            response = (
                sat.recover_comprobante_received_request(
                    fecha_inicial=start_date,
                    fecha_final=end_date,
                    estado_comprobante=EstadoComprobante.VIGENTE,
                )
            )

        elif direction == "emitted":

            response = (
                sat.recover_comprobante_emitted_request(
                    fecha_inicial=start_date,
                    fecha_final=end_date,
                    rfc_emisor=signer.rfc,
                )
            )

        else:
            raise ValueError(
                "Invalid direction"
            )

        print(response)

        request_id = (
            response.get("IdSolicitud")
            or response.get("id_solicitud")
        )
        if not request_id:
            return {
                "success": False,
                "sat_response": response,
            }



        download = DownloadRequest(
            certificate_id=certificate.id,
            request_id=request_id,
            direction=direction,
            status="requested",
        )

        self.db.add(download)
        self.db.commit()
        self.db.refresh(download)


        return {
            "id": download.id,
            "request_id": request_id,
            "sat_response": response,
        }
