import time, random, sys, os
import numpy as np
import matplotlib.pyplot as plt
import csv  # Nuovo import per la gestione dei file CSV

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# se le strutture vengono importate male, lancio di un errore più chiaro e intuitivo
try:
    from data_structures.hash_table_dict import HashTableDict
    from data_structures.abr_dict import ABRDict
    from data_structures.linked_list_dict import LinkedListDict
except ImportError:
    print("Errore: Assicurati che i file delle strutture dati si trovino in una cartella 'data_structures'")
    print("Struttura attesa: Dizionari/performance_comparison.py, Dizionari/data_structures/abr_dict.py, ecc.")
    sys.exit(1)


def run_performance_test(dict_class, keys_to_insert, keys_to_search, keys_to_delete):
    # Per HashTableDict scelgo una dimensione che sia un numero primo
    # e maggiore del numero di elementi per ridurre le collisioni
    if dict_class == HashTableDict:
        size = len(keys_to_insert) * 2 + 1                          # dimensione circa il doppio delle chiavi
        while not all(size % i for i in range(2, int(size ** 0.5) + 1)):    # controllo di primalità
            size += 2                                               # sennò passa al prossimo numero dispari
        dict_instance = dict_class(size=size)
    else:
        dict_instance = dict_class()

    results = {}

    # Test INSERIMENTO
    start_time_insert = time.perf_counter()                         # misuro il tempo per l'inserimento delle chiavi
    for key in keys_to_insert:
        dict_instance.insert(key, f"value_{key}")
    end_time_insert = time.perf_counter()
    results['insert'] = end_time_insert - start_time_insert

    # Test RICERCA (CON SUCCESSO)
    start_time_search_hit = time.perf_counter()                     # tempo per la ricerca delle chiavi esistenti
    for key in keys_to_search:
        dict_instance.search(key)
    end_time_search_hit = time.perf_counter()
    results['search_hit'] = end_time_search_hit - start_time_search_hit

    # Test RICERCA (SENZA SUCCESSO)
    miss_keys = [k + len(keys_to_insert) * 2 for k in keys_to_search]       # chiavi che sicuramente non esistono
    start_time_search_miss = time.perf_counter()                    # tempo per la ricerca delle chiavi non esistenti
    for key in miss_keys:
        try:
            dict_instance.search(key)
        except KeyError:
            pass                                                    # mi aspetto l'eccezione quindi la ignoro
    end_time_search_miss = time.perf_counter()
    results['search_miss'] = end_time_search_miss - start_time_search_miss

    # Test CANCELLAZIONE
    start_time_delete = time.perf_counter()                         # misuro il tempo per la cancellazione delle chiavi
    for key in keys_to_delete:
        dict_instance.delete(key)
    end_time_delete = time.perf_counter()
    results['delete'] = end_time_delete - start_time_delete

    return results


def plot_results(results_data, n, scenario):
    # Funzione per creare e salvare un grafico a barre con i risultati
    labels = ['Inserimento', 'Ricerca (con successo)', 'Ricerca (senza successo)', 'Cancellazione']

    # Estraggo i dati per ogni struttura
    list_times = [results_data['Lista Concatenata'][op] for op in ['insert', 'search_hit', 'search_miss', 'delete']]
    abr_times = [results_data['ABR (Albero Binario di Ricerca)'][op] for op in ['insert', 'search_hit', 'search_miss', 'delete']]
    hash_times = [results_data['Tabella Hash'][op] for op in ['insert', 'search_hit', 'search_miss', 'delete']]

    x = np.arange(len(labels))                                      # posizioni delle etichette
    width = 0.27                                                    # la larghezza delle barre

    fig, ax = plt.subplots(figsize=(15, 8))
    rects1 = ax.bar(x - width, list_times, width, label='Lista Concatenata', color='#e15759')
    rects2 = ax.bar(x, abr_times, width, label='ABR (Albero Binario di Ricerca)', color='#edc949')
    rects3 = ax.bar(x + width, hash_times, width, label='Tabella Hash', color='#76b7b2')

    ax.set_ylabel('Tempo (secondi)')                                # aggiungo etichette, titolo e legenda
    # Uso la scala logaritmica per visualizzare meglio le grandi differenze di tempo
    # è particolarmente utile quando ci sono ordini di grandezza diversi tra le strutture
    ax.set_yscale('log')
    ax.set_title(f'Performance per N = {n} con chiavi in ordine {scenario} (scala logaritmica)')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # etichette con i valori sopra le barre
    ax.bar_label(rects1, padding=3, fmt='%.5f')
    ax.bar_label(rects2, padding=3, fmt='%.5f')
    ax.bar_label(rects3, padding=3, fmt='%.5f')

    fig.tight_layout()

    # salvo il grafico in un file
    filename = f"performance_{n}_{scenario.lower().replace(' ', '_')}.png"
    plt.savefig(filename)
    print(f"\nGrafico salvato come: {filename}\n")
    plt.close(fig)                                                  # chiudo la figura per liberare memoria


