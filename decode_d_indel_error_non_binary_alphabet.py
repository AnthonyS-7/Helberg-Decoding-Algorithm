real_print = print
do_print_and_debug = True
def print(obj):
    if do_print_and_debug:
        real_print(obj)

import decode_d_deletion_error_non_binary_alphabet as deletion_decoder
import numpy as np

def perform_best_deletion_to_minimize_moment(y: list[int]) -> list[int]:
    """
    Performs the best deletion to minimize the moment.
    If y == [], returns [].
    """
    if y == []:
        return []
    for num in range(len(y) - 1, 0, -1):
        if y[num] > y[num - 1]: # then delete y[num]
            return y[0:num] + y[num+1:]
    return y[1:]

def get_original_moment(y: list[int], n: int, r: int, a: int, weights_array: list[int]) -> int:
    """
    Uses the Moment Theorem to find the original moment.
    """
    for num in range(a):
        y = perform_best_deletion_to_minimize_moment(y)
    if calculate_moment(y, weights_array) <= r:
        return r
    return r + weights_array[n + 1]

def calculate_moment(x: list[int], weights_array: list[int]) -> int:
    """
    Takes a 0-indexed x and a 1-indexed weights_array.
    """
    result = 0
    for i, bit in enumerate(x):
        result += bit * weights_array[i + 1]
    return result

def calculate_weights(q: int, d: int, num_weights: int) -> list[int]:
    """
    Returns a list such that w_i = weights_array[i].
    That means this is 1-indexed.

    All weights up to w_{num_weights} are included
    """
    p = q - 1
    weights_array = [0]
    for num in range(1, num_weights + 1):
        new_weight = 1
        for num_2 in range(1, d + 1):
            new_weight += weights_array[max(num - num_2, 0)] * p
        weights_array.append(new_weight)
    return weights_array

def decode_brute_force(y: list[int], n: int, q: int, r: int, weights_array: list[int]):
    """
    Brute force decoding for d=1.
    """
    print("Brute force decoding")
    print(f"{n=} {q=} {r=} {weights_array=}")
    if len(y) == n:
        return y
    weights_array = calculate_weights(q, 1, n + 1)
    if len(y) > n:
        assert len(y) == n + 1 # just a sanity check
        for num in range(len(y)):
            possible_result = y[0:num] + y[num+1:]
            this_moment = calculate_moment(possible_result, weights_array)
            if this_moment % weights_array[n + 1] == r:
                return possible_result
    else:
        assert len(y) == n - 1 # just a sanity check
        for num in range(len(y) + 1):
            for bit in range(q):
                possible_result = y[0:num] + [bit] + y[num:]
                this_moment = calculate_moment(possible_result, weights_array)
                if this_moment % weights_array[n + 1] == r:
                    return possible_result
    return []

def longest_common_subsequence(a: list[int], b: list[int]) -> int:
    """
    Returns the length of the longest common subsequence of a and b.
    """
    result_matrix : list[list[int]] = [] # we want result_matrix[i][j] to hold lcs(a[0:i+1], b[0:j+1])
    # len(result_matrix) should be len(a) and len(result_matrix[i]) should be len(b)
    for i in range(len(a)):
        result_matrix.append([])
        for j in range(len(b)):
            if a[i] == b[j]:
                result_matrix[i].append(1 + (result_matrix[i - 1][j - 1] if i != 0 and j != 0 else 0))
            else:
                result_matrix[i].append(max((result_matrix[i - 1][j] if i != 0 else 0), (result_matrix[i][j - 1] if j != 0 else 0)))
    return result_matrix[-1][-1]
def first_common_subsequence(x: list[int], y: list[int], required_length: int) -> int:
    """
    Returns the minimum nonnegative v such that longest_common_subsequence(x, y[0:v]) >= required_length.

    This is equivalent to the minimum nonnegative v such that longest_common_subsequence(x, y[0:v]) == required_length.
    Therefore, by applying the usual longest common subsequence algorithm, which involves computing the longest common
    subsequence of all pairs of (x[0:v_1], y[0:v_2]), we can find our answer in O(n^2) time.

    Returns -1 if no such index exists.

    """
    if required_length == 0:
        return 0
    print(f"Finding v for {x=}, {y=}, {required_length=}.")
    matrix = np.zeros(shape=(len(x), len(y))) # matrix[i][j] will hold the length of the longest common subsequence 
                                              # of x[0:i + 1], y[0:j + 1]
    for i in range(len(x)):
        for j in range(len(y)):
            if x[i] == y[j]:
                matrix[i][j] = (matrix[i - 1][j - 1] if i != 0 and j != 0 else 0) + 1
            else:
                matrix[i][j] = max((matrix[i - 1][j] if i >= 1 else 0), (matrix[i][j - 1] if j >= 1 else 0))
    for possible_v in range(len(y)):
        for i in range(len(x)):
            if matrix[i][possible_v] == required_length:
                print(f"Found v={possible_v + 1}")
                return possible_v + 1
    print(f"Found v=-1.")
    return -1

