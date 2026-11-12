
class Compatibilidad:

    def __init__(self, usuario, mascota):
        self.usuario = usuario
        self.mascota = mascota
        self.porcentaje = 0

    def calcular(self, actividad_preferida):
        puntos = 0
        total = 4

        # 1. Compatibilidad según la vivienda
        if self.usuario.vivienda == "Casa":
            puntos += 1
        elif self.usuario.vivienda == "Departamento":
            if self.mascota.tamaño == "Pequeño":
                puntos += 1
            elif self.mascota.especie in [
                "Gato", "Hámster", "Canario", "Periquito"
            ]:
                puntos += 1

        # 2. Compatibilidad según el tiempo disponible
        if self.usuario.tiempo_disponible == "Mucho":
            puntos += 1
        elif self.usuario.tiempo_disponible == "Medio":
            if self.mascota.nivel_actividad in ["Bajo", "Medio"]:
                puntos += 1
        elif self.usuario.tiempo_disponible == "Poco":
            if self.mascota.nivel_actividad == "Bajo":
                puntos += 1

        # 3. Compatibilidad según la actividad preferida
        if actividad_preferida == "Indiferente":
            puntos += 1
        elif actividad_preferida == "Tranquilo":
            if self.mascota.nivel_actividad in ["Bajo", "Medio"]:
                puntos += 1
        elif actividad_preferida == "Activo":
            if self.mascota.nivel_actividad == "Alto":
                puntos += 1

        # 4. Compatibilidad según la personalidad
        if actividad_preferida == "Tranquilo":
            if self.mascota.personalidad in [
                "Tranquila", "Cariñoso"
            ]:
                puntos += 1
        elif actividad_preferida == "Activo":
            if self.mascota.personalidad == "Activo":
                puntos += 1
        else:
            puntos += 1

        self.porcentaje = round((puntos / total) * 100)

        return self.porcentaje
