from models import Client, Pedido
from pedidos import cantidad_de_pedidos
from database import guardar_pedido_db, conectar, cargar_inventario_db
import sqlite3
from entradas import pedir_si_no, pedir_decimal, pedir_forma_pago

def nuevo_pedido(invent_pro):
   nombre = input("Nombre: ")
   telefono = input("Telefono: ")
   direccion = input("Direccion: ")
   if pedir_si_no("Entrega a Domicilio?"):
      tipo_entrega = "Entrega"
      taxa_entrega = pedir_decimal("Introduzca el Valor de la Taxa de Entrega: ")
   else:
      tipo_entrega = "Balcao"
      taxa_entrega = 0.0

   forma_pagamento = pedir_forma_pago()

   cliente = Client(nombre, telefono, direccion)
   conexao = conectar()
   pedido_guardado = False
   try:
       pedido = cantidad_de_pedidos(invent_pro, conexao)
       if len(pedido) == 0:
           conexao.rollback()
           return

       pedido_f = Pedido(cliente, pedido, tipo_entrega, taxa_entrega, forma_pagamento)
       pedido_f.mostrar_pedido()
       if pedir_si_no("¿Confirmar pedido?"):
           guardar_pedido_db(pedido_f, conexao)
           conexao.commit()
           pedido_guardado = True
       else:
           conexao.rollback()
           return
   except (sqlite3.Error, ValueError) as e:
       conexao.rollback()
       print(f"No se pudo guardar el pedido: {e}")
   finally:
       conexao.close()
   if pedido_guardado:
        try:
            invent_pro.update(cargar_inventario_db())
        except sqlite3.Error as e:
            print(f"El pedido se guardó, pero no se pudo actualizar el inventario en memoria: {e}")