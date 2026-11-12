
class SolicitudAdopcion:

    def __init__(self, usuario, mascota, motivo):
        self.usuario = usuario
        self.mascota = mascota
        self.motivo = motivo
        self.estado = "Pendiente"

    def mostrar_solicitud(self):
        return (
            f"Solicitud de {self.usuario} "
            f"para adoptar a {self.mascota}. "
            f"Estado: {self.estado}"
        )
