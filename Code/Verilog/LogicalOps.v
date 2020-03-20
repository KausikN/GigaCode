/*
Summary
Library of Hardware Modules made by ME
*/

// Logical Ops
module Decoder(E, D);
input [3:1] E;
output [8:1] D;
assign D[1]=(~E[3]&~E[2]&~E[1]);
assign D[2]=(~E[3]&~E[2]&E[1]);
assign D[3]=(~E[3]&E[2]&~E[1]);
assign D[4]=(~E[3]&E[2]&E[1]);
assign D[5]=(E[3]&~E[2]&~E[1]);
assign D[6]=(E[3]&~E[2]&E[1]);
assign D[7]=(E[3]&E[2]&~E[1]);
assign D[8]=(E[3]&E[2]&E[1]);
endmodule

module MUX (Chooser, A1, A2, A3, A4, A5, A6, A7, A8, out);

input [3:1] Chooser;
input [16:1] A1, A2, A3, A4, A5, A6, A7, A8;

output [16:1] out;

wire [8:1] D;
Decoder decoder (Chooser, D);

assign out =    (D[1]) ? A1 : 
                (D[2]) ? A2 : 
                (D[3]) ? A3 : 
                (D[4]) ? A4 : 
                (D[5]) ? A5 : 
                (D[6]) ? A6 : 
                (D[7]) ? A7 : 
                A8;

endmodule

module Comp2s (A, out);

input [16:1] A;

output [16:1] out;

wire [16:1] nA;
wire carry;

NOT notop (A, nA);
RDAdder addr (nA, 16'b0000000000000001, 1'b0, out, carry);

endmodule

module AND (A, B, out);

input [16:1] A, B;

output [16:1] out;

assign out[1] = A[1] & B[1];
assign out[2] = A[2] & B[2];
assign out[3] = A[3] & B[3];
assign out[4] = A[4] & B[4];
assign out[5] = A[5] & B[5];
assign out[6] = A[6] & B[6];
assign out[7] = A[7] & B[7];
assign out[8] = A[8] & B[8];
assign out[9] = A[9] & B[9];
assign out[10] = A[10] & B[10];
assign out[11] = A[11] & B[11];
assign out[12] = A[12] & B[12];
assign out[13] = A[13] & B[13];
assign out[14] = A[14] & B[14];
assign out[15] = A[15] & B[15];
assign out[16] = A[16] & B[16];

endmodule

module NAND (A, B, out);

input [16:1] A, B;

output [16:1] out;

assign out[1] = !(A[1] & B[1]);
assign out[2] = !(A[2] & B[2]);
assign out[3] = !(A[3] & B[3]);
assign out[4] = !(A[4] & B[4]);
assign out[5] = !(A[5] & B[5]);
assign out[6] = !(A[6] & B[6]);
assign out[7] = !(A[7] & B[7]);
assign out[8] = !(A[8] & B[8]);
assign out[9] = !(A[9] & B[9]);
assign out[10] = !(A[10] & B[10]);
assign out[11] = !(A[11] & B[11]);
assign out[12] = !(A[12] & B[12]);
assign out[13] = !(A[13] & B[13]);
assign out[14] = !(A[14] & B[14]);
assign out[15] = !(A[15] & B[15]);
assign out[16] = !(A[16] & B[16]);

endmodule

module NOR (A, B, out);

input [16:1] A, B;

output [16:1] out;

assign out[1] = !(A[1] | B[1]);
assign out[2] = !(A[2] | B[2]);
assign out[3] = !(A[3] | B[3]);
assign out[4] = !(A[4] | B[4]);
assign out[5] = !(A[5] | B[5]);
assign out[6] = !(A[6] | B[6]);
assign out[7] = !(A[7] | B[7]);
assign out[8] = !(A[8] | B[8]);
assign out[9] = !(A[9] | B[9]);
assign out[10] = !(A[10] | B[10]);
assign out[11] = !(A[11] | B[11]);
assign out[12] = !(A[12] | B[12]);
assign out[13] = !(A[13] | B[13]);
assign out[14] = !(A[14] | B[14]);
assign out[15] = !(A[15] | B[15]);
assign out[16] = !(A[16] | B[16]);

endmodule

module NOT (A, out);

input [16:1] A;

output [16:1] out;

assign out[1] = !A[1];
assign out[2] = !A[2];
assign out[3] = !A[3];
assign out[4] = !A[4];
assign out[5] = !A[5];
assign out[6] = !A[6];
assign out[7] = !A[7];
assign out[8] = !A[8];
assign out[9] = !A[9];
assign out[10] = !A[10];
assign out[11] = !A[11];
assign out[12] = !A[12];
assign out[13] = !A[13];
assign out[14] = !A[14];
assign out[15] = !A[15];
assign out[16] = !A[16];

endmodule

module OR (A, B, out);

input [16:1] A, B;

output [16:1] out;

