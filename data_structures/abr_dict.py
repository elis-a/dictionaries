class Node:
    """
    Classe che rappresenta un nodo dell'ABR
    Ogni nodo contiene una coppia chiave-valore e puntatori ai nodi sinistro e destro
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None                                 # puntatore al nodo sinistro
        self.right = None                                # puntatore al nodo destro

    def __str__(self):
        return f"Node(key={self.key}, value={self.value})"


class ABRDict:
    """
    Classe che rappresenta un dizionario basato su ABR
    """
    def __init__(self):
        self.root = None                                # inizialmente la radice dell'ABR è nulla

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)                # se l'albero è vuoto, creo la radice
            return

        current = self.root
        while True:
            if key < current.key:                       # se la chiave è minore, cerco nel sotto-albero sinistro
                if current.left is None:
                    current.left = Node(key, value)
                    return
                current = current.left
            elif key > current.key:                     # se la chiave è maggiore, cerco nel sotto-albero destro
                if current.right is None:
                    current.right = Node(key, value)
                    return
                current = current.right
            else:                                       # se la chiave esiste già, aggiorna il valore e termina
                current.value = value
                return

    def search(self, key):
        current = self.root
        while current is not None:
            if key < current.key:                       # se la chiave è minore, cerco a sinistra
                current = current.left
            elif key > current.key:                     # se la chiave è maggiore, cerco a destra
                current = current.right
            else:                                       # chiave trovata
                return current.value

        # se non trovo la chiave, lancio un'eccezione
        raise KeyError(f"La chiave '{key}' non è presente nel dizionario.")

    def delete(self, key):
        parent = None                                   # genitore del nodo da cancellare

        current = self.root
        while current is not None and current.key != key:   # devo trovare il nodo da cancellare e il suo genitore
            parent = current                            # tengo traccia del genitore
            if key < current.key:                       # se la chiave è minore, vado a sinistra
                current = current.left
            else:                                       # se la chiave è maggiore, vado a destra
                current = current.right

        # se non trovo la chiave, lancio un'eccezione
        if current is None:
            raise KeyError(f"Impossibile cancellare: la chiave '{key}' non è presente.")

        if current.left is None and current.right is None:          # il nodo da cancellare è una foglia
            if current == self.root:                                # se il nodo da cancellare è la radice
                self.root = None                                    # l'albero diventa vuoto
            elif parent.left == current:                            # se il nodo da cancellare è un figlio sinistro
                parent.left = None
            else:                                                   # se il nodo da cancellare è un figlio destro
                parent.right = None

        elif current.left is None:                                  # il nodo ha solo il figlio destro
            if current == self.root:                                # se il nodo da cancellare è la radice
                self.root = current.right                           # la nuova radice sarà il figlio destro
            elif parent.left == current:                            # se il nodo da cancellare è un figlio sinistro
                parent.left = current.right                         # collego il genitore al figlio destro
            else:                                                   # se il nodo da cancellare è un figlio destro
                parent.right = current.right                        # collego il genitore al figlio destro

        elif current.right is None:                                 # il nodo ha solo il figlio sinistro
            if current == self.root:                                # tutto specchiato rispetto al caso precedente
                self.root = current.left
            elif parent.left == current:
                parent.left = current.left
            else:
                parent.right = current.left

        else:                                                       # il nodo ha due figli
            successor_parent = current                              # il genitore del successore
            successor = current.right                               # trovo il successore (min nel sotto-albero destro)
            while successor.left is not None:                       # scendo a sinistra finché posso
                successor_parent = successor                        # tengo traccia del genitore
                successor = successor.left                          # vado a sinistra

            current.key = successor.key                             # copio chiave e valore del successore
            current.value = successor.value                         # nel nodo da cancellare

            if successor_parent.left == successor:              # se il succ è il figlio sx del nodo da cancellare
                successor_parent.left = successor.right         # collego il genitore del succ a figlio dx del succ
            else:                                               # se il succ è il figlio dx del nodo da cancellare
                successor_parent.right = successor.right        # collego il genitore del succ al figlio dx del succ

    def __str__(self):
        elements = []
        self._build_str_in_order(self.root, elements)   # inorder-tree-walk per ottenere gli elementi in ordine
        return "{ " + ", ".join(elements) + " }"

    def _build_str_in_order(self, node, elements):
        if node is None:
            return

        self._build_str_in_order(node.left, elements)
        elements.append(f"[{node.key}: {node.value}]")
        self._build_str_in_order(node.right, elements)
