import csv
from collections import Counter


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
        symptoms_province[province] = \
            sorted(symptoms_province_counter[province].most_common(), key=lambda x: (-x[1], x[0]))[0][0]
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
    covid()


if __name__ == '__main__':
    main()
