import scrapy
import os


# Definiere einen neuen Spider mit dem Namen 'beschluesse'
class BeschluesseSpider(scrapy.Spider):
    name = 'beschluesse'
    # Start-URLs für den Crawl-Prozess
    start_urls = ['https://www.bundesnetzagentur.de/DE/Beschlusskammern/BK04/BK4_01_Aktuell/BK4_Aktuell.html']

    def parse(self, response, **kwargs):
        # Durchsuche die Seite nach spezifischen Links
        for href in response.css('a.CourtDecision::attr(href)').extract():
            full_url = response.urljoin(href)  # Erstelle die vollständige URL
            # Erstelle eine neue Anfrage für jede gefundene URL, um Dokumente zu parsen
            yield scrapy.Request(full_url, self.parse_document)

    # um den Inhalt jedes Dokuments zu extrahieren und zu speichern
    def parse_document(self, response):
        filename = response.url.split('/')[-1] + '.txt'  # Erstelle den Dateinamen
        download_path = 'C:\\Users\\rflueck\\Downloads'  # Definiere den Download-Pfad
        file_path = os.path.join(download_path, 'documents', filename)  # Kompletter Pfad
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Erstelle Verzeichnis, falls nicht vorhanden
        page_content = response.xpath('//body//text()').getall()  # Extrahiere den Text der Seite
        page_text = ' '.join(page_content).strip()  # Bereinige den Text
        with open(file_path, 'w', encoding='utf-8') as file:  # Speichere den Text in einer Datei
            file.write(page_text)

