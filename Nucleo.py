import time


class Mundo:  # Clase que maneja el juego

    def __init__(self, center=(0, 0), coordinates=(), interfaz=None,
                 tiempo=0, limite=-1, print_during=False, debugging=False):
        # Self-Explanatory
        self.variacion = ((-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0))
        self.debugging = debugging
        self.interfaz = interfaz
        self.center = center
        self.coordinates = coordinates
        self.cells = {}
        self.toBorn = []
        self.toKill = []
        self.analized = {}
        self.limite = limite
        self.tiempo = tiempo
        self.print_during = print_during
        self.builder(self.coordinates)

    def run(self):  # LOOP DEL JUEGO
        salir = 0
        tiempoinicial = time.time()
        while salir != self.limite:
            if self.print_during is True and self.interfaz is not None:
                self.interfaz.run(self.cells)
            self.refresher()
            if self.tiempo > 0:
                time.sleep(self.tiempo)
            self.toBorn = []
            salir += 1
        self.final(tiempoinicial, salir)

    def final(self, tiempo, loops):  # Final del juego
        if self.debugging is True:
            tiempo = time.time() - tiempo
            celulas = len(self.cells)
            print("Tiempo total: " + str(tiempo))
            print("Media por loop: " + str(tiempo/loops))
            print("Loops por segundo: " + str(loops/tiempo))
            print("Loops:" + str(loops) + "\nCelulas vivas: " + str(celulas))
        if self.interfaz is not None:
            self.interfaz.run(self.cells)
        return self.cells

    def builder(self, lista):  # Guarda las coordenadas de las células que deben nacer en el diccionario
        for x in lista:
            if x not in self.cells:
                self.cells[x] = None

    def refresher(self):  # Refresca la situación de las células
        for x in self.cells.keys():
            self.refresh(x)
        self.builder(self.toBorn)
        self.toBorn = []
        self.kill()
        self.analized = {}

    def kill(self):  # Borra del diccionario las células que deben morir
        for x in self.toKill:
            objecto = self.cells[x]
            del objecto
            del self.cells[x]
        self.toKill = []

    def adjacent_life(self, square):  # Cuenta las células vivas alrededor de una casilla
        counter = 0
        for x in self.variacion:
            if (square[0] + x[0], square[1] + x[1]) in self.cells:
                counter += 1
        return counter

    def survivality(self, coordinates):  # Detecta si la célula sobrevive o muere
        if self.adjacent_life(coordinates) > 3 or self.adjacent_life(coordinates) < 2:
            self.toKill.append(coordinates)

    def refresh(self, coordinates):  # Refresca la situación de una coordenada
        self.survivality(coordinates)
        for x in self.variacion:
            coordenadas = (x[0] + coordinates[0], x[1] + coordinates[1])
            if coordenadas not in self.analized:
                if self.adjacent_life(coordenadas) == 3:
                    self.toBorn.append(coordenadas)
                self.analized[coordenadas] = None


def main():
    coordenadas = [(0, 0), (1, 0), (-1, 0)]
    mundo = Mundo(coordinates=coordenadas, limite=200000, debugging=True)
    mundo.run()

if __name__ == "__main__":
    main()
