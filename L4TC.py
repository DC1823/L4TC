from AFN import *

def ShuntingYard(exp):
    #The output queue
    Output = []
    #The operator Pila
    Stack = []
    #Operator precedence
    Prec = {'(': 1, '|': 2, '.': 3, '?': 4, '*': 4, '+': 4, '^': 5}
    #Loop through the input a c at a time
    for c in exp:
        #c is an operator
        if c in {'*', '.', '|', '?', '+', '^'}:
            #Check what is on the Pila
            while Stack and Prec[c] < Prec[Stack[-1]]:
                #Append operator at the top of the Pila to the output queue
                Output.append(Stack.pop())
            #Push c to the Pila
            Stack.append(c)
        elif c == '(':
            #Push c to the Pila
            Stack.append(c)
        elif c == ')':
            while Stack[-1] != '(':
                #Append operator at the top of the Pila to the output queue
                Output.append(Stack.pop())
            #Remove open bracket from Pila
            Stack.pop()
        else:
            #Push c to the output queue
            Output.append(c)
    #Append all operators on the Pila to the output queue
    while Stack:
        Output.append(Stack.pop())
    #Convert output list to string
    return ''.join(Output)


class Nodo:
    def __init__(self, val):
        self.val = val
        self.izquierda = None
        self.derecha = None
        self.siguiente = []

class PrintAF(object):
    def constru(self, exprecionReg):
        Pila = []
        for c in exprecionReg:
            if c not in "*|^":
                nuevarama = Nodo(c)
                Pila.append(nuevarama)
            else:
                if c == "*":
                    if len(Pila) >= 1:
                        nodos = Pila.pop()
                        nuevarama = Nodo(c)
                        nuevarama.siguiente.append(nodos)
                        Pila.append(nuevarama)
                    else:
                        raise Exception("Falta op de *")
                else:
                    if c in "|^":
                        if len(Pila) >= 2:
                            nuevarama = Nodo(c)
                            nododere = Pila.pop()
                            nodoizq = Pila.pop()
                            nuevarama.siguiente.append(nodoizq)
                            nuevarama.siguiente.append(nododere)
                            Pila.append(nuevarama)
                        else:
                            raise Exception("Falta op de | o ^")
        return Pila[0] if len(Pila) == 1 else None 



def evaluarcadena(r):
    ShuY = ShuntingYard(r)
    print("Postfix es:", ShuY)
    f = graf.constru(ShuY)
    Estado.cn = 1
    afn = thmpsn(f)
    enviardoc = afn.diagram()
    #Abrira un pdf
    enviardoc.render(f'AFN', view = True, cleanup=True)
    w = input("Ingrese una cadena w:")
    result = DibujarAFN(afn, w)
    if result:
        print("la cadena fue aceptada")
    else:
        print("la cadena no fue aceptada")
graf = PrintAF()
r = str(input("Ingrese una expresion regular r: "))
evaluarcadena(r)