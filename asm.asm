move areg, #10
move breg, #5
move creg, #0
add dreg, areg, breg
sub ereg, dreg, creg
and freg, dreg, ereg
or greg, freg, creg
cmp hreg, greg, creg
je 10010, hreg
jne 10011, hreg
ja 10100, hreg
jae 10101, hreg
jb 10110, hreg
jbe 10111, hreg
jmp 11000
10010:
move creg, #0
10011:
sub ereg, dreg, creg
10100:
add dreg, areg, breg
10101:
add dreg, areg, breg
10110:
add dreg, areg, breg
sub ereg, dreg, creg
10111:
move breg, #5
move creg, #0
11000:  
move breg, #5