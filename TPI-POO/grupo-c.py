# TPI - Paradigma POO (Grupo C) Integrantes:
# - Rafael Gorrochategui
# - Juan Pablo Iurato
# - Franco Caraffa
# - Zahir Argañaraz

import hashlib
from datetime import datetime, timedelta

class Configuracion:
  def __init__(self, clave_sistema):
    self.__hashClave = self.__generar_hash(clave_sistema)
  def __generar_hash (self, clave):
    return hashlib.sha256(clave.encode()).hexdigest()
  def validar_clave(self, clave_ingresada):
    return self.__generar_hash(clave_ingresada) == self.__hashClave

class Transporte:
  def __init__(self, nroID, patente):
    self.__nroID = nroID
    self.__patente = patente
  def get_patente(self):
    return self.__patente
  def get_nroID(self):
    return self.__nroID

class Camion(Transporte):
  def __init__(self, nroID, patente, capacidadKg):
    super().__init__(nroID, patente)
    self.__capacidadKg = capacidadKg

class Avion(Transporte):
  def __init__(self, nroID, patente, tiempoVuelo):
    super().__init__(nroID, patente)
    self.__tiempoVuelo = tiempoVuelo

class Despacho:
  def __init__(self):
    self.fecha_despacho = None
    self.transporte = None
    self.estado = False
    self.lista_contenedores = []
  def agregar_contenedor(self, contenedor):
    self.lista_contenedores.append(contenedor)
  def get_peso_total(self)->float:
    PESO_DESPACHO = 0
    for contenedor in self.lista_contenedores:
      PESO_DESPACHO += contenedor.get_peso_total()
    return PESO_DESPACHO
  def asignar_transporte(self, transporte:Transporte):
    self.transporte = transporte
  def fecha_correcta (self,fecha_a, fecha_b):
    if (self.fecha_despacho is not None):
        if (self.fecha_despacho >= fecha_a and self.fecha_despacho <= fecha_b):
            return self.get_peso_total()
    return 0
  def asignar_fecha(self):
    self.fecha_despacho = datetime.now()
  def estado_despachado(self):
    self.estado = True
  def __str__(self):
    tipo = type(self.transporte).__name__
    res = (f"\n[PEDIDO DESPACHADO]\n"
           f"Identidad del Transporte (ID: {self.transporte.get_nroID()}): {tipo} {self.transporte.get_patente()}\n"
           f"Estado: DESPACHADO exitosamente.\n"
           f"Carga Total: {self.get_peso_total()} kg.\n"
           f"Verificación de Seguridad: Hash SHA256 Validado.\n"
           f"Detalle de la Carga:\n"
           f"-------------------------------------------------")
    for i, c in enumerate(self.lista_contenedores):
      res += f"\nContenedor {i+1} (Peso: {c.get_peso_total()} kg), contiene:"
      for j, p in enumerate(c.paquetes, 1):
        res += f"\n* Paquete {j} ({p.get_peso()} kg)"
    return res

class Paquete:
  def __init__(self, peso):
    self.__peso = peso
  def get_peso(self):
   return self.__peso

class Contenedor:
  def __init__(self):
    self.paquetes = []
  def agregar_paquete(self, paquete):
    self.paquetes.append(paquete)
  def get_peso_total(self)->float:
    PESO_TOTAL = 0
    for paquete in self.paquetes:
      PESO_TOTAL += paquete.get_peso()
    return PESO_TOTAL

class SistemaLogistica:
    def __init__(self, sist: Configuracion):
        self.configuracion = sist 
        self.despachos = []
    def agregar_despacho(self, despacho: Despacho):
        self.despachos.append(despacho)
    def calcular_sumatoria_pesos(self, fecha_a, fecha_b):
        TOTAL = 0
        for despacho in self.despachos:
            TOTAL += despacho.fecha_correcta(fecha_a, fecha_b)
        return TOTAL
    def despachar(self, password, carga: Despacho, transporte): 
        if self.configuracion.validar_clave(password) and not carga.estado:
            carga.asignar_transporte(transporte)
            carga.asignar_fecha()
            carga.estado_despachado()
            print(carga) 
        else: 
            print("Despacho Fallido")

if __name__ == "__main__":
    clave = input("Cree una clave para el sistema: ")
    config = Configuracion(clave)
    sistema = SistemaLogistica(config)

    print("\n--- CARGA DE TRANSPORTE ---")
    tipo = input("Avion o Camion: ").capitalize()
    nroID = int(input("Ingrese ID: "))
    patente = input("Ingrese Patente: ")
    if tipo == "Avion":
        capacidad = float(input("Capacidad en Kg: "))
        transporte = Avion(nroID, patente, capacidad)
    else:
        capacidad = float(input("Capacidad en Kg: "))
        transporte = Camion(nroID, patente, capacidad)

    despacho = Despacho()
    
    cant_cont = int(input("\nCantidad de contenedores a cargar: "))
    for i in range(cant_cont):
        print(f"\n> Carga Contenedor {i+1}:")
        contenedor = Contenedor()
        cant_paq = int(input(f" Cant. de paquetes del contenedor {i+1}?: "))
        for j in range(cant_paq):
            peso = float(input(f"    Peso paquete {j+1} (kg): "))
            contenedor.agregar_paquete(Paquete(peso))
        despacho.agregar_contenedor(contenedor)

    sistema.agregar_despacho(despacho)
    print("\nDespacho: ")
    pass_intento = input("Ingrese clave para despachar: ")
    
    sistema.despachar(pass_intento, despacho, transporte)

    opcion = input("\nQuiere ver el peso total por fecha? (s/n): ")

    if opcion.lower() == "s":
        inicio_txt = input("Fecha de inicio, en formato AAAA-MM-DD: ")
        fin_txt = input("Fecha de fin, en formato AAAA-MM-DD: ")

        fecha_inicio = datetime.strptime(inicio_txt, "%Y-%m-%d")
        fecha_fin = datetime.strptime(fin_txt, "%Y-%m-%d") + timedelta(days=1)

        total = sistema.calcular_sumatoria_pesos(fecha_inicio, fecha_fin)
        print(f"Peso total en el periodo elegido: {total} kg")