        .arch armv7-a
        .eabi_attribute 28, 1
        .eabi_attribute 20, 1
        .eabi_attribute 21, 1
        .eabi_attribute 23, 3
        .eabi_attribute 24, 1
        .eabi_attribute 25, 1
        .eabi_attribute 26, 2
        .eabi_attribute 30, 6
        .eabi_attribute 34, 1
        .eabi_attribute 18, 4
        .file   "main.c"
        .text
        .section        .rodata
        .align  2
.LC0:
        .ascii  "rb\000"
        .align  2
.LC1:
        .ascii  "vic.ppm\000"
        .align  2
.LC2:
        .ascii  "cannot open input file\012\000"
        .align  2
.LC3:
        .ascii  "wb\000"
        .align  2
.LC4:
        .ascii  "output.ppm\000"
        .align  2
.LC5:
        .ascii  "Invalid image format (must be 'P6')\012\000"
        .align  2
.LC6:
        .ascii  "P6\012\000"
        .align  2
.LC7:
        .ascii  "%i %i\012\000"
        .align  2
.LC8:
        .ascii  "%i\012\000"
        .align  2
.LC9:
        .ascii  "%d\012\000"
        .text
        .align  2
        .global main
        .arch armv7-a
        .syntax unified
        .arm
        .fpu vfpv3-d16
        .type   main, %function
