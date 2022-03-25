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
    num_above = num_below = 0
    reader = csv.DictReader(open(filename))
    for index, row in enumerate(reader):
        pokeType = row['type']
        weakness = row['weakness']
        if float(row['level']) > 40:
            num_above += 1
            if row['hp'] != 'NaN':
                sum_hp_above += float(row['hp'])
            if row['atk'] != 'NaN':
                sum_atk_above += float(row['atk'])
            if row['def'] != 'NaN':
                sum_def_above += float(row['def'])
        elif float(row['level']) <= 40:
            num_below += 1
            if row['hp'] != 'NaN':
                sum_hp_below += float(row['hp'])
            if row['atk'] != 'NaN':
                sum_atk_below += float(row['atk'])
            if row['def'] != 'NaN':
                sum_def_below += float(row['def'])
        if pokeType == 'NaN' or weakness == 'NaN':
            continue
        if weakness not in weaknesses:
            weaknesses[weakness] = Counter()
        weaknesses[weakness][pokeType] += 1
    avg_hp_above, avg_atk_above, avg_def_above, avg_hp_below, avg_atk_below, avg_def_below = round(
        sum_hp_above / num_above, 1), round(sum_atk_above / num_above, 1), round(sum_def_above / num_above, 1), round(
        sum_hp_below / num_below, 1), round(sum_atk_below / num_below, 1), round(sum_def_below / num_below, 1)
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
        out.write(f'Average hit point for Pokemons of stage 3.0 = {round(sum_stage_3 / num_stage_3, 1)}')


def covid():
    reader = csv.DictReader(open('covidTrain.csv'))
    provinces = {}
    cities_counter = {}
    symptoms_province_counter = {}
    for row in reader:
        p = row['province']
        if p not in provinces:
            provinces[p] = [0 for _ in range(4)]
        if p not in cities_counter:
            cities_counter[p] = Counter()
        if p not in symptoms_province_counter:
            symptoms_province_counter[p] = Counter()
        lat = row['latitude']
        long = row['longitude']
        if lat != 'NaN':
            provinces[p][0] += float(lat)
            provinces[p][1] += 1
        if long != 'NaN':
            provinces[p][2] += float(long)
            provinces[p][3] += 1
        if row['city'] != 'NaN':
            cities_counter[p][row['city']] += 1
        if row['symptoms'] != 'NaN':
            symptoms = row['symptoms'].split(';')
            for s in symptoms:
                symptoms_province_counter[p][s.strip()] += 1
    cities_to_province = {}
    symptoms_province = {}
    for province in cities_counter.keys():
        cities_to_province[province] = sorted(cities_counter[province].most_common(), key=lambda x: (-x[1], x[0]))[0][0]
    for province in symptoms_province_counter.keys():
        symptoms_province[province] = sorted(symptoms_province_counter[province].most_common(), key=lambda x: (-x[1], x[0]))[0][0]
    with open('covidResult.csv', 'w', newline='') as covid_result:
        reader = csv.DictReader(open('covidTrain.csv'))
        writer = csv.DictWriter(covid_result, fieldnames=reader.fieldnames, delimiter=',')
        writer.writeheader()
        for row in reader:
            if '-' in row['age']:
                nums = row['age'].split('-')
                row['age'] = round((float(nums[0]) + float(nums[1])) / 2)

            dates = row['date_onset_symptoms'].split('.')
            row['date_onset_symptoms'] = f'{dates[1]}.{dates[0]}.{dates[2]}'
            dates = row['date_admission_hospital'].split('.')
            row['date_admission_hospital'] = f'{dates[1]}.{dates[0]}.{dates[2]}'
            dates = row['date_confirmation'].split('.')
            row['date_confirmation'] = f'{dates[1]}.{dates[0]}.{dates[2]}'

            if row['latitude'] == 'NaN':
                province = provinces[row['province']]
                row['latitude'] = round(province[0] / province[1], 2)
            if row['longitude'] == 'NaN':
                province = provinces[row['province']]
                row['longitude'] = round(province[2] / province[3], 2)

            if row['city'] == 'NaN':
                row['city'] = cities_to_province[row['province']]
            if row['symptoms'] == 'NaN':
                row['symptoms'] = symptoms_province[row['province']]
            writer.writerow(row)


def main():
    # pokemon()
    covid()


if __name__ == '__main__':
    main()
