import requests
from bs4 import BeautifulSoup
import os

# URL der zu crawlenden Seite
url = 'https://www.bundesnetzagentur.de/DE/Beschlusskammern/BK04/BK4_01_Aktuell/BK4_Aktuell.html'

# HTML-Inhalt der Seite abrufen
response = requests.get(url)

# BeautifulSoup verwenden, um den HTML-Inhalt zu analysieren
soup = BeautifulSoup(response.text, 'html.parser')

# Alle `a`-Tags extrahieren, die ein href-Attribut haben
links = soup.find_all('a', href=True)

# Pfad für Downloads im aktuellen virtuellen Verzeichnis anlegen
download_path = 'C:\\Users\\rflueck\\Downloads'
if not os.path.exists(download_path):
    os.makedirs(download_path)

# Für jeden Link den Inhalt herunterladen und als Textdatei speichern
for link in links:
    # Überprüfen, ob die URL absolut oder relativ ist
    document_url = link['href']
    if not document_url.startswith('http'):
        # Für dieses Beispiel nehmen wir an, dass alle URLs relativ sind und ergänzen die Basis-URL
        document_url = url + document_url

    # Den Inhalt der verlinkten Seite abrufen
    response = requests.get(document_url)

    # Einen simplen Dateinamen basierend auf dem Index des Links generieren
    filename = 'document_' + str(links.index(link)) + '.txt'
    file_path = os.path.join(download_path, filename)

    # Den Inhalt in einer Datei speichern
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response.text)

print(f"Alle Dokumente wurden im Verzeichnis {download_path} gespeichert.")