main:
        @ args = 0, pretend = 0, frame = 96
        @ frame_needed = 1, uses_anonymous_args = 0
        push    {r4, r5, r6, r7, r8, r9, r10, fp, lr}
        add     fp, sp, #32
        sub     sp, sp, #100
        mov     r3, sp
        mov     r10, r3
        movw    r1, #:lower16:.LC0
        movt    r1, #:upper16:.LC0
        movw    r0, #:lower16:.LC1
        movt    r0, #:upper16:.LC1
        bl      fopen
        str     r0, [fp, #-52]
        ldr     r3, [fp, #-52]
        cmp     r3, #0
        bne     .L2
        movw    r3, #:lower16:stderr
        movt    r3, #:upper16:stderr
        ldr     r3, [r3]
        mov     r2, #23
        mov     r1, #1
        movw    r0, #:lower16:.LC2
        movt    r0, #:upper16:.LC2
        bl      fwrite
        mov     r3, #1
        b       .L3
.L2:
        movw    r1, #:lower16:.LC3
        movt    r1, #:upper16:.LC3
        movw    r0, #:lower16:.LC4
        movt    r0, #:upper16:.LC4
        bl      fopen
        str     r0, [fp, #-56]
        ldr     r3, [fp, #-52]
        cmp     r3, #0
        bne     .L4
        movw    r3, #:lower16:stderr
        movt    r3, #:upper16:stderr
        ldr     r3, [r3]
        mov     r2, #23
        mov     r1, #1
        movw    r0, #:lower16:.LC2
        movt    r0, #:upper16:.LC2
        bl      fwrite
        mov     r3, #1
        b       .L3
.L4:
        sub     r3, fp, #108
        ldr     r2, [fp, #-52]
        mov     r1, #16
        mov     r0, r3
        bl      fgets
        ldrb    r3, [fp, #-108] @ zero_extendqisi2
        cmp     r3, #80
        bne     .L5
        ldrb    r3, [fp, #-107] @ zero_extendqisi2
        cmp     r3, #54
        beq     .L6
.L5:
        movw    r3, #:lower16:stderr
        movt    r3, #:upper16:stderr
        ldr     r3, [r3]
        mov     r2, #36
        mov     r1, #1
        movw    r0, #:lower16:.LC5
        movt    r0, #:upper16:.LC5
        bl      fwrite
        ldr     r0, [fp, #-52]
        bl      fclose
        ldr     r0, [fp, #-56]
        bl      fclose
        mov     r0, #1
        bl      exit
.L6:
        ldr     r3, [fp, #-56]
        mov     r2, #3
        mov     r1, #1
        movw    r0, #:lower16:.LC6
        movt    r0, #:upper16:.LC6
        bl      fwrite
        sub     r3, fp, #116
        sub     r2, fp, #112
        movw    r1, #:lower16:.LC7
        movt    r1, #:upper16:.LC7
        ldr     r0, [fp, #-52]
        bl      __isoc99_fscanf
        ldr     r2, [fp, #-112]
        ldr     r3, [fp, #-116]
        movw    r1, #:lower16:.LC7
        movt    r1, #:upper16:.LC7
        ldr     r0, [fp, #-56]
        bl      fprintf
        sub     r3, fp, #120
        mov     r2, r3
        movw    r1, #:lower16:.LC8
        movt    r1, #:upper16:.LC8
        ldr     r0, [fp, #-52]
        bl      __isoc99_fscanf
        ldr     r3, [fp, #-120]
        mov     r2, r3
        movw    r1, #:lower16:.LC9
        movt    r1, #:upper16:.LC9
        ldr     r0, [fp, #-56]
        bl      fprintf
        ldr     r1, [fp, #-112]
        mov     r3, r1
        sub     r3, r3, #1
        str     r3, [fp, #-60]
        mov     r4, r1
        mov     r5, #0
        mov     r2, r4
        mov     r3, r5
        adds    r6, r2, r2
        adc     r7, r3, r3
        mov     r2, r6
        mov     r3, r7
        adds    r2, r2, r4
        adc     r3, r3, r5
        mov     r4, #0
        mov     r5, #0
        lsl     r5, r3, #3
        orr     r5, r5, r2, lsr #29
        lsl     r4, r2, #3
        mov     r2, r4
        mov     r3, r5
        mov     r3, r1
        lsl     r3, r3, #1
        add     r4, r3, r1
        mov     r6, r1
        mov     r7, #0
        mov     r2, r6
        mov     r3, r7
        adds    r0, r2, r2
        str     r0, [fp, #-132]
        adc     r3, r3, r3
        str     r3, [fp, #-128]
        ldrd    r2, [fp, #-132]
        adds    r2, r2, r6
        adc     r3, r3, r7
        mov     r6, #0
        mov     r7, #0
        lsl     r7, r3, #4
        orr     r7, r7, r2, lsr #28
        lsl     r6, r2, #4
        mov     r2, r6
        mov     r3, r7
        mov     r3, r1
        lsl     r3, r3, #1
        add     r3, r3, r1
        lsl     r3, r3, #1
        mov     r6, r1
        mov     r7, #0
        mov     r2, r6
        mov     r3, r7
        adds    r8, r2, r2
        adc     r9, r3, r3
        mov     r2, r8
        mov     r3, r9
        adds    r2, r2, r6
        adc     r3, r3, r7
        mov     r6, #0
        mov     r7, #0
        lsl     r7, r3, #4
        orr     r7, r7, r2, lsr #28
        lsl     r6, r2, #4
        mov     r2, r6
        mov     r3, r7
        mov     r3, r1
        lsl     r3, r3, #1
        add     r3, r3, r1
        lsl     r3, r3, #1
        add     r3, r3, #7
        lsr     r3, r3, #3
        lsl     r3, r3, #3
        sub     sp, sp, r3
        mov     r3, sp
        add     r3, r3, #0
        str     r3, [fp, #-64]
        ldr     ip, [fp, #-112]
        mov     r3, ip
        sub     r3, r3, #1
        str     r3, [fp, #-68]
        mov     r0, ip
        mov     r1, #0
        mov     r2, #0
        mov     r3, #0
        lsl     r3, r1, #5
        orr     r3, r3, r0, lsr #27
        lsl     r2, r0, #5
        mov     r0, ip
        mov     r1, #0
        mov     r2, #0
        mov     r3, #0
        lsl     r3, r1, #5
        orr     r3, r3, r0, lsr #27
        lsl     r2, r0, #5
        lsl     r3, ip, #2
        add     r3, r3, #7
        lsr     r3, r3, #3
        lsl     r3, r3, #3
        sub     sp, sp, r3
        mov     r3, sp
        add     r3, r3, #3
        lsr     r3, r3, #2
        lsl     r3, r3, #2
        str     r3, [fp, #-72]
        ldr     r3, [fp, #-112]
        lsr     ip, r3, #1
        mov     r3, ip
        sub     r3, r3, #1
        str     r3, [fp, #-76]
        mov     r0, ip
        mov     r1, #0
        mov     r2, #0
        mov     r3, #0
        lsl     r3, r1, #5
        orr     r3, r3, r0, lsr #27
        lsl     r2, r0, #5
        mov     r0, ip
        mov     r1, #0
        mov     r2, #0
        mov     r3, #0
        lsl     r3, r1, #5
        orr     r3, r3, r0, lsr #27
        lsl     r2, r0, #5
        lsl     r3, ip, #2
        add     r3, r3, #7
        lsr     r3, r3, #3
        lsl     r3, r3, #3
        sub     sp, sp, r3
        mov     r3, sp
        add     r3, r3, #3
        lsr     r3, r3, #2
        lsl     r3, r3, #2
        str     r3, [fp, #-80]
        ldr     r3, [fp, #-112]
        lsr     ip, r3, #1
        mov     r3, ip
        sub     r3, r3, #1
        str     r3, [fp, #-84]
        mov     r0, ip
        mov     r1, #0
        mov     r2, #0
        mov     r3, #0
        lsl     r3, r1, #5
        orr     r3, r3, r0, lsr #27
        lsl     r2, r0, #5
        mov     r0, ip
        mov     r1, #0
        mov     r2, #0
        mov     r3, #0
        lsl     r3, r1, #5
        orr     r3, r3, r0, lsr #27
        lsl     r2, r0, #5
        lsl     r3, ip, #2
        add     r3, r3, #7
        lsr     r3, r3, #3
        lsl     r3, r3, #3
        sub     sp, sp, r3
        mov     r3, sp
        add     r3, r3, #3
        lsr     r3, r3, #2
        lsl     r3, r3, #2
        str     r3, [fp, #-88]
        mov     r3, #0
        str     r3, [fp, #-44]
        b       .L7
.L18:
        mov     r3, #0
        str     r3, [fp, #-40]
        b       .L8
.L9:
        ldr     r0, [fp, #-52]
        bl      getc
        mov     r3, r0
        uxtb    r3, r3
        strb    r3, [fp, #-124]
        ldr     r0, [fp, #-52]
        bl      getc
        mov     r3, r0
        uxtb    r3, r3
        strb    r3, [fp, #-123]
        ldr     r0, [fp, #-52]
        bl      getc
        mov     r3, r0
        uxtb    r3, r3
        strb    r3, [fp, #-122]
        ldrb    r3, [fp, #-124] @ zero_extendqisi2
        ldrb    r1, [fp, #-123] @ zero_extendqisi2
        ldrb    r2, [fp, #-122] @ zero_extendqisi2
        mov     r0, r3
        bl      convertRGBtoYCC
        str     r0, [fp, #-48]
        ldr     r3, [fp, #-48]
        ldrb    r3, [r3]        @ zero_extendqisi2
        strb    r3, [fp, #-124]
        ldr     r3, [fp, #-48]
        ldrb    r3, [r3, #1]    @ zero_extendqisi2
        strb    r3, [fp, #-123]
        ldr     r3, [fp, #-48]
        ldrb    r3, [r3, #2]    @ zero_extendqisi2
        strb    r3, [fp, #-122]
        ldr     r1, [fp, #-64]
        ldr     r2, [fp, #-40]
        mov     r3, r2
        lsl     r3, r3, #1
        add     r3, r3, r2
        add     r3, r1, r3
        mov     r2, r3
        sub     r3, fp, #124
        ldrh    r1, [r3]        @ unaligned
        ldrb    r3, [r3, #2]
        strh    r1, [r2]        @ unaligned
        strb    r3, [r2, #2]
        ldr     r3, [fp, #-40]
        add     r3, r3, #1
        str     r3, [fp, #-40]
.L8:
        ldr     r2, [fp, #-40]
        ldr     r3, [fp, #-112]
        cmp     r2, r3
        bcc     .L9
        mov     r3, #0
        str     r3, [fp, #-40]
        b       .L10
.L11:
        ldr     r0, [fp, #-52]
        bl      getc
        mov     r3, r0
        uxtb    r3, r3
        strb    r3, [fp, #-124]
        ldr     r0, [fp, #-52]
        bl      getc
        mov     r3, r0
        uxtb    r3, r3
        strb    r3, [fp, #-123]
        ldr     r0, [fp, #-52]
        bl      getc
        mov     r3, r0
        uxtb    r3, r3
        strb    r3, [fp, #-122]
        ldrb    r3, [fp, #-124] @ zero_extendqisi2
        ldrb    r1, [fp, #-123] @ zero_extendqisi2
        ldrb    r2, [fp, #-122] @ zero_extendqisi2
        mov     r0, r3
        bl      convertRGBtoYCC
        str     r0, [fp, #-48]
        ldr     r3, [fp, #-48]
        ldrb    r3, [r3]        @ zero_extendqisi2
        strb    r3, [fp, #-124]
        ldr     r3, [fp, #-48]
        ldrb    r3, [r3, #1]    @ zero_extendqisi2
        strb    r3, [fp, #-123]
        ldr     r3, [fp, #-48]
        ldrb    r3, [r3, #2]    @ zero_extendqisi2
        strb    r3, [fp, #-122]
        ldr     r1, [fp, #-64]
        ldr     r2, [fp, #-40]
        mov     r3, r2
        lsl     r3, r3, #1
        add     r3, r3, r2
        add     r3, r1, r3
        add     r3, r3, r4
        mov     r2, r3
        sub     r3, fp, #124
        ldrh    r1, [r3]        @ unaligned
        ldrb    r3, [r3, #2]
        strh    r1, [r2]        @ unaligned
        strb    r3, [r2, #2]
        ldr     r3, [fp, #-40]
        add     r3, r3, #1
        str     r3, [fp, #-40]
.L10:
        ldr     r2, [fp, #-40]
        ldr     r3, [fp, #-112]
        cmp     r2, r3
        bcc     .L11
        mov     r3, #0
        str     r3, [fp, #-40]
        b       .L12
.L13:
        ldr     r3, [fp, #-40]
        asr     r3, r3, #1
        str     r3, [fp, #-92]
        ldr     r1, [fp, #-64]
        ldr     r2, [fp, #-40]
        mov     r3, r2
        lsl     r3, r3, #1
        add     r3, r3, r2
        add     r3, r1, r3
        add     r3, r3, #1
        ldrb    r0, [r3]        @ zero_extendqisi2
        ldr     r3, [fp, #-40]
        add     r2, r3, #1
        ldr     r1, [fp, #-64]
        mov     r3, r2
        lsl     r3, r3, #1
        add     r3, r3, r2
        add     r3, r1, r3
        add     r3, r3, #1
        ldrb    ip, [r3]        @ zero_extendqisi2
        ldr     r1, [fp, #-64]
        ldr     r2, [fp, #-40]
        mov     r3, r2
        lsl     r3, r3, #1
        add     r3, r3, r2
        add     r3, r1, r3
        add     r3, r3, r4
        add     r3, r3, #1
        ldrb    lr, [r3]        @ zero_extendqisi2
        ldr     r3, [fp, #-40]
        add     r2, r3, #1
        ldr     r1, [fp, #-64]
        mov     r3, r2
        lsl     r3, r3, #1
        add     r3, r3, r2
        add     r3, r1, r3
        add     r3, r3, r4
        add     r3, r3, #1
        ldrb    r3, [r3]        @ zero_extendqisi2
        mov     r2, lr
        mov     r1, ip
        bl      avg
        mov     r3, r0
        mov     r1, r3
        ldr     r3, [fp, #-80]
        ldr     r2, [fp, #-92]
        str     r1, [r3, r2, lsl #2]
        ldr     r1, [fp, #-64]
        ldr     r2, [fp, #-40]
        mov     r3, r2
        lsl     r3, r3, #1
        add     r3, r3, r2
        add     r3, r1, r3
        add     r3, r3, #2
        ldrb    r0, [r3]        @ zero_extendqisi2
        ldr     r3, [fp, #-40]
        add     r2, r3, #1
        ldr     r1, [fp, #-64]
        mov     r3, r2
        lsl     r3, r3, #1
        add     r3, r3, r2
        add     r3, r1, r3
        add     r3, r3, #2
        ldrb    ip, [r3]        @ zero_extendqisi2
        ldr     r1, [fp, #-64]
        ldr     r2, [fp, #-40]
        mov     r3, r2
        lsl     r3, r3, #1
        add     r3, r3, r2
        add     r3, r1, r3
        add     r3, r3, r4
        add     r3, r3, #2
        ldrb    lr, [r3]        @ zero_extendqisi2
        ldr     r3, [fp, #-40]
        add     r2, r3, #1
        ldr     r1, [fp, #-64]
        mov     r3, r2
        lsl     r3, r3, #1
        add     r3, r3, r2
        add     r3, r1, r3
        add     r3, r3, r4
        add     r3, r3, #2
        ldrb    r3, [r3]        @ zero_extendqisi2
        mov     r2, lr
        mov     r1, ip
        bl      avg
        mov     r3, r0
        mov     r1, r3
        ldr     r3, [fp, #-88]
        ldr     r2, [fp, #-92]
        str     r1, [r3, r2, lsl #2]
        ldr     r3, [fp, #-40]
        add     r3, r3, #2
        str     r3, [fp, #-40]
.L12:
        ldr     r2, [fp, #-40]
        ldr     r3, [fp, #-112]
        cmp     r2, r3
        bcc     .L13
        mov     r3, #0
        str     r3, [fp, #-40]
        b       .L14
.L15:
        ldr     r3, [fp, #-40]
        asr     r3, r3, #1
        str     r3, [fp, #-92]
        ldr     r1, [fp, #-64]
        ldr     r2, [fp, #-40]
        mov     r3, r2
        lsl     r3, r3, #1
        add     r3, r3, r2
        add     r3, r1, r3
        ldrb    r0, [r3]        @ zero_extendqisi2
        ldr     r3, [fp, #-80]
        ldr     r2, [fp, #-92]
        ldr     r3, [r3, r2, lsl #2]
        uxtb    r1, r3
        ldr     r3, [fp, #-88]
        ldr     r2, [fp, #-92]
        ldr     r3, [r3, r2, lsl #2]
        uxtb    r3, r3
        mov     r2, r3
        bl      convertYCCtoRGB
        str     r0, [fp, #-48]
        ldr     r3, [fp, #-56]
        mov     r2, #1
        mov     r1, #1
        ldr     r0, [fp, #-48]
        bl      fwrite
        ldr     r3, [fp, #-48]
        add     r0, r3, #1
        ldr     r3, [fp, #-56]
        mov     r2, #1
        mov     r1, #1
        bl      fwrite
        ldr     r3, [fp, #-48]
        add     r0, r3, #2
        ldr     r3, [fp, #-56]
        mov     r2, #1
        mov     r1, #1
        bl      fwrite
        ldr     r3, [fp, #-40]
        add     r2, r3, #1
        ldr     r1, [fp, #-64]
        mov     r3, r2
        lsl     r3, r3, #1
        add     r3, r3, r2
        add     r3, r1, r3
        ldrb    r0, [r3]        @ zero_extendqisi2
        ldr     r3, [fp, #-80]
        ldr     r2, [fp, #-92]
        ldr     r3, [r3, r2, lsl #2]
        uxtb    r1, r3
        ldr     r3, [fp, #-88]
        ldr     r2, [fp, #-92]
        ldr     r3, [r3, r2, lsl #2]
        uxtb    r3, r3
        mov     r2, r3
        bl      convertYCCtoRGB
        str     r0, [fp, #-48]
        ldr     r3, [fp, #-56]
        mov     r2, #1
        mov     r1, #1
        ldr     r0, [fp, #-48]
        bl      fwrite
        ldr     r3, [fp, #-48]
        add     r0, r3, #1
        ldr     r3, [fp, #-56]
        mov     r2, #1
        mov     r1, #1
        bl      fwrite
        ldr     r3, [fp, #-48]
        add     r0, r3, #2
        ldr     r3, [fp, #-56]
        mov     r2, #1
        mov     r1, #1
        bl      fwrite
        ldr     r3, [fp, #-40]
        add     r3, r3, #2
        str     r3, [fp, #-40]
.L14:
        ldr     r2, [fp, #-40]
        ldr     r3, [fp, #-112]
        cmp     r2, r3
        bcc     .L15
        mov     r3, #0
        str     r3, [fp, #-40]
        b       .L16
.L17:
        ldr     r3, [fp, #-40]
        asr     r3, r3, #1
        str     r3, [fp, #-92]
        ldr     r1, [fp, #-64]
        ldr     r2, [fp, #-40]
        mov     r3, r2
        lsl     r3, r3, #1
        add     r3, r3, r2
        add     r3, r1, r3
        add     r3, r3, r4
        ldrb    r0, [r3]        @ zero_extendqisi2
        ldr     r3, [fp, #-80]
        ldr     r2, [fp, #-92]
        ldr     r3, [r3, r2, lsl #2]
        uxtb    r1, r3
        ldr     r3, [fp, #-88]
        ldr     r2, [fp, #-92]
        ldr     r3, [r3, r2, lsl #2]
        uxtb    r3, r3
        mov     r2, r3
        bl      convertYCCtoRGB
        str     r0, [fp, #-48]
        ldr     r3, [fp, #-56]
        mov     r2, #1
        mov     r1, #1
        ldr     r0, [fp, #-48]
        bl      fwrite
        ldr     r3, [fp, #-48]
        add     r0, r3, #1
        ldr     r3, [fp, #-56]
        mov     r2, #1
        mov     r1, #1
        bl      fwrite
        ldr     r3, [fp, #-48]
        add     r0, r3, #2
        ldr     r3, [fp, #-56]
        mov     r2, #1
        mov     r1, #1
        bl      fwrite
        ldr     r3, [fp, #-40]
        add     r2, r3, #1
        ldr     r1, [fp, #-64]
        mov     r3, r2
        lsl     r3, r3, #1
        add     r3, r3, r2
        add     r3, r1, r3
        add     r3, r3, r4
        ldrb    r0, [r3]        @ zero_extendqisi2
        ldr     r3, [fp, #-80]
        ldr     r2, [fp, #-92]
        ldr     r3, [r3, r2, lsl #2]
        uxtb    r1, r3
        ldr     r3, [fp, #-88]
        ldr     r2, [fp, #-92]
        ldr     r3, [r3, r2, lsl #2]
        uxtb    r3, r3
        mov     r2, r3
        bl      convertYCCtoRGB
        str     r0, [fp, #-48]
        ldr     r3, [fp, #-56]
        mov     r2, #1
        mov     r1, #1
        ldr     r0, [fp, #-48]
        bl      fwrite
        ldr     r3, [fp, #-48]
        add     r0, r3, #1
        ldr     r3, [fp, #-56]
        mov     r2, #1
        mov     r1, #1
        bl      fwrite
        ldr     r3, [fp, #-48]
        add     r0, r3, #2
        ldr     r3, [fp, #-56]
        mov     r2, #1
        mov     r1, #1
        bl      fwrite
        ldr     r3, [fp, #-40]
        add     r3, r3, #2
        str     r3, [fp, #-40]
.L16:
        ldr     r2, [fp, #-40]
        ldr     r3, [fp, #-112]
        cmp     r2, r3
        bcc     .L17
        ldr     r3, [fp, #-44]
        add     r3, r3, #2
        str     r3, [fp, #-44]
.L7:
        ldr     r2, [fp, #-44]
        ldr     r3, [fp, #-116]
        cmp     r2, r3
        bcc     .L18
        ldr     r0, [fp, #-48]
        bl      free
        ldr     r0, [fp, #-52]
        bl      fclose
        ldr     r0, [fp, #-56]
        bl      fclose
        mov     r3, #0
.L3:
        mov     sp, r10
        mov     r0, r3
        sub     sp, fp, #32
        @ sp needed
        pop     {r4, r5, r6, r7, r8, r9, r10, fp, pc}
        .size   main, .-main
        .align  2
        .global convertRGBtoYCC
        .syntax unified
        .arm
        .fpu vfpv3-d16
        .type   convertRGBtoYCC, %function
convertRGBtoYCC:
        @ args = 0, pretend = 0, frame = 8
        @ frame_needed = 1, uses_anonymous_args = 0
        push    {r4, fp, lr}
        add     fp, sp, #8
        sub     sp, sp, #12
        mov     r3, r0
        strb    r3, [fp, #-13]
        mov     r3, r1
        strb    r3, [fp, #-14]
        mov     r3, r2
        strb    r3, [fp, #-15]
        mov     r0, #12
        bl      malloc
        mov     r3, r0
        mov     r4, r3
        ldrb    r3, [fp, #-13]  @ zero_extendqisi2
        lsl     r2, r3, #6
        ldrb    r3, [fp, #-13]  @ zero_extendqisi2
        lsl     r3, r3, #1
        add     r2, r2, r3
        ldrb    r3, [fp, #-14]  @ zero_extendqisi2
        lsl     r3, r3, #7
        add     r2, r2, r3
        ldrb    r3, [fp, #-14]  @ zero_extendqisi2
        add     r2, r2, r3
        ldrb    r3, [fp, #-15]  @ zero_extendqisi2
        lsl     r3, r3, #4
        add     r2, r2, r3
        ldrb    r3, [fp, #-15]  @ zero_extendqisi2
        lsl     r3, r3, #3
        add     r2, r2, r3
        ldrb    r3, [fp, #-15]  @ zero_extendqisi2
        add     r3, r2, r3
        asr     r3, r3, #8
        uxtb    r3, r3
        add     r3, r3, #16
        uxtb    r3, r3
        strb    r3, [r4]
        ldrb    r3, [fp, #-13]  @ zero_extendqisi2
        lsl     r2, r3, #5
        ldrb    r3, [fp, #-13]  @ zero_extendqisi2
        lsl     r3, r3, #2
        add     r2, r2, r3
        ldrb    r3, [fp, #-13]  @ zero_extendqisi2
        lsl     r3, r3, #1
        add     r3, r2, r3
        rsb     r2, r3, #0
        ldrb    r3, [fp, #-14]  @ zero_extendqisi2
        lsl     r1, r3, #6
        ldrb    r3, [fp, #-14]  @ zero_extendqisi2
        lsl     r3, r3, #3
        add     r1, r1, r3
        ldrb    r3, [fp, #-14]  @ zero_extendqisi2
        lsl     r3, r3, #1
        add     r3, r1, r3
        sub     r2, r2, r3
        ldrb    r3, [fp, #-15]  @ zero_extendqisi2
        lsl     r3, r3, #7
        add     r2, r2, r3
        ldrb    r3, [fp, #-15]  @ zero_extendqisi2
        lsl     r3, r3, #4
        sub     r3, r2, r3
        asr     r3, r3, #8
        uxtb    r2, r3
        add     r3, r4, #1
        sub     r2, r2, #128
        uxtb    r2, r2
        strb    r2, [r3]
        ldrb    r3, [fp, #-13]  @ zero_extendqisi2
        lsl     r2, r3, #7
        ldrb    r3, [fp, #-13]  @ zero_extendqisi2
        lsl     r3, r3, #4
        sub     r2, r2, r3
        ldrb    r3, [fp, #-14]  @ zero_extendqisi2
        lsl     r1, r3, #6
        ldrb    r3, [fp, #-14]  @ zero_extendqisi2
        lsl     r3, r3, #5
        add     r1, r1, r3
        ldrb    r3, [fp, #-14]  @ zero_extendqisi2
        lsl     r3, r3, #1
        sub     r3, r1, r3
        sub     r2, r2, r3
        ldrb    r3, [fp, #-15]  @ zero_extendqisi2
        lsl     r1, r3, #4
        ldrb    r3, [fp, #-15]  @ zero_extendqisi2
        lsl     r3, r3, #1
        add     r3, r1, r3
        sub     r3, r2, r3
        asr     r3, r3, #8
        uxtb    r2, r3
        add     r3, r4, #2
        sub     r2, r2, #128
        uxtb    r2, r2
        strb    r2, [r3]
        mov     r3, r4
        mov     r0, r3
        sub     sp, fp, #8
        @ sp needed
        pop     {r4, fp, pc}
        .size   convertRGBtoYCC, .-convertRGBtoYCC
        .align  2
        .global convertYCCtoRGB
        .syntax unified
        .arm
        .fpu vfpv3-d16
        .type   convertYCCtoRGB, %function
convertYCCtoRGB:
        @ args = 0, pretend = 0, frame = 8
        @ frame_needed = 1, uses_anonymous_args = 0
        push    {r4, fp, lr}
        add     fp, sp, #8
        sub     sp, sp, #12
        mov     r3, r0
        strb    r3, [fp, #-13]
        mov     r3, r1
        strb    r3, [fp, #-14]
        mov     r3, r2
        strb    r3, [fp, #-15]
        mov     r0, #3
        bl      malloc
        mov     r3, r0
        mov     r4, r3
        ldrb    r3, [fp, #-13]  @ zero_extendqisi2
        vmov    s15, r3 @ int
        vcvt.f64.s32    d6, s15
        ldrb    r3, [fp, #-15]  @ zero_extendqisi2
        sub     r3, r3, #128
        vmov    s15, r3 @ int
        vcvt.f64.s32    d7, s15
        vldr.64 d5, .L24
        vmul.f64        d7, d7, d5
        vadd.f64        d7, d6, d7
        vcvt.u32.f64    s15, d7
        vstr.32 s15, [fp, #-20] @ int
        ldr     r3, [fp, #-20]
        uxtb    r3, r3
        strb    r3, [r4]
        ldrb    r3, [fp, #-13]  @ zero_extendqisi2
        vmov    s15, r3 @ int
        vcvt.f64.s32    d6, s15
        ldrb    r3, [fp, #-14]  @ zero_extendqisi2
        sub     r3, r3, #128
        vmov    s15, r3 @ int
        vcvt.f64.s32    d7, s15
        vldr.64 d5, .L24+8
        vmul.f64        d7, d7, d5
        vsub.f64        d6, d6, d7
        ldrb    r3, [fp, #-15]  @ zero_extendqisi2
        sub     r3, r3, #128
        vmov    s15, r3 @ int
        vcvt.f64.s32    d7, s15
        vldr.64 d5, .L24+16
        vmul.f64        d7, d7, d5
        vsub.f64        d7, d6, d7
        add     r3, r4, #1
        vcvt.u32.f64    s15, d7
        vstr.32 s15, [fp, #-20] @ int
        ldr     r2, [fp, #-20]
        uxtb    r2, r2
        strb    r2, [r3]
        ldrb    r3, [fp, #-13]  @ zero_extendqisi2
        vmov    s15, r3 @ int
        vcvt.f64.s32    d6, s15
        ldrb    r3, [fp, #-14]  @ zero_extendqisi2
        sub     r3, r3, #128
        vmov    s15, r3 @ int
        vcvt.f64.s32    d7, s15
        vldr.64 d5, .L24+24
        vmul.f64        d7, d7, d5
        vadd.f64        d7, d6, d7
        add     r3, r4, #2
        vcvt.u32.f64    s15, d7
        vstr.32 s15, [fp, #-20] @ int
        ldr     r2, [fp, #-20]
        uxtb    r2, r2
        strb    r2, [r3]
        mov     r3, r4
        mov     r0, r3
        sub     sp, fp, #8
        @ sp needed
        pop     {r4, fp, pc}
.L25:
        .align  3
.L24:
        .word   -1924145349
        .word   1073114775
        .word   1674831087
        .word   1070990939
        .word   -1113805279
        .word   1072093747
        .word   -1408749273
        .word   1073502748
        .size   convertYCCtoRGB, .-convertYCCtoRGB
        .align  2
        .global avg
        .syntax unified
        .arm
        .fpu vfpv3-d16
        .type   avg, %function
avg:
        @ args = 0, pretend = 0, frame = 8
        @ frame_needed = 1, uses_anonymous_args = 0
        @ link register save eliminated.
        str     fp, [sp, #-4]!
        add     fp, sp, #0
        sub     sp, sp, #12
        mov     ip, r0
        mov     r0, r1
        mov     r1, r2
        mov     r2, r3
        mov     r3, ip
        strb    r3, [fp, #-5]
        mov     r3, r0
        strb    r3, [fp, #-6]
        mov     r3, r1
        strb    r3, [fp, #-7]
        mov     r3, r2
        strb    r3, [fp, #-8]
        ldrb    r2, [fp, #-5]   @ zero_extendqisi2
        ldrb    r3, [fp, #-6]   @ zero_extendqisi2
        add     r2, r2, r3
        ldrb    r3, [fp, #-6]   @ zero_extendqisi2
        add     r2, r2, r3
        ldrb    r3, [fp, #-8]   @ zero_extendqisi2
        add     r3, r2, r3
        asr     r3, r3, #2
        uxtb    r3, r3
        mov     r0, r3
        add     sp, fp, #0
        @ sp needed
        ldr     fp, [sp], #4
        bx      lr
        .size   avg, .-avg
        .ident  "GCC: (GNU) 8.2.1 20180801 (Red Hat 8.2.1-2)"
        .section        .note.GNU-stack,"",%progbits
