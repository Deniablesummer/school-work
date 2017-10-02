;Version 1.1
;22 Oct 2015
.device ATmega2560
;this program adds two matrices of size 5x5
;			  subtracts two matrices of size 5x5
;first we initialize matrices (mymatrix1 and mymatrix2) and then store the added result in mymatrix3
;then we then store the subtracted result in mymatrix4

;first get a pointer to matrix1 and put it in Register X: R27:R26
	ldi R26, low(mymatrix1); get the low order byte of the address
	ldi R27, high(mymatrix1); get the higher order byte of the address
	ldi R16, 45; starting value of matrix1
	ldi R17, 25; number of values to initializeis matrix size 2x2
;do while (r17 > 0) loop
loop: 
	st X+, r16;
	inc R16; next value to initialize
	dec R17; decrement count R17
	breq nextinit ; initialized first matrix. Go to next oneif R17=0
	rjmp loop

;now initialize second matrix
nextinit:
	ldi R28, low(mymatrix2); get the low order byte of the address
	ldi r29, high(mymatrix2); get the higher order byte of the address
	ldi R16, 10; starting value of mymatrix2
	ldi R17, 25; number of values to initialize
;do while (r17 > 0) loop
loop1: 
	st X+, r16;
	inc R16; next value to initialize
	dec R17;
	breq add_matrix; initialied second matrix. go to add them
	rjmp loop1
add_matrix:
	;get the address of matrix1 into X(R27:R26)register
	ldi R26, low(mymatrix1); get the low order byte of the address
	ldi R27, high(mymatrix1); get the higher order byte of the address
	;get the address of matrix2 into Y(R29:R28)register
	ldi R28, low(mymatrix2); get the low order byte of the address
	ldi R29, high(mymatrix2); get the higher order byte of the address
	;get the address of matrix into Z(R31:R30)register
	ldi R30, low(mymatrix3); get the low order byte of the address
	ldi R31, high(mymatrix3); get the higher order byte of the address
	;add matrices in a loop
	ldi R17, 25; number of values to initialize
loop2:
	ld R0,X+;get the element from matrix1 into R0
	ld R1,Y+;get the element from matrix2 into R1
	add R0, R1; R0=R0+R1 add the elements
	st Z+,R0; store the resultin appropriate location
	dec R17;
	breq sub_matrix ; if not continue
	rjmp loop2
sub_matrix:
	;get the address of matrix1 into X(R27:R26)register
	ldi R26, low(mymatrix1); get the low order byte of the address
	ldi R27, high(mymatrix1); get the higher order byte of the address
	;get the address of matrix2 into Y(R29:R28)register
	ldi R28, low(mymatrix2); get the low order byte of the address
	ldi R29, high(mymatrix2); get the higher order byte of the address
	;get the address of matrix into Z(R31:R30)register
	ldi R30, low(mymatrix4); get the low order byte of the address
	ldi R31, high(mymatrix4); get the higher order byte of the address
	;subtract matrices in a loop
	ldi R17, 25; number of values to initialize
loop3:
	ld R0,X+;get the element from matrix1 into R0
	ld R1,Y+;get the element from matrix2 into R1
	sub R0, R1; R0=R0-R1 add the elements
	st Z+,R0; store the result in appropriate location
	dec R17;
	breq done; we are done subtracting matrices
	rjmp loop3
	;if not continue



done:
	rjmp done; infinite loop
.dseg
.org 0x000200 ; ATmega2560 data memory starts at 0x000200
mymatrix1:	.byte 25	; defines 25 bytes of storage for mymatrix1
mymatrix2:	.byte 25	; defines 25 bytes of storage for mymatrix2
mymatrix3:	.byte 25	; defines 25 bytes of storage for mymatrix3
mymatrix4:	.byte 25	; defines 25 bytes of storage for mymatrix4
