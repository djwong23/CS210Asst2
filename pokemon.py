import csv


def pokemon1(reader):
    out = open("pokemon1.txt", "w")
    numFire = numAbove = float(0)

    for index, row in enumerate(reader):
        print(row)
        if row['type'] == 'fire':
            numFire += 1
            if float(row['level']) >= 40:
                numAbove += 1
    percent = round(100 * numAbove / numFire)
    out.write(f'Percentage of fire type Pokemons at or above level 40 = {percent}')


def main():
    reader = csv.DictReader(open('pokemonTrain.csv'))
    pokemon1(reader)


if __name__ == '__main__':
    main()
