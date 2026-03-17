def validar_entry(texto):
    if texto == "":
        return True
    if not all(c.isdigit() or c == "." for c in texto):
        return False
    if texto.count(".") > 1:
        return False
    return True


def validar_triangulo(valores):
    a = valores.get("angle1")
    b = valores.get("angle2")

    if a is not None and b is not None:
        suma = a + b

        if suma >= 180:
            return False, "The sum of the angles must be less than 180°"

        if a <= 0 or b <= 0:
            return False, "Angles must be greater than 0°"

    return True, ""


def validar_triangulo_rectangulo(valores):
    adj = valores.get("adjacent")
    opp = valores.get("opposite")
    hyp = valores.get("hipotenuse")
    ang = valores.get("angle")

    if adj is not None and opp is not None and hyp is not None:
        if abs((adj**2 + opp**2) - (hyp**2)) > 0.001:
            return False, "Does not satisfy the Pythagorean theorem"

    if ang is not None:
        if ang <= 0 or ang >= 90:
            return False, "Angle must be between 0° and 90°"

    return True, ""
