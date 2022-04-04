import requests
import json
import re

urlbase = 'https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes'

def galeguiza(cadea):
    substutucions = (
        ("^CALLE$", "RÚA"),
        ("^CL$", "RÚA"),
        ("^PLAZA$", "PRAZA"),
        ("^C/$", "R/"),
        ("^LA$", "A" ),
        ("^\(LA\)$", "(A)" ),
        ("^\(EL\)$", "(O)" ),
        ("^EL$", "O"),
        ("^LOS$", "OS"),
        ("^DEL$", "DO"),
        ("^CR$", "ESTRADA"),
        ("^CARRETERA$", "ESTRADA"),
        ("^CAMINO$", "CAMIÑO"),
        ("^AÉROPUERTO$", "AEROPORTO"),
        ("^AEROPUERTO$", "AEROPORTO"),
        ("^BAJO$", "BAIXO"),
        ("FINISTERRE", "FISTERRA"),
        ("^Y$", "E"),
        ("Y", "I")
    )

    lista = cadea.split()
    for a, b in substutucions:
        lista = [re.sub(a, b, item, flags=re.IGNORECASE) for item in lista]

    return " ".join(lista)

def listaConcelhos():
    lista = []
    idComunidade = '12'
    urlProvincias = f"{urlbase}/Listados/ProvinciasPorComunidad/{idComunidade}"
    resposta = requests.get(urlProvincias)
    datos = json.loads(resposta.content)
    for provincia in datos:
        idProvincia = provincia['IDPovincia']
        if idProvincia is not None:
            urlConcellosPorPovincia = f"{urlbase}/Listados/MunicipiosPorProvincia/{idProvincia}"
            resposta = requests.get(urlConcellosPorPovincia)
            datos = json.loads(resposta.content)
            for municipio in datos:
                idConcello = municipio['IDMunicipio']
                nomeConcello = municipio['Municipio']
                concello = (idConcello, nomeConcello)
                lista.append(concello)
    lista_ordenada = sorted(lista, key=lambda d: d[1])
    return lista_ordenada

def datosConcelho(idConcellos, ordepor):
    lista = []
    for idConcello in idConcellos:
        url = f"{urlbase}/EstacionesTerrestres/FiltroMunicipio/{idConcello}"
        resposta = requests.get(url)
        datos = json.loads(resposta.content)
        for datos_gasolineira in datos['ListaEESSPrecio']:
            nome = datos_gasolineira['Rótulo']
            direccion = galeguiza(datos_gasolineira['Dirección'].upper())
            concello = galeguiza(datos_gasolineira['Municipio'].upper())
            localidade = galeguiza(datos_gasolineira['Localidad'].upper())
            latitude = datos_gasolineira['Latitud'].replace(',','.')
            lonxitude = datos_gasolineira['Longitud (WGS84)'].replace(',','.')
            p_gasoleo_a = datos_gasolineira['Precio Gasoleo A'].replace(',','.')
            p_gasoleo_p = datos_gasolineira['Precio Gasoleo Premium'].replace(',','.')
            p_gasoleo_b = datos_gasolineira['Precio Gasoleo B'].replace(',','.')
            p_gasolina_95 = datos_gasolineira['Precio Gasolina 95 E5'].replace(',','.')
            p_gasolina_98 = datos_gasolineira['Precio Gasolina 98 E5'].replace(',','.')
            tipo_venda = datos_gasolineira['Tipo Venta']

            gasolineira = {
                'nome' : nome,
                'enderezo' : direccion,
                'concello' : concello,
                'localidade' : localidade,
                'latitude' : latitude,
                'lonxitude' : lonxitude,
                'maps' : f"https://maps.google.com/?q={latitude},{lonxitude}",
                'p_gasoleo_a' : p_gasoleo_a,
                'p_gasoleo_p': p_gasoleo_p,
                'p_gasoleo_b' : p_gasoleo_b, 
                'p_gasolina_95' : p_gasolina_95, 
                'p_gasolina_98' : p_gasolina_98,
            }

            if tipo_venda.upper() == 'P':
                if ordepor != "nada":
                    if gasolineira[ordepor] != '':
                        lista.append(gasolineira)
                else:
                    lista.append(gasolineira)
    
    if ordepor == "nada":
        return lista
    else:
        lista_ordenada = sorted(lista, key=lambda d: d[ordepor])
        return lista_ordenada

if __name__ == '__main__':
    print(datosConcelho(["2122","2123"], "nada"))
    #print(listaConcelhos)