from models import Product
from inventario import ver_menu, SABOR_MAR, BEBIDAS, MARMI_SIZE, PRECIO_BEB
from entradas import pedir_entero_positivo

def cantidad_de_pedidos(invent_pro, conexao):
    cursor = conexao.cursor()
    pedido = []
    op = "s"
    while op.lower() == "s":
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
            if invent_pro[sabor]>=cantidad:
                invent_pro[sabor]-= cantidad
                cursor.execute(
                 "UPDATE inventario SET quantidade = quantidade - ? WHERE producto = ?", 
                  (cantidad,SABOR_MAR[marmi]),  
                )
                for i in range(cantidad):
                    producto = Product(sabor, valor_u)
                    pedido.append(producto) 
            else:
                print(f"Stock Insuficiente solo hay {invent_pro[sabor]} de ese sabor")     
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
            if invent_pro[sab_beb]>=canti_beb:
                invent_pro[sab_beb]-= canti_beb
                cursor.execute(
                    "UPDATE inventario SET quantidade = quantidade -? WHERE producto = ?",
                    (canti_beb,BEBIDAS[beb1]),
                )
                for i in range(canti_beb):
                    producto=Product(sab_beb,pre_beb)
                    pedido.append(producto) 
            else:
                print(f"Stock Insuficiente solo hay {invent_pro[sab_beb]} de ese sabor")
        else :
            print("Opcion Invalida")     
        op=input("Desea agregar otro Producto S/N: ").lower()
    return pedido