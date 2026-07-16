from pathlib import Path
from lxml import etree

CFDI_NS = {
    "cfdi": "http://www.sat.gob.mx/cfd/4",
    "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital",
}

for xml in Path(".").glob("*.xml"):

    root = etree.parse(str(xml)).getroot()

    uuid = root.xpath(
        "//tfd:TimbreFiscalDigital/@UUID",
        namespaces=CFDI_NS,
    )[0]

    rfc_emisor = root.xpath(
        "//cfdi:Emisor/@Rfc",
        namespaces=CFDI_NS,
    )[0]

    fecha = root.get("Fecha")

    total = root.get("Total")

    iva = root.xpath(
        "//cfdi:Impuestos/@TotalImpuestosTrasladados",
        namespaces=CFDI_NS,
    )

    iva = iva[0] if iva else "0.00"

    print(
        f"""
Archivo : {xml.name}
UUID    : {uuid}
Emisor  : {rfc_emisor}
Fecha   : {fecha}
Total   : {total}
IVA     : {iva}
"""
    )
