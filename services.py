from models import Client, Pedido
from pedidos import cantidad_de_pedidos
from database import guardar_pedido_db, conectar
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
   try:
       pedido = cantidad_de_pedidos(invent_pro, conexao)
       if len(pedido) == 0:
           return

       pedido_f = Pedido(cliente, pedido, tipo_entrega, taxa_entrega, forma_pagamento)
       pedido_f.mostrar_pedido()

       guardar_pedido_db(pedido_f, conexao)
       conexao.commit()
   except (sqlite3.Error, ValueError) as e:
       conexao.rollback()
       print(f"No se pudo guardar el pedido: {e}")
   finally:
       conexao.close()