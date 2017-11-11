import os

project_dir = os.path.dirname(os.path.abspath(__file__))+'/'
raw_dir=project_dir+'doc/raw/'
intermediate_dir=project_dir+'doc/intermediate/'
result_dir=project_dir+'doc/result/'

if not os.path.exists(raw_dir):
    os.makedirs(raw_dir)
if not os.path.exists(intermediate_dir):
    os.makedirs(intermediate_dir)
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

START_FROM_AUTO = 0
START_FROM_COR  = 1
START_FROM_DROP = 2
START_FROM_NORM = 3
START_FROM_SHIFT= 63
SHIFT_INPUT =4
SHIFT_TEST=8
SHIFT_TRAIN=16
SHIFT_VALIDATION=32