assign out[1] = A[1] | B[1];
assign out[2] = A[2] | B[2];
assign out[3] = A[3] | B[3];
assign out[4] = A[4] | B[4];
assign out[5] = A[5] | B[5];
assign out[6] = A[6] | B[6];
assign out[7] = A[7] | B[7];
assign out[8] = A[8] | B[8];
assign out[9] = A[9] | B[9];
assign out[10] = A[10] | B[10];
assign out[11] = A[11] | B[11];
assign out[12] = A[12] | B[12];
assign out[13] = A[13] | B[13];
assign out[14] = A[14] | B[14];
assign out[15] = A[15] | B[15];
assign out[16] = A[16] | B[16];

endmodule

module XNOR (A, B, out);

input [16:1] A, B;

output [16:1] out;

assign out[1] = !(A[1] ^ B[1]);
assign out[2] = !(A[2] ^ B[2]);
assign out[3] = !(A[3] ^ B[3]);
assign out[4] = !(A[4] ^ B[4]);
assign out[5] = !(A[5] ^ B[5]);
assign out[6] = !(A[6] ^ B[6]);
assign out[7] = !(A[7] ^ B[7]);
assign out[8] = !(A[8] ^ B[8]);
assign out[9] = !(A[9] ^ B[9]);
assign out[10] = !(A[10] ^ B[10]);
assign out[11] = !(A[11] ^ B[11]);
assign out[12] = !(A[12] ^ B[12]);
assign out[13] = !(A[13] ^ B[13]);
assign out[14] = !(A[14] ^ B[14]);
assign out[15] = !(A[15] ^ B[15]);
assign out[16] = !(A[16] ^ B[16]);

endmodule

module XOR (A, B, out);

input [16:1] A, B;

output [16:1] out;

assign out[1] = A[1] ^ B[1];
assign out[2] = A[2] ^ B[2];
assign out[3] = A[3] ^ B[3];
assign out[4] = A[4] ^ B[4];
assign out[5] = A[5] ^ B[5];
assign out[6] = A[6] ^ B[6];
assign out[7] = A[7] ^ B[7];
assign out[8] = A[8] ^ B[8];
assign out[9] = A[9] ^ B[9];
assign out[10] = A[10] ^ B[10];
assign out[11] = A[11] ^ B[11];
assign out[12] = A[12] ^ B[12];
assign out[13] = A[13] ^ B[13];
assign out[14] = A[14] ^ B[14];
assign out[15] = A[15] ^ B[15];
assign out[16] = A[16] ^ B[16];

endmodule

module RDAdder( a, b, cin, sum, carry);
	input [16:1] a,b;
	input cin;
	
	output wire [16:1] sum;  
	output wire carry;

	wire [1:0] pgk [16:1];
	
	wire [1:0] temp_1 [16:1];
	wire [1:0] temp_2 [16:1];
	wire [1:0] temp_3 [16:1];
	wire [1:0] temp_4 [16:1];

	wire [16:1] gk;
	

//pgk -- 00-kill && 11-generate && 10-propagate

	
//PGK Generating
assign pgk[1][0]=(a[1]&b[1]) | (b[1]&cin) | (cin&a[1]);
assign pgk[1][1]=(a[1]&b[1]) | (b[1]&cin) | (cin&a[1]);

assign pgk[2][0]=a[2]&b[2]; 
assign pgk[2][1]=a[2]|b[2];

assign pgk[3][0]=a[3]&b[3]; 
assign pgk[3][1]=a[3]|b[3];

assign pgk[4][0]=a[4]&b[4]; 
assign pgk[4][1]=a[4]|b[4];

assign pgk[5][0]=a[5]&b[5]; 
assign pgk[5][1]=a[5]|b[5];

assign pgk[6][0]=a[6]&b[6]; 
assign pgk[6][1]=a[6]|b[6];

assign pgk[7][0]=a[7]&b[7]; 
assign pgk[7][1]=a[7]|b[7];

assign pgk[8][0]=a[8]&b[8]; 
assign pgk[8][1]=a[8]|b[8];

assign pgk[9][0]=a[9]&b[9]; 
assign pgk[9][1]=a[9]|b[9];

assign pgk[10][0]=a[10]&b[10]; 
assign pgk[10][1]=a[10]|b[10];

assign pgk[11][0]=a[11]&b[11]; 
assign pgk[11][1]=a[11]|b[11];

assign pgk[12][0]=a[12]&b[12]; 
assign pgk[12][1]=a[12]|b[12];

assign pgk[13][0]=a[13]&b[13]; 
assign pgk[13][1]=a[13]|b[13];

assign pgk[14][0]=a[14]&b[14]; 
assign pgk[14][1]=a[14]|b[14];

assign pgk[15][0]=a[15]&b[15]; 
assign pgk[15][1]=a[15]|b[15];

assign pgk[16][0]=a[16]&b[16]; 
assign pgk[16][1]=a[16]|b[16];


