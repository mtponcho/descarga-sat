# backend/app/services/certificate_service.py

from pathlib import Path
from uuid import uuid4

from satcfdi.models import Signer

from app.models.taxpayer import Taxpayer
from app.models.certificate import Certificate


STORAGE = Path("/app/app/storage/taxpayers")


class CertificateService:

    def __init__(self, db):
        self.db = db

    def register(
        self,
        cer_file,
        key_file,
        password,
    ):

        cer_data = cer_file.file.read()
        key_data = key_file.file.read()

        signer = Signer.load(
            certificate=cer_data,
            key=key_data,
            password=password,
        )

        rfc = signer.rfc

        taxpayer = (
            self.db.query(Taxpayer)
            .filter(Taxpayer.rfc == rfc)
            .first()
        )

        if not taxpayer:
            taxpayer = Taxpayer(rfc=rfc)
            self.db.add(taxpayer)
            self.db.commit()
            self.db.refresh(taxpayer)

        certificate_id = str(uuid4())

        directory = (
            STORAGE /
            rfc /
            "certificates"
        )

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

        cer_path = directory / f"{certificate_id}.cer"
        key_path = directory / f"{certificate_id}.key"

        cer_path.write_bytes(cer_data)
        key_path.write_bytes(key_data)

        certificate = Certificate(
            taxpayer_id=taxpayer.id,
            cer_file=str(cer_path),
            key_file=str(key_path),
            serial_number=str(
                signer.certificate.get_serial_number()
            ),
            subject=str(
                signer.certificate.get_subject()
            ),
            issuer=str(
                signer.certificate.get_issuer()
            ),
            not_before=str(
                signer.certificate.get_notBefore()
            ),
            not_after=str(
                signer.certificate.get_notAfter()
            ),
        )

        self.db.add(certificate)
        self.db.commit()
        self.db.refresh(certificate)

        return {
            "id": certificate.id,
            "rfc": rfc,
            "certificate_id": certificate_id,
        }