def main():
    # numero di elementi da testare
    sizes = [1000, 5000, 10000]

    # strutture dati da testare
    structures = {
        "Lista Concatenata": LinkedListDict,
        "ABR (Albero Binario di Ricerca)": ABRDict,
        "Tabella Hash": HashTableDict
    }

    print("Inizio del confronto delle performance dei dizionari...\n")

    # lista per raccogliere tutti i risultati per il salvataggio CSV
    all_results_for_csv = []

    for n in sizes:
        print(f"======================================================")
        print(f"  TEST CON N = {n} ELEMENTI")
        print(f"======================================================")

        # DATI CASUALI
        print("\n--- CASO 1: Dati con chiavi CASUALI ---\n")
        random_keys = random.sample(range(n * 10), n)  # random.sample garantisce l'assenza di duplicati

        # estraggo sottoinsiemi disgiunti per ricerca e cancellazione
        search_keys_subset = random.sample(random_keys, n // 2)
        # rimuovo le chiavi usate per la ricerca dal pool per la cancellazione
        remaining_keys = list(set(random_keys) - set(search_keys_subset))
        delete_keys_subset = random.sample(remaining_keys, n // 2)

        # dizionario per raccogliere i risultati di questo scenario per il plotting
        results_random = {}
        for name, dict_class in structures.items():
            results = run_performance_test(
                dict_class,
                keys_to_insert=random_keys,
                keys_to_search=search_keys_subset,
                keys_to_delete=delete_keys_subset
            )
            results_random[name] = results                          # salvo i risultati per il plotting
            print(f"  {name}:")
            print(f"    - Inserimento:               {results['insert']:.6f} secondi")
            print(f"    - Ricerca (con successo):    {results['search_hit']:.6f} secondi")
            print(f"    - Ricerca (senza successo):  {results['search_miss']:.6f} secondi")
            print(f"    - Cancellazione:             {results['delete']:.6f} secondi")

            # aggiungo i risultati al dizionario per il CSV
            for op_name, op_time in results.items():
                all_results_for_csv.append({
                    'N': n,
                    'Scenario': "Casuale",
                    'Structure': name,
                    'Operation': op_name.replace('_', ' ').title(),
                    'Time (seconds)': op_time
                })

        # chiamo la funzione per creare il grafico dello scenario casuale
        plot_results(results_random, n, "Casuale")

        # DATI ORDINATI
        print("\n--- CASO 2: Dati con chiavi ORDINATE (crescenti) ---\n")
        ordered_keys = list(range(n))  # chiavi ordinate da 0 a n-1

        # per il test di ricerca e cancellazione uso chiavi alternate
        keys_for_search = ordered_keys[::2]  # prendo elementi con indici pari
        keys_for_delete = ordered_keys[1::2]  # prendo elementi con indici dispari

        results_ordered = {}  # dizionario per raccogliere i risultati di questo scenario per il plotting
        for name, dict_class in structures.items():
            results = run_performance_test(
                dict_class,
                keys_to_insert=ordered_keys,
                keys_to_search=keys_for_search,
                keys_to_delete=keys_for_delete
            )
            results_ordered[name] = results                         # salvo i risultati per il plotting
            print(f"  {name}:")
            print(f"    - Inserimento:               {results['insert']:.6f} secondi")
            print(f"    - Ricerca (con successo):    {results['search_hit']:.6f} secondi")
            print(f"    - Ricerca (senza successo):  {results['search_miss']:.6f} secondi")
            print(f"    - Cancellazione:             {results['delete']:.6f} secondi")

            # aggiungo i risultati al dizionario per il CSV
            for op_name, op_time in results.items():
                all_results_for_csv.append({
                    'N': n,
                    'Scenario': "Ordinato",
                    'Structure': name,
                    'Operation': op_name.replace('_', ' ').title(),
                    'Time (seconds)': op_time
                })

        # chiamo la funzione per creare il grafico dello scenario ordinato
        plot_results(results_ordered, n, "Ordinato")

    print(f"\n======================================================")
    print("Test completati.")
    print(f"======================================================")

    # salvataggio di tutti i risultati numerici in un file CSV
    csv_filename = "performance_results.csv"
    # definisco l'ordine delle colonne (intestazioni)
    fieldnames = ['N', 'Scenario', 'Structure', 'Operation', 'Time (seconds)']

    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Scrivo l'intestazione
        writer.writerows(all_results_for_csv)                       # scrivo tutti i dati raccolti

    print(f"Risultati numerici salvati in: {csv_filename}")


if __name__ == "__main__":
    main()