//PGK Reducing
// 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1
// 1 - 16.15  15.14  14.13  13.12  12.11  11.10  10.9  9.8  8.7  7.6  6.5  5.4  4.3  3.2  2.1  1
// 2 - 16.14  15.13  14.12  13.11  12.10  11.9  10.8  9.7  8.6  7.5  6.4  5.3  4.2  3.1  2  1
// 4 - 16.12  15.11  14.10  13.9  12.8  11.7  10.6  9.5  8.4  7.3  6.2  5.1  4  3  2  1
// 8 - 16.8  15.7  14.6  13.5  12.4  11.3  10.2  9.1  8  7  6  5  4  3  2  1
// 16- NIL

// 1 - 16.15  15.14  14.13  13.12  12.11  11.10  10.9  9.8  8.7  7.6  6.5  5.4  4.3  3.2  2.1  1
assign temp_1[1][0]=pgk[1][0];
assign temp_1[1][1]=pgk[1][1];

assign temp_1[2][0]=(pgk[2][0])|(pgk[2][1]&pgk[1][0]);
assign temp_1[2][1]=(pgk[2][0])|(pgk[2][1]&pgk[1][1]);

assign temp_1[3][0]=(pgk[3][0])|(pgk[3][1]&pgk[2][0]);
assign temp_1[3][1]=(pgk[3][0])|(pgk[3][1]&pgk[2][1]);

assign temp_1[4][0]=(pgk[4][0])|(pgk[4][1]&pgk[3][0]);
assign temp_1[4][1]=(pgk[4][0])|(pgk[4][1]&pgk[3][1]);

assign temp_1[5][0]=(pgk[5][0])|(pgk[5][1]&pgk[4][0]);
assign temp_1[5][1]=(pgk[5][0])|(pgk[5][1]&pgk[4][1]);

assign temp_1[6][0]=(pgk[6][0])|(pgk[6][1]&pgk[5][0]);
assign temp_1[6][1]=(pgk[6][0])|(pgk[6][1]&pgk[5][1]);

assign temp_1[7][0]=(pgk[7][0])|(pgk[7][1]&pgk[6][0]);
assign temp_1[7][1]=(pgk[7][0])|(pgk[7][1]&pgk[6][1]);

assign temp_1[8][0]=(pgk[8][0])|(pgk[8][1]&pgk[7][0]);
assign temp_1[8][1]=(pgk[8][0])|(pgk[8][1]&pgk[7][1]);

assign temp_1[9][0]=(pgk[9][0])|(pgk[9][1]&pgk[8][0]);
assign temp_1[9][1]=(pgk[9][0])|(pgk[9][1]&pgk[8][1]);

assign temp_1[10][0]=(pgk[10][0])|(pgk[10][1]&pgk[9][0]);
assign temp_1[10][1]=(pgk[10][0])|(pgk[10][1]&pgk[9][1]);

assign temp_1[11][0]=(pgk[11][0])|(pgk[11][1]&pgk[10][0]);
assign temp_1[11][1]=(pgk[11][0])|(pgk[11][1]&pgk[10][1]);

assign temp_1[12][0]=(pgk[12][0])|(pgk[12][1]&pgk[11][0]);
assign temp_1[12][1]=(pgk[12][0])|(pgk[12][1]&pgk[11][1]);

assign temp_1[13][0]=(pgk[13][0])|(pgk[13][1]&pgk[12][0]);
assign temp_1[13][1]=(pgk[13][0])|(pgk[13][1]&pgk[12][1]);

assign temp_1[14][0]=(pgk[14][0])|(pgk[14][1]&pgk[13][0]);
assign temp_1[14][1]=(pgk[14][0])|(pgk[14][1]&pgk[13][1]);

assign temp_1[15][0]=(pgk[15][0])|(pgk[15][1]&pgk[14][0]);
assign temp_1[15][1]=(pgk[15][0])|(pgk[15][1]&pgk[14][1]);

assign temp_1[16][0]=(pgk[16][0])|(pgk[16][1]&pgk[15][0]);
assign temp_1[16][1]=(pgk[16][0])|(pgk[16][1]&pgk[15][1]);




// 2 - 16.14  15.13  14.12  13.11  12.10  11.9  10.8  9.7  8.6  7.5  6.4  5.3  4.2  3.1  2  1
assign temp_2[1][0]=temp_1[1][0];
assign temp_2[1][1]=temp_1[1][1];

assign temp_2[2][0]=temp_1[2][0];
assign temp_2[2][1]=temp_1[2][1];

assign temp_2[3][0]=(temp_1[3][0])|(temp_1[3][1]&temp_1[1][0]);
assign temp_2[3][1]=(temp_1[3][0])|(temp_1[3][1]&temp_1[1][1]);

