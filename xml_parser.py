import xml.etree.ElementTree as ET

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = {"general": [], "productos": []}

    for at001_row in root.findall(".//at001/row"):
        def get_float(element, field):
            value = element.findtext(field)
            return float(value) if value is not None else 0.0

        tipo_cambio = get_float(at001_row, "F001TIPCAM")
        general_data = {
            "Pedimento": at001_row.findtext("C001NUMPED"),
            "Aduana": at001_row.findtext("C001ADUSEC"),
            "T Operacion": at001_row.findtext("C001TIPOPE"),
            "CVE.Pedimento": at001_row.findtext("C001CVEDOC"),
            "regimen": at001_row.findtext("C001TIPREG"),
            "TC": tipo_cambio,
            "valor_dolares": at001_row.findtext("F001VALDOL"),
            "valor_aduana": at001_row.findtext("N001VALADU"),
            "precio_pagado": at001_row.findtext("N001VALCOM"),
            "Patente": at001_row.findtext("C001PATEN"),
            "val_seguro": get_float(at001_row, "F001VALSEG") * tipo_cambio,
            "seguro": get_float(at001_row, "F001SEGURO") * tipo_cambio,
            "Flete aerero": get_float(at001_row, "F001FLETES") * tipo_cambio,
            "embalaje": get_float(at001_row, "F001EMBALA") * tipo_cambio,
            "O.Incrementales": get_float(at001_row, "F001OTRINC") * tipo_cambio,
        }
        data["general"].append(general_data)

    for at016_row in root.findall(".//at016/row"):
        product = {
            "Pedimento": at016_row.findtext("C016NUMPED"),
            "descripcion": at016_row.findtext("C016DESMER"),
            "fraccion": at016_row.findtext("C016FRAC"),
            "subfraccion": at016_row.findtext("I016SUBFRA"),
            "cantidad_umc": at016_row.findtext("F016CANUMC"),
            "unidad_medida_umc": at016_row.findtext("C016UNIUMC"),
            "cantidad_umt": at016_row.findtext("F016CANUMT"),
            "unidad_medida_umt": at016_row.findtext("C016UNIUMT"),
            "valor_dolares": at016_row.findtext("F016VALDOL"),
            "precio_unitario": at016_row.findtext("F016PREUNI"),
            "pais_origen": at016_row.findtext("C016PAISOD"),
        }
        data["productos"].append(product)

    return data
