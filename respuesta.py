class Respuesta:

    def __init__(self, pregunta, valor):
        self.pregunta = pregunta
        self.valor = valor

    def mostrar_respuesta(self):
        return f"{self.pregunta}: {self.valor}"