assign temp_2[4][0]=(temp_1[4][0])|(temp_1[4][1]&temp_1[2][0]);
assign temp_2[4][1]=(temp_1[4][0])|(temp_1[4][1]&temp_1[2][1]);

assign temp_2[5][0]=(temp_1[5][0])|(temp_1[5][1]&temp_1[3][0]);
assign temp_2[5][1]=(temp_1[5][0])|(temp_1[5][1]&temp_1[3][1]);

assign temp_2[6][0]=(temp_1[6][0])|(temp_1[6][1]&temp_1[4][0]);
assign temp_2[6][1]=(temp_1[6][0])|(temp_1[6][1]&temp_1[4][1]);

assign temp_2[7][0]=(temp_1[7][0])|(temp_1[7][1]&temp_1[5][0]);
assign temp_2[7][1]=(temp_1[7][0])|(temp_1[7][1]&temp_1[5][1]);

assign temp_2[8][0]=(temp_1[8][0])|(temp_1[8][1]&temp_1[6][0]);
assign temp_2[8][1]=(temp_1[8][0])|(temp_1[8][1]&temp_1[6][1]);

assign temp_2[9][0]=(temp_1[9][0])|(temp_1[9][1]&temp_1[7][0]);
assign temp_2[9][1]=(temp_1[9][0])|(temp_1[9][1]&temp_1[7][1]);

assign temp_2[10][0]=(temp_1[10][0])|(temp_1[10][1]&temp_1[8][0]);
assign temp_2[10][1]=(temp_1[10][0])|(temp_1[10][1]&temp_1[8][1]);

assign temp_2[11][0]=(temp_1[11][0])|(temp_1[11][1]&temp_1[9][0]);
assign temp_2[11][1]=(temp_1[11][0])|(temp_1[11][1]&temp_1[9][1]);

assign temp_2[12][0]=(temp_1[12][0])|(temp_1[12][1]&temp_1[10][0]);
assign temp_2[12][1]=(temp_1[12][0])|(temp_1[12][1]&temp_1[10][1]);

assign temp_2[13][0]=(temp_1[13][0])|(temp_1[13][1]&temp_1[11][0]);
assign temp_2[13][1]=(temp_1[13][0])|(temp_1[13][1]&temp_1[11][1]);

assign temp_2[14][0]=(temp_1[14][0])|(temp_1[14][1]&temp_1[12][0]);
assign temp_2[14][1]=(temp_1[14][0])|(temp_1[14][1]&temp_1[12][1]);

assign temp_2[15][0]=(temp_1[15][0])|(temp_1[15][1]&temp_1[13][0]);
assign temp_2[15][1]=(temp_1[15][0])|(temp_1[15][1]&temp_1[13][1]);

assign temp_2[16][0]=(temp_1[16][0])|(temp_1[16][1]&temp_1[14][0]);
assign temp_2[16][1]=(temp_1[16][0])|(temp_1[16][1]&temp_1[14][1]);




// 4 - 16.12  15.11  14.10  13.9  12.8  11.7  10.6  9.5  8.4  7.3  6.2  5.1  4  3  2  1
assign temp_3[1][0]=temp_2[1][0];
assign temp_3[1][1]=temp_2[1][1];

assign temp_3[2][0]=temp_2[2][0];
assign temp_3[2][1]=temp_2[2][1];

assign temp_3[3][0]=temp_2[3][0];
assign temp_3[3][1]=temp_2[3][1];

assign temp_3[4][0]=temp_2[4][0];
assign temp_3[4][1]=temp_2[4][1];

assign temp_3[5][0]=(temp_2[5][0])|(temp_2[5][1]&temp_2[1][0]);
assign temp_3[5][1]=(temp_2[5][0])|(temp_2[5][1]&temp_2[1][1]);

assign temp_3[6][0]=(temp_2[6][0])|(temp_2[6][1]&temp_2[2][0]);
assign temp_3[6][1]=(temp_2[6][0])|(temp_2[6][1]&temp_2[2][1]);

assign temp_3[7][0]=(temp_2[7][0])|(temp_2[7][1]&temp_2[3][0]);
assign temp_3[7][1]=(temp_2[7][0])|(temp_2[7][1]&temp_2[3][1]);

assign temp_3[8][0]=(temp_2[8][0])|(temp_2[8][1]&temp_2[4][0]);
assign temp_3[8][1]=(temp_2[8][0])|(temp_2[8][1]&temp_2[4][1]);

assign temp_3[9][0]=(temp_2[9][0])|(temp_2[9][1]&temp_2[5][0]);
assign temp_3[9][1]=(temp_2[9][0])|(temp_2[9][1]&temp_2[5][1]);

assign temp_3[10][0]=(temp_2[10][0])|(temp_2[10][1]&temp_2[6][0]);
assign temp_3[10][1]=(temp_2[10][0])|(temp_2[10][1]&temp_2[6][1]);

