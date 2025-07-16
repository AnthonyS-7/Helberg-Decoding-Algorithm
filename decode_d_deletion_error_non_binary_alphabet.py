real_print = print
do_print_and_debug = True
def print(obj):
    if do_print_and_debug:
        real_print(obj)


def calculate_moment(x: list[int], weights_array: list[int]):
    """
    Note: q is treated as 0.
    """
    result = 0
    for i, bit in enumerate(x):
        if bit != -1:
            result += weights_array[i + 1] * bit
    return result

def calculate_i(m: int, x: list[int], weights_array: list[int]):
    return m - calculate_moment(x, weights_array)

def generate_weights_array(n: int, d: int, q: int):
    print(f"Deletion algorithm generating weights array for {n=}, {d=}, {q=}")
    p = q - 1
    weights_array = [0]
    for num in range(1, n + 1):
        this_weight = 1
        for num2 in range(num - d, num):
            this_weight += weights_array[num2] * p if num2 >= 0 else 0
        weights_array.append(this_weight)
    print(f"{weights_array=}")
    return weights_array
 
# def decode_if_all_deletions_at_end(y: str, m: int, d: int, n: int, weights_array: list[int]) -> str:
#     """
#     If all deletions were at the end of x, will decode successfully. Otherwise, returns the empty string.
#     """
#     print(f"Attempting to decode {y=}, while assuming all deletions are at the end.")
#     print(f"Desired moment: {m=}. {d=}")

#     remaining_moment = m - calculate_moment(y, weights_array)
#     current_string = [] # reversed, so x_n will be current_string[0], x_{n - 1} will be current_string[1], etc

#     for num in range(n, max(n - d, 0), -1):
#         if weights_array[num] > remaining_moment:
#             current_string.append("0")
#         elif sum(weights_array[len(y) + 1:num]) < remaining_moment:
#             current_string.append("1")
#             remaining_moment -= weights_array[num]
#         else:
#             assert False

#     print(f"{remaining_moment=}")
#     print(f"{current_string}")

#     if remaining_moment == 0:
#         return y + ''.join(current_string[::-1])
#     else:
#         return ''

def decode_if_all_deletions_at_end(x_prime: list[int], n: int, m: int, weights_array: list[int], c: int, q: int) -> list[int]:
    x_prime_copy = [num for num in x_prime]
    remaining_moment = m - calculate_moment(x_prime, weights_array)
    capital_p = n
    while capital_p > n - c:
        x_prime_copy[capital_p - 1] = remaining_moment // weights_array[capital_p]
        if x_prime_copy[capital_p - 1] > (q - 1):
            return []
        remaining_moment -= x_prime_copy[capital_p - 1] * weights_array[capital_p]
        capital_p -= 1
    if remaining_moment != 0:
        return []
    return x_prime_copy

    
def shift_a_to_right_of_b(a: int, b: int, y: list):
    """
    Given 1-indexed indices a and b, shifts the element y_a to the right of y_b.
    """
    assert a < b
    value = y.pop(a - 1)
    y.insert(b - 1, value)

# def get_weight(c: int, weights_array: list[int]) -> int:
#     return 0 if c <= 0 else weights_array[c]

# def delta_i_position(i: int, y: list, delta_symbols: list[str]):
#     """
#     Returns the 1-indexed position of delta_i within y.
#     """
#     return y.index(delta_symbols[i]) + 1

# def print_current_x(x_prime: str | list[int | str], delta_symbols: list[str], delta_values: list[int]):
#     delta_index = 1
#     result = ''
#     for c in x_prime:
#         if str(c) in ["0", "1"]:
#             result += str(c)
#         elif delta_values[delta_index] == -1:
#             result += delta_symbols[delta_index]
#             delta_index += 1
#         else:
#             result += str(delta_values[delta_index])
#             delta_index += 1
#     return result

