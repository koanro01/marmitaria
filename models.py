
class Client :
    def __init__(self, name, number, address,):
        self.name = name
        self.number = number
        self.address = address
        
class Product :
    def __init__(self, item, cost,):
        self.item = item
        self.cost = cost
          
class Pedido :
    def __init__(self, client_obj, list_prod, tipo_entrega, taxa_entrega, forma_pagamento):
        self.client_obj=client_obj
        self.list_prod=list_prod
        self.tipo_entrega=tipo_entrega
        self.taxa_entrega=taxa_entrega
        self.forma_pagamento=forma_pagamento
        
    def calcular_total(self):
        total = 0
        for element in self.list_prod:
            total += element.cost
            
        return total
 
    def mostrar_pedido(self,):
            print(f"Nombre del Cliente: {self.client_obj.name}")
            print(f"Telefono: {self.client_obj.number}")
            print(f"Direccion: {self.client_obj.address}")
            print(f"Tipo: {self.tipo_entrega}")
            print(f"Taxa de Entrega: {self.taxa_entrega}")
            print(f"Forma de Pagamento: {self.forma_pagamento}")
            for element in self.list_prod:
                print(f"Producto: {element.item}  R$:{element.cost}")
            print(f"Total: {self.calcular_total_final()}")
            
    def calcular_total_final(self):
        total_final=self.calcular_total()+self.taxa_entrega
        return total_final