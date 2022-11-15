# ELL710: Coding-Theory

## About
Assignments done as part of the course ELL710: Coding Theory, offered by IIT Delhi (Fall 2022 Semester)

You can find the detailed description of each assignment in their individual folders. A high level overview of them is as follows:
### Assignment 1
- This programming assignment required us to encode and decode binary message bits using linear block codes
- 2 types of Linear Codes were used:
  - Linear code 1: Repetition code of size n with a 1 × n generator matrix G with n = 3
  - Linear code 2: A (2<sup>m</sup> − 1, 2<sup>m</sup> − 1 − m) binary Hamming code with m = 3
- 2 types of errors were incorporated in the data:
  - Random binary error pattern of some definite length with fixed hamming weight such that the non-zero entries are uniformly distributed
  - Random binary error pattern of some definite length with fixed hamming weight such that the non-zero entries appear in burst (in successive positions)

### Assignment 2
- This programming assignment required us to implement a viterbi decoder for the following convolution code:
  ![2022-11-15 21_44_14-Programming_assignemnt_Vitterbi_Decoder pdf and 8 more pages - Person 1 - Micros](https://user-images.githubusercontent.com/62442188/201970260-f553f8c1-4e1d-4675-97a1-c313c3a12fe9.png)
- The user enters a codeword and a single error bit. The algorithm is expected to recover the codeword using the Viterbi Decoder
- For this assignment, I use 2 methods to implement the decoder
  - Greedy approach: For this, I find the state which gives minimum hamming weight and proceeds for that alone
  - Recursive approach: For this, I recurse over all possible combinations, giving better results at the expense of time complexity

## Author
[Vansh Gupta](https://github.com/V-G-spec)  
Undergraduate student, Electrical Engineering Department  
Indian Institute of Technology, Delhi  

## License
Copyright -2022 -Indian Institute of Technology, Delhi

Part of course ELL710: Coding Theory (Taught by professor [Harshan Jagadeesh](https://sites.google.com/site/jharshan/))
