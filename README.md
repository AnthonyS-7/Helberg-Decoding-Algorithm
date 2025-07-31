# Helberg-Decoding-Algorithm

This repository contains an algorithm to decode Helberg codes, and test files to verify the programs work.

Note: The Deletions Algorithm (in decode_d_deletion_error_non_binary_alphabet.py) is implemented in a way where
it requires the exact moment, because that is what is needed in the Indel Algorithm. This could be easily changed 
to only take the remainder of the moment, by using the Moment Algorithm to first recover the exact moment, and then 
doing the rest of the Deletions Algorithm as implemented.

### Instructions

To test the Indels Algorithm, use the file test_program_indels_nonbinary.py. This script tests the algorithm on every codeword of every codebook that has n, d, and q in the specified range. Alternatively, if specific_x is non-empty, it will only do the strings in specific_x (which must have length in the specified range of n).

Specify the following parameters by writing them in the script:
- n_min, n_max: The range of n (length of the original codeword), inclusive on both ends
- d_min, d_max: The range of d (maximum number of errors), inclusive on both ends
- q_min, q_max: The range of q (alphabet size), inclusive on both ends. q_min should be at least 2.
- do_full_print, do_any_print, print_starting_new_x: Determines how much information should be printed about the program's progress. If do_full_print is set to True, then do_any_print must also be set to True.
- specific_x: If non-empty, the program will only test the strings in specific_x (which must have length in the specified range of n).
- crash_on_fail: If True, the program will crash if it fails to decode any string. 
- log_file: The name of the file to write logs in. **If this file already exists, it will be overwritten.**

To test the Deletions Algorithm, use the file test_program_deletions_nonbinary.py. The parameters are the same as above, except there is no specific_x.

README.md creation date: Jul 16, 2025.
