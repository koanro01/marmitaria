from datetime import datetime
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "marmitaria.db")

def conectar():
    return sqlite3.connect(DB_PATH)

def crear_banco():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        telefone TEXT,
        endereco TEXT,
        total REAL
      
    )
    """)
    cursor.execute("PRAGMA table_info(pedidos)")
    columnas = cursor.fetchall()
    nom_columnas=[]
    for tup in columnas:
        nom_columnas.append(tup[1])
    if "data" not in nom_columnas:
        cursor.execute("ALTER TABLE pedidos ADD COLUMN data TEXT;")
        
    if "hora" not in nom_columnas:
        cursor.execute("ALTER TABLE pedidos ADD COLUMN hora TEXT;")
    
    if "tipo" not in nom_columnas:
            cursor.execute("ALTER TABLE pedidos ADD COLUMN tipo TEXT;")
            
    if "taxa_entrega" not in nom_columnas:
            cursor.execute("ALTER TABLE pedidos ADD COLUMN taxa_entrega REAL;")
    if "forma_pagamento" not in nom_columnas:
                cursor.execute("ALTER TABLE pedidos ADD COLUMN forma_pagamento TEXT;")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS itens_pedido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER,
        item TEXT,
        cost REAL,
        FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
    )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto TEXT,
        quantidade INTEGER)
        """)

    conexao.commit()
    conexao.close()
    
def iniciar_inventario_db():
    
    conexao = conectar()
    cursor = conexao.cursor() 
    
    cursor.execute("SELECT COUNT(*) FROM inventario;")
    elementos_en_tabla = cursor.fetchone()
    
    if elementos_en_tabla[0]==0:
        productos = [
                ("Carne ao Molho", 0),
                ("Coxinha de frango Frito", 0),
                ("File de frango Grelhado", 0),
                ("Linguicinha Assada", 0),
                ("Strogonoff de Frango", 0),
                ("Bife acebolado", 0),
                ("Bisteca Suina", 0),
                ("Cocacola de Lata", 0),
                ("Cocacola 600ml", 0),
                ("Guarana Lata",0)
                ]
        insertar= "INSERT INTO inventario (producto,quantidade) VALUES (?,?)"
        cursor.executemany(insertar,productos)
        conexao.commit()
        conexao.close()
    
    else:
        print("Inventario Ya Inicializado")
        
def cargar_inventario_db():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT producto, quantidade FROM inventario")
    prod_en_inv=cursor.fetchall()
    conexao.close()
    dict_inv={}
    for llave, valor in prod_en_inv:
        dict_inv[llave]=valor
    return dict_inv  
        
def repor_inventario_db():       
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT producto, quantidade FROM inventario")
    inventario_actual = cursor.fetchall()
    print("--- ACTUALIZACIÓN DE INVENTARIO ---")
    for producto, cantidad_actual in inventario_actual:
        while True:
            try:
                entrada = input(f"Nueva cantidad para '{producto}' (Actual: {cantidad_actual}): ")
                nueva_cantidad = int(entrada)
                if nueva_cantidad < 0:
                    print("Por favor, introduce un número mayor o igual a 0.")
                    continue

                cursor.execute(
                "UPDATE inventario SET quantidade = ? WHERE producto = ?",
                    (nueva_cantidad, producto),
            )
                break

            except ValueError:
                print("Entrada no válida. Por favor, introduce un número entero.")

    conexao.commit()
    print("\n¡Inventario actualizado con éxito!")
    conexao.close()

def guardar_pedido_db(pedido_f, conexao):
    cursor = conexao.cursor()
    ahora=datetime.now()
    data=ahora.strftime("%d/%m/%Y")
    hora=ahora.strftime("%H:%M:%S")
    total=pedido_f.calcular_total_final()
    cursor.execute(
    "INSERT INTO pedidos (nome, telefone, endereco, total, data, hora, tipo, taxa_entrega, forma_pagamento) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
    (
        pedido_f.client_obj.name,
        pedido_f.client_obj.number,
        pedido_f.client_obj.address,
        total,
        data,
        hora,
        pedido_f.tipo_entrega,
        pedido_f.taxa_entrega,
        pedido_f.forma_pagamento
    )     
    )
    pedido_id = cursor.lastrowid
    for producto in pedido_f.list_prod:
        cursor.execute(
        "INSERT INTO itens_pedido (pedido_id, item, cost) VALUES (?, ?, ?)",
        (
            pedido_id,
            producto.item,
            producto.cost
        )
    )

