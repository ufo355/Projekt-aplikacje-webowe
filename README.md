# Projekt-aplikacje-webowe

**Jeżeli jesteś Frontem - patrz od razu sekcja 'Foldery'**

Jeżeli jesteś Backiem - nie zapomnij omieszkać sekcji  **'W przypadku rozwoju'**


Zaprojektowanie struktury aplikacji na pakiety (packages).
Struktura tego pakietu i aplikacji zostałą zrobiona na podstawie\
tutorialu YT: [Python Flask Tutorial: Full-Featured Web App Part 5 - Package Structure](https://www.youtube.com/watch?v=44PvX0Yv368)

Gdyby kod był niejasny i było za mało komentarzy, dajcie znać ;) (mi pewnie też się przydadzą XDDD)

**UWAGA!!!** - Odpalałem to w PyCharmie, więc nie wiem czy nie bd komplikacje\
w przypadku uruchamiania w innym IDE albo  osobno.

## Podział plików:
- **run.py** - plik służący do uruchamiania całej aplikacji
- **\_\_init__.py** - plik w którym inicjalizuje się obiekty klas Flaskowych *app* oraz *db* (baza danych)
- **routes.py** - plik z "route'ami" do zrobionych stron
- **user_database.py** - plik do tworzenia obiektów bazy danych: każdy obiekt to osobna tabela
- **drug_database.db** - plik z utworzoną bazą danych w SQLAlchemy


## Foldery
- **formapp** głowny folder aplikacji - w nim znajdują się kolejne foldery oraz pliki do działania aplikacji
- **templates** folder z plikami .html służących do renderowania stron www aplikacji lub formularzy **FRONT-  to tutaj działacie** 
## W przypadku rozwoju
Kolejne pliki do rozwoju aplikacji, np. plik .py definujący formularz (patrz na tutorial w *linku* na początku)  
należy wrzucać do folderu **formapp**, który jest utworzonym pakietem do aplikacji formularza.  
Dodatkowo należy zwracać uwagę na importowanie, aby importować pakiery lub moduły   
w opowiedniej kolejności tak aby nie było problemów, jak przed podziałem na pakiety.