assign temp_3[11][0]=(temp_2[11][0])|(temp_2[11][1]&temp_2[7][0]);
assign temp_3[11][1]=(temp_2[11][0])|(temp_2[11][1]&temp_2[7][1]);

assign temp_3[12][0]=(temp_2[12][0])|(temp_2[12][1]&temp_2[8][0]);
assign temp_3[12][1]=(temp_2[12][0])|(temp_2[12][1]&temp_2[8][1]);

assign temp_3[13][0]=(temp_2[13][0])|(temp_2[13][1]&temp_2[9][0]);
assign temp_3[13][1]=(temp_2[13][0])|(temp_2[13][1]&temp_2[9][1]);

assign temp_3[14][0]=(temp_2[14][0])|(temp_2[14][1]&temp_2[10][0]);
assign temp_3[14][1]=(temp_2[14][0])|(temp_2[14][1]&temp_2[10][1]);

assign temp_3[15][0]=(temp_2[15][0])|(temp_2[15][1]&temp_2[11][0]);
assign temp_3[15][1]=(temp_2[15][0])|(temp_2[15][1]&temp_2[11][1]);

assign temp_3[16][0]=(temp_2[16][0])|(temp_2[16][1]&temp_2[12][0]);
assign temp_3[16][1]=(temp_2[16][0])|(temp_2[16][1]&temp_2[12][1]);




// 8 - 16.8  15.7  14.6  13.5  12.4  11.3  10.2  9.1  8  7  6  5  4  3  2  1
assign temp_4[1][0]=temp_3[1][0];
assign temp_4[1][1]=temp_3[1][1];

assign temp_4[2][0]=temp_3[2][0];
assign temp_4[2][1]=temp_3[2][1];

assign temp_4[3][0]=temp_3[3][0];
assign temp_4[3][1]=temp_3[3][1];

assign temp_4[4][0]=temp_3[4][0];
assign temp_4[4][1]=temp_3[4][1];

assign temp_4[5][0]=temp_3[5][0];
assign temp_4[5][1]=temp_3[5][1];

assign temp_4[6][0]=temp_3[6][0];
assign temp_4[6][1]=temp_3[6][1];

assign temp_4[7][0]=temp_3[7][0];
assign temp_4[7][1]=temp_3[7][1];

assign temp_4[8][0]=temp_3[8][0];
assign temp_4[8][1]=temp_3[8][1];

assign temp_4[9][0]=(temp_3[9][0])|(temp_3[9][1]&temp_3[1][0]);
assign temp_4[9][1]=(temp_3[9][0])|(temp_3[9][1]&temp_3[1][1]);

assign temp_4[10][0]=(temp_3[10][0])|(temp_3[10][1]&temp_3[2][0]);
assign temp_4[10][1]=(temp_3[10][0])|(temp_3[10][1]&temp_3[2][1]);

assign temp_4[11][0]=(temp_3[11][0])|(temp_3[11][1]&temp_3[3][0]);
assign temp_4[11][1]=(temp_3[11][0])|(temp_3[11][1]&temp_3[3][1]);

assign temp_4[12][0]=(temp_3[12][0])|(temp_3[12][1]&temp_3[4][0]);
assign temp_4[12][1]=(temp_3[12][0])|(temp_3[12][1]&temp_3[4][1]);

assign temp_4[13][0]=(temp_3[13][0])|(temp_3[13][1]&temp_3[5][0]);
assign temp_4[13][1]=(temp_3[13][0])|(temp_3[13][1]&temp_3[5][1]);

assign temp_4[14][0]=(temp_3[14][0])|(temp_3[14][1]&temp_3[6][0]);
assign temp_4[14][1]=(temp_3[14][0])|(temp_3[14][1]&temp_3[6][1]);

assign temp_4[15][0]=(temp_3[15][0])|(temp_3[15][1]&temp_3[7][0]);
assign temp_4[15][1]=(temp_3[15][0])|(temp_3[15][1]&temp_3[7][1]);

assign temp_4[16][0]=(temp_3[16][0])|(temp_3[16][1]&temp_3[8][0]);
assign temp_4[16][1]=(temp_3[16][0])|(temp_3[16][1]&temp_3[8][1]);




//GK Calculating
assign gk[1]=temp_4[1][1];
assign gk[2]=temp_4[2][1];
assign gk[3]=temp_4[3][1];
assign gk[4]=temp_4[4][1];
assign gk[5]=temp_4[5][1];
assign gk[6]=temp_4[6][1];
assign gk[7]=temp_4[7][1];
assign gk[8]=temp_4[8][1];
assign gk[9]=temp_4[9][1];
assign gk[10]=temp_4[10][1];
assign gk[11]=temp_4[11][1];
assign gk[12]=temp_4[12][1];
assign gk[13]=temp_4[13][1];
assign gk[14]=temp_4[14][1];
assign gk[15]=temp_4[15][1];
assign gk[16]=temp_4[16][1];