def ver_pedidos_db():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM pedidos")

    pedidos = cursor.fetchall()

    conexao.close()

    for pedido in pedidos:
        print(pedido)

def buscar_pedido_db(telefone_buscado):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM pedidos WHERE telefone = ?",
    
    (telefone_buscado,)
    )
    pedidos=cursor.fetchall()
    
    conexao.close()
    print ("===== PEDIDOS ENCONTRADOS =====")
    for pedido in pedidos:
        for i, ped in enumerate(pedido):
            if i == 0:
                print(f"Id: {ped}")
            elif i == 1:
                print(f"Nombre: {ped}")
            elif i == 2:
                print(f"Telefono: {ped}")
            elif i == 3:
                print(f"Direccion: {ped}")
            elif i == 4:
                print(f"Total: {ped}")
            elif i == 5:
                print(f"Fecha: {ped}")
            elif i == 6:
                print(f"Hora: {ped}")
            elif i == 7:
                print(f"Tipo: {ped}")
            elif i == 8:
                print(f"Taxa de Entrega: {ped}")
            elif i == 9:
                print(f"Forma de Pagamento: {ped}")
                
        print("-" * 30)
    
    
def editar_pedido_db(telefone_buscado):
    from pedidos import cantidad_de_pedidos
    conexao = conectar()
    cursor = conexao.cursor()
    nueva_taxa_entrega=0.0
    try:

        buscar_pedido_db(telefone_buscado)
        id_a_modificar=int(input("Introduzca el Id del Pedido a Modificar:"))
        cursor.execute(" SELECT  id FROM pedidos WHERE id=? AND telefone=? ",
                       (id_a_modificar,telefone_buscado,))
        consulta=cursor.fetchone()
        if consulta is None:
            print("El Pedido no Existe")
            print("ó el Id que Introdujo no pertenece a este Usuario")
            return
        else:
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
                    cursor.execute("UPDATE pedidos SET nome = ? WHERE id=?",
                    (nuevo_nome,id_a_modificar,)
                    )
                    lineas_afectadas = cursor.rowcount
                    conexao.commit()
                    if lineas_afectadas == 0:
                        print("No Se Ha modificado")
                    else:
                        print(f"Se Ha Modificado: {lineas_afectadas} Pedido(s)")
                        print("Pedido Actualizado con Exito")
                        continue
                elif op == "2": 
                    print("Vamos a Cambiar el Telefono")
                    nuevo_telefone=input("Introduzca el Nuevo Telefono: ")
                    cursor.execute("UPDATE pedidos SET telefone = ? WHERE id=?",
                    (nuevo_telefone,id_a_modificar,)
                    )
                    lineas_afectadas = cursor.rowcount
                    conexao.commit()
                    if lineas_afectadas == 0:
                        print("No Se Ha modificado")
                    else:
                        print(f"Se Ha Modificado: {lineas_afectadas} Pedido(s)")
                        print("Pedido Actualizado con Exito")
                        continue   
                elif op == "3": 
                    print("Vamos a Cambiar La Direccion")
                    nueva_direccion=input("Introduzca la Nueva Direccion: ")
                    cursor.execute("UPDATE pedidos SET endereco = ? WHERE id=?",
                    (nueva_direccion,id_a_modificar,)
                    )
                    lineas_afectadas = cursor.rowcount
                    conexao.commit()
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
                            nueva_taxa_entrega=0.0
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
                    cursor.execute("""
                    SELECT SUM(cost)
                    FROM itens_pedido
                    WHERE pedido_id = ?
                    """, (id_a_modificar,))
                    subtotal = cursor.fetchone()[0]
                    total_final = subtotal + nueva_taxa_entrega
                    cursor.execute("UPDATE pedidos SET tipo = ?, taxa_entrega=?, total=? WHERE id=?",
                    (tipo_entrega,nueva_taxa_entrega,total_final,id_a_modificar,)
                    )
                    lineas_afectadas = cursor.rowcount
                    conexao.commit()
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
                    cursor.execute("""
                    SELECT SUM(cost)
                        FROM itens_pedido
                        WHERE pedido_id = ?
                    """, (id_a_modificar,))
                    subtotal = cursor.fetchone()[0] or 0
                    if subtotal == 0:
                        print("No se puede modificar la tasa: el pedido no tiene productos")
                        continue

                    total_final = subtotal + nueva_taxa_entrega
                    cursor.execute(
                        "UPDATE pedidos SET taxa_entrega = ?, total = ? WHERE id = ?",
                        (nueva_taxa_entrega, total_final, id_a_modificar)
                    )
                    lineas_afectadas = cursor.rowcount
                    conexao.commit()
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
                    cursor.execute("UPDATE pedidos SET forma_pagamento=? WHERE id=?",
                    (nueva_forma_de_pagamento,id_a_modificar,)
                    )
                    lineas_afectadas = cursor.rowcount
                    conexao.commit()
                    if lineas_afectadas == 0:
                        print("No Se Ha modificado")
                    else:
                        print(f"Se Ha Modificado: {lineas_afectadas} Pedido(s)")
                        print("Pedido Actualizado con Exito")
                        continue   
                elif op == "7":
                    cursor.execute("""
                    SELECT id, item, cost
                    FROM itens_pedido
                    WHERE pedido_id = ?
                    """, (id_a_modificar,))
                    produ=cursor.fetchall()
                    for i, pro in enumerate(produ):
                        print(f"===== Producto {i+1} =====")
                        print(f"Id: {pro[0]}")
                        print(f"Producto: {pro[1]}")
                        print(f"Precio: {pro[2]}")
                        print("-"*30)
                    print("1. Agregar producto")
                    print("2. Quitar producto")
                    print("3. Volver")
                    print("")
                    opci=input("Indrodozca el Numero Correspondiente a la Opcion Requerida:")
                    if opci == "1":
                       invent_pro = cargar_inventario_db()
                       nuevos_productos = cantidad_de_pedidos(invent_pro, conexao)
                       for producto in nuevos_productos:
                           cursor.execute("""
                            INSERT INTO itens_pedido (pedido_id, item, cost) 
                            VALUES (?, ?, ?)
                            """,(id_a_modificar, producto.item, producto.cost,))
                       cursor.execute(
                       "SELECT SUM(cost) FROM itens_pedido WHERE pedido_id = ?",
                       (id_a_modificar,)
                       )
                       sum_pro_restantes = cursor.fetchone()
                       cursor.execute("""
                       SELECT taxa_entrega
                       FROM pedidos
                       WHERE id = ?
                       """, (id_a_modificar,))
                       taxa_entre_restante = cursor.fetchone()
                       subtotal_sum = sum_pro_restantes[0] or 0
                       subtotal_taxa = taxa_entre_restante[0] or 0
                       total_restantes = subtotal_sum + subtotal_taxa
                       cursor.execute(
                       "UPDATE pedidos SET total = ? WHERE id = ?", 
                       (total_restantes,id_a_modificar,) )
                       conexao.commit()
                       print(f"Éxito: Se guardaron {len(nuevos_productos)} productos en el pedido {id_a_modificar}.")
                    elif opci == "2":
                        pro_id_modi=input("Introduzca el Id del Producto a Quitar:")
                        cursor.execute("""
                        SELECT item, cost
                        FROM itens_pedido
                        WHERE id = ? AND pedido_id= ?
                        """, (pro_id_modi,id_a_modificar,))
                        produ_encontrado=cursor.fetchone()
                        if produ_encontrado == None:
                            print("Producto No Encontrado")
                        else:
                            cursor.execute("""
                            SELECT COUNT(*)
                            FROM itens_pedido
                            WHERE pedido_id = ?
                            """, (id_a_modificar,))
                            cantidad_productos = cursor.fetchone()[0]
                            if cantidad_productos== 1:
                                print("No se Pudo eliminar Porque Solo Queda un Producto")
                                print("Busque la Opcion * CANCELAR PEDIDO *")
                            else:
                                producto_eliminar=produ_encontrado[0]
                                precio_eliminar=produ_encontrado[1]   
                                print(f"vamos a quitar {producto_eliminar} con valor de {precio_eliminar}")
                                cursor.execute(
                                "UPDATE inventario SET quantidade = quantidade + ? WHERE producto = ?", 
                                (1,producto_eliminar,) )
                                cursor.execute(
                                "DELETE FROM itens_pedido WHERE id = ? AND pedido_id= ?",
                                (pro_id_modi,id_a_modificar,)
                                )
                                cursor.execute(
                                "SELECT SUM(cost) FROM itens_pedido WHERE pedido_id = ?",
                                (id_a_modificar,)
                                )
                                sum_pro_restantes = cursor.fetchone()
                                cursor.execute("""
                                SELECT taxa_entrega
                                FROM pedidos
                                WHERE id = ?
                                """, (id_a_modificar,))
                                taxa_entre_restante = cursor.fetchone()
                                subtotal_sum = sum_pro_restantes[0] or 0
                                subtotal_taxa = taxa_entre_restante[0] or 0
                                total_restantes = subtotal_sum + subtotal_taxa
                                cursor.execute(
                                "UPDATE pedidos SET total = ? WHERE id = ?", 
                                (total_restantes,id_a_modificar,) )
                                conexao.commit()
                    elif opci == "3":
                        print("Saliendo")
                        return
                elif op == "8":
                    return                
    except ValueError:
        print("No hay Registros")
    conexao.commit()
    conexao.close()
    