def compute_v(x: list[int], y: list[int], n: int, n_prime: int, d: int, a: int):
    b = d - a
    v = first_common_subsequence((x[n_prime - d:n])[::-1], y[::-1], n - n_prime + d - b)
    if v == -1:
        return len(y) + 1
    return v

# def compute_v(x: list[int], y: list[int], n: int, n_prime: int, d: int, a: int):
#     b = d - a
#     x_reversed = (x[n_prime - d - 1:])[::-1]
#     y_reversed = y[::-1]
#     result_matrix : list[list[int]] = []
#     for i in range(len(y_reversed)):
#         result_matrix.append([])
#         for j in range(len(x_reversed)):
#             if y_reversed[i] == x_reversed[j]:
#                 result_matrix[i].append(1 + (result_matrix[i - 1][j - 1] if i != 0 and j != 0 else 0))
#             else:
#                 result_matrix[i].append(max((result_matrix[i - 1][j] if i != 0 else 0), (result_matrix[i][j - 1] if j != 0 else 0)))
#             if result_matrix[i][j] >= n - n_prime + d - b:
#                 return i + 1
#     return len(y) + 1 # Means no such v exists.

def do_hard_case(x: list[int], y: list[int], d: int, q: int, m: int, n: int, n_prime: int, a: int, lower_possible_value: int, weights_array: list[int]) -> tuple[bool, list[int]]:
    """
    If solved completely, returns (True, solution).
    If not solved completely, returns (True, []) if the higher value of x_{n_prime} is correct, and (False, []) if the lower value is correct.

    Returns True if the higher value of x_{n_prime} is correct, and False if it is wrong.
    """
    b = d - a
    p = q - 1
    print(f"{q=}, {p=}, {d=}, {b=}, {a=}")

    x_1 = [num for num in x] # This is not named in the paper. It means x in case 1.
    x_1[n_prime - 1] = lower_possible_value
    for num in range(n_prime - d + 1, n_prime):
        x_1[num - 1] = p
    x_2 = [num for num in x] # This is not named in the paper. It means x in case 2.
    x_2[n_prime - 1] = lower_possible_value + 1
    for num in range(n_prime - d + 1, n_prime):
        x_2[num - 1] = 0

    print(f"{x_1=}")
    print(f"{x_2=}")

    v_1 = compute_v(x_1, y, n, n_prime, d, a)
    v_2 = compute_v(x_2, y, n, n_prime, d, a)

    print(f"{v_1=}")
    print(f"{v_2=}")

    if v_1 >= v_2:
        case_to_investigate = x_1
        other_case = x_2
        investigated_case_is_lower_value = True
    else:
        case_to_investigate = x_2
        other_case = x_1
        investigated_case_is_lower_value = False
    v = max(v_1, v_2)
    print(f"{investigated_case_is_lower_value=}")
    print(f"{case_to_investigate=}")

    if v >= n - n_prime + 2 * a + 1:
        print("We have v >= n - n_prime + 2 * a + 1.")
        return (investigated_case_is_lower_value, [])
    elif v == n - n_prime + 2 * a:
        print("We have v == n - n_prime + 2 * a.")
        m_double_prime = m - calculate_moment(case_to_investigate, weights_array)
        print(f"{m_double_prime=}")
        print(f"{y[0:max(0, len(y)-v-b)]=}")
        possible_result = deletion_decoder.decode(y=y[0:max(0, len(y)-v-b)], m=m_double_prime, d=d, n=n_prime - d, q=q, do_print_and_debug_parameter=False) + case_to_investigate[n_prime - d:]
        print(f"{possible_result=}")
        case_is_correct = calculate_moment(possible_result, weights_array) == m and longest_common_subsequence(possible_result, y) >= n - b
        print(f"{case_is_correct=}")
        if case_is_correct:
            return (True, possible_result)
        return (investigated_case_is_lower_value, [])
    elif v == n - n_prime + 2 * a - 1:
        print("We have v == n - n_prime + 2 * a - 1.")
        m_double_prime = m - calculate_moment(case_to_investigate, weights_array)
        print(f"{m_double_prime=}")
        print(f"{len(y) - v - b + 1=}")
        for j in range(1, len(y) - v - b + 1):
            y_with_j_removed = y[0:j-1] + y[j:len(y)-v-b]
            print(f"{j=} and {y_with_j_removed=}")
            possible_result = deletion_decoder.decode(y=y_with_j_removed, m=m_double_prime, d=d, n=n_prime - d, q=q, do_print_and_debug_parameter=False) + case_to_investigate[n_prime - d:]
            print(f"{possible_result=}, {''.join([str(t) for t in possible_result])}")
            print(f"{calculate_moment(possible_result, weights_array)}")
            case_is_correct = calculate_moment(possible_result, weights_array) == m and longest_common_subsequence(possible_result, y) >= n - b
            if case_is_correct:
                return (True, possible_result)
        if y[0:max(0, len(y)-v-b)] == []: # If this is true, the above loop has not run
            possible_result = deletion_decoder.decode(y=[], m=m_double_prime, d=d, n=n_prime - d, q=q, do_print_and_debug_parameter=False) + case_to_investigate[n_prime - d:]
            print(f"{possible_result=}")
            case_is_correct = calculate_moment(possible_result, weights_array) == m and longest_common_subsequence(possible_result, y) >= n - b
            if case_is_correct:
                return (True, possible_result)
        return (investigated_case_is_lower_value, [])
    assert False # This should never be reached


