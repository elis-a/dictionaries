class Node:
    """
    Classe che rappresenta un nodo della lista concatenata
    Ogni nodo contiene una coppia chiave-valore e un puntatore al prossimo nodo
    """

    # Costruttore (init)
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None                                # inizialmente il puntatore al prossimo nodo è nullo

    # Metodo per rappresentare il nodo come stringa (str)
    def __str__(self):
        return f"Node(key={self.key}, value={self.value})"


class LinkedListDict:
    """
    Classe che rappresenta un dizionario basato su una lista concatenata
    """

    def __init__(self):
        self.head = None                                # inizialmente la testa della lista è nulla

    def insert(self, key, value):
        """
        Inserisce o aggiorna una coppia chiave-valore nella lista
        Se la chiave esiste già, il valore corrispondente viene aggiornato, sennò viene creato un nuovo nodo in testa
        """
        current = self.head
        while current:                                  # scorro la lista finché non arrivo alla fine
            if current.key == key:
                current.value = value                   # aggiorna il valore se la chiave esiste già
                return
            current = current.next

        new_node = Node(key, value)                     # crea un nuovo nodo se la chiave non esiste
        new_node.next = self.head                       # inserisce il nuovo nodo in testa
        self.head = new_node

    def search(self, key):
        """
        Cerca un valore data una chiave
        Restituisce il valore se viene trovata la chiave, sennò lancia un'eccezione KeyError
        """
        current = self.head
        while current:
            if current.key == key:
                return current.value
            current = current.next

        raise KeyError(f"La Chiave '{key}' non è presente nel dizionario.")

    def delete(self, key):
        """
        Cancella una coppia chiave-valore data una chiave
        Se non viene trovata, lancia un'eccezione KeyError
        """
        current = self.head
        previous = None

        while current:
            if current.key == key:                      # entro nell'if se trovo il nodo da cancellare
                if previous:                            # se la chiave da cancellare non è la testa
                    previous.next = current.next        # collego il next precedente al next del nodo corrente
                else:                                   # se la chiave da cancellare è la testa
                    self.head = current.next            # aggiorno la testa al next del nodo corrente
                return

            previous = current                          # scorro la lista aggiornando previous e current
            current = current.next

        raise KeyError(f"La Chiave '{key}' non è presente nel dizionario.")

    def __str__(self):
        elements = []
        current = self.head
        while current:
            elements.append(f"[{current.key}: {current.value}]")
            current = current.next
        return "{ " + ", ".join(elements) + " }"
