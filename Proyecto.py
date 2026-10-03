import metro
import heapq

class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = []
        self.estacion_anterior = None
        self.estacion_siguiente = None
        self.color = ""
        self.distancia = -1
        self.padre = None
        self.d = 0
        self.t = 0

    def agregar_vecino(self, nodoP, nodoU, peso):
        if nodoP in [vecino[0] for vecino in self.vecinos]:
            nombreNodoP = nodoP.nombre
            nombreNodoU = nodoU.nombre
            print("\nError. Ya existe el vecino", nombreNodoP, "para el vertice", nombreNodoU)
        else:
            self.vecinos.append((nodoP, peso))

class Grafo:
    def __init__(self):
        self.vertices = {}

    def agregar_nodo(self, nombreNodo):
        if nombreNodo in self.vertices:
            print("\nError. Ya existe la estacion", nombreNodo)
        else:
            nuevo = Nodo(nombreNodo)
            self.vertices[nombreNodo] = nuevo

    def agregar_arista(self, nombreNodo1, nombreNodo2, peso):
        if nombreNodo1 not in self.vertices:
            print("\nError. No existe el nodo", nombreNodo1)
            if nombreNodo2 not in self.vertices:
                print("y tampoco existe el nodo", nombreNodo2, "\n")
        elif nombreNodo2 not in self.vertices:
            print("\nError. No existe el nodo", nombreNodo2)
        elif (nombreNodo1 and nombreNodo2) in self.vertices:
            nodo1 = self.vertices[nombreNodo1]
            nodo2 = self.vertices[nombreNodo2]
            nodo1.agregar_vecino(nodo2, nodo1, peso)
            nodo2.agregar_vecino(nodo1, nodo2, peso)
            nodo1.estacion_siguiente = nodo2
            nodo2.estacion_anterior = nodo1

    def BFS(self, nombreNodoInicial):
        s = self.vertices[nombreNodoInicial]
        V = self.vertices.values()
        for u in V:
            u.color = "blanco"
            u.distancia = -1
            u.padre = None
        s.color = "gris"
        s.distancia = 0
        s.padre = None
        Q = []
        Q.append(s)
        while len(Q) > 0:
            u = Q.pop(0)
            for v, peso in u.vecinos:
                if v.color == "blanco":
                    v.color = "gris"
                    v.distancia = u.distancia + peso
                    v.padre = u
                    Q.append(v)
            u.color = "negro"

    def Print(self):
        for nombre in self.vertices.keys():
            print(nombre, "--> ", end='[')
            for v, peso in self.vertices[nombre].vecinos:
                print(f"({v.nombre}, {peso}s)", end=', ')
            print("]")
            print()

    def DFS(self, nombreNodoInicial):
        n = self.vertices[nombreNodoInicial]
        V = self.vertices.values()
        for u in V:
            u.color = "blanco"
            u.padre = None
        for u in V:
            if n.color == "blanco":
                self.DFS_VISITAR(n)

    def DFS_VISITAR(self, u):
        tiempo = 0
        tiempo += 1
        u.d = tiempo
        u.color = "gris"
        for v, peso in u.vecinos:
            if v.color == "blanco":
                v.padre = u
                self.DFS_VISITAR(v)
        u.color = "negro"
        tiempo += 1
        u.t = tiempo

    def encontrar_camino_BFS(self, nombreVerticeInicial, nombreVerticeFinal):
        self.BFS(nombreVerticeInicial)
        s = self.vertices[nombreVerticeFinal]
        camino = []
        camino.append(s.nombre)
        while s.padre != None:
            s = self.vertices[s.padre.nombre]
            camino.append(s.nombre)
        print("El recorrido realizado por BFS es: [", end=' ')
        for dato in camino[::-1]:
            print(dato, end='-> ')
        print("]")
        print("\nEl número de estaciones recorridas es:", len(camino))

    def encontrar_camino_DFS(self, nombreVerticeInicial, nombreVerticeFinal):
        self.DFS(nombreVerticeInicial)
        s = self.vertices[nombreVerticeFinal]
        camino = []
        camino.append(s.nombre)
        while s.padre != None:
            s = self.vertices[s.padre.nombre]
            camino.append(s.nombre)
        print("\n\nEl recorrido realizado por DFS es: [", end=' ')
        for dato in camino[::-1]:
            print(dato, end='-> ')
        print("]")
        print("\nEl número de estaciones recorridas es:", len(camino))

    def dijkstra(self, inicio, fin):
        # Ruta más corta por tiempo
        self._dijkstra_ruta(inicio, fin, criterio="tiempo")
        # Ruta más corta por número de estaciones
        self._dijkstra_ruta(inicio, fin, criterio="estaciones")

    def _dijkstra_ruta(self, inicio, fin, criterio):
        Q = []
        distancias = {v: float('inf') for v in self.vertices}
        distancias[inicio] = 0
        heapq.heappush(Q, (0, inicio))
        padres = {v: None for v in self.vertices}

        while Q:
            (dist, actual) = heapq.heappop(Q)

            if actual == fin:
                break

            for vecino, peso in self.vertices[actual].vecinos:
                if criterio == "tiempo":
                    distancia = dist + peso
                elif criterio == "estaciones":
                    distancia = dist + 1

                if distancia < distancias[vecino.nombre]:
                    distancias[vecino.nombre] = distancia
                    padres[vecino.nombre] = actual
                    heapq.heappush(Q, (distancia, vecino.nombre))

        # Reconstruir el camino
        camino = []
        actual = fin
        while actual is not None:
            camino.append(actual)
            actual = padres[actual]

        camino = camino[::-1]
        criterio_texto = "tiempo" if criterio == "tiempo" else "número de estaciones"
        print(f"\nLa ruta más corta por {criterio_texto} es: [", end=' ')
        for estacion in camino:
            print(estacion, end='-> ')
        print("]")
        print(f"\nEl número de estaciones recorridas es: {len(camino)}")

    def ordenar_linea(self, linea, orden):
        estaciones = getattr(metro, f'linea{linea}')
        intervalos = []

        for i in range(len(estaciones) - 1):
            estacion1 = estaciones[i]
            estacion2 = estaciones[i + 1]
            nodo1 = self.vertices[estacion1]
            for vecino, peso in nodo1.vecinos:
                if vecino.nombre == estacion2:
                    intervalos.append((estacion1, estacion2, peso))

        intervalos.sort(key=lambda x: x[2], reverse=(orden == "desc"))

        for intervalo in intervalos:
            print(f"{intervalo[0]} - {intervalo[1]} ({intervalo[2]} segundos)")

