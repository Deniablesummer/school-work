	.file	"main.c"
	.text
	.section	.rodata
.LC0:
	.string	"rb"
.LC1:
	.string	"rgb-smaller.PPM"
.LC2:
	.string	"cannot open input file\n"
.LC3:
	.string	"wb"
.LC4:
	.string	"output.ppm"
	.align 8
.LC5:
	.string	"Invalid image format (must be 'P6')\n"
.LC6:
	.string	"%c%c"
.LC7:
	.string	"%02x"
.LC8:
	.string	"%02x%02x%02x"
	.text
	.globl	main
	.type	main, @function
main:
.LFB5:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$80, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	leaq	.LC0(%rip), %rsi
	leaq	.LC1(%rip), %rdi
	call	fopen@PLT
	movq	%rax, -48(%rbp)
	cmpq	$0, -48(%rbp)
	jne	.L2
	movq	stderr(%rip), %rax
	movq	%rax, %rcx
	movl	$23, %edx
	movl	$1, %esi
	leaq	.LC2(%rip), %rdi
	call	fwrite@PLT
	movl	$1, %eax
	jmp	.L19
.L2:
	leaq	.LC3(%rip), %rsi
	leaq	.LC4(%rip), %rdi
	call	fopen@PLT
	movq	%rax, -40(%rbp)
	cmpq	$0, -48(%rbp)
	jne	.L4
	movq	stderr(%rip), %rax
	movq	%rax, %rcx
	movl	$23, %edx
	movl	$1, %esi
	leaq	.LC2(%rip), %rdi
	call	fwrite@PLT
	movl	$1, %eax
	jmp	.L19
.L4:
	movq	-48(%rbp), %rdx
	leaq	-32(%rbp), %rax
	movl	$16, %esi
	movq	%rax, %rdi
	call	fgets@PLT
	movzbl	-32(%rbp), %eax
	cmpb	$80, %al
	jne	.L5
	movzbl	-31(%rbp), %eax
	cmpb	$54, %al
	je	.L6
.L5:
	movq	stderr(%rip), %rax
	movq	%rax, %rcx
	movl	$36, %edx
	movl	$1, %esi
	leaq	.LC5(%rip), %rdi
	call	fwrite@PLT
	movl	$1, %edi
	call	exit@PLT
