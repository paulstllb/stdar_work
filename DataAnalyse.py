import os
import csv
import re

#Dieses Script sammelt alle Protokolle und Probleme aus den CSV-Dateien in einem Verzeichnis und schreibt die Daten in eine neue CSV-Datei.
#       Probleme die nicht gelöst werden konnten, werden gelöscht.
#       Probleme die nicht gelöst werden konnten, werden mit 500 Sekunden markiert.


def read_csv_files(folder_path):
    # Überprüfe, ob der angegebene Pfad ein gültiges Verzeichnis ist
    if not os.path.isdir(folder_path):
        print("Der angegebene Pfad ist kein gültiges Verzeichnis.")
        return
    
    # Durchsuche das Verzeichnis nach CSV-Dateien
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]
    

    
    # Sammle die Daten aus den CSV-Dateien
    data = {}
    for csv_file in csv_files:
        print(f"Verarbeite Datei: {csv_file}")
        protocol_name = os.path.splitext(csv_file)[0]
        with open(os.path.join(folder_path, csv_file), 'r', newline='') as file:
            # Verwende regulären Ausdruck, um Leerzeichen als Trennzeichen zu erkennen
            for line in file:
                # Trenne die Zeile anhand von Leerzeichen (beliebiger Länge)
                row = re.split(r'\s+', line.strip())
                problem_name = row[0]
                time = row[2]
                if problem_name not in data:
                    data[problem_name] = {}
                # Überprüfe, ob die Zeit "-" ist und setze sie auf 500, wenn ja
                data[problem_name][protocol_name] = '500' if time == '-' else time
    


    # Schreibe die Daten in eine neue CSV-Datei
    output_file = 'outputt.csv'
    with open(output_file, 'w', newline='') as file:
        csv_writer = csv.writer(file, delimiter=';')
        
        # Schreibe die Kopfzeile
        protocols = list(next(iter(data.values())).keys())  # Holen die Protokollnamen aus dem ersten Datensatz
        csv_writer.writerow([''] + protocols)
        
        # Schreibe die Daten
        for problem_name, times in data.items():
            if all(time == '500' for time in times.values()):
                continue  # Überspringe das Problem, wenn alle Zeiten '500' sind
            
            row = [problem_name] + [times.get(protocol, '500') for protocol in protocols]
            csv_writer.writerow(row)
    
    print(f"Die Daten wurden erfolgreich in die Datei '{output_file}' geschrieben.")

# Beispielaufruf
folder_path = './TESTRUNS_UNIFIED'  # Passe den Pfad zum gewünschten Ordner an
read_csv_files(folder_path)
