;Assignment 1: Part 2 - Question 6
;30 Sep 15
;
;Program stores numbers 0x00 to 0x4F in consecutive memory
;locations starting at 0x200.



.cseg ;select current segment as code
.org 0 ;begin assembling at address 0

;Initiate initial values
ldi r18, 0x00

ldi r26, 00 ;Setting x to point to memory location 0x200
ldi r27, 02

lp: ;Beginning of loop

st x+, r18

inc r18
cpi r18, 0x50
breq exit ;jump to exit - numbers stored up to 0x4F

jmp lp ;back to top of loop

exit: ;End of program


