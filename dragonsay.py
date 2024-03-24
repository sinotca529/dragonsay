#!/bin/python3

import shutil
import unicodedata
from itertools import zip_longest


def char_width(c):
    if unicodedata.east_asian_width(c) in 'FWA':
        return 2
    else:
        return 1


def wrap_str(s, max_width):
    current_width = 0
    lines = []

    slice_begin_idx = 0
    slice_length = 0

    for c in s:
        cw = char_width(c)
        if current_width + cw > max_width:
            line = s[slice_begin_idx:][:slice_length]

            mergin = max_width - current_width
            lines.append(" " * (mergin//2) + line + " " * (mergin - mergin//2))

            slice_begin_idx += slice_length
            slice_length = 0
            current_width = 0

        slice_length += 1
        current_width += cw

    line = s[slice_begin_idx:][:slice_length]
    mergin = max_width - current_width
    lines.append(" " * (mergin//2) + line + " " * (mergin - mergin//2))

    return lines


dragon = r'''
             ___
            / --\
           _\_\_/_
          / _     \
 /~~----_/ / \     |
'---.___           |
 .__~~~'           /~--/~----~/
 \___~~~|          ~---/~----~/
        /  /           |      (
       /  /      `---__|_--~~-\
      /  /~|      |    '
     </ /~~|      \
     <~~'~~'\     \-/
        (   )       \/_
        (   )\_       \|_
     \~~\   /  ''\__   '\|_
      \~~~~~\       ""~~~~~>'''.split('\n')

dragon_width = max(map(len, dragon))
term_width = shutil.get_terminal_size().columns
text_width = 30

msg_open = '/-' + '-' * text_width + '-\\'
msg_brank = '| ' + ' ' * text_width + ' |'
msg_close = '\\-' + '-' * text_width + '-/'
msg_space = ' ' * len(msg_open)

if dragon_width + text_width > term_width:
    print('The width of the terminal is not enough.')
    exit(0)


m = wrap_str(input(), text_width)
offset_y = max(2, 6 - len(m))

msg = [
    *[msg_space for i in range(offset_y)],
    msg_open,
    msg_brank,
    *['| ' + s + ' |' for s in m],
    msg_brank,
    msg_close
]
for i, (m, d) in enumerate(zip_longest(msg, dragon, fillvalue=msg_space)):
    if i == 7:
        print(f'{m[:-1]} >   {d}')
    else:
        print(f'{m}    {d}')
