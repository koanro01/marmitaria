import json
from inventario import SABOR_MAR, BEBIDAS
        
def ver_historial():
    try:
        with open("marmitaria/historial.json", "r") as f:
            pedidos_existentes = json.load(f) 
            if len(pedidos_existentes) == 0:
               print("No hay pedidos todavía.")
               return
            total_ventas = 0                  
            for  i , pedido in enumerate(pedidos_existentes, start=1):
        
                print(f"===== Pedido {i} =====")
                print(pedido.get("nombre","Sin Nombre"))
                print(pedido.get("direccion","Sin Direccion"))
                print(pedido.get("telefono","Sin telefono"))
                print()
                print("Pedido: ")
                lista_productos=pedido.get("productos",[])
                total_ventas+=pedido.get("total",0)
                for producto in lista_productos:
                    print(f"{producto['item']} - R$:{producto['cost']}")
                print(f'Total: R$ {pedido.get("total","0")}')
            print()
        
            print("\n ===== RESUMEN DEL DIA =====")
            cantidad_pedidos = len(pedidos_existentes)
            print(f"Pedidos Realizados: {cantidad_pedidos}")
            print(f"Total vendido: R$: {total_ventas}")
        
            borrar_lista=input("Desea Borrar El Historial S/N").lower()
            if borrar_lista== "s":
                with open("marmitaria/historial.json", "w") as f:
                    json.dump([],f)
                    print("Historial Borrado con Exito")
    except (FileNotFoundError, json.JSONDecodeError):
        print("No hay Pedidos Todavia") 
        
def caja_del_dia ():
    try:
        with open("marmitaria/historial.json", "r") as f:
            pedidos_existentes = json.load(f)
            cantidad_pedidos=0
            total_ventas=0
            if len(pedidos_existentes) == 0:
                print("No hay pedidos todavía.")
                return
            ventas_productos = {}
            for pedido in pedidos_existentes:
                cantidad_pedidos+=1
                total_ventas=total_ventas+pedido.get("total",0)
                lista_productos=pedido.get("productos",[])
                for producto in lista_productos:
                    item = producto.get("item")
                    if item not in ventas_productos:
                        ventas_productos.update({item : 0})
                    ventas_productos[item] += 1
            print("===== CAJA DEL DIA =====")
            print(f"Pedidos realizados:{cantidad_pedidos}")
            print(f"Total vendido:R$ {total_ventas}")
            print("===== PRODUCTOS VENDIDOS =====")
            marmi_top = ""
            canti_mar_top = 0
            beb_top = ""
            canti_beb_top = 0
            ventas_marmitas={}
            ventas_bebidas={}
            for itm, canti in ventas_productos.items():
                print(f"{itm} ----- Vendidos: {canti}")
                if itm in SABOR_MAR.values():
                    ventas_marmitas.update({itm : canti})
                elif itm in BEBIDAS.values():
                    ventas_bebidas.update({itm : canti})    
                
            for itm, canti in ventas_marmitas.items():
                if canti > canti_mar_top:
                    marmi_top=itm
                    canti_mar_top=canti
            if len(ventas_marmitas)==0:
                print("Aun No Se Han Vendido Marmitas")
            else:
                print("===== MARMITA MAS VENDIDA =====")
                print(f"{marmi_top} Unidades Vendidas: {canti_mar_top}")
            for itm, canti in ventas_bebidas.items():
                if canti > canti_beb_top:
                    beb_top=itm
                    canti_beb_top=canti
            if len(ventas_bebidas)==0:
                print("Aun No Se Han Vendido BEBIDAS")
            else:
                print("===== BEBIDAS MAS VENDIDA =====")
                print(f"{beb_top} Unidades Vendidas: {canti_beb_top}")        
            
    except (FileNotFoundError, json.JSONDecodeError):
        print("NO HAY REGISTROS AUN")       