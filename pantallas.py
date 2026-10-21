

def mostrar_pedidos(pedidos):
    if not pedidos:
        print("No se encontraron pedidos con ese telefono.")
        return

    print("===== PEDIDOS ENCONTRADOS =====")
    for pedido in pedidos:
        print(f"Id: {pedido['id']}")
        print(f"Nombre: {pedido['nome']}")
        print(f"Telefono: {pedido['telefone']}")
        print(f"Direccion: {pedido['endereco']}")
        print(f"Total: {pedido['total']}")
        print(f"Fecha: {pedido['data']}")
        print(f"Hora: {pedido['hora']}")
        print(f"Tipo: {pedido['tipo']}")
        print(f"Taxa de Entrega: {pedido['taxa_entrega']}")
        print(f"Forma de Pagamento: {pedido['forma_pagamento']}")
        print("-" * 30)