import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from works_parser import get_top, can_be_equal


def get_count_by_check_words(check_word_1, check_data_1, check_word_2, check_data_2):
    count = 0
    for record_1, record_2 in zip(check_data_1, check_data_2):
        if can_be_equal(check_word_1, record_1) and can_be_equal(check_word_2, record_2):
            count += 1
    return count


def get_plot_titles_and_array(data):
    qualifications_top = get_top('менеджер', data['jobTitle'], data['qualification'])
    jobs_top = get_top('инженер', data['qualification'], data['jobTitle'])
    result_arr = [[0, 0, 0, 0, 0] for k in range(5)]
    qualifications = []
    jobs = []
    for i in range(5):
        qualifications.append(qualifications_top[i][0])
        jobs.append(jobs_top[i][0])
        for j in range(5):
            result_arr[i][j] = get_count_by_check_words(
                qualifications_top[i][0], data['qualification'],
                jobs_top[j][0], data['jobTitle'],
            )
    return qualifications, jobs, result_arr


def main():
    works = pd.read_csv("works.csv", encoding='utf-8')
    qualifications, jobs, counts = get_plot_titles_and_array(works)

    fig, ax = plt.subplots()
    im = ax.imshow(counts)

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(jobs)), labels=jobs)
    ax.set_yticks(np.arange(len(qualifications)), labels=qualifications)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(qualifications)):
        for j in range(len(jobs)):
            text = ax.text(j, i, counts[i][j],
                           ha="center", va="center", color="w")

    ax.set_title("Top-5 профессий и Top-5 должностей")
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
