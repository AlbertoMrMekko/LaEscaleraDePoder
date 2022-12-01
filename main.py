import random


class Player:
    life = 10
    sop = 0
    step = 0
    name = ''
    status = ''
    liststatus = ['Soldado', 'Caballero blindado', 'Escudero acorazado', 'Guardia Real', 'Jefe de Espías',
                  'Consejero Militar', 'Consejero Naval', 'Consejero de la Moneda', 'Lord Comandante',
                  'Mano del Rey',
                  'Rey de Reyes']

    def __init__(self):
        self.name = self.createName()
        self.status = self.liststatus[0]

    def getLife(self):
        return self.life

    def setLife(self, life):
        self.life = life

    def getSop(self):
        return self.sop

    def addSop(self):
        self.sop += 1

    def resetSop(self):
        self.sop = 0

    def getStep(self):
        return self.step

    def addStep(self):
        self.step += 1

    def getName(self):
        return self.name

    def getStatus(self):
        return self.status

    def setStatus(self):
        self.status = self.liststatus[int(self.getStep() / 2)]

    def showProgress(self):
        print(f"\nVidas: {str(self.life)}  Escalón: {str(self.step)}  Estrellas de poder: {str(self.sop)}")

    # noinspection PyMethodMayBeStatic
    def createName(self):
        name = ""
        valid = False
        while not valid:
            print("Indica tu nombre, jugador/a (sin \";\"): ")
            name = input()
            if name.find(";") == -1:
                valid = True
            else:
                print("Nombre no válido, inténtalo de nuevo.")
        return name


class Menu:

    def menu(self):
        i = -1
        loop = True
        x = True
        while loop:
            while x:
                self.printMenu()
                print("Introduce un número: ")
                i = input()
                x = self.checkAnswer(i)
            x = True
            i = int(i)
            if i:
                self.action(i)
                print("Pulsa cualquier tecla para continuar: ")
                input()
            else:
                print("Hasta la próxima, jugador.")
                loop = False

    # noinspection PyMethodMayBeStatic
    def printMenu(self):
        print("===== MENÚ =====")
        print("1. Jugar")
        print("2. Reglas")
        print("3. Hall de la Fama")
        print("4. Países y capitales")
        print("0. Salir")
        print("================")

    # noinspection PyMethodMayBeStatic
    def checkAnswer(self, i):
        if i.isnumeric():
            i = int(i)
            if 0 <= i <= 4:
                return False
            else:
                print("Entrada no válida.")
                return True
        else:
            print("Entrada no válida.")
            return True

    # noinspection PyMethodMayBeStatic
    def action(self, i):
        game = Game()
        if i == 1:
            game.play()
        elif i == 2:
            game.rules()
        elif i == 3:
            game.hallOfFame()
        else:
            game.showQA()