def cancelar_pedido_db(telefone_buscado):
    conexao = conectar()
    try:
        with conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id FROM pedidos WHERE telefone = ? ",
                (telefone_buscado,)         
                        
            )
            pedidos_encontrados = cursor.fetchall()
            if not pedidos_encontrados:
                print("No existen pedidos con ese teléfono.")
                return
            for pedido in pedidos_encontrados:
                print(pedido[0])
            id_eli=int(input("Inroduzca el numero de ID a cancelar:"))
            if any(id_eli == pedido[0] for pedido in pedidos_encontrados):
                cursor.execute(
                """
                SELECT item
                FROM itens_pedido
                WHERE pedido_id=?
                """,
                (id_eli,)
                )
                productos_pedido = cursor.fetchall()
            else:
                print("Este id no pertenece a este pedido")
                return
            
            if  not productos_pedido:
                print("No hay productos asociados a este pedido.")
                raise sqlite3.Error ("Deshaciendo los cambios")
            for producto in productos_pedido:
                cursor.execute("""UPDATE inventario
                SET quantidade = quantidade + 1
                WHERE producto = ?""",
                (producto[0],)
                )
                invent_actulizado=cursor.rowcount
                if invent_actulizado == 0:
                    print("No Se Han actualizado Producto(s)")
                    raise sqlite3.Error ("Deshaciendo los cambios")
                else:
                    print("Actualizado con Exito")
                    print(f"Se Ha Modificado: {invent_actulizado} Producto(s)")
            cursor.execute(
                "DELETE FROM itens_pedido WHERE pedido_id = ?",
                (id_eli,)   
            )
            produ_elim=cursor.rowcount
            cursor.execute("DELETE FROM pedidos WHERE id = ?",
                (id_eli,)           
            )
            pedido_eliminado = cursor.rowcount
            if produ_elim == 0:
                print("No Se Han Eliminado Producto(s)")
                raise sqlite3.Error ("Deshaciendo los cambios")
            else:
                print("Eliminado con Exito")
                print(f"Se Ha Modificado: {produ_elim} Producto(s)")
            if pedido_eliminado == 0:
                print("No Se Han Eliminado Pedidos(s)")
                raise sqlite3.Error ("Deshaciendo los cambios")
            else:
                print(f"Se Ha Modificado: {pedido_eliminado} Pedido(s)")
            conexao.commit()
    except sqlite3.Error as e:
        print(f"Se detectó un fallo: {e}")
    finally:    
        conexao.close() 
    
