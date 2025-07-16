import itertools
import csv
from typing import Iterable
import decode_d_indel_error_non_binary_alphabet as decode_indel

n_min = 2
n_max = 7
d_min = 2
d_max = 6
q_min = 4
q_max = 4

print_starting_new_x = False
do_full_print = False
do_any_print = True
assert do_any_print or not do_full_print

specific_x: list[str | list[int]] = [] #if non-empty, will test these values for x
crash_on_fail = True
failed_trials = []
failed_a_b_info = set()

log_file = "log_indels_nonbinary_4.csv"

# --------------- Parameters End ---------------


d_range = range(d_min, d_max + 1)
n_range = range(n_min, n_max + 1)
q_range = range(q_min, q_max + 1)
successful_trial_count = 0

for i, x in enumerate(specific_x):
    specific_x[i] = [int(num) for num in x]

def test_insertion_deletion(insertion_indices: tuple, deletion_indices: tuple, x: list[int], weights_array: list[int], q: int, n: int):
    """
    Takes in a tuple of insertion indices and a tuple of deletion indices, and tests that case with x.

    insertion_indices can contain duplicates.
    deletion_indices cannot contain duplicates.
    """
    global successful_trial_count

    insertion_indices_list = list(insertion_indices)
    insertion_indices_list.sort(reverse=True)
    deletion_indices_list = list(deletion_indices)
    deletion_indices_list.sort(reverse=True)

    for num in range(0, q ** len(insertion_indices)):
        items_to_insert = number_in_base_q(num, len(insertion_indices), q)
        if do_full_print:
            print(f"x: {x}")
        x_copy = [c for c in x]
        for i, insertion_index in enumerate(insertion_indices_list):
            x_copy.insert(insertion_index, items_to_insert[i])
        for deletion_index in deletion_indices_list:
            x_copy.pop(deletion_index)
        
        y = x_copy
        if do_full_print:
            print(f"y: {y}")
        decoded_string = decode_indel.decode(y=y, n=n, q=q, d=d, r=(decode_indel.calculate_moment(x, weights_array) % weights_array[n + 1]), debug=do_full_print)
        if do_full_print:
            print(f'{decoded_string=}')
        if not (decoded_string == x or decoded_string == ''):
            if crash_on_fail:
                assert False
            else:
                failed_trials.append((x, y, decoded_string))
                print(f"Failed to decode {y}! Debug: ")
                print(f"{x=}")
                print(f"{y=}")
                print(f"{decoded_string=}")
                failed_a_b_info.add((len(insertion_indices_list), len(deletion_indices_list)))
        else:
            successful_trial_count += 1
                 

def test_x(x: list[int], weights_array: list[int], n: int, d: int, q: int):
    if print_starting_new_x:
        print(f"Starting new x: {x}")
    for a in range(d + 1):
        for b in range(d + 1 - a):
            insert_indices_list = itertools.combinations_with_replacement([num for num in range(0, n + 1)], a)
            delete_indices_list = itertools.combinations([num for num in range(0, n + a)], b)
            for insertion_indices in insert_indices_list:
                for deletion_indices in delete_indices_list:
                    test_insertion_deletion(insertion_indices, deletion_indices, x, weights_array, q=q, n=n)

def number_in_base_q(num: int, length: int, q: int) -> list[int]:
    result = []
    while num > 0:
        result.append(num % q)
        num = num // q
    result += [0] * (length - len(result))
    return result

def test_n_d_q_combination(n: int, d: int, q: int):
    weights_array = decode_indel.calculate_weights(q=q, d=d, num_weights=n + d)
    if specific_x:
        for x in specific_x:
            if len(x) == n:
                test_x(x, weights_array, n, d, q) # type: ignore
    else:
        for num in range(q ** n):
            test_x(number_in_base_q(num=num, length=n, q=q), weights_array=weights_array, n=n, d=d, q=q)


for d in d_range:
    print(f"Starting {d=}.")
    for n in n_range:
        print(f"Starting {d=}, {n=}.")
        if d > n:
            continue
        for q in q_range:
            print(f"Starting {d=}, {n=}, {q=}")
            test_n_d_q_combination(n, d, q)

with open(log_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["x", "y", "decoded_string"])
    for fail in failed_trials:
        csv_writer.writerow(fail)
    csv_writer.writerow(["-------------------------"])
    csv_writer.writerow(["Successful Trial Count", "Failed Trial Count"])
    csv_writer.writerow([successful_trial_count, len(failed_trials)])
    csv_writer.writerow(["n_min", "n_max", "d_min", "d_max", "q_min", "q_max"])
    csv_writer.writerow([n_min, n_max, d_min, d_max, q_min, q_max])

    