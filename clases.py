class Categoria:
    def __init__(self, id, nombre, descripcion, cargaTrabajo):
        self.id=id
        self.nombre=nombre
        self.descripcion=descripcion
        self.cargaTrabajo=cargaTrabajo
        self.lista_configuraciones=[]
        self.montoTotal=0

class Configuracion:
    def __init__(self, id, nombre, descripcion):
        self.id=id
        self.nombre=nombre
        self.descripcion=descripcion
        self.lista_recursos=[]
        self.montoTotal=0

class RecursosC:
    def __init__(self, id,cantidad):
        self.id=id
        self.cantidad=cantidad  


class Consumos:
    def __init__(self, nitCliente, idInstancia, tiempo,fechaHora):
        self.nitCliente=nitCliente
        self.idInstancia=idInstancia
        self.tiempo=tiempo
        self.fechaHora=fechaHora


class Factura:
    def __init__(self, id,fecha, monto, instancia, cliente, tiempo):
        self.id = id
        self.fecha = fecha
        self.monto=monto
        self.instancia=instancia
        self.recursos= []
        self.cliente=cliente
        self.tiempo=tiempo
