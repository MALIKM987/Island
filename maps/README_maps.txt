Dodatkowe mapy do wczytywania

Uruchamianie z katalogu island_project:

python main.py maps/small_split_3x3.txt
python main.py maps/vertical_channel_6x6.txt
python main.py maps/horizontal_channel_7x7.txt
python main.py maps/no_split_plateau_6x6.txt
python main.py maps/internal_valleys_7x7.txt
python main.py maps/diagonal_not_connected_6x6.txt
python main.py maps/delayed_gate_8x8.txt
python main.py maps/large_two_basins_10x10.txt

Oczekiwane wyniki:

small_split_3x3.txt              -> Minimalny wzrost poziomu morza: 1 stopy
vertical_channel_6x6.txt         -> Minimalny wzrost poziomu morza: 2 stopy
horizontal_channel_7x7.txt       -> Minimalny wzrost poziomu morza: 3 stopy
no_split_plateau_6x6.txt         -> Wyspa nie zostanie podzielona.
internal_valleys_7x7.txt         -> Wyspa nie zostanie podzielona.
diagonal_not_connected_6x6.txt   -> Wyspa nie zostanie podzielona.
delayed_gate_8x8.txt             -> Minimalny wzrost poziomu morza: 4 stopy
large_two_basins_10x10.txt       -> Minimalny wzrost poziomu morza: 4 stopy