def ver_historial_db():
    conexao = conectar()
    
    cursor = conexao.cursor()
    
    cursor.execute("SELECT * FROM pedidos")
    
    pedidos = cursor.fetchall()
    conexao.close()
    
    cantidad_pedidos = 0
    total_ventas = 0
    if len(pedidos)==0:
        print("NO HAY PEDIDOS TODAVIA")
    else:
        for i , pedido in enumerate(pedidos,start=1):
            cantidad_pedidos +=1
            total_ventas+= pedido[4]
            print(f"Nombre: {pedido[1]}")
            print(f"Telefono: {pedido[2]}")
            print(f"Direccion: {pedido[3]}")
            print(f"Total: R$ {pedido[4]}")
            print()
    
        print("===== RESUMEN DEL DIA =====")
        print(f"{cantidad_pedidos} Pedidos Realizados")
        print(f"Total Vendido R$:{total_ventas}")
        
def ver_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

    tabelas = cursor.fetchall()

    conexao.close()

    print(tabelas) 
    
def ver_itens_db():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM itens_pedido")

    itens = cursor.fetchall()

    conexao.close()

    for item in itens:
        print(item) 
        
def ver_historial_completo_db():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
    """
    SELECT *
    FROM pedidos
    LEFT JOIN itens_pedido
    ON pedidos.id = itens_pedido.pedido_id
    """
    )
        
    resultado = cursor.fetchall()
    pedido_atual = None
    for fila in resultado:
        if pedido_atual!= fila[0]:
           pedido_atual = fila[0]
           print(f"===== Pedido {pedido_atual} =====")
           print(f"Cliente: {fila[1]}")
           print(f"Telefono: {fila[2]}")
           print(f"Direccion: {fila[3]}")
           print(f"Total: {fila[4]}")
        if fila[12] is None:
            print("Sin productos asociados.")
        else:
            print(f"Producto: {fila[12]}  R$: {fila[13]}")


    conexao.close()         
    
