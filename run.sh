#!/usr/bin/env bash
# this is script to run the python code for the Insight Data Engineering Code Challenge
# there are 5 parameters:
# 1. path for the batch_file
# 2. path for the stream_file
# 3. path for the output_file 1
# 4. path for the output_file 2
# 5. path for the output_file 3

# the code works well in the environment of Python 2.

python ./src/insight.py ./paymo_input/batch_payment.txt ./paymo_input/stream_payment.txt ./paymo_output/output1.txt ./paymo_output/output2.txt ./paymo_output/output3.txt