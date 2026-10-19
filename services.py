from models import Client, Pedido
from pedidos import cantidad_de_pedidos
from database import guardar_pedido_db
import sqlite3

def nuevo_pedido(invent_pro):
   nombre = input("Nombre: ")
   telefono = input("Telefono: ")
   direccion = input("Direccion: ")
   taxa_entrega=0.0
   forma_de_pagamento=0
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
               taxa_entrega = float(input("Introduzca el Valor de la Taxa de Entrega:"))

               if taxa_entrega < 0:
                 print("La Taxa No Puede Ser Negativa")
                 continue
               break

            except ValueError:
               print("Introduzca un Valor Numerico")
         break
      
   print("===== FORMA DE PAGAMENTO =====")   
   print("1. Pix")
   print("2. Cartao")
   print("3. Dinheiro")
   while True:
      try:
         forma_de_pagamento=int(input("Indroduzca el Numero Correspondiente a la Opcion:"))
         if forma_de_pagamento <= 0 :
            print("Intente de Nuevo : 1. para Pix 2. para Cartao o 3. para Dinheiro")
            continue
         elif forma_de_pagamento > 3 :
            print("Intente de Nuevo : 1. para Pix 2. para Cartao o 3. para Dinheiro")
            continue
         break
      except ValueError:
         print("Introduzca un Valor Numerico")
   if forma_de_pagamento == 1:
      forma_pagamento= "PIX"
   elif forma_de_pagamento== 2:
      forma_pagamento= "CARTAO"
   else:
      forma_pagamento= "DINHEIRO"
     

   cliente = Client(nombre, telefono, direccion)
   conexao = sqlite3.connect("marmitaria/marmitaria.db")
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