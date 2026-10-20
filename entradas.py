def pedir_si_no(mensaje):
    while True:
        respuesta = input(f"{mensaje} (S/N): ").lower()
        if respuesta in ("s", "n"):
            return respuesta == "s"
        print("Opcion invalida, escoja S o N")


def pedir_decimal(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("El valor no puede ser negativo")
                continue
            return valor
        except ValueError:
            print("Introduzca un valor numerico")


def pedir_entero_positivo(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor > 0:
                return valor
            print("La cantidad debe ser mayor que cero.")
        except ValueError:
            print("Introduce un numero entero valido.")


def pedir_forma_pago():
    formas = {1: "PIX", 2: "CARTAO", 3: "DINHEIRO"}
    print("===== FORMA DE PAGAMENTO =====")
    for numero, nombre in formas.items():
        print(f"{numero}. {nombre.capitalize()}")
    while True:
        try:
            opcion = int(input("Introduzca el numero correspondiente a la opcion: "))
        except ValueError:
            print("Introduzca un valor numerico")
            continue
        if opcion in formas:
            return formas[opcion]
        print("Intente de nuevo: 1. Pix, 2. Cartao o 3. Dinheiro")