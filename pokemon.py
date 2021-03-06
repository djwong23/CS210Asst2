import csv
from collections import Counter


def pokemon():
    filename = 'pokemonTrain.csv'
    reader = csv.DictReader(open(filename))
    out = open("pokemon1.txt", "w")
    numFire = numAbove = float(0)

    for index, row in enumerate(reader):
        # print(row)
        if row['type'] == 'fire':
            numFire += 1
            if float(row['level']) >= 40:
                numAbove += 1
    percent = round(100 * numAbove / numFire)
    out.write(f'Percentage of fire type Pokemons at or above level 40 = {percent}')
    weaknesses = {}
    sum_hp_above = sum_hp_below = sum_atk_above = sum_atk_below = sum_def_above = sum_def_below = 0
    num_hp_above = num_hp_below = num_atk_above = num_atk_below = num_def_above = num_def_below = 0
    reader = csv.DictReader(open(filename))
    for index, row in enumerate(reader):
        pokeType = row['type']
        weakness = row['weakness']
        if float(row['level']) > 40:
            if row['hp'] != 'NaN':
                sum_hp_above += float(row['hp'])
                num_hp_above += 1
            if row['atk'] != 'NaN':
                sum_atk_above += float(row['atk'])
                num_atk_above += 1
            if row['def'] != 'NaN':
                sum_def_above += float(row['def'])
                num_def_above += 1
        elif float(row['level']) <= 40:
            if row['hp'] != 'NaN':
                sum_hp_below += float(row['hp'])
                num_hp_below += 1
            if row['atk'] != 'NaN':
                sum_atk_below += float(row['atk'])
                num_atk_below += 1
            if row['def'] != 'NaN':
                sum_def_below += float(row['def'])
                num_def_below += 1
        if pokeType == 'NaN' or weakness == 'NaN':
            continue
        if weakness not in weaknesses:
            weaknesses[weakness] = Counter()
        weaknesses[weakness][pokeType] += 1
    avg_hp_above, avg_atk_above, avg_def_above, avg_hp_below, avg_atk_below, avg_def_below = round(
        sum_hp_above / num_hp_above, 1), round(sum_atk_above / num_atk_above, 1), round(sum_def_above / num_def_above,
                                                                                        1), round(
        sum_hp_below / num_hp_below, 1), round(sum_atk_below / num_atk_below, 1), round(sum_def_below / num_def_below,
                                                                                        1)
    out = {}
    for key in weaknesses.keys():
        out[key] = sorted(weaknesses[key].most_common(), key=lambda x: (-x[1], x[0]))[0][0]
    with open('pokemonResult.csv', 'w', newline='') as csvfile:
        reader = csv.DictReader(open(filename))
        writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames, delimiter=',')
        writer.writeheader()
        for row in reader:
            if row['type'] == 'NaN':
                row['type'] = out[row['weakness']]
            if float(row['level']) > 40:
                if row['hp'] == 'NaN':
                    row['hp'] = avg_hp_above
                if row['atk'] == 'NaN':
                    row['atk'] = avg_atk_above
                if row['def'] == 'NaN':
                    row['def'] = avg_def_above
            elif float(row['level']) <= 40:
                if row['hp'] == 'NaN':
                    row['hp'] = avg_hp_below
                if row['atk'] == 'NaN':
                    row['atk'] = avg_atk_below
                if row['def'] == 'NaN':
                    row['def'] = avg_def_below
            writer.writerow(row)
    with open('pokemonResult.csv') as newcsv:
        reader = csv.DictReader(newcsv)
        personalities = {}
        sum_stage_3 = num_stage_3 = 0
        for row in reader:
            if float(row['stage']) == 3:
                sum_stage_3 += float(row['hp'])
                num_stage_3 += 1
            pokeType = row['type']
            personality = row['personality']
            if pokeType not in personalities:
                personalities[pokeType] = [personality]
            else:
                if personality not in personalities[pokeType]:
                    personalities[pokeType].append(personality)
            personalities[pokeType].sort()
        sorted_personalities = sorted(personalities.items())
        out = open('pokemon4.txt', 'w')
        out.write('Pokemon type to personality mapping:\n')
        for item in sorted_personalities:
            out.write(f'\n\t{item[0]}: ')
            first = True
            for p in item[1]:
                if first:
                    out.write(f'{p}')
                    first = False
                else:
                    out.write(f', {p}')
        out = open('pokemon5.txt', 'w')
        out.write(f'Average hit point for Pokemons of stage 3.0 = {round(sum_stage_3 / num_stage_3)}')


def main():
    pokemon()


if __name__ == '__main__':
    main()