//calculating sum
assign sum[1]=a[1]^b[1]^cin;
assign sum[2]=gk[1]^a[2]^b[2];
assign sum[3]=gk[2]^a[3]^b[3];
assign sum[4]=gk[3]^a[4]^b[4];
assign sum[5]=gk[4]^a[5]^b[5];
assign sum[6]=gk[5]^a[6]^b[6];
assign sum[7]=gk[6]^a[7]^b[7];
assign sum[8]=gk[7]^a[8]^b[8];
assign sum[9]=gk[8]^a[9]^b[9];
assign sum[10]=gk[9]^a[10]^b[10];
assign sum[11]=gk[10]^a[11]^b[11];
assign sum[12]=gk[11]^a[12]^b[12];
assign sum[13]=gk[12]^a[13]^b[13];
assign sum[14]=gk[13]^a[14]^b[14];
assign sum[15]=gk[14]^a[15]^b[15];
assign sum[16]=gk[15]^a[16]^b[16];
assign carry=gk[16];


endmodule

// Main Module
module LogicalOps (A, B, Operation, out);

input [16:1] A, B;
input [3:1] Operation;

output [16:1] out;

wire [16:1] w_and, w_or, w_not, w_xor, w_nand, w_nor, w_xnor, w_comp2s;

AND andop (A, B, w_and);
OR orop (A, B, w_or);
NOT notop (A, w_not);
XOR xorop (A, B, w_xor);
NAND nandop (A, B, w_nand);
NOR norop (A, B, w_nor);
XNOR xnorop (A, B, w_xnor);
Comp2s comp2sop (A, w_comp2s);

MUX mux (Operation, w_and, w_or, w_not, w_xor, w_nand, w_nor, w_xnor, w_comp2s, out);

endmodule

// Shifter
// Util Modules
module LeftBarrelShifter(a, shift, out);

input [16:1]  a;
input [4:1] shift;

output [16:1] out;

wire [16:1] l1, l2, l3;

