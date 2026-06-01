Zestaw dużych map testowych do projektu „zalewanie wyspy”.

Format każdego pliku:
pierwsza linia: n
kolejne n linii: macierz n x n z wysokościami pól

Oczekiwane wyniki zweryfikowane algorytmem BFS + DFS:

- meandrujacy_kanion_120x120.txt: Minimalny wzrost poziomu morza: 4 stop
- pierscien_z_laguna_130x130.txt: Minimalny wzrost poziomu morza: 6 stop
- krzyzowe_kanaly_125x125.txt: Minimalny wzrost poziomu morza: 7 stop
- gorska_wyspa_bez_podzialu_110x110.txt: Wyspa nie zostanie podzielona.
- dwa_kanaly_150x150.txt: Minimalny wzrost poziomu morza: 5 stop

Opis map:
- meandrujacy_kanion_120x120.txt: wijący się kanał od górnej do dolnej krawędzi; testuje podział lewa/prawa część.
- pierscien_z_laguna_130x130.txt: zalewany pierścień połączony z morzem kanałem; testuje oddzielenie centrum od zewnętrznej części.
- krzyzowe_kanaly_125x125.txt: kanały poziomy i pionowy; po zalaniu mogą powstać cztery suche obszary.
- gorska_wyspa_bez_podzialu_110x110.txt: gładka wyspa warstwowa; powinna znikać od brzegów bez podziału.
- dwa_kanaly_150x150.txt: dwa kanały o różnych wysokościach; pierwszy podział następuje wcześniej, drugi później.

Ważne:
W mapach występują wewnętrzne niskie doliny. Nie wolno ich zalewać automatycznie, jeśli nie mają połączenia z morzem.