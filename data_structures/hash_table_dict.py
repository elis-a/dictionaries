class Node:
    """
        Classe che rappresenta un nodo dell'hash
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __str__(self):
        return f"Node(key={self.key}, value={self.value})"


class HashTableDict:
    """
    Classe che rappresenta un dizionario basato su tabelle hash
    """
    def __init__(self, size=11):
        """
        Inizializzo la tabella hash, uso numero primo come size per migliorare la distribuzione delle chiavi
        e ridurre collisioni
        self.table è una lista Python che funge da array, inizializzo la tabella con None
        """
        self.size = size
        self.table = [None] * self.size                             # ogni cella verrà chiamata 'slot'

    def _hash(self, key):
        if not isinstance(key, int):                                # mi assicuro che la chiave sia un intero
            raise TypeError("La chiave deve essere un intero.")
        return key % self.size                                      # uso l'operatore modulo

    def insert(self, key, value):
        index = self._hash(key)                                     # calcolo indice dello slot usando la funzione hash
        head = self.table[index]                                    # accedo alla testa della lista nello slot

        current = head                                              # scorro la lista per vedere se chiave esiste già
        while current:
            if current.key == key:
                current.value = value                               # aggiorno il valore se la chiave esiste già
                return
            current = current.next

        # creo un nuovo nodo se la chiave non esiste e lo inserisco in testa alla lista
        new_node = Node(key, value)
        new_node.next = head                                        # il next del nuovo nodo punta alla vecchia testa
        self.table[index] = new_node                                # aggiorno la testa della lista nello slot

    def search(self, key):
        index = self._hash(key)                                     # calcolo indice dello slot usando la funzione hash

        current = self.table[index]
        while current:                                              # scorro la lista nello slot
            if current.key == key:
                return current.value                                # restituisco il valore associato se trovo la chiave
            current = current.next

        raise KeyError(f"La chiave '{key}' non è presente nel dizionario.")    # se non trovo la chiave lancio eccezione

    def delete(self, key):
        index = self._hash(key)                                     # calcolo indice dello slot usando la funzione hash

        current =self.table[index]                                  # scorro tenendo traccia del nodo precedente
        previous = None                                             # previous serve per collegare nodi quando cancello
        while current:
            if current.key == key:
                if previous is None:
                    self.table[index] = current.next                # se la chiave da cancellare è in testa
                else:
                    previous.next = current.next                    # se la chiave da cancellare non è in testa
                return                                              # cancellazione

            previous = current                                          # scorro la lista aggiornando previous e current
            current = current.next

        raise KeyError(f"Impossibile cancellare: la chiave '{key}' non è presente.") # se non trovo la chiave lancio ecc

    def __str__(self):
        elements = []
        for i in range(self.size):
            current = self.table[i]
            while current:
                elements.append(f"[{current.key}: {current.value}]")
                current = current.next
        return "{ " + ", ".join(elements) + " }"
