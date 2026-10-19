import json
import sqlite3
from models import Product
from inventario import ver_menu, SABOR_MAR, BEBIDAS, MARMI_SIZE, PRECIO_BEB
from database import buscar_pedido_db

def cantidad_de_pedidos(invent_pro, conexao):
    cursor = conexao.cursor()
    pedido = []
    op = "s"
    while op.lower() == "s":
        while True:
            opcion = input(" Seleccione *M* para marmita o *B* para Bebidas").lower()
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
            while True:
                try:
                    cantidad = int(input("cuantas marmitas de este tamanho y sabor: "))
                    if cantidad > 0:
                        break
                    print("La cantidad debe ser mayor que cero.")
                except ValueError:
                    print("Introduce un número entero válido.")
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
            
            while True:
                try:
                    canti_beb=int(input("Cuantas BEBIDAS de ese Sabor: "))
                    if canti_beb > 0:
                        break
                    print("La cantidad debe ser mayor que cero.")
                except ValueError:
                    print("Introduce un número entero válido.")
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
        op=input("Desea agregar otro Producto S/N").lower()
    return pedido

def buscar_pedido ():
            
    try:
        with open("historial.json", "r") as f:
            pedidos_existentes = json.load(f)
            telefono_buscado=input("Introduzca el numero de telefono a buscar:")
            encontrado=False
            for  i , pedido in enumerate(pedidos_existentes, start=1):
                temp_num=pedido.get("telefono","0") 
                if telefono_buscado==temp_num:
                    encontrado=True
                    print(f"===== Pedido {i} =====")
                    print(pedido.get("nombre","Sin Nombre"))
                    print(pedido.get("direccion","Sin Direccion"))
                    print(pedido.get("telefono","Sin telefono"))
                    print()
                    print("Pedido: ")
                    lista_productos=pedido.get("productos",[])
                    for producto in lista_productos:
                        print(f"{producto['item']} - R$:{producto['cost']}")
                    print(f'Total: R$ {pedido.get("total","0")}')
                    print()
                    break
            if not encontrado:
                print("Telefono no Encontrado: ")
    except (FileNotFoundError, json.JSONDecodeError):
        print("No Hay Historial De Pedidos Todavia") 
        
