### Sitema Marmitaria

class Client :
    def __init__(self, name, number, address,):
        self.name = name
        self.number = number
        self.address = address
        
class Product :
    def __init__(self, item, cost):
        self.item = item
        self.cost = cost
        
        
class Pedido :
    def __init__(self, client_obj, list_prod):
        self.client_obj=client_obj
        self.list_prod=list_prod
        
    def calcular_total(self):
        total = 0
        for element in self.list_prod:
            total += element.cost
        return total
        
    def mostrar_pedido(self):
        print(f"Nombre del Cliente: {self.client_obj.name}")
        print(f"Telefono: {self.client_obj.number}")
        print(f"Direccion: {self.client_obj.address}")
        for element in self.list_prod:
            print(f"Producto: {element.item}  R$:{element.cost}")
        
            
cliente = Client("Antonio", "459991212", "Rua Urbano Caldeira 696")
producto = Product("Marmita de bife", 25)
producto2 = Product("cocacola",5)
pedido= Pedido(cliente,[producto,producto2])
pedido.mostrar_pedido()
print(f"Total: {pedido.calcular_total()}")
