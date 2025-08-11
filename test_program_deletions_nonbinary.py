import itertools
import csv
import decode_d_deletion_error_non_binary_alphabet as decode_deletions

# ---- Parameters Start ----

n_min = 1
n_max = 8
d_min = 1
d_max = 4
q_min = 2
q_max = 4


print_starting_new_x = True
do_full_print = False
assert print_starting_new_x or not do_full_print

specific_x = []
crash_on_fail = True

log_file = "log_deletions_non_binary_2.csv"

# ---- Parameters End ----

d_range = range(d_min, d_max + 1)
n_range = range(n_min, n_max + 1)
q_range = range(q_min, q_max + 1)
successful_trial_count = 0
failed_trials = []

for i, x in enumerate(specific_x):
    specific_x[i] = [int(num) for num in x]



def test_deletion(deletion_indices: tuple, x: list[int], weights_array: list[int], q: int):
    """
    Takes in a tuple of deletion indices, and tests that case with x.

    deletion_indices cannot contain duplicates.
    """
    global successful_trial_count
    deletion_indices_list = list(deletion_indices)
    deletion_indices_list.sort(reverse=True)

    if do_full_print:
        print(f"x: {x}")
    y = [num for num in x]
    for deletion_index in deletion_indices_list:
        y.pop(deletion_index)        
    decoded_string = decode_deletions.decode(y, m=decode_deletions.calculate_moment(x, weights_array), d=d, n=n, do_print_and_debug_parameter=do_full_print, q=q)
    if do_full_print:
        print(f'{decoded_string=}')
    if not decoded_string == x:
        if crash_on_fail:
            assert False
        else:
            failed_trials.append((x, y, decoded_string))
            print(f"Failed to decode {y}! Debug: ")
            print(f"{x=}")
            print(f"{y=}")
            print(f"{decoded_string=}")
    else:
        successful_trial_count += 1

def test_x(x: list[int], weights_array: list[int], n: int, d: int, q: int):
    if print_starting_new_x:
        print(f"Starting new x: {x}")
    for b in range(min(d + 1, n + 1)):
        delete_indices_list = itertools.combinations([num for num in range(0, n)], b)
        for deletion_indices in delete_indices_list:
            test_deletion(deletion_indices, x, weights_array=weights_array, q=q)

def number_in_base_q(num: int, length: int, q: int) -> list[int]:
    result = []
    while num > 0:
        result.append(num % q)
        num = num // q
    result += [0] * (length - len(result))
    return result

def test_n_d_q_combination(n: int, d: int, q: int):
    weights_array = decode_deletions.generate_weights_array(n + d, d, q)
    if specific_x:
        for x in specific_x:
            if len(x) == n:
                test_x(x, weights_array, n, d, q)
    else:
        for num in range(q ** n):
            test_x(number_in_base_q(num=num, length=n, q=q), weights_array=weights_array, n=n, d=d, q=q)
            
for d in d_range:
    print(f"Starting {d=}.")
    for n in n_range:
        for q in q_range:
            test_n_d_q_combination(n, d, q)

with open(log_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["x", "y", "decoded_string"])
    for fail in failed_trials:
        csv_writer.writerow(fail)
    csv_writer.writerow(["-------------------------"])
    csv_writer.writerow(["Successful Trial Count", "Failed Trial Count"])
    csv_writer.writerow([successful_trial_count, len(failed_trials)])
    csv_writer.writerow(["n_min", "n_max", "d_min", "d_max", "q_min"])
    csv_writer.writerow([n_min, n_max, d_min, d_max, q_min, q_max])