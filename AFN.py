from graphviz import Digraph

def thmpsn(node):
    if not node.siguiente:
        return AFN.gtc(node.val)
    
    if node.val == "*":
        afnt = thmpsn(node.siguiente[0])
        inicio = Estado()
        final = Estado()
        inicio.add(None, afnt.estadoS)
        inicio.add(None, final)
        afnt.estadoE.add(None, afnt.estadoS)
        afnt.estadoE.add(None, final)
        return AFN(inicio, final)

    if node.val == "|":
        nodofl = thmpsn(node.siguiente[0])
        nodofr = thmpsn(node.siguiente[1])
        inicio = Estado()
        final = Estado()
        inicio.add(None, nodofl.estadoS)
        inicio.add(None, nodofr.estadoS)
        nodofl.estadoE.add(None, final)
        nodofr.estadoE.add(None, final)

        return AFN(inicio, final)

    if node.val == "^":
        nodofl = thmpsn(node.siguiente[0])
        nodofr = thmpsn(node.siguiente[1])
        nodofl.conection(nodofr)
        return AFN(nodofl.estadoS, nodofr.estadoE)

def DibujarAFN(afn, afnv):
    tm = set([afn.estadoS])
    tm = LLenarEP(tm)
    for c in afnv:
        sets = set()
        for estad in tm:
            if c in estad.changes:
                for nextS in estad.changes[c]:
                    sets.add(nextS)
        sets = LLenarEP(sets)
        tm = sets
    for estad in tm:
        if estad.final:
            return True
    return False

def LLenarEP(states):
    Pila = list(states)
    LLenarEP = set(states)

    while Pila:
        estad = Pila.pop()
        if (None) in estad.changes:
            for nextS in estad.changes[None]:
                if nextS not in LLenarEP:
                    LLenarEP.add(nextS)
                    Pila.append(nextS)

    return LLenarEP



class Estado:
    cn = 1
    def __init__(self):
        self.number = Estado.cn
        self.changes = {}
        self.final = False
        Estado.cn += 1

    def add(self, c, estad):
        if c not in self.changes:
            self.changes[c] = []
        self.changes[c].append(estad)

class AFN:
    @staticmethod
    def gtc(c):
        inicio = Estado()
        final = Estado()
        inicio.add(c, final)
        return AFN(inicio, final)

    def __init__(self, inicio=None, final=None):
        if inicio:
            self.estadoS = inicio
        else:
            self.estadoS = Estado()

        if final:
            self.estadoE = final
        else:
            self.estadoE = Estado()
        self.estadoE.final = True

    def conection(self, nfaN, c=None):
        self.estadoE.add(c, nfaN.estadoS)

    def diagram(self):
        dot = Digraph()
        NewS = [self.estadoS]
        pastS = set()

        while NewS:
            thisS = NewS.pop()
            for c, sets in thisS.changes.items():
                for nextS in sets:
                    if thisS == self.estadoS:
                        dot.node(str(id(thisS)), label="Inicio", shape="circle")
                    else:
                        dot.node(str(id(thisS)), label=str(thisS.number), shape="circle")

                    if nextS.final and nextS == self.estadoE:
                        dot.node(str(id(nextS)), label="Final", shape="doublecircle")
                    else:
                        dot.node(str(id(nextS)), label=str(nextS.number), shape="circle")

                    if c:
                        dot.edge(str(id(thisS)), str(id(nextS)), label=c)
                    else:
                        dot.edge(str(id(thisS)), str(id(nextS)), label="ε")

                    if nextS not in pastS:
                        NewS.append(nextS)

            pastS.add(thisS)
        return dot

    def toAFNparams(self):
        num_states = Estado.cn
        states = [str(i) for i in range(1, num_states + 1)]
        num_alphabet = len(self.estadoS.get_alphabet())
        alphabet = list(self.estadoS.get_alphabet())
        inicio = '1'
        num_final = 1
        final_states = [str(num_states)]
        num_transitions = sum(len(s.changes) for s in Estado.states)
        transitions = []

        for estad in Estado.states:
            state_name = str(estad.number)
            for c, next_states in estad.changes.items():
                for next_state in next_states:
                    next_state_name = str(next_state.number)
                    transitions.append([state_name, c, next_state_name])

        return num_states, states, num_alphabet, alphabet, inicio, num_final, final_states, num_transitions, transitions

