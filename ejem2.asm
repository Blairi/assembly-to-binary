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