.L6:
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	_IO_getc@PLT
	movl	%eax, -80(%rbp)
	movq	-40(%rbp), %rdx
	leaq	-80(%rbp), %rax
	movq	%rdx, %rcx
	movl	$1, %edx
	movl	$1, %esi
	movq	%rax, %rdi
	call	fwrite@PLT
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	_IO_getc@PLT
	movl	%eax, -76(%rbp)
	movq	-40(%rbp), %rdx
	leaq	-76(%rbp), %rax
	movq	%rdx, %rcx
	movl	$1, %edx
	movl	$1, %esi
	movq	%rax, %rdi
	call	fwrite@PLT
	movl	-76(%rbp), %edx
	movl	-80(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC6(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	_IO_getc@PLT
	movl	%eax, -80(%rbp)
	movq	-40(%rbp), %rdx
	leaq	-80(%rbp), %rax
	movq	%rdx, %rcx
	movl	$1, %edx
	movl	$1, %esi
	movq	%rax, %rdi
	call	fwrite@PLT
	movl	-80(%rbp), %eax
	movl	%eax, %edi
	call	putchar@PLT
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	_IO_getc@PLT
	movl	%eax, -80(%rbp)
	jmp	.L7
.L8:
	movl	-80(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC7(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movq	-40(%rbp), %rdx
	leaq	-80(%rbp), %rax
	movq	%rdx, %rcx
	movl	$1, %edx
	movl	$1, %esi
	movq	%rax, %rdi
	call	fwrite@PLT
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	_IO_getc@PLT
	movl	%eax, -80(%rbp)
.L7:
	movl	-80(%rbp), %eax
	cmpl	$10, %eax
	jne	.L8
	movl	-80(%rbp), %eax
	movl	%eax, %edi
	call	putchar@PLT
	movq	-40(%rbp), %rdx
	leaq	-80(%rbp), %rax
	movq	%rdx, %rcx
	movl	$1, %edx
	movl	$1, %esi
	movq	%rax, %rdi
	call	fwrite@PLT
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	_IO_getc@PLT
	movl	%eax, -80(%rbp)
	jmp	.L9
.L10:
	movl	-80(%rbp), %eax
	movl	%eax, %edi
	call	putchar@PLT
	movq	-40(%rbp), %rdx
	leaq	-80(%rbp), %rax
	movq	%rdx, %rcx
	movl	$1, %edx
	movl	$1, %esi
	movq	%rax, %rdi
	call	fwrite@PLT
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	_IO_getc@PLT
	movl	%eax, -80(%rbp)
.L9:
	movl	-80(%rbp), %eax
	cmpl	$10, %eax
	jne	.L10
	movl	-80(%rbp), %eax
	movl	%eax, %edi
	call	putchar@PLT
	movq	-40(%rbp), %rdx
	leaq	-80(%rbp), %rax
	movq	%rdx, %rcx
	movl	$1, %edx
	movl	$1, %esi
	movq	%rax, %rdi
	call	fwrite@PLT
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	_IO_getc@PLT
	movl	%eax, -80(%rbp)
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	_IO_getc@PLT
	movl	%eax, -76(%rbp)
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	_IO_getc@PLT
	movl	%eax, -72(%rbp)
	movl	$0, -68(%rbp)
	jmp	.L11
.L15:
	movl	-72(%rbp), %eax
	movzbl	%al, %edx
	movl	-76(%rbp), %eax
	movzbl	%al, %ecx
	movl	-80(%rbp), %eax
	movzbl	%al, %eax
	movl	%ecx, %esi
	movl	%eax, %edi
	call	convertRGBtoYCC
	movq	%rax, -64(%rbp)
	movq	-64(%rbp), %rax
	addq	$2, %rax
	movzbl	(%rax), %eax
	movzbl	%al, %edx
	movq	-64(%rbp), %rax
	addq	$1, %rax
	movzbl	(%rax), %eax
	movzbl	%al, %ecx
	movq	-64(%rbp), %rax
	movzbl	(%rax), %eax
	movzbl	%al, %eax
	movl	%ecx, %esi
	movl	%eax, %edi
	call	convertYCCtoRGB
	movq	%rax, -56(%rbp)
	movq	-40(%rbp), %rdx
	movq	-56(%rbp), %rax
	movq	%rdx, %rcx
	movl	$1, %edx
	movl	$1, %esi
	movq	%rax, %rdi
	call	fwrite@PLT
	movq	-56(%rbp), %rax
	leaq	1(%rax), %rdi
	movq	-40(%rbp), %rax
	movq	%rax, %rcx
	movl	$1, %edx
	movl	$1, %esi
	call	fwrite@PLT
	movq	-56(%rbp), %rax
	leaq	2(%rax), %rdi
	movq	-40(%rbp), %rax
	movq	%rax, %rcx
	movl	$1, %edx
	movl	$1, %esi
	call	fwrite@PLT
	movl	-72(%rbp), %ecx
	movl	-76(%rbp), %edx
	movl	-80(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC8(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movl	-68(%rbp), %ecx
	movl	$1717986919, %edx
	movl	%ecx, %eax
	imull	%edx
	sarl	$3, %edx
	movl	%ecx, %eax
	sarl	$31, %eax
	subl	%eax, %edx
	movl	%edx, %eax
	sall	$2, %eax
	addl	%edx, %eax
	sall	$2, %eax
	subl	%eax, %ecx
	movl	%ecx, %edx
	cmpl	$19, %edx
	jne	.L12
	movl	$10, %edi
	call	putchar@PLT
	jmp	.L13
.L12:
	movl	$32, %edi
	call	putchar@PLT
.L13:
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	_IO_getc@PLT
	movl	%eax, -80(%rbp)
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	_IO_getc@PLT
	movl	%eax, -76(%rbp)
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	_IO_getc@PLT
	movl	%eax, -72(%rbp)
	addl	$1, -68(%rbp)
.L11:
	movl	-80(%rbp), %eax
	cmpl	$-1, %eax
	je	.L14
	movl	-76(%rbp), %eax
	cmpl	$-1, %eax
	je	.L14
	movl	-72(%rbp), %eax
	cmpl	$-1, %eax
	jne	.L15
.L14:
	movl	-80(%rbp), %eax
	cmpl	$-1, %eax
	je	.L16
	movq	-40(%rbp), %rdx
	leaq	-80(%rbp), %rax
	movq	%rdx, %rcx
	movl	$1, %edx
	movl	$1, %esi
	movq	%rax, %rdi
	call	fwrite@PLT
	movl	-80(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC7(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
.L16:
	movl	-76(%rbp), %eax
	cmpl	$-1, %eax
	je	.L17
	movq	-40(%rbp), %rdx
	leaq	-76(%rbp), %rax
	movq	%rdx, %rcx
	movl	$1, %edx
	movl	$1, %esi
	movq	%rax, %rdi
	call	fwrite@PLT
	movl	-76(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC7(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
.L17:
	movl	-72(%rbp), %eax
	cmpl	$-1, %eax
	je	.L18
	movq	-40(%rbp), %rdx
	leaq	-72(%rbp), %rax
	movq	%rdx, %rcx
	movl	$1, %edx
	movl	$1, %esi
	movq	%rax, %rdi
	call	fwrite@PLT
	movl	-72(%rbp), %eax
	movl	%eax, %esi
	leaq	.LC7(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
.L18:
	movl	$10, %edi
	call	putchar@PLT
	movq	-64(%rbp), %rax
	movq	%rax, %rdi
	call	free@PLT
	movq	-56(%rbp), %rax
	movq	%rax, %rdi
	call	free@PLT
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	fclose@PLT
	movq	-40(%rbp), %rax
	movq	%rax, %rdi
	call	fclose@PLT
	movq	-40(%rbp), %rax
	movq	%rax, %rdi
	call	fclose@PLT
	movl	$0, %eax
.L19:
	movq	-8(%rbp), %rsi
	xorq	%fs:40, %rsi
	je	.L20
	call	__stack_chk_fail@PLT
.L20:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE5:
	.size	main, .-main
	.globl	convertRGBtoYCC
	.type	convertRGBtoYCC, @function
convertRGBtoYCC:
.LFB6:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movl	%esi, %ecx
	movl	%edx, %eax
	movl	%edi, %edx
	movb	%dl, -20(%rbp)
	movl	%ecx, %edx
	movb	%dl, -24(%rbp)
	movb	%al, -28(%rbp)
	movl	$12, %edi
	call	malloc@PLT
	movq	%rax, -8(%rbp)
	movzbl	-20(%rbp), %eax
	cvtsi2sd	%eax, %xmm0
	movsd	.LC9(%rip), %xmm1
	mulsd	%xmm0, %xmm1
	movzbl	-24(%rbp), %eax
	cvtsi2sd	%eax, %xmm0
	movsd	.LC10(%rip), %xmm2
	mulsd	%xmm2, %xmm0
	addsd	%xmm0, %xmm1
	movzbl	-28(%rbp), %eax
	cvtsi2sd	%eax, %xmm0
	movsd	.LC11(%rip), %xmm2
	mulsd	%xmm2, %xmm0
	addsd	%xmm1, %xmm0
	movsd	.LC12(%rip), %xmm1
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %eax
	movl	%eax, %edx
	movq	-8(%rbp), %rax
	movb	%dl, (%rax)
	movzbl	-20(%rbp), %eax
	cvtsi2sd	%eax, %xmm0
	movsd	.LC13(%rip), %xmm1
	mulsd	%xmm1, %xmm0
	movzbl	-24(%rbp), %eax
	cvtsi2sd	%eax, %xmm1
	movsd	.LC14(%rip), %xmm2
	mulsd	%xmm2, %xmm1
	subsd	%xmm1, %xmm0
	movapd	%xmm0, %xmm1
	movzbl	-28(%rbp), %eax
	cvtsi2sd	%eax, %xmm0
	movsd	.LC15(%rip), %xmm2
	mulsd	%xmm2, %xmm0
	addsd	%xmm1, %xmm0
	movsd	.LC16(%rip), %xmm1
	addsd	%xmm1, %xmm0
	movq	-8(%rbp), %rax
	addq	$1, %rax
	cvttsd2si	%xmm0, %edx
	movb	%dl, (%rax)
	movzbl	-20(%rbp), %eax
	cvtsi2sd	%eax, %xmm0
	movsd	.LC15(%rip), %xmm1
	mulsd	%xmm1, %xmm0
	movzbl	-24(%rbp), %eax
	cvtsi2sd	%eax, %xmm1
	movsd	.LC17(%rip), %xmm2
	mulsd	%xmm2, %xmm1
	subsd	%xmm1, %xmm0
	movzbl	-28(%rbp), %eax
	cvtsi2sd	%eax, %xmm1
	movsd	.LC18(%rip), %xmm2
	mulsd	%xmm2, %xmm1
	subsd	%xmm1, %xmm0
	movsd	.LC16(%rip), %xmm1
	addsd	%xmm1, %xmm0
	movq	-8(%rbp), %rax
	addq	$2, %rax
	cvttsd2si	%xmm0, %edx
	movb	%dl, (%rax)
	movq	-8(%rbp), %rax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	convertRGBtoYCC, .-convertRGBtoYCC
	.globl	convertYCCtoRGB
	.type	convertYCCtoRGB, @function
convertYCCtoRGB:
.LFB7:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movl	%edi, -20(%rbp)
	movl	%esi, -24(%rbp)
	movl	%edx, -28(%rbp)
	movl	$12, %edi
	call	malloc@PLT
	movq	%rax, -8(%rbp)
	cvtsi2sd	-20(%rbp), %xmm1
	movl	-28(%rbp), %eax
	addl	$-128, %eax
	cvtsi2sd	%eax, %xmm0
	movsd	.LC19(%rip), %xmm2
	mulsd	%xmm2, %xmm0
	addsd	%xmm1, %xmm0
	cvttsd2si	%xmm0, %eax
	movl	%eax, %edx
	movq	-8(%rbp), %rax
	movb	%dl, (%rax)
	cvtsi2sd	-20(%rbp), %xmm0
	movl	-24(%rbp), %eax
	addl	$-128, %eax
	cvtsi2sd	%eax, %xmm1
	movsd	.LC20(%rip), %xmm2
	mulsd	%xmm2, %xmm1
	subsd	%xmm1, %xmm0
	movl	-28(%rbp), %eax
	addl	$-128, %eax
	cvtsi2sd	%eax, %xmm1
	movsd	.LC21(%rip), %xmm2
	mulsd	%xmm2, %xmm1
	subsd	%xmm1, %xmm0
	movq	-8(%rbp), %rax
	addq	$1, %rax
	cvttsd2si	%xmm0, %edx
	movb	%dl, (%rax)
	cvtsi2sd	-20(%rbp), %xmm1
	movl	-24(%rbp), %eax
	addl	$-128, %eax
	cvtsi2sd	%eax, %xmm0
	movsd	.LC22(%rip), %xmm2
	mulsd	%xmm2, %xmm0
	addsd	%xmm1, %xmm0
	movq	-8(%rbp), %rax
	addq	$2, %rax
	cvttsd2si	%xmm0, %edx
	movb	%dl, (%rax)
	movq	-8(%rbp), %rax
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	convertYCCtoRGB, .-convertYCCtoRGB
	.section	.rodata
	.align 8
.LC9:
	.long	549755814
	.long	1070625456
	.align 8
.LC10:
	.long	2611340116
	.long	1071653060
	.align 8
.LC11:
	.long	721554506
	.long	1069094535
	.align 8
.LC12:
	.long	0
	.long	1076887552
	.align 8
.LC13:
	.long	4226247819
	.long	-1077743191
	.align 8
.LC14:
	.long	1992864825
	.long	1070768062
	.align 8
.LC15:
	.long	1958505087
	.long	1071388819
	.align 8
.LC16:
	.long	0
	.long	1080033280
	.align 8
.LC17:
	.long	755914244
	.long	1071095218
	.align 8
.LC18:
	.long	1443109011
	.long	1068641550
	.align 8
.LC19:
	.long	2370821947
	.long	1073114775
	.align 8
.LC20:
	.long	1674831087
	.long	1070990939
	.align 8
.LC21:
	.long	3181162017
	.long	1072093747
	.align 8
.LC22:
	.long	2886218023
	.long	1073502748
	.ident	"GCC: (Ubuntu 7.4.0-1ubuntu1~18.04.1) 7.4.0"
	.section	.note.GNU-stack,"",@progbits
