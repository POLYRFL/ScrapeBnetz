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
links = soup.find_all("a", {"class": "CourtDecision"})

# Pfad für Downloads im aktuellen virtuellen Verzeichnis anlegen
download_path = 'C:\\Users\\rflueck\\Downloads'
if not os.path.exists(download_path):
    os.makedirs(download_path)

# Für jeden Link den Inhalt herunterladen und als Datei speichern
for link in links:
    # Überprüfen, ob die URL absolut oder relativ ist
    document_url_link = link['href']
    temp_url = "https://www.bundesnetzagentur.de/"
    document_url = requests.compat.urljoin(temp_url, document_url_link)

    # Den Inhalt der verlinkten Seite abrufen
    response = requests.get(document_url)

    # Prüfen, ob die Seite erfolgreich abgerufen wurde
    if response.status_code == 200:
        # Überprüfen, ob der Link auf eine PDF-Datei verweist
        if document_url.lower().endswith('.pdf'):
            # PDF-Datei herunterladen
            pdf_response = requests.get(document_url)
            if pdf_response.status_code == 200:
                pdf_filename = os.path.join(download_path, os.path.basename(document_url))
                with open(pdf_filename, 'wb') as pdf_file:
                    pdf_file.write(pdf_response.content)
                print(f'PDF-Datei heruntergeladen und gespeichert: {pdf_filename}')
        else:
            # BeautifulSoup verwenden, um den HTML-Inhalt der verlinkten Seite zu analysieren
            document_soup = BeautifulSoup(response.content, 'html.parser')

            # Den Text des ersten `h1`-Tags extrahieren
            h1_tag = document_soup.find('h1', class_='lay')
            if h1_tag and h1_tag.text.strip():
                # Den Text des `h1`-Tags als Dateinamen verwenden und ungültige Zeichen ersetzen
                filename = h1_tag.text.strip().replace('/', '_').replace('\\', '_').replace(':', '_').replace('*',
                                                                                                              '_').replace(
                    '?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_') + '.txt'
            else:
                # Falls kein `h1`-Tag gefunden wird, einen simplen Dateinamen basierend auf dem Index des Links generieren
                filename = 'document_' + str(links.index(link)) + '.txt'

            file_path = os.path.join(download_path, filename)

            # Den Inhalt in einer Datei speichern
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f'Dokument heruntergeladen und gespeichert: {file_path}')

print(f"Alle Dokumente wurden im Verzeichnis {download_path} gespeichert.")