def case_is_possible_step_1(possible_g: int, m_prime: int, weights_array: list[int], weights_sum_array: list[int], n_prime: int, p: int):
    return possible_g >= 0 and possible_g <= p and \
           possible_g * weights_array[n_prime] <= m_prime and \
           m_prime <= possible_g * weights_array[n_prime] + weights_sum_array[n_prime - 1] * p


def decode(y: list[int], n: int, q: int, d: int, r: int, debug=False) -> list[int]:
    """
    This implementation (including all variable names) is nearly faithful to the algorithm described 
    in the paper. Any deviations (for speed or elegance) are marked in the code.
    """
    global do_print_and_debug
    do_print_and_debug = debug


    # Deviation from paper: q represents the size of the alphabet.

    assert d <= n # If d > n, then each codebook has only one string, which is not useful.
    if d == 1:
        return decode_brute_force(y, n, q, r, weights_array=calculate_weights(q, d, n + 1))
    a = (d + len(y) - n) // 2
    b = (d - len(y) + n) // 2
    if a + b < d:
        print("Deleting one extra character to ensure a + b = d.")
        return decode(y[1:], n, q, d, r, debug=debug)
    weights_array = calculate_weights(q, d, n + 1)
    m = get_original_moment(y, n, r, a, weights_array)
    print(f"Original moment: {m}")
    p = q - 1

    weights_sum_array = [0] * len(weights_array) # weights_sum_array[i] = sum_{j=1}^{i}w_i
    for num in range(1, len(weights_array)):
        weights_sum_array[num] = weights_array[num] + weights_sum_array[num - 1]

    x = [0] * n # Note: x is 0-indexed.
    n_prime = n
    while n_prime > 0:
        m_prime = m - calculate_moment(x, weights_array) # Note: Recomputing m_prime from scratch like this is inefficient.

        print(f"Starting loop iteration with {n_prime=}, {m_prime=}")
        # STEP 1 BEGIN
        lower_possible_value_of_x_n_prime = (m_prime // weights_array[n_prime]) - 1 # Corresponds to q or g in the paper (depending on which place one is reading)
        lower_case_is_possible = case_is_possible_step_1(possible_g=lower_possible_value_of_x_n_prime, m_prime=m_prime, 
                                weights_array=weights_array, weights_sum_array=weights_sum_array, n_prime=n_prime, p=p)
        higher_case_is_possible = case_is_possible_step_1(possible_g=lower_possible_value_of_x_n_prime + 1, m_prime=m_prime, 
                                weights_array=weights_array, weights_sum_array=weights_sum_array, n_prime=n_prime, p=p)
        if lower_case_is_possible and higher_case_is_possible:
            # STEP 2 BEGIN
            print("Beginning step 2.")
            higher_case_correct, full_solution = do_hard_case(x=x, y=y, d=d, q=q, m=m, n=n, n_prime=n_prime, a=a, lower_possible_value=lower_possible_value_of_x_n_prime, weights_array=weights_array)
            if full_solution:
                return full_solution
            if higher_case_correct:
                x[n_prime - 1] = lower_possible_value_of_x_n_prime + 1
                for num in range(1, d):
                    x[n_prime - 1 - num] = 0
            else:
                x[n_prime - 1] = lower_possible_value_of_x_n_prime
                for num in range(1, d):
                    x[n_prime - 1 - num] = p
            n_prime -= d
            # STEP 2 END
        else:
            x[n_prime - 1] = lower_possible_value_of_x_n_prime + (0 if lower_case_is_possible else 1) # the -1 compensates for being 0 indexed
            n_prime -= 1
        # STEP 1 END
        print(f"One loop iteration complete; {x=}")
    return x






