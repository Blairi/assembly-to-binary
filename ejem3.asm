move areg, #10  
move breg, #5 
move creg, #0 
add dreg, areg, breg 
sub ereg, dreg, creg 
xor freg, dreg, ereg 
shl greg, freg, #2  
cmp hreg, greg, #20 
je 10010, hreg 
jne 10011, hreg 
ja 10100, hreg 
jb 10110, hreg 
jmp 11000