def menu():
    g = Grafo()

    # Tiempo promedio en segundos entre estaciones, supuesto para todas las aristas.
    peso_fijo = 120  # 2 minutos

    for i in metro.linea1:
        g.agregar_nodo(i)
    for i in metro.linea2:
        g.agregar_nodo(i)
    for i in metro.linea3:
        g.agregar_nodo(i)
    for i in metro.linea4:
        g.agregar_nodo(i)
    for i in metro.linea5:
        g.agregar_nodo(i)
    for i in metro.linea6:
        g.agregar_nodo(i)
    for i in metro.linea7:
        g.agregar_nodo(i)
    for i in metro.linea8:
        g.agregar_nodo(i)
    for i in metro.linea9:
        g.agregar_nodo(i)
    for i in metro.lineaA:
        g.agregar_nodo(i)
    for i in metro.lineaB:
        g.agregar_nodo(i)
    for i in metro.linea12:
        g.agregar_nodo(i)

    for linea in metro.lineas:
        it = iter(linea)
        estacion_anterior = next(it, None)
        while True:
            estacion_actual = next(it, None)
            if estacion_actual is None:
                break
            g.agregar_arista(estacion_anterior, estacion_actual, peso_fijo)
            estacion_anterior = estacion_actual

    while True:
        print("\nMenu:")
        print("1. Recorrido Dijkstra")
        print("2. Recorrido BFS")
        print("3. Recorrido DFS")
        print("4. Ordenamiento de línea de menor a mayor")
        print("5. Ordenamiento de línea de mayor a menor")
        print("6. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            inicio = input("Ingresa la estación de salida: ")
            destino = input("Ingresa la estación de destino: ")
            if inicio in g.vertices and destino in g.vertices:
                g.dijkstra(inicio, destino)
            else:
                print("Estaciones no válidas.")
        elif opcion == '2':
            inicio = input("Ingresa la estación de salida: ")
            destino = input("Ingresa la estación de destino: ")
            if inicio in g.vertices and destino in g.vertices:
                g.encontrar_camino_BFS(inicio, destino)
            else:
                print("Estaciones no válidas.")
        elif opcion == '3':
            inicio = input("Ingresa la estación de salida: ")
            destino = input("Ingresa la estación de destino: ")
            if inicio in g.vertices and destino in g.vertices:
                g.encontrar_camino_DFS(inicio, destino)
            else:
                print("Estaciones no válidas.")
        elif opcion == '4':
            linea = input("Ingresa el número o letra de línea (1 a 12, A o B): ")
            g.ordenar_linea(linea, "asc")
        elif opcion == '5':
            linea = input("Ingresa el número o letra de línea (1 a 12, A o B): ")
            g.ordenar_linea(linea, "desc")
        elif opcion == '6':
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    menu()
