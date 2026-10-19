
SABOR_MAR= {"1" : "Carne ao Molho",
                "2" : "Coxinha de frango Frito",
                "3" : "File de frango Grelhado",
                "4" : "Linguicinha Assada",
                "5" : "Strogonoff de Frango",
                "6" : "Bife acebolado",
                "7" : "Bisteca Suina"}

BEBIDAS={"1":"Cocacola de Lata",
            "2":"Cocacola 600ml",
            "3":"Guarana Lata"}

MARMI_SIZE={"p":18,"m":22,"g":25}

PRECIO_BEB={"1":5,"2":8,"3":4}

def inventario ():
        print("Bienvenido vamos a Agregar la cantidad de Productos Disponibles")
        invent_pro={"Carne ao Molho":0,
                    "Coxinha de frango Frito":0,
                    "File de frango Grelhado":0,
                    "Linguicinha Assada":0,
                    "Strogonoff de Frango":0,
                    "Bife acebolado":0,
                    "Bisteca Suina":0,
                    "Cocacola de Lata":0,
                    "Cocacola 600ml":0,
                    "Guarana Lata":0}
        for inv in invent_pro:
            invent_pro[inv]=int(input(f"Que cantidad disponible para la venta hay de: {inv}"))
        return invent_pro
    
def ver_menu(invent_pro, tipo):
    if tipo == "M":
       productos = SABOR_MAR
    else:
       productos = BEBIDA

    print("\n====== Menu del Dia ======")
    print("Marmitas de:\n")
    for i, llave in enumerate(productos.values(), start=1):
        valor = invent_pro[llave]
        if valor == 0:
            print(f"{i}.{llave} ----- AGOTADO")
        elif valor<=3:
            print(f"{i}.{llave} = {valor} ----- STOCK BAJO")
        else:
            print(f"{i}.{llave} ----- Stock: {valor}")
    print("*********************")    