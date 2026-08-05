from app.models.cfdi_document import CfdiDocument
from app.models.download_package import DownloadPackage
from app.models.download_package_document import DownloadPackageDocument


class CfdiQueryService:

    def __init__(self, db):
        self.db = db

    def _rows(self, download_id: int):

        return (
            self.db.query(CfdiDocument)
            .join(
                DownloadPackageDocument,
                CfdiDocument.id
                == DownloadPackageDocument.cfdi_document_id,
            )
            .join(
                DownloadPackage,
                DownloadPackageDocument.download_package_id
                == DownloadPackage.id,
            )
            .filter(
                DownloadPackage.download_request_id == download_id,
            )
            .order_by(
                CfdiDocument.fecha,
            )
            .all()
        )

    def summary(self, download_id: int):

        rows = self._rows(download_id)

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

    def summary_tsv(self, download_id: int):

        rows = self._rows(download_id)

        output = []

        output.append(
            "Fecha\tRFC\tTotal\tIVA"
        )

        total = 0
        iva = 0

        for cfdi in rows:

            output.append(
                f"{cfdi.fecha.date()}\t"
                f"{cfdi.rfc_emisor}\t"
                f"{cfdi.total}\t"
                f"{cfdi.iva_trasladado}"
            )

            total += cfdi.total
            iva += cfdi.iva_trasladado

        output.append(
            f"TOTAL\t\t{total}\t{iva}"
        )

        return "\n".join(output)
