// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

(LOOP)
	@R1
	D=M 
	@END 
	D;JEQ // if R1==0 go to END
	
	@R0  
	D=M
	@R2
	M=D+M  // R2 = R2 + R0 
	
	@R1 
	M=M-1  // decrement R1
	@LOOP
	0;JMP  // goto LOOP

(END)
    @END  // program's end 
    0;JMP // infinite loop