def editar_pedido():
    conexao = sqlite3.connect("marmitaria/marmitaria.db")
    cursor = conexao.cursor()
    nueva_taxa_entrega=0.0
    try:
        telefone_buscado=input("Introduzca el Numero de Telefono a Buscar:")
        buscar_pedido_db(telefone_buscado)
        
        while True :
            print("===== Editar Pedido =====")
            print("Cual Dato Desea Cambiar:")
            print()
            print("1. Nombre")
            print("2. Telefono")
            print("3. Direccion")
            print("4. Tipo de entrega")
            print("5. Taxa")
            print("6. Forma de pagamento")
            print("7. Productos")
            print("8. Salir al Menu Principal")
            print()
            op=input("Intuzca el Numero Correspondiente a la Opcion:")
            if op == "1": 
                print("Vamos a Cambiar el Nombre")
                nuevo_nome=input("Introduzca el Nuevo Nombre: ")
                cursor.execute("UPDATE pedidos SET nome = ? WHERE telefone = ?",
                (nuevo_nome,telefone_buscado,)
                )
                lineas_afectadas = cursor.rowcount
                if lineas_afectadas == 0:
                    print("No Se Ha modificado")
                else:
                    print(f"Se Ha Modificado: {lineas_afectadas} Pedido(s)")
                    print("Pedido Actualizado con Exito")
                    continue
            elif op == "2": 
                print("Vamos a Cambiar el Telefono")
                nuevo_telefone=input("Introduzca el Nuevo Telefono: ")
                cursor.execute("UPDATE pedidos SET telefone = ? WHERE telefone = ?",
                (nuevo_telefone,telefone_buscado,)
                )
                lineas_afectadas = cursor.rowcount
                if lineas_afectadas == 0:
                    print("No Se Ha modificado")
                else:
                    print(f"Se Ha Modificado: {lineas_afectadas} Pedido(s)")
                    print("Pedido Actualizado con Exito")
                    continue   
            elif op == "3": 
                print("Vamos a Cambiar La Direccion")
                nueva_direccion=input("Introduzca la Nueva Direccion: ")
                cursor.execute("UPDATE pedidos SET endereco = ? WHERE telefone = ?",
                (nueva_direccion,telefone_buscado,)
                )
                lineas_afectadas = cursor.rowcount
                if lineas_afectadas == 0:
                    print("No Se Ha modificado")
                else:
                    print(f"Se Ha Modificado: {lineas_afectadas} Pedido(s)")
                    print("Pedido Actualizado con Exito")
                    continue
            elif op == "4": 
                print("Vamos a Cambiar el Tipo de Entrega")
                while True :
                    tipo_entrega= input("Entrega a Domicilio? S/N").lower()
                    if tipo_entrega != "s" and tipo_entrega != "n":
                        print("Opcion Invalida Escoja S o N")
                        continue
                    elif tipo_entrega == "s":
                        tipo_entrega="Entrega"
                    else:
                        tipo_entrega= "Balcao"
                        break
                    if tipo_entrega == "Entrega":
                        while True:
                            try:
                                nueva_taxa_entrega = float(input("Introduzca el Valor de la Taxa de Entrega:"))
                
                                if nueva_taxa_entrega < 0:
                                    print("La Taxa No Puede Ser Negativa")
                                    continue
                                break
                
                            except ValueError:
                                print("Introduzca un Valor Numerico")
                            break
                cursor.execute("UPDATE pedidos SET tipo = ?, taxa_entrega=? WHERE telefone = ?",
                (tipo_entrega,nueva_taxa_entrega,telefone_buscado,)
                )
                lineas_afectadas = cursor.rowcount
                if lineas_afectadas == 0:
                    print("No Se Ha modificado")
                else:
                    print(f"Se Ha Modificado: {lineas_afectadas} Pedido(s)")
                    print("Pedido Actualizado con Exito")
                    continue
            elif op == "5": 
                print("Vamos a Cambiar La Taxa")
                while True:
                    try:
                        nueva_taxa_entrega = float(input("Introduzca el Valor de la Taxa de Entrega:"))
        
                        if nueva_taxa_entrega < 0:
                            print("La Taxa No Puede Ser Negativa")
                            continue
                        break
        
                    except ValueError:
                        print("Introduzca un Valor Numerico")
                    break
                cursor.execute("UPDATE pedidos SET taxa_entrega=? WHERE telefone = ?",
                (nueva_taxa_entrega,telefone_buscado,)
                )
                lineas_afectadas = cursor.rowcount
                if lineas_afectadas == 0:
                    print("No Se Ha modificado")
                else:
                    print(f"Se Ha Modificado: {lineas_afectadas} Pedido(s)")
                    print("Pedido Actualizado con Exito")
                    continue
            elif op == "6":
                print("Vamos a Cambiar La Forma de Pagamento")
                print("1. Pix")
                print("2. Cartao")
                print("3. Dinheiro")
                while True:
                    try:
                        nueva_forma_de_pagamento=int(input("Indroduzca el Numero Correspondiente a la Opcion:"))
                        if nueva_forma_de_pagamento <= 0 :
                            print("Intente de Nuevo : 1. para Pix 2. para Cartao o 3. para Dinheiro")
                            continue
                        elif nueva_forma_de_pagamento > 3 :
                            print("Intente de Nuevo : 1. para Pix 2. para Cartao o 3. para Dinheiro")
                            continue
                        break
                    except ValueError:
                        print("Introduzca un Valor Numerico")
                if nueva_forma_de_pagamento == 1:
                    nueva_forma_de_pagamento= "PIX"
                elif nueva_forma_de_pagamento== 2:
                    nueva_forma_de_pagamento= "CARTAO"
                else:
                    nueva_forma_de_pagamento= "DINHEIRO" 
                cursor.execute("UPDATE pedidos SET forma_pagamento=? WHERE telefone = ?",
                (nueva_forma_de_pagamento,telefone_buscado,)
                )
                lineas_afectadas = cursor.rowcount
                if lineas_afectadas == 0:
                    print("No Se Ha modificado")
                else:
                    print(f"Se Ha Modificado: {lineas_afectadas} Pedido(s)")
                    print("Pedido Actualizado con Exito")
                    continue   
            elif op == "8":
                return                
    except ValueError:
        print("No hay Registros")
    conexao.commit()
    conexao.close()
        
def cancelar_pedido(invent_pro):
    try:
            with open("historial.json", "r") as f:
                pedidos_existentes = json.load(f)
                telefono_buscado=input("Introduzca el numero de telefono a buscar:")
                encontrado=False
                for  i , pedido in enumerate(pedidos_existentes, start=1):
                    temp_num=pedido.get("telefono","0") 
                    if telefono_buscado==temp_num:
                        encontrado=True
                        print(f"===== Pedido {i} =====")
                        print(pedido.get("nombre","Sin Nombre"))
                        print(pedido.get("direccion","Sin Direccion"))
                        print(pedido.get("telefono","Sin telefono"))
                        print()
                        print("Pedido: ")
                        lista_productos=pedido.get("productos",[])
                        for producto in lista_productos:
                            print(f"{producto['item']} - R$:{producto['cost']}")
                        print(f'Total: R$ {pedido.get("total","0")}')
                        eliminar=input("Desea Eliminar este pedido: S/N").lower()
                        if eliminar== "s":
                            for borrar in lista_productos:
                                reponer = borrar.get("item")
                                invent_pro[reponer] += 1
                            del pedidos_existentes[i-1]
                            with open("historial.json", "w") as f:
                                json.dump(pedidos_existentes, f, indent=4)
                                print("Pedido Cancelado con Exito")
                            break
                        else:
                            print("Pedido no Borrado")
                            break 
                if not encontrado:
                    print("Telefono no Encontrado")
                    return  
    except (FileNotFoundError, json.JSONDecodeError):
        print("No Hay Pedidos Todavia")
        

                        
