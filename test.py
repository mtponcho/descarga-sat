from pathlib import Path
from lxml import etree

CFDI_NS = {
    "cfdi": "http://www.sat.gob.mx/cfd/4",
    "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital",
}

for xml in Path("/tmp/cfdi_test").glob("*.xml"):
    root = etree.parse(xml).getroot()

    uuid = root.xpath(
        "//tfd:TimbreFiscalDigital/@UUID",
        namespaces=CFDI_NS,
    )[0]

    total = root.get("Total")

    iva = root.xpath(
        "//cfdi:Impuestos/@TotalImpuestosTrasladados",
        namespaces=CFDI_NS,
    )

    print(xml.name, uuid, total, iva)
