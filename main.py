from database import (
    crear_banco,
    obtener_pedidos_por_telefono,
    ver_historial_completo_db,
    caja_del_dia_db,
    editar_pedido_db,
    cancelar_pedido_db,
    iniciar_inventario_db,
    cargar_inventario_db,
    repor_inventario_db,
    listar_pedidos_db
)
import sqlite3
from pantallas import mostrar_pedidos
from inventario import ver_menu
from services import nuevo_pedido
from entradas import pedir_entero_positivo

def menu_principal(invent_pro):
    
    salir = False
    while salir == False:
        print("=== MARMITARIA ===")
        print("1. Nuevo pedido")
        print("2. Ver Menu")
        print("3. Ver Historial")
        print("4. Buscar Pedido por Telefono")
        print("5. Editar Pedido")
        print("6. Cancelar Pedido")
        print("7. Caja del Dia:")
        print("8. Actualizar Inventario")
        print("9. Salir")
        try:
            opcion = int(input("Seleccione una opcion: "))
        except ValueError:
            print("Introduzca un numero del 1 al 9")
            continue
        
        if opcion == 1:
           nuevo_pedido(invent_pro)
           invent_pro = cargar_inventario_db()     
        elif opcion == 2:
           ver_menu(invent_pro, "M")
           ver_menu(invent_pro, "B") 
        elif opcion == 3:
           ver_historial_completo_db()
        elif opcion == 4:
            telefone_buscado = input("Telefono del cliente: ")
            mostrar_pedidos(obtener_pedidos_por_telefono(telefone_buscado))
        elif opcion == 5:
           telefone_buscado = input("Telefono del cliente: ")
           editar_pedido_db(telefone_buscado)
           invent_pro = cargar_inventario_db()
        elif opcion == 6:
           try:
               pedidos_encontrados = listar_pedidos_db()
               if pedidos_encontrados:
                  etiquetas = ["Id", "Nombre", "Telefono", "Total"]
                  for pedido in pedidos_encontrados:
                     for etiqueta, valor in zip(etiquetas, pedido):
                        print(f"{etiqueta}: {valor}")
                     print("-" * 20)
                  id_pedido = pedir_entero_positivo("ID del pedido a cancelar: ")
                  cancelar_pedido_db(id_pedido)
                  invent_pro = cargar_inventario_db()
               else :
                  print("No hay pedidos para cancelar")
           except (ValueError, sqlite3.Error) as e:
               print(f"No se pudo cancelar el pedido: {e}")
        elif opcion == 7:
           caja_del_dia_db()
        elif opcion == 8:
           repor_inventario_db()
           invent_pro = cargar_inventario_db()
        elif opcion == 9:
           salir=True
        else:
           print("Opcion invalida, elija un numero del 1 al 9")
    return opcion

crear_banco()
iniciar_inventario_db()
invent_pro = cargar_inventario_db()

menu_principal(invent_pro)
