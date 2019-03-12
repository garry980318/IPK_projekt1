# Dokumentácia k 1. projektu z predmetu IPK - Klient pre OpenWeatherMap API

Tento klient funguje na princípe HTTP requestu a následnej odpovedi zo strany servera. Pri vypracovaní projektu som využil Python 3.

## Popis riešenia

Ako prvé som ošetril aby sa dal pri spúšťaní klienta zadať len správny počet argumentov. Následne som tieto argumenty načítal do premenných a vytvoril som si string, do ktorého som priradil HTTP reqeust v správnom formáte (riadky 19-25 v súbore `OWclient.py`). Potom som si na komunikáciu so serverom vytvoril TCP socket a do bloku `try: except:` som zabalil pokus o pripojenie k serveru. Po úspešnom pripojení sa odošle request, ktorý musí byť zakódovaný vo formáte bytes a príjme sa odpoveď, ktorá musí byť opäť dekódovaná na formát string. Po prijatí odpovede som socket uzavrel (riadky 27-35 v súbore `OWclient.py`). Ďalej som skontroloval, či server neposlal chybovú odpoveď (riadky 39-41 v súbore `OWclient.py`). Z odpovede som následne orezal dátovú časť, v ktorej sú údaje o počasí a pomocou knižnice `json` som ich dekódoval. Tu nastával jeden problém, že ak rýchlosť vetra bola veľmi malá, tak údaj o smere vetre sa v odpovedi zo servera nenachádzal. Vyriešil som to jednoducho na riadkoch 46-47 v súbore `OWclient.py`. Rozhodol som sa, že výpis doplním o ďalšie užitočné informácie. Najzložitejšie bolo spracovať informácie o východe a západe slnka. Moje riešenie je vidno na riadkoch 49-50 v súbore `OWclient.py`. Nakoniec som informácie o počasí vypísal na STDIN.

### ZDROJE:
https://docs.python.org/3  
https://docs.python.org/3/library/sys  
https://docs.python.org/3/library/socket  
https://docs.python.org/3/library/json  
https://docs.python.org/3/library/time  
https://docs.python.org/3/library/re  
https://steelkiwi.com/blog/working-tcp-sockets/  
https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet  
https://openweathermap.org/current
