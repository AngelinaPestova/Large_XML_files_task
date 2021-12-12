import re
import pandas as pd
from nltk.stem.snowball import RussianStemmer


stop_words = ["отдел", "главн", "специалист", "бакалавр", "ведущ", "мастер"]

def get_top(check_word, checking_data, return_data):
    d = dict()
    for checking_record, return_record in zip(checking_data, return_data):
        if return_record == return_record and can_be_equal(check_word, checking_record):
            keys = get_words_for_comparison(return_record)
            for key in keys:
                if len(key) >= 5 and key not in stop_words:
                    if key not in d.keys():
                        d[key] = 0
                    d[key] += 1
    return sorted(d.items(), key=lambda x: -x[1])


def get_words_for_comparison(record):
    stemmer = RussianStemmer()
    r = list(filter(None, re.findall(r"[\w']+", str(record).lower())))
    return [stemmer.stem(x) for x in r]


def can_be_equal(record_1, record_2):
    r_1 = get_words_for_comparison(record_1)
    r_2 = get_words_for_comparison(record_2)

    for word in r_1:
        if word in r_2:
            return True
    return False


def count_people_with_different_positions(works, checking_data_title_1, checking_data_title_2):
    result = 0
    for record_1, record_2 in zip(works[checking_data_title_1], works[checking_data_title_2]):
        if not can_be_equal(record_1, record_2):
            result += 1
    return result


def main():
    works = pd.read_csv("works.csv", encoding='utf-8')

    # У какого количества людей профессия и должность не совпадают?
    amount = count_people_with_different_positions(works, "jobTitle", "qualification")
    print(f"Профессия и должность не совпадают у {amount} из {len(works)}")

    # Люди с каким образованием становятся менеджерами (топ-5)?
    qualifications_top = get_top('менеджер', works['jobTitle'], works['qualification'])
    print("Топ-5 образований, c которыми становятся менеджерами:")
    for i in range(5):
        print(qualifications_top[i])

    # Кем работают люди, которые по диплому являются инженерами (топ-5)?
    jobs_top = get_top('инженер', works['qualification'], works['jobTitle'])
    print("Топ-5 профессий людей, имеющих диплом инженера")
    for i in range(5):
        print(jobs_top[i])


if __name__ == '__main__':
    main()
