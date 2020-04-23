slowo = "feed" \
        "thed" \
        "og"
slowo = "haveaniceday"
slowo = "chillout"

sqrt = int(len(slowo) ** (1 / 2))
if sqrt ** 2 < len(slowo):
    sqrt += 1


for nr_kolumny in range(sqrt):
    for nr_wiersza in range(sqrt):
        poz = nr_wiersza * sqrt + nr_kolumny
        if poz < len(slowo):
            print(slowo[poz], end="")
    print(" ", end="")
# wynik+=slowo[nr_wiersza*len_x+nr_kolumny]]


















lubie
_jesc
_plac
ki__













