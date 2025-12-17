# Barberia/utils.py

def validar_rut(rut: str) -> bool:
    # Eliminar puntos y guion y pasar a mayúsculas
    rut = rut.replace(".", "").replace("-", "").upper()

    # Debe tener al menos 8 caracteres (7 de cuerpo + DV)
    if len(rut) < 8:
        return False

    cuerpo = rut[:-1]
    dv = rut[-1]

    # Algoritmo módulo 11
    suma = 0
    multiplo = 2

    for c in reversed(cuerpo):
        suma += int(c) * multiplo
        multiplo += 1
        if multiplo > 7:
            multiplo = 2

    resto = suma % 11
    calculado = 11 - resto

    if calculado == 11:
        dv_calc = "0"
    elif calculado == 10:
        dv_calc = "K"
    else:
        dv_calc = str(calculado)

    return dv_calc == dv


def formatear_rut(rut: str) -> str:
    # Eliminar formato previo
    rut = rut.replace(".", "").replace("-", "").upper()
    cuerpo = rut[:-1]
    dv = rut[-1]

    # Poner puntos cada 3 dígitos desde la derecha
    invertido = cuerpo[::-1]
    grupos = [invertido[i:i+3] for i in range(0, len(invertido), 3)]
    cuerpo_formateado = ".".join(g[::-1] for g in grupos[::-1])

    return f"{cuerpo_formateado}-{dv}"