def caja_del_dia_db():
    agora = datetime.now()
    data = agora.strftime("%d/%m/%Y")
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""SELECT COUNT(*) FROM pedidos WHERE data = ?
        """, (data,))
    cantidad_pedidos = cursor.fetchone()
    if cantidad_pedidos[0] == 0:
        print()
        print("HOY NO HAY PEDIDOS TODAVIA")
        print()
        return
    else:
        cursor.execute("""SELECT SUM(total) FROM pedidos WHERE data = ?
            """, (data,))
        total_ventas = cursor.fetchone()
        
        cursor.execute("""SELECT SUM(taxa_entrega) FROM pedidos WHERE data = ?
        """, (data,))
        total_taxa_entregas = cursor.fetchone()
        
        cursor.execute("""SELECT itens_pedido.item, pedidos.data, COUNT(*) 
        FROM itens_pedido  INNER JOIN pedidos ON itens_pedido.pedido_id = pedidos.id 
        WHERE pedidos.data = ?  GROUP BY item
        ORDER BY COUNT(*) DESC """, (data,))
        pedidos = cursor.fetchall()
        
        cursor.execute("""SELECT itens_pedido.item, pedidos.data, COUNT(*) 
        FROM itens_pedido  INNER JOIN pedidos ON itens_pedido.pedido_id = pedidos.id 
        WHERE pedidos.data = ?  GROUP BY item
        ORDER BY COUNT(*) DESC LIMIT 1""", (data,))
        mas_vedido=cursor.fetchone()
        
        
        cursor.execute("""
        SELECT forma_pagamento, total
        FROM pedidos
        WHERE data = ?
        """, (data,))
        resultados=cursor.fetchall()
        
        conexao.close()
        print()
        print("===== CAJA DEL DIA =====")
        print(f"Cantidad de Pedidos: {cantidad_pedidos[0]}")
        print(f"Ventas de Productos: {total_ventas[0]-total_taxa_entregas[0]}")
        print(f"Taxas de Entrega: {total_taxa_entregas[0]}")
        print(f"Total Recebido: {total_ventas[0]}")
        print()
        print("===== PRODUCTOS VENDIDOS =====")
        for fila in pedidos:
            print(f"{fila[0]} ----- Vendidos: {fila[2]}")
        
        print()
            
        print("===== PRODUCTO MAS VENDIDO =====")
        print(f"{mas_vedido[0]} -------- {mas_vedido[2]}")
        print()
        total_pix = 0
        total_cartao = 0
        total_dinheiro = 0
        for llave, valor in resultados:
            if llave == "PIX":
                total_pix+=valor
            elif llave == "CARTAO":
                total_cartao+=valor
            else:
                total_dinheiro+=valor
            
        print("===== TOTAL DE CADA FORMA DE PAGAMENTO =====")
        print(f"Total Pix: {total_pix}")
        print(f"Total Cartao: {total_cartao}")
        print(f"Total Dinheiro: {total_dinheiro}")
        print()
        print()
        