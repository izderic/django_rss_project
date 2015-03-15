# README #

Aplikacija dohvaća RSS feedove s unesenih adresa, sprema riječi unosa za aktivne feedove, broj pojavljivanja pojedine riječi po feedu, unosu i ukupno te omogućava pregled riječi sortiranih po broju pojavljivanja.

### Management command za spremanje riječi i unosa ###

    python manage.py save_feed_data

### Home page ###

Na home stranici se nalaze linkovi na stranicu s listom feedova (unos novog feeda, izmjena statusa) te stranicu s listom riječi (filtriranje po feedu, paginacija)

### JSON API ###

Parametri: word, feed_url, entry_url

Ako je samo riječ parametar vraća se ukupni broj pojavljivanja riječi. Ako je zadan feed_url ili entry_url vraća se broj pojavljivanja riječi za taj feed ili entry. Ako nema parametara onda se vraćaju sve riječi.

Primjer: /word/?word=a&feed_url=http://www.24sata.hr/feeds/sport.xml