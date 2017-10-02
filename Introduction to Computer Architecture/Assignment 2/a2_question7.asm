;
;a2_question7
;
;
;
;

.cseg

.def A=r16
.def B=r17
clr A
clr B
ldi A, 0xA  ;A = 10
ldi B, 0x19 ;B = 25

;A+B stored in r4
mov r4,r16
add r4, r17

;A-B stored in r5
mov r5,r16
sub r5,r17

;A.B stored in r6
mov r6,r16
and r6, r17

;A|B
mov r7,r16
or r7, r17

;A<<1
mov r8, r16
lsl r8

;A>>1
mov r9, r17
lsr  r9




.dseg
.org 0x200
