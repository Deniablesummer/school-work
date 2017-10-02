.device ATmega2560
;9 Nov 15

;Assignment 3
;This program will alternate 2 messages, gradually moving them across
;and down the LCD screen.

;Documentation is poop. Good luck debugging.

#define LCD_LIBONLY
.include "lcd.asm"
;available subroutines:
;	lcd_init
;	lcd_gotoxy
;	lcd_puts
;	lcd_clr
;	str_init

.cseg
.def xCounter =r22 ;defines x and y counter registers
.def yCounter =r23
;main {


call lcd_init ;initialize the lcd screen
call init_strings ;move strings from program memory to data memory
call lcd_clr  ;clear the lcd screen
clr r20
ldi r19, 0x03 ;loop variable
loop0: ;do while r20 != 0x03
	call lcd_clr
	call resetRowColCounter
	call displayRow
	call incRowColCounter
	call displayRow

	inc r20	;loop code
	cpse r20, r19
	jmp loop0

call flashChar


end: jmp end
;}end of main

;display message 1
displayMes1:
	push r16
	ldi r16, high(msg1)
	push r16
	ldi r16, low(msg1)
	push r16
	call lcd_puts
	pop r16
	pop r16

	pop r16
	ret

;display message 2
displayMes2:
	push r16
	ldi r16, high(msg2)
	push r16
	ldi r16, low(msg2)
	push r16
	call lcd_puts
	pop r16
	pop r16

	pop r16
	ret

;display row 1
displayRow:
	call setRowCol
		call displayMes1
		call halfSecPause
		call lcd_clr
		call setRowcol
		call displayMes2
		call halfSecPause
		call lcd_clr



;set row/column of lcd screen
setRowCol:
	push yCounter
	push xCounter
	call lcd_gotoxy
	pop xCounter
	pop yCounter
	ret

;reset row/column counter to 0
resetRowColCounter:
	ldi yCounter, 0x00
	ldi xCounter, 0x00
	ret

;increment row/column counter
incRowColCounter:
	inc yCounter
	inc xCounter
	ret

;0.5 second pause loop (subroutine)
halfSecPause:
	push r16
	push r17
	push r18
	clr r16
	clr r17
	clr r18
	loop00:
		loop01:
			loop02:
				nop
				nop
				inc r16
				cpi r16, 0x00
				brne loop02
			inc r17
			cpi r17, 0x00
			brne loop01
		inc r18
		cpi r18, 0x20
		brne loop00
	pop r16
	pop r17
	pop r18
	ret
	
;Flashes a single character in center of screen
flashChar:
	push r20
	push r19
	clr r20
	ldi r19, 0x03
	loop1: ;do while r20 != 0x03
		ldi r16, 0x00
		push r16
		ldi r16, 0x00
		push r16
		call lcd_gotoxy
		pop r16
		pop r16
		ldi r16, high(char1)
		push r16
		ldi r16, low(char1)
		push r16
		call lcd_puts
		pop r16
		pop r16
		call halfSecPause
		call lcd_clr
		call halfSecPause
		inc r20	;loop code
		cpse r20, r19
		jmp loop1

	pop r19
	pop r20
	ret
	
;Code provided from lcd_example.asm
init_strings:
	push r16
	; copy strings from program memory to data memory
	ldi r16, high(msg1)		; this the destination
	push r16
	ldi r16, low(msg1)
	push r16
	ldi r16, high(msg1_p << 1) ; this is the source
	push r16
	ldi r16, low(msg1_p << 1)
	push r16
	call str_init			; copy from program to data
	pop r16					; remove the parameters from the stack
	pop r16
	pop r16
	pop r16

	ldi r16, high(msg2)
	push r16
	ldi r16, low(msg2)
	push r16
	ldi r16, high(msg2_p << 1)
	push r16
	ldi r16, low(msg2_p << 1)
	push r16
	call str_init
	pop r16
	pop r16
	pop r16
	pop r16

	ldi r16, high(char1)
	push r16
	ldi r16, low(char1)
	push r16
	ldi r16, high(char1_p << 1)
	push r16
	ldi r16, low(char1_p << 1)
	push r16
	call str_init
	pop r16
	pop r16
	pop r16
	pop r16

	pop r16
	ret

msg1_p: .db "James A Ryan   ", 0
msg2_p: .db "CSC 230 Student", 0
char1_p: .db "       R       ", 0

.dseg
msg1: .byte 200
msg2: .byte 200
char1: .byte 200
