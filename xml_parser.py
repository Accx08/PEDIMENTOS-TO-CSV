import xml.etree.ElementTree as ET
from datetime import datetime

def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = {"general": [], "productos": []}

    def format_date(date_str):
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y%m%d')
                return date_obj.strftime('%d/%m/%Y')
            except:
                return date_str
        return ''

    for at001_row in root.findall(".//at001/row"):
        def get_float(element, field):
            value = element.findtext(field)
            return float(value) if value is not None else 0.0

        tipo_cambio = get_float(at001_row, "F001TIPCAM")
        general_data = {
            "Pedimento"         : at001_row.findtext("C001NUMPED")  ,
            "Importador"        : at001_row.findtext("C001NOMCLI")  ,
            "Aduana"            : at001_row.findtext("C001ADUSEC")  ,
            "CVE.Pedimento"     : at001_row.findtext("C001CVEDOC")  ,
            "T.Operacion"       : at001_row.findtext("C001TIPREG")  ,
            "Fecha"             : format_date(at001_row.findtext("D001FECEP"))      ,
            "TC"                : tipo_cambio                       ,
            "valor_dolares"     : at001_row.findtext("F001VALDOL")  ,
            "valor_aduana"      : at001_row.findtext("N001VALADU")  ,
            "zcnPrecioComercial": at001_row.findtext("N001VALCOM")  ,
            "Patente"           : at001_row.findtext("C001PATEN")   ,
            "val_seguro"        : get_float(at001_row, "F001VALSEG") * tipo_cambio  ,
            "seguro"            : get_float(at001_row, "F001SEGURO") * tipo_cambio  ,
            "Flete aerero"      : get_float(at001_row, "F001FLETES") * tipo_cambio  ,
            "embalaje"          : get_float(at001_row, "F001EMBALA") * tipo_cambio  ,
            "O.Incrementales"   : get_float(at001_row, "F001OTRINC") * tipo_cambio  ,
            "PRV"               : at001_row.findtext("F001TASPRE")  ,
            "PRV iva"           : get_float(at001_row, "F001OTRINC")    *   0.16    ,
            "DTA"               : get_float(at001_row, "I001TTDTA1"),
            "TASA IEPS"         : get_float(at001_row, "F016TASIEP"),
        }
        
        data["general"].append(general_data)

    for at016_row in root.findall(".//at016/row"):
        
        product = {
            "Pedimento": at016_row.findtext("C016NUMPED"),
            "descripcion"       : at016_row.findtext("C016DESMER")  ,
            "fraccion"          : at016_row.findtext("C016FRAC")    ,
            "subfraccion"       : at016_row.findtext("I016SUBFRA")  ,
            "cantidad_umc"      : get_float(at016_row, "F016CANUMC"),
            "unidad_medida_umc" : at016_row.findtext("C016UNIUMC")  ,
            "cantidad_umt"      : get_float(at016_row, "F016CANUMT"),
            "unidad_medida_umt" : at016_row.findtext("C016UNIUMT")  ,
            "valor_dolares"     : get_float(at016_row, "F016VALDOL"),
            "precio_unitario"   : get_float(at016_row, "F016PREUNI"),
            "valor_aduana"      : get_float(at016_row, "N016VALADU"),
            "iva_producto"      : get_float(at016_row, "N016VALADU")*get_float(at016_row, "F016TASIVA")/100,
            "igi"               : get_float(at016_row, "N016MONIGI"),
            "prov"              : root.findtext("C019IDE2CAS"),
       }
        data["productos"].append(product)

    return data


#Importar solo los elementos generales:

"""
def parse_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = {"general": []}

    def format_date(date_str):
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, '%Y%m%d')
                return date_obj.strftime('%d/%m/%Y')
            except:
                return date_str
        return ''

    for at001_row in root.findall(".//at001/row"):
        def get_float(element, field):
            value = element.findtext(field)
            return float(value) if value is not None else 0.0

        tipo_cambio = get_float(at001_row, "F001TIPCAM")
        general_data = {
            "Pedimento"         : at001_row.findtext("C001NUMPED"),
            "Importador"        : at001_row.findtext("C001NOMCLI"),
            "Aduana"            : at001_row.findtext("C001ADUSEC"),
            "CVE.Pedimento"     : at001_row.findtext("C001CVEDOC"),
            "T.Operacion"       : at001_row.findtext("C001TIPREG"),
            "Fecha"             : format_date(at001_row.findtext("D001FECEP")),
            "TC"                : tipo_cambio,
            "valor_dolares"     : at001_row.findtext("F001VALDOL"),
            "valor_aduana"      : at001_row.findtext("N001VALADU"),
            "zcnPrecioComercial": at001_row.findtext("N001VALCOM"),
            "Patente"           : at001_row.findtext("C001PATEN"),
            "val_seguro"        : get_float(at001_row, "F001VALSEG") * tipo_cambio,
            "seguro"            : get_float(at001_row, "F001SEGURO") * tipo_cambio,
            "Flete aerero"      : get_float(at001_row, "F001FLETES") * tipo_cambio,
            "embalaje"          : get_float(at001_row, "F001EMBALA") * tipo_cambio,
            "O.Incrementales"   : get_float(at001_row, "F001OTRINC") * tipo_cambio,
            "PRV"               : at001_row.findtext("F001TASPRE"),
            "PRV iva"           : get_float(at001_row, "F001OTRINC") *0.16,
            "DTA"               : get_float(at001_row, "I001TTDTA1"),
            "TASA IEPS"         : get_float(at001_row, "F016TASIEP"),
        }
        
        data["general"].append(general_data)

    return data
"""