// Bit 1
MUX_2_1 lm1_1 (a[1], 1'b0, shift[1], l1[1]);
MUX_2_1 lm1_2 (a[2], a[1], shift[1], l1[2]);
MUX_2_1 lm1_3 (a[3], a[2], shift[1], l1[3]);
MUX_2_1 lm1_4 (a[4], a[3], shift[1], l1[4]);
MUX_2_1 lm1_5 (a[5], a[4], shift[1], l1[5]);
MUX_2_1 lm1_6 (a[6], a[5], shift[1], l1[6]);
MUX_2_1 lm1_7 (a[7], a[6], shift[1], l1[7]);
MUX_2_1 lm1_8 (a[8], a[7], shift[1], l1[8]);
MUX_2_1 lm1_9 (a[9], a[8], shift[1], l1[9]);
MUX_2_1 lm1_10 (a[10], a[9], shift[1], l1[10]);
MUX_2_1 lm1_11 (a[11], a[10], shift[1], l1[11]);
MUX_2_1 lm1_12 (a[12], a[11], shift[1], l1[12]);
MUX_2_1 lm1_13 (a[13], a[12], shift[1], l1[13]);
MUX_2_1 lm1_14 (a[14], a[13], shift[1], l1[14]);
MUX_2_1 lm1_15 (a[15], a[14], shift[1], l1[15]);
MUX_2_1 lm1_16 (a[16], a[15], shift[1], l1[16]);

// Bit 2
MUX_2_1 lm2_1 (l1[1], 1'b0, shift[2], l2[1]);
MUX_2_1 lm2_2 (l1[2], 1'b0, shift[2], l2[2]);
MUX_2_1 lm2_3 (l1[3], l1[1], shift[2], l2[3]);
MUX_2_1 lm2_4 (l1[4], l1[2], shift[2], l2[4]);
MUX_2_1 lm2_5 (l1[5], l1[3], shift[2], l2[5]);
MUX_2_1 lm2_6 (l1[6], l1[4], shift[2], l2[6]);
MUX_2_1 lm2_7 (l1[7], l1[5], shift[2], l2[7]);
MUX_2_1 lm2_8 (l1[8], l1[6], shift[2], l2[8]);
MUX_2_1 lm2_9 (l1[9], l1[7], shift[2], l2[9]);
MUX_2_1 lm2_10 (l1[10], l1[8], shift[2], l2[10]);
MUX_2_1 lm2_11 (l1[11], l1[9], shift[2], l2[11]);
MUX_2_1 lm2_12 (l1[12], l1[10], shift[2], l2[12]);
MUX_2_1 lm2_13 (l1[13], l1[11], shift[2], l2[13]);
MUX_2_1 lm2_14 (l1[14], l1[12], shift[2], l2[14]);
MUX_2_1 lm2_15 (l1[15], l1[13], shift[2], l2[15]);
MUX_2_1 lm2_16 (l1[16], l1[14], shift[2], l2[16]);

// Bit 3
MUX_2_1 lm3_1 (l2[1], 1'b0, shift[3], l3[1]);
MUX_2_1 lm3_2 (l2[2], 1'b0, shift[3], l3[2]);
MUX_2_1 lm3_3 (l2[3], 1'b0, shift[3], l3[3]);
MUX_2_1 lm3_4 (l2[4], 1'b0, shift[3], l3[4]);
MUX_2_1 lm3_5 (l2[5], l2[1], shift[3], l3[5]);
MUX_2_1 lm3_6 (l2[6], l2[2], shift[3], l3[6]);
MUX_2_1 lm3_7 (l2[7], l2[3], shift[3], l3[7]);
MUX_2_1 lm3_8 (l2[8], l2[4], shift[3], l3[8]);
MUX_2_1 lm3_9 (l2[9], l2[5], shift[3], l3[9]);
MUX_2_1 lm3_10 (l2[10], l2[6], shift[3], l3[10]);
MUX_2_1 lm3_11 (l2[11], l2[7], shift[3], l3[11]);
MUX_2_1 lm3_12 (l2[12], l2[8], shift[3], l3[12]);
MUX_2_1 lm3_13 (l2[13], l2[9], shift[3], l3[13]);
MUX_2_1 lm3_14 (l2[14], l2[10], shift[3], l3[14]);
MUX_2_1 lm3_15 (l2[15], l2[11], shift[3], l3[15]);
MUX_2_1 lm3_16 (l2[16], l2[12], shift[3], l3[16]);

// Bit 4
MUX_2_1 lm4_1 (l3[1], 1'b0, shift[4], out[1]);
MUX_2_1 lm4_2 (l3[2], 1'b0, shift[4], out[2]);
MUX_2_1 lm4_3 (l3[3], 1'b0, shift[4], out[3]);
MUX_2_1 lm4_4 (l3[4], 1'b0, shift[4], out[4]);
MUX_2_1 lm4_5 (l3[5], 1'b0, shift[4], out[5]);
MUX_2_1 lm4_6 (l3[6], 1'b0, shift[4], out[6]);
MUX_2_1 lm4_7 (l3[7], 1'b0, shift[4], out[7]);
MUX_2_1 lm4_8 (l3[8], 1'b0, shift[4], out[8]);
MUX_2_1 lm4_9 (l3[9], l3[1], shift[4], out[9]);
MUX_2_1 lm4_10 (l3[10], l3[2], shift[4], out[10]);
MUX_2_1 lm4_11 (l3[11], l3[3], shift[4], out[11]);
MUX_2_1 lm4_12 (l3[12], l3[4], shift[4], out[12]);
MUX_2_1 lm4_13 (l3[13], l3[5], shift[4], out[13]);
MUX_2_1 lm4_14 (l3[14], l3[6], shift[4], out[14]);
MUX_2_1 lm4_15 (l3[15], l3[7], shift[4], out[15]);
MUX_2_1 lm4_16 (l3[16], l3[8], shift[4], out[16]);

endmodule

module RightBarrelShifter(a, shift, out);

input [16:1]  a;
input [4:1] shift;

output [16:1] out;

wire [16:1] l1, l2, l3;

// Bit 1
MUX_2_1 rm1_1 (a[1], a[2], shift[1], l1[1]);
MUX_2_1 rm1_2 (a[2], a[3], shift[1], l1[2]);
MUX_2_1 rm1_3 (a[3], a[4], shift[1], l1[3]);
MUX_2_1 rm1_4 (a[4], a[5], shift[1], l1[4]);
MUX_2_1 rm1_5 (a[5], a[6], shift[1], l1[5]);
MUX_2_1 rm1_6 (a[6], a[7], shift[1], l1[6]);
MUX_2_1 rm1_7 (a[7], a[8], shift[1], l1[7]);
MUX_2_1 rm1_8 (a[8], a[9], shift[1], l1[8]);
MUX_2_1 rm1_9 (a[9], a[10], shift[1], l1[9]);
MUX_2_1 rm1_10 (a[10], a[11], shift[1], l1[10]);
MUX_2_1 rm1_11 (a[11], a[12], shift[1], l1[11]);
MUX_2_1 rm1_12 (a[12], a[13], shift[1], l1[12]);
MUX_2_1 rm1_13 (a[13], a[14], shift[1], l1[13]);
MUX_2_1 rm1_14 (a[14], a[15], shift[1], l1[14]);
MUX_2_1 rm1_15 (a[15], a[16], shift[1], l1[15]);
MUX_2_1 rm1_16 (a[16], 1'b0, shift[1], l1[16]);

// Bit 2
MUX_2_1 rm2_1 (l1[1], l1[3], shift[2], l2[1]);
MUX_2_1 rm2_2 (l1[2], l1[4], shift[2], l2[2]);
MUX_2_1 rm2_3 (l1[3], l1[5], shift[2], l2[3]);
MUX_2_1 rm2_4 (l1[4], l1[6], shift[2], l2[4]);
MUX_2_1 rm2_5 (l1[5], l1[7], shift[2], l2[5]);
MUX_2_1 rm2_6 (l1[6], l1[8], shift[2], l2[6]);
MUX_2_1 rm2_7 (l1[7], l1[9], shift[2], l2[7]);
MUX_2_1 rm2_8 (l1[8], l1[10], shift[2], l2[8]);
MUX_2_1 rm2_9 (l1[9], l1[11], shift[2], l2[9]);
MUX_2_1 rm2_10 (l1[10], l1[12], shift[2], l2[10]);
MUX_2_1 rm2_11 (l1[11], l1[13], shift[2], l2[11]);
MUX_2_1 rm2_12 (l1[12], l1[14], shift[2], l2[12]);
MUX_2_1 rm2_13 (l1[13], l1[15], shift[2], l2[13]);
MUX_2_1 rm2_14 (l1[14], l1[16], shift[2], l2[14]);
MUX_2_1 rm2_15 (l1[15], 1'b0, shift[2], l2[15]);
MUX_2_1 rm2_16 (l1[16], 1'b0, shift[2], l2[16]);

// Bit 3
MUX_2_1 rm3_1 (l2[1], l2[5], shift[3], l3[1]);
MUX_2_1 rm3_2 (l2[2], l2[6], shift[3], l3[2]);
MUX_2_1 rm3_3 (l2[3], l2[7], shift[3], l3[3]);
MUX_2_1 rm3_4 (l2[4], l2[8], shift[3], l3[4]);
MUX_2_1 rm3_5 (l2[5], l2[9], shift[3], l3[5]);
MUX_2_1 rm3_6 (l2[6], l2[10], shift[3], l3[6]);
MUX_2_1 rm3_7 (l2[7], l2[11], shift[3], l3[7]);
MUX_2_1 rm3_8 (l2[8], l2[12], shift[3], l3[8]);
MUX_2_1 rm3_9 (l2[9], l2[13], shift[3], l3[9]);
MUX_2_1 rm3_10 (l2[10], l2[14], shift[3], l3[10]);
MUX_2_1 rm3_11 (l2[11], l2[15], shift[3], l3[11]);
MUX_2_1 rm3_12 (l2[12], l2[16], shift[3], l3[12]);
MUX_2_1 rm3_13 (l2[13], 1'b0, shift[3], l3[13]);
MUX_2_1 rm3_14 (l2[14], 1'b0, shift[3], l3[14]);
MUX_2_1 rm3_15 (l2[15], 1'b0, shift[3], l3[15]);
MUX_2_1 rm3_16 (l2[16], 1'b0, shift[3], l3[16]);

// Bit 4
MUX_2_1 rm4_1 (l3[1], l3[9], shift[4], out[1]);
MUX_2_1 rm4_2 (l3[2], l3[10], shift[4], out[2]);
MUX_2_1 rm4_3 (l3[3], l3[11], shift[4], out[3]);
MUX_2_1 rm4_4 (l3[4], l3[12], shift[4], out[4]);
MUX_2_1 rm4_5 (l3[5], l3[13], shift[4], out[5]);
MUX_2_1 rm4_6 (l3[6], l3[14], shift[4], out[6]);
MUX_2_1 rm4_7 (l3[7], l3[15], shift[4], out[7]);
MUX_2_1 rm4_8 (l3[8], l3[16], shift[4], out[8]);
MUX_2_1 rm4_9 (l3[9], 1'b0, shift[4], out[9]);
MUX_2_1 rm4_10 (l3[10], 1'b0, shift[4], out[10]);
MUX_2_1 rm4_11 (l3[11], 1'b0, shift[4], out[11]);
MUX_2_1 rm4_12 (l3[12], 1'b0, shift[4], out[12]);
MUX_2_1 rm4_13 (l3[13], 1'b0, shift[4], out[13]);
MUX_2_1 rm4_14 (l3[14], 1'b0, shift[4], out[14]);
MUX_2_1 rm4_15 (l3[15], 1'b0, shift[4], out[15]);
MUX_2_1 rm4_16 (l3[16], 1'b0, shift[4], out[16]);

endmodule

module MUX_2_1(A, B, S, out);
input A, B, S;
output out;
assign out = ((!S) & A) | (S & B);
endmodule

// Universal Barrel Shifter
module UniversalBarrelShifter (A, Shift, ShiftChoice, out);

input [16:1] A;
input [4:1] Shift;
input ShiftChoice;  // Left Shift if 1, else if 0 Right Shift

output [16:1] out;

wire [16:1] ls, rs;

LeftBarrelShifter leftshift (A, Shift, ls);
RightBarrelShifter rightshift (A, Shift, rs);

assign out = (ShiftChoice) ? ls : rs;

endmodule
