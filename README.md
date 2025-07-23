# Helberg-Decoding-Algorithm

This repository contains an algorithm to decode Helberg codes, and test files to verify the programs work.

Note: The Deletions Algorithm (in decode_d_deletion_error_non_binary_alphabet.py) is implemented in a way where
it requires the exact moment, because that is what is needed in the Indel Algorithm. This could be easily changed 
to only take the remainder of the moment, by using the Moment Algorithm to first recover the exact moment, and then 
doing the rest of the Deletions Algorithm as implemented.