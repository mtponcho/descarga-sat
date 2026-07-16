from app.models.cfdi_document import CfdiDocument
from app.models.download_package import DownloadPackage


class CfdiQueryService:

    def __init__(self, db):
        self.db = db


    def summary(self, download_id: int):

        rows = (
            self.db.query(CfdiDocument)
            .join(
                DownloadPackage,
                CfdiDocument.download_package_id == DownloadPackage.id
            )
            .filter(
                DownloadPackage.download_request_id == download_id
            )
            .order_by(
                CfdiDocument.fecha
            )
            .all()
        )


        documents = []

        total = 0
        iva = 0

        for cfdi in rows:

            documents.append(
                {
                    "fecha": cfdi.fecha.date().isoformat(),
                    "rfc": cfdi.rfc_emisor,
                    "uuid": cfdi.uuid,
                    "total": float(cfdi.total),
                    "iva": float(cfdi.iva_trasladado),
                }
            )

            total += cfdi.total
            iva += cfdi.iva_trasladado


        return {
            "documents": len(documents),
            "total": float(total),
            "iva": float(iva),
            "rows": documents,
        }