# def decode_remaining_when_p_equals_c(capital_i: int, p: int, weights_array: list[int], delta_values: list[int]):
#     result = ''
#     for num in range(p, 0, -1):
#         if weights_array[num] > capital_i:
#             result += '0'
#         else:
#             result += '1'
#             capital_i -= weights_array[num]
#     result = result[::-1]
#     print(f"{result=}")
#     for num in range(1, p + 1):
#         delta_values[num] = int(result[num - 1])
#     print(f"{delta_values=}")

def decode_remaining_when_p_equals_c(capital_i: int, capital_p: int, x_prime: list[int], weights_array: list[int]):
    while capital_p > 0:
        x_prime[capital_p - 1] = capital_i // weights_array[capital_p]
        capital_i -= x_prime[capital_p - 1] * weights_array[capital_p]
        capital_p -= 1


def decode(y: list[int], m: int, d: int, q: int, n: int, do_print_and_debug_parameter=True) -> list[int]:
    global do_print_and_debug
    do_print_and_debug = do_print_and_debug_parameter

    c = n - len(y) # Number of unfound deltas
    x_prime = y + [-1] * c # Using -1 for delta
    weights_array = generate_weights_array(n, d, q)
    capital_i = calculate_i(m, x_prime, weights_array)

    print(f"Beginning decode of '{x_prime}' with {m=}, {n=}, {d=}, {q=}.")

    weights_sum_array = [0]
    for num in range(1, len(weights_array)):
        weights_sum_array.append(weights_sum_array[num - 1] + weights_array[num])

    possible_result = decode_if_all_deletions_at_end(x_prime=x_prime, n=n, m=m, weights_array=weights_array, c=c, q=q)
    if possible_result != []:
        return possible_result

    capital_p = n # 1-indexed
    
    while capital_p > 0:
        capital_i = calculate_i(m, x_prime, weights_array)
        print(f"Current State: {x_prime=}, {capital_p=} {capital_i=}")
        if c == 0:
            break
        if capital_p == c:
            decode_remaining_when_p_equals_c(capital_i, capital_p, x_prime, weights_array)
            break
        if weights_array[capital_p] > capital_i:
            if x_prime[capital_p - c - 1] == 0:
                shift_a_to_right_of_b(capital_p - c, capital_p, x_prime)
                capital_p = capital_p - 1
            else:
                if capital_i < weights_array[capital_p] - weights_array[capital_p - c]:
                    x_prime[capital_p - 1] = 0
                    capital_p -= 1
                    c -= 1
                else:
                    shift_a_to_right_of_b(capital_p - c, capital_p, x_prime)
                    # capital_i = capital_i - x_prime[capital_p - c - 1] * (weights_array[capital_p] - weights_array[capital_p - c])
                    capital_p -= 1
        elif weights_array[capital_p] < capital_i:
            sigma_max = min(q - 1, capital_i // (weights_array[capital_p] - weights_array[capital_p - c]))
            print(f"{sigma_max=}")
            if x_prime[capital_p - c - 1] > sigma_max:
                x_prime[capital_p - 1] = sigma_max
                # capital_i -= sigma_max * weights_array[capital_p]
                capital_p = capital_p - 1
                c = c - 1
            elif x_prime[capital_p - c - 1] < sigma_max:
                if sigma_max * weights_array[capital_p] <= capital_i:
                    x_prime[capital_p - 1] = sigma_max
                    # capital_i -= sigma_max * weights_array[capital_p]
                    capital_p -= 1
                    c -= 1
                else:
                    shift_a_to_right_of_b(capital_p - c, capital_p, x_prime)
                    capital_p -= 1
            else:
                shift_a_to_right_of_b(capital_p - c, capital_p, x_prime)
                # capital_i = sigma_max * (weights_array[capital_p] - weights_array[capital_p - c])
                capital_p = capital_p - 1
        else: # All deltas are 0 except for the one at index p, which is 1. Note this case was not described in the paper, and
            # can probably be removed (and handled by changing the weights_array[capital_p] < capital_i to a <=)
            x_prime[capital_p - 1] = 1
            for i, num in enumerate(x_prime):
                if num == -1:
                    x_prime[i] = 0
            capital_p = 0
            c = 0
    
    return x_prime
