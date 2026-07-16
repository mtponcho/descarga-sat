from datetime import datetime
from decimal import Decimal
from pathlib import Path
import zipfile

from lxml import etree

from app.models.cfdi_document import CfdiDocument
from app.models.download_package import DownloadPackage


CFDI_NS = {
    "cfdi": "http://www.sat.gob.mx/cfd/4",
    "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital",
}
XML_STORAGE = Path("/app/app/storage/packages/xml")
XML_STORAGE.mkdir(
    parents=True,
    exist_ok=True,
)


class CfdiService:

    def __init__(self, db):
        self.db = db

    def process(self, download_id: int):

        packages = (
            self.db.query(DownloadPackage)
            .filter(
                DownloadPackage.download_request_id == download_id
            )
            .all()
        )

        if not packages:
            raise ValueError("No packages found")

        inserted = 0

        for package in packages:

            zip_path = Path(package.file_path)

            if not zip_path.exists():
                continue

            with zipfile.ZipFile(zip_path) as z:

                for filename in z.namelist():

                    if not filename.lower().endswith(".xml"):
                        continue

                    with z.open(filename) as f:
                        xml_bytes = f.read()

                    root = etree.fromstring(xml_bytes)

                    uuid = root.xpath(
                        "//tfd:TimbreFiscalDigital/@UUID",
                        namespaces=CFDI_NS,
                    )[0]
                    xml_path = XML_STORAGE / f"{uuid}.xml"

                    if not xml_path.exists():
                        xml_path.write_bytes(xml_bytes)

                    #
                    # Evitar duplicados
                    #
                    exists = (
                        self.db.query(CfdiDocument)
                        .filter(
                            CfdiDocument.uuid == uuid
                        )
                        .first()
                    )

                    if exists:
                        continue

                    rfc_emisor = root.xpath(
                        "//cfdi:Emisor/@Rfc",
                        namespaces=CFDI_NS,
                    )[0]

                    fecha = datetime.fromisoformat(
                        root.get("Fecha")
                    )

                    total = Decimal(
                        root.get("Total")
                    )

                    iva = root.xpath(
                        "/cfdi:Comprobante/cfdi:Impuestos/@TotalImpuestosTrasladados",
                        namespaces=CFDI_NS,
                    )

                    iva = Decimal(
                        iva[0] if iva else "0.00"
                    )

                    document = CfdiDocument(
                        download_package_id=package.id,
                        uuid=uuid,
                        rfc_emisor=rfc_emisor,
                        fecha=fecha,
                        total=total,
                        iva_trasladado=iva,
                        xml_file=str(xml_path),
                    )

                    self.db.add(document)

                    inserted += 1

        self.db.commit()

        return {
            "packages": len(packages),
            "documents": inserted,
        }
