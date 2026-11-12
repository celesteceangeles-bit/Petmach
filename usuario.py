class Usuario:

    def __init__(self, nombre, edad, vivienda, tiempo_disponible, otros_animales):
        self.nombre = nombre
        self.edad = edad
        self.vivienda = vivienda
        self.tiempo_disponible = tiempo_disponible
        self.otros_animales = otros_animales

    def mostrar_informacion(self):
        return f"{self.nombre}, {self.edad} años - Vive en {self.vivienda}"