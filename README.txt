Projekt: zalewanie wyspy

1. Cel programu

Program rozwiazuje zadanie grafowe nr 14: zalewanie wyspy.

Dany jest plik tekstowy z mapa wyspy w postaci macierzy n x n. Kazda liczba
oznacza wysokosc pola nad poziomem morza w stopach. Program znajduje minimalny
wzrost poziomu morza, przy ktorym wyspa zostanie podzielona na co najmniej dwie
osobne suche czesci.

Program ma tez tryb graficzny Tkinter pokazujacy kolejne stany wyspy podczas
podnoszenia poziomu wody.

2. Format danych wejsciowych

Plik tekstowy powinien miec postac:

n
a11 a12 ... a1n
a21 a22 ... a2n
...
an1 an2 ... ann

Pierwsza linia zawiera liczbe n. Nastepne n linii zawiera po n liczb
calkowitych.

Przyklad:

5
8 5 7 3 1
5 5 6 7 3
1 4 2 4 4
2 3 5 5 6
2 3 2 4 4

3. Sposob uruchomienia

W folderze dist znajduje się plik wykonywalny dla wersji graficznej.

Przykladowe testy:

python main.py tests/example.txt
python main.py tests/no_split.txt
python main.py tests/split_by_channel.txt
python main.py tests/internal_valley.txt
python main.py tests/large_island_20x20.txt

4. Opis algorytmu

Program sprawdza kolejne poziomy morza od 0 do maksymalnej wysokosci na mapie.
Dla kazdego poziomu wykonywane sa dwa glowne kroki:

- BFS do symulacji zalewania od brzegu. BFS startuje z pol brzegowych,
  ktorych wysokosc jest mniejsza lub rowna aktualnemu poziomowi morza.
  Nastepnie przechodzi tylko na sasiadow bokiem, ktorych wysokosc tez jest
  mniejsza lub rowna temu poziomowi. W ten sposob zalane sa tylko pola, do
  ktorych morze moze faktycznie dojsc od brzegu mapy.
- DFS do policzenia suchych komponentow. Suche pole to pole, ktore nie zostalo
  zalane przez BFS. DFS przechodzi tylko po suchych polach i nadaje etykiety
  komponentom, dzieki czemu GUI moze kolorowac rozne suche czesci wyspy.

Sasiedztwo pol jest liczone tylko bokami: gora, dol, lewo, prawo. Przekatne nie
sa uwzgledniane.

Wewnetrzne doliny nie sa zalewane automatycznie. Nawet jesli maja wysokosc
mniejsza lub rowna poziomowi morza, pozostaja suche, dopoki nie maja polaczenia
z morzem od brzegu mapy.

5. Opis plikow

main.py:
- obsluga argumentow programu,
- tryb tekstowy,
- tryb GUI po podaniu opcji --gui.

island_logic.py:
- wczytywanie i walidacja danych,
- BFS do zalewania wyspy,
- DFS do liczenia suchych komponentow,
- generowanie stanow dla kolejnych poziomow morza,
- znajdowanie minimalnego poziomu podzialu.

visualizer.py:
- GUI w Tkinterze,
- rysowanie planszy,
- obsluga przyciskow,
- animacja kolejnych poziomow wody.

tests:
- example.txt: przyklad z tresci zadania, wynik 4,
- no_split.txt: przypadek, gdy wyspa sie nie dzieli,
- split_by_channel.txt: przypadek z niskim pasem, wynik 1,
- internal_valley.txt: zamknieta dolina, ktora nie powinna byc zalana wczesniej,
- large_island_20x20.txt: mapa 20x20, oczekiwany wynik 4.
- inne ...

6. GUI

GUI pokazuje wyspe jako siatke kwadratow. W kazdym polu widoczna jest wysokosc.

Kolory:
- pola zalane sa niebieskie,
- pola nowo zalane wzgledem poprzedniego poziomu sa jasnoniebieskie,
- pola suche maja kolor zielono-brazowy zalezny od wysokosci,
- po podziale rozne suche komponenty sa kolorowane roznymi kolorami.

Dostepne przyciski:
- Wczytaj plik,
- Poprzedni poziom,
- Nastepny poziom,
- Start animacji,
- Stop animacji,
- Reset.

7. Obsluga bledow

Program wypisuje czytelne komunikaty dla:
- braku pliku wejsciowego,
- pustego pliku,
- blednego formatu danych,
- zlego rozmiaru macierzy,
- wartosci niebedacych liczbami calkowitymi,
- ujemnego lub zerowego n.

8. Biblioteki

Program korzysta wylacznie ze standardowej biblioteki Pythona. GUI uzywa
modulu Tkinter, ktory jest czescia standardowej biblioteki.

9. Tworzenie pliku .exe w Windows 11

Mozna uzyc programu PyInstaller:

pip install pyinstaller
pyinstaller --onefile main.py

Po zakonczeniu budowania plik wykonywalny powinien znajdowac sie tutaj:

dist/main.exe

Jesli program ma dziala jak zwykla aplikacja okienkowa po dwukliku, bez okna
konsoli, nalezy zbudowac plik app.py:

pyinstaller --onefile --windowed --name ZalewanieWyspy app.py

Wtedy plik wykonywalny bedzie tutaj:

dist/ZalewanieWyspy.exe

Po uruchomieniu aplikacja od razu otworzy GUI. Pliki map mozna wczytywac
przyciskiem Wczytaj plik.

