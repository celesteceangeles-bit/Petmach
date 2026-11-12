
class Mascota:

    def __init__(
        self,
        nombre,
        especie,
        edad,
        tamaño,
        personalidad,
        nivel_actividad,
        imagen
    ):
        self.nombre = nombre
        self.especie = especie
        self.edad = edad
        self.tamaño = tamaño
        self.personalidad = personalidad
        self.nivel_actividad = nivel_actividad
        self.imagen = imagen

    def mostrar_informacion(self):
        return f"{self.nombre} - {self.especie} - {self.edad} años"
