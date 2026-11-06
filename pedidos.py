from models import Product
from inventario import ver_menu, SABOR_MAR, BEBIDAS, MARMI_SIZE, PRECIO_BEB
from entradas import pedir_entero_positivo
from entradas import pedir_entero_positivo, pedir_si_no
def cantidad_de_pedidos(invent_pro, conexao):
    cursor = conexao.cursor()
    pedido = []
    agregar_otro = True
    while agregar_otro:
        while True:
            opcion = input(" Seleccione *M* para marmita o *B* para Bebidas: ").lower()
            if opcion == "m" or opcion == "b":
                break
            else:
                print("Introduzca una opcion valida")   
        if opcion == "m":
            while True:
                tamanho = input("seleccione el tamaño *P* *M* *G* : ").lower()
                if tamanho in MARMI_SIZE:
                    valor_u = MARMI_SIZE[tamanho]
                    break
                else:
                    print("Introduzca una opcion valida")
            ver_menu(invent_pro,"M")
            while True:
                marmi=input("Ingrese el Numero Correspondiente a la Marmita: ")
                if marmi in SABOR_MAR:
                    sabor=SABOR_MAR[marmi]
                    break
                else:
                    print("Introduzca una opcion valida")
            cantidad = pedir_entero_positivo("cuantas marmitas de este tamanho y sabor: ")
            cursor.execute(
                "UPDATE inventario SET quantidade = quantidade - ? WHERE producto = ? AND quantidade >= ?", 
                (cantidad,sabor,cantidad),  
            )
            if cursor.rowcount == 0:
                cursor.execute(
                    "SELECT  producto, quantidade FROM inventario WHERE producto = ?",
                (sabor,)
                )
                resultado = cursor.fetchone()
                if resultado is None:
                    raise ValueError("El producto no existe.")
                else:
                    print(f"Stock insuficiente solo hay {resultado[1]} unidades.")
            else:
                for i in range(cantidad):
                    producto = Product(sabor, valor_u)
                    pedido.append(producto) 
        elif opcion.lower()== "b":
            print("1.Cocacola de Lata")
            print("2.Cocacola 600ml")
            print("3.Guarana Lata")
            while True:
                    beb1=input("Seleccione una BEBIDA *1* *2* *3* : ")
                    if beb1 in BEBIDAS and beb1 in PRECIO_BEB:
                        pre_beb = PRECIO_BEB[beb1]
                        sab_beb=BEBIDAS[beb1]
                        break
                    else:
                        print("Introduzca una opcion valida")
            canti_beb = pedir_entero_positivo("Cuantas BEBIDAS de ese Sabor: ")
            cursor.execute(
                "UPDATE inventario SET quantidade = quantidade - ? WHERE producto = ? AND quantidade >= ?", 
                (canti_beb,sab_beb,canti_beb),  
            )
            if cursor.rowcount == 0:
                cursor.execute(
                    "SELECT producto, quantidade FROM inventario WHERE producto = ?",
                (sab_beb,)
                )
                resultado_beb = cursor.fetchone()
                if resultado_beb is None:
                    raise ValueError("El producto no existe.")
                else:
                    print(f"Stock insuficiente solo hay {resultado_beb[1]} unidades.")
                    continue
            else:
                for i in range(canti_beb):
                    producto = Product(sab_beb, pre_beb)
                    pedido.append(producto)
        if pedir_si_no("Desea agregar otro produto?"):
            continue
        else:
            agregar_otro=False
    return pedido

