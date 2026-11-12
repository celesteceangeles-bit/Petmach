class Pregunta:

    def __init__(self, texto, opciones):
        self.texto = texto
        self.opciones = opciones

    def mostrar(self):
        return self.texto