class Game:

    # --------------- CODE OF PLAY ----------------

    def play(self):
        player = Player()

        print(f"¡Que comience el ascenso, {player.getName()}, {player.getStatus()}!")
        lista = self.getDataOption1("Capitals.txt")
        listrandom = random.sample(lista, lista.__len__())
        aux = 1
        while (player.getLife() > 0) & (player.getStep() < 20):
            element = listrandom.pop(0)
            player.showProgress()
            aux = self.round(player, element, aux)
        if (player.getLife() == -10) | (player.getStep() == 20):  # si life = -10, salida por retirada.
            title = player.getName() + ", " + player.getStatus()
            result = self.calculateResult(player.getStep())
            print(f"Tus resultados: \n  Título: {title}.\n  Escalones ascendidos: {str(player.step)}.\n  "
                  f"Preguntas acertadas: {str(result)}.")
            element = [title, str(player.getStep()), str(result)]
            self.saveGame(result, element)
        else:
            print("Derrota.")

    # noinspection PyMethodMayBeStatic
    def getDataOption1(self, filename):
        lista = []
        try:
            fin = open(filename, encoding="utf8")
            for aux in fin.readlines():
                aux = aux.strip("\n")
                aux = aux.split(":")
                list.append(lista, aux)
            fin.close()
        except FileNotFoundError:
            print("ERROR, file not found.")
        return lista

    def round(self, player, element, aux):
        print(f"Pregunta: ¿Cuál es la capital de {element[0]}?")
        answer = input()
        if answer == "PASO":
            self.answerPASO(player, element[1])
        elif answer == "RETIRADA":
            self.answerRETIRADA(player, element[1])
        elif answer == element[1]:
            aux = self.answerCorrect(player, aux)
        else:
            self.answerIncorrect(player, element[1])
        return aux

    # noinspection PyMethodMayBeStatic
    def answerPASO(self, player, answer):
        print(f"Has pasado. La respuesta correcta es {answer}.")
        player.setLife(player.getLife() - 1)
        if player.getLife() > 0:
            print("Has perdido 1 vida.")

    # noinspection PyMethodMayBeStatic
    def answerRETIRADA(self, player, answer):
        print(f"Te has retirado. La respuesta correcta es {answer}.")
        player.setLife(-10)

    # noinspection PyMethodMayBeStatic
    def answerCorrect(self, player, aux):
        print("¡Correcto!")
        player.addSop()
        if aux == player.getSop():
            player.addStep()
            print(f"Has ascendido al escalón {str(player.getStep())}.")
            if player.getStep() % 5 == 0 & player.getStep() != 20:
                player.setLife(player.getLife() + (player.getStep() / 5 * 2))
                # step 5 => +2 life; step 10 => +4 life; step 15 => +6 life;
                print(f"Has conseguido {str(player.getStep() / 5 * 2)} vidas extra.")
            aux = (player.getStep() + 5) / 5
            aux = int(aux)
            player.resetSop()
            if player.getStep() % 2 == 0:
                player.setStatus()
                print(f"¡Enhorabuena, tu status ascendió a {player.getStatus()}!")
        return aux

    # noinspection PyMethodMayBeStatic
    def answerIncorrect(self, player, answer):
        print(f"Incorrecto. La respuesta correcta es {answer}.")
        player.setLife(player.getLife() - 3)
        if player.getLife() > 0:
            print("Has perdido 3 vidas.")
        else:
            player.setLife(0)

    # noinspection PyMethodMayBeStatic
    def calculateResult(self, step):
        if step <= 5:
            return step
        elif step <= 10:
            return 5 + (step - 5) * 2
        elif step <= 15:
            return 15 + (step - 10) * 3
        else:
            return 30 + (step - 15) * 4

    # noinspection PyMethodMayBeStatic
    def getDataOption2(self, filename):
        lista = []
        try:
            file = open(filename, "r")
            for aux in file.readlines():
                aux = aux.strip("\n")
                aux = aux.split(";")
                list.append(lista, aux)
            file.close()
        except FileNotFoundError:
            print("ERROR, file not found. Results could not be saved.")
        return lista

    # noinspection PyMethodMayBeStatic
    def saveGame(self, result, element):
        lista = self.getDataOption2("records.txt")
        cont = True
        i = 0
        while (i < lista.__len__()) & cont:
            old = lista[i]
            if int(old[2]) < result:
                cont = False
            else:
                i += 1

        if not cont:
            lista = self.updateLista(lista, element, i)
            self.updateHallOfFame(lista)

    # noinspection PyMethodMayBeStatic
    def updateLista(self, lista, element, i):
        j = 0
        while j < i:
            j += 1
        actual = element
        while j < lista.__len__():
            extra = lista[j]
            lista[j] = actual
            actual = extra
            j += 1
        return lista

    # noinspection PyMethodMayBeStatic
    def updateHallOfFame(self, lista):
        try:
            with open("records.txt", "w") as fout:
                for k in lista:
                    fout.write(f"{k[0]};{k[1]};{k[2]}\n")
            fout.close()
        except FileNotFoundError:
            print("ERROR, file not found.")

    # --------------- CODE OF RULES ----------------

    # noinspection PyMethodMayBeStatic
    def rules(self):
        print("------------------------------ REGLAS DEL JUEGO ------------------------------\n"
              "El objetivo principal es ascender en la escalera de poder lo máximo posible.\n"
              "En cada ronda hay que adivinar la capital del país que se indique. El jugador tiene tres opciones:\n"
              "       a) Contestar a la pregunta, en cuyo caso:\n"
              "               - Si acierta, gana una estrella de poder.\n"
              "               - Si falla, pierde 3 vidas.\n"
              "       b) No contestar, indicándolo con la palabra PASO. De este modo, el jugador pierde 1 vida y no gana "
              "estrellas de poder.\n"
              "       c) Plantarse, indicándolo con la palabra RETIRADA. En este caso, la partida termina y el jugador\n"
              "mantiene su status y sus escalones ascendidos.\n"
              "En los primeros 5 escalones, tan sólo se necesita una estrella de poder para avanzar. Entre los escalones\n"
              "6 y 10 se necesitarán 2 estrellas de poder para ascender, para los escalones 11 al 15 se necesitarán 3\n"
              "estrellas de poder, y para los escalones 16 a 20 se necesitarán 4 estrellas de poder. Si el jugador \n"
              "alcanza el escalón 20, llegará a la Sala del Trono de Hierro, y ganará la partida.\n"
              "El jugador empieza con 10 vidas. Si pierde todas las vidas, perderá todos los escalones ascendidos y la\n"
              "partida finalizará.\n"
              "Cuando el jugador alcance el escalón 5, ganará 2 vidas extra.\n"
              "Cuando el jugador alcance el escalón 10, ganará 4 vidas extra.\n"
              "Cuando el jugador alcance el escalón 15, ganará 6 vidas extra.\n"
              "Cada 2 escalones superados, el status del jugador ascenderá de uno de menor rango a uno mayor.\n"
              "---------------------------- FIN REGLAS DEL JUEGO ----------------------------"
              )

    # --------------- CODE OF HALL OF FAME ----------------

    # noinspection PyMethodMayBeStatic
    def hallOfFame(self):
        print("========== HALL DE LA FAMA ==========")
        i = 1
        try:
            fich = open("records.txt", encoding="utf8")
            for aux in fich.readlines():
                aux = aux.strip("\n")
                aux = aux.split(";")
                print(f"{str(i)}º: {aux[0]}.     Escalones ascendidos: {aux[1]}.     Preguntas acertadas: {aux[2]}.")
                i += 1
            print("=====================================")
        except FileNotFoundError:
            print("ERROR, file not found.")

    # --------------- CODE OF SHOW QA ----------------

    # noinspection PyMethodMayBeStatic
    def showQA(self):
        try:
            fin = open("Capitals.txt", encoding="utf8")
            for aux in fin.readlines():
                aux = aux.strip("\n")
                aux = aux.split(":")
                print(f"País: {aux[0]} => Capital: {aux[1]}.")
            fin.close()
        except FileNotFoundError:
            print("ERROR, file not found.")


# main


m = Menu()
m.menu()
