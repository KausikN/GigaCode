/*
Summary
Library of Floating Point Hardware Modules made by ME
*/

// Shifter
module BarrelShifterLeft (a, shift, b);

input [11:1] a;
input [5:1] shift;
output [11:1] b;

wire [11:1] o1, o2, o3, o4;
wire [11:1] w1, w21, w22, w31, w32, w33, w34, w41, w42, w43, w44, w45, w46, w47, w48;

// Bit 1
ShiftLeftOnce_11Bit s_1 (a, w1);
assign o1 = (shift[1]) ? w1 : a;

// Bit 2
ShiftLeftOnce_11Bit s_21 (o1, w21);
ShiftLeftOnce_11Bit s_22 (w21, w22);
assign o2 = (shift[2]) ? w22 : o1;

// Bit 3
ShiftLeftOnce_11Bit s_31 (o2, w31);
ShiftLeftOnce_11Bit s_32 (w31, w32);
ShiftLeftOnce_11Bit s_33 (w32, w33);
ShiftLeftOnce_11Bit s_34 (w33, w34);
assign o3 = (shift[3]) ? w34 : o2;

// Bit 4
ShiftLeftOnce_11Bit s_41 (o3, w41);
ShiftLeftOnce_11Bit s_42 (w41, w42);
ShiftLeftOnce_11Bit s_43 (w42, w43);
ShiftLeftOnce_11Bit s_44 (w43, w44);
ShiftLeftOnce_11Bit s_45 (w44, w45);
ShiftLeftOnce_11Bit s_46 (w45, w46);
ShiftLeftOnce_11Bit s_47 (w46, w47);
ShiftLeftOnce_11Bit s_48 (w47, w48);
assign o4 = (shift[4]) ? w48 : o3;

// If Bit 5 is 1, as a is only 11 bits, output is 0 - all right shifted
assign b = (shift[5]) ? 11'b00000000000 : o4;

endmodule

module BarrelShifterRight (a, shift, b);

input [11:1] a;
input [5:1] shift;
output [11:1] b;

wire [11:1] o1, o2, o3, o4;
wire [11:1] w1, w21, w22, w31, w32, w33, w34, w41, w42, w43, w44, w45, w46, w47, w48;

// Bit 1
ShiftRightOnce_11Bit s_1 (a, w1);
assign o1 = (shift[1]) ? w1 : a;

// Bit 2
ShiftRightOnce_11Bit s_21 (o1, w21);
ShiftRightOnce_11Bit s_22 (w21, w22);
assign o2 = (shift[2]) ? w22 : o1;

// Bit 3
ShiftRightOnce_11Bit s_31 (o2, w31);
ShiftRightOnce_11Bit s_32 (w31, w32);
ShiftRightOnce_11Bit s_33 (w32, w33);
ShiftRightOnce_11Bit s_34 (w33, w34);
assign o3 = (shift[3]) ? w34 : o2;

// Bit 4
ShiftRightOnce_11Bit s_41 (o3, w41);
ShiftRightOnce_11Bit s_42 (w41, w42);
ShiftRightOnce_11Bit s_43 (w42, w43);
ShiftRightOnce_11Bit s_44 (w43, w44);
ShiftRightOnce_11Bit s_45 (w44, w45);
ShiftRightOnce_11Bit s_46 (w45, w46);
ShiftRightOnce_11Bit s_47 (w46, w47);
ShiftRightOnce_11Bit s_48 (w47, w48);
assign o4 = (shift[4]) ? w48 : o3;

// If Bit 5 is 1, as a is only 11 bits, output is 0 - all right shifted
assign b = (shift[5]) ? 11'b00000000000 : o4;

endmodule

// Utils
module Bit5Adder (a, b, sum, carry);

input [5:1] a;
input [5:1] b;

output [5:1] sum;
output carry;

wire [16:1] A, B, SUM;
wire CARRY;

assign A[5:1] = a;
assign A[16:6] = 11'b00000000000;
assign B[5:1] = b;
assign B[16:6] = 11'b00000000000;

RDAdder addr (A, B, 1'b0, SUM, CARRY);

assign sum = SUM[5:1];
assign carry = SUM[6];

endmodule

module Bit5Adder (a, b, sum, carry);

input [5:1] a;
input [5:1] b;

output [5:1] sum;
output carry;

wire [4:1] w;

FullAdder fa_1 (a[1], b[1], 1'b0, sum[1], w[1]);
FullAdder fa_2 (a[2], b[2], w[1], sum[2], w[2]);
FullAdder fa_3 (a[3], b[3], w[2], sum[3], w[3]);
FullAdder fa_4 (a[4], b[4], w[3], sum[4], w[4]);
FullAdder fa_5 (a[5], b[5], w[4], sum[5], carry);

endmodule

module Bit5MUX (a, b, select, out);

input [5:1] a;
input [5:1] b;
input select;

output [5:1] out;

assign out[1] = ((!select) & a[1]) | ((select) & b[1]);
assign out[2] = ((!select) & a[2]) | ((select) & b[2]);
assign out[3] = ((!select) & a[3]) | ((select) & b[3]);
assign out[4] = ((!select) & a[4]) | ((select) & b[4]);
assign out[5] = ((!select) & a[5]) | ((select) & b[5]);

endmodule


module Bit10MUX (a, b, select, out);

input [10:1] a;
input [10:1] b;
input select;

output [10:1] out;

assign out[1] = ((!select) & a[1]) | ((select) & b[1]);
assign out[2] = ((!select) & a[2]) | ((select) & b[2]);
assign out[3] = ((!select) & a[3]) | ((select) & b[3]);
assign out[4] = ((!select) & a[4]) | ((select) & b[4]);
assign out[5] = ((!select) & a[5]) | ((select) & b[5]);
assign out[6] = ((!select) & a[6]) | ((select) & b[6]);
assign out[7] = ((!select) & a[7]) | ((select) & b[7]);
assign out[8] = ((!select) & a[8]) | ((select) & b[8]);
assign out[9] = ((!select) & a[9]) | ((select) & b[9]);
assign out[10] = ((!select) & a[10]) | ((select) & b[10]);

endmodule

module Bit11Adder (a, b, sum, carry);

input [11:1] a;
input [11:1] b;

output [11:1] sum;
output carry;

wire [16:1] A, B, SUM;
wire CARRY;

assign A[11:1] = a;
assign A[16:12] = 5'b00000;
assign B[11:1] = b;
assign B[16:12] = 5'b00000;

RDAdder addr (A, B, 1'b0, SUM, CARRY);

assign sum = SUM[11:1];
assign carry = SUM[12];

endmodule

module Bit11Adder (a, b, sum, carry);

input [11:1] a;
input [11:1] b;

output [11:1] sum;
output carry;

wire [10:1] w;

FullAdder fa_1 (a[1], b[1], 1'b0, sum[1], w[1]);
FullAdder fa_2 (a[2], b[2], w[1], sum[2], w[2]);
FullAdder fa_3 (a[3], b[3], w[2], sum[3], w[3]);
FullAdder fa_4 (a[4], b[4], w[3], sum[4], w[4]);
FullAdder fa_5 (a[5], b[5], w[4], sum[5], w[5]);
FullAdder fa_6 (a[6], b[6], w[5], sum[6], w[6]);
FullAdder fa_7 (a[7], b[7], w[6], sum[7], w[7]);
FullAdder fa_8 (a[8], b[8], w[7], sum[8], w[8]);
FullAdder fa_9 (a[9], b[9], w[8], sum[9], w[9]);
FullAdder fa_10 (a[10], b[10], w[9], sum[10], w[10]);
FullAdder fa_11 (a[11], b[11], w[10], sum[11], carry);

endmodule

module BitwiseAND_5Bit (a, select, b);

input [5:1] a;
input select;
output [5:1] b;

assign b[1] = select & a[1];
assign b[2] = select & a[2];
assign b[3] = select & a[3];
assign b[4] = select & a[4];
assign b[5] = select & a[5];

endmodule

module carry_look_ahead_16bit(a,b, cin, sum,cout);
input [15:0] a,b;
input cin;
output [15:0] sum;
output cout;
wire c1,c2,c3;
 
carry_look_ahead_4bit cla1 (.a(a[3:0]), .b(b[3:0]), .cin(cin), .sum(sum[3:0]), .cout(c1));
carry_look_ahead_4bit cla2 (.a(a[7:4]), .b(b[7:4]), .cin(c1), .sum(sum[7:4]), .cout(c2));
carry_look_ahead_4bit cla3(.a(a[11:8]), .b(b[11:8]), .cin(c2), .sum(sum[11:8]), .cout(c3));
carry_look_ahead_4bit cla4(.a(a[15:12]), .b(b[15:12]), .cin(c3), .sum(sum[15:12]), .cout(cout));
 
endmodule

module carry_look_ahead_8bit(a,b, cin, sum,cout);
input [7:0] a,b;
input cin;
output [7:0] sum;
output cout;
wire c1;
 
carry_look_ahead_4bit cla1 (.a(a[3:0]), .b(b[3:0]), .cin(cin), .sum(sum[3:0]), .cout(c1));
carry_look_ahead_4bit cla2 (.a(a[7:4]), .b(b[7:4]), .cin(c1), .sum(sum[7:4]), .cout(cout));
 
endmodule

module carry_look_ahead_4bit(a,b, cin, sum,cout);
input [3:0] a,b;
input cin;
output [3:0] sum;
output cout;
 
wire [3:0] p,g,c;
 
assign p=a^b;//propagate
assign g=a&b; //generate
 
assign c[0]=cin;
assign c[1]= g[0]|(p[0]&c[0]);
assign c[2]= g[1] | (p[1]&g[0]) | p[1]&p[0]&c[0];
assign c[3]= g[2] | (p[2]&g[1]) | p[2]&p[1]&g[0] | p[2]&p[1]&p[0]&c[0];
assign cout= g[3] | (p[3]&g[2]) | p[3]&p[2]&g[1] | p[3]&p[2]&p[1]&p[0]&c[0];
assign sum=p^c;
 
endmodule

module Complement2s_5Bit (a, b);
input [5:1] a;
output [5:1] b;
	
wire [5:1] comp1s;
wire c;
assign comp1s[1] = !a[1];
assign comp1s[2] = !a[2];
assign comp1s[3] = !a[3];
assign comp1s[4] = !a[4];
assign comp1s[5] = !a[5];

Bit5Adder addr (comp1s, 5'b00001, b, c);

endmodule

module Complement2s_11Bit (a, b);
input [11:1] a;
output [11:1] b;
	
wire [11:1] comp1s;
assign comp1s[1] = !a[1];
assign comp1s[2] = !a[2];
assign comp1s[3] = !a[3];
assign comp1s[4] = !a[4];
assign comp1s[5] = !a[5];
assign comp1s[6] = !a[6];
assign comp1s[7] = !a[7];
assign comp1s[8] = !a[8];
assign comp1s[9] = !a[9];
assign comp1s[10] = !a[10];
assign comp1s[11] = !a[11];

wire c;

Bit11Adder addr (comp1s, 11'b00000000001, b, c);

endmodule

module Encoder11Bit_to_5Bit (a, b);

input [11:1] a;
output [5:1] b;

reg [5:1] n_0 = 5'b00000;
reg [5:1] n_1 = 5'b00001;
reg [5:1] n_2 = 5'b00010;
reg [5:1] n_3 = 5'b00011;
reg [5:1] n_4 = 5'b00100;
reg [5:1] n_5 = 5'b00101;
reg [5:1] n_6 = 5'b00110;
reg [5:1] n_7 = 5'b00111;
reg [5:1] n_8 = 5'b01000;
reg [5:1] n_9 = 5'b01001;
reg [5:1] n_10 = 5'b01010;
reg [5:1] n_11 = 5'b01011;

wire [5:1] a_1, a_2, a_3, a_4, a_5, a_6, a_7, a_8, a_9, a_10, a_11;
BitwiseAND_5Bit b_1 (n_1, a[1], a_1);
BitwiseAND_5Bit b_2 (n_2, a[2], a_2);
BitwiseAND_5Bit b_3 (n_3, a[3], a_3);
BitwiseAND_5Bit b_4 (n_4, a[4], a_4);
BitwiseAND_5Bit b_5 (n_5, a[5], a_5);
BitwiseAND_5Bit b_6 (n_6, a[6], a_6);
BitwiseAND_5Bit b_7 (n_7, a[7], a_7);
BitwiseAND_5Bit b_8 (n_8, a[8], a_8);
BitwiseAND_5Bit b_9 (n_9, a[9], a_9);
BitwiseAND_5Bit b_10 (n_10, a[10], a_10);
BitwiseAND_5Bit b_11 (n_11, a[11], a_11);

assign b[1] = a_1[1] | a_2[1] | a_3[1] | a_4[1] | a_5[1] | a_6[1] | a_7[1] | a_8[1] | a_9[1] | a_10[1] | a_11[1];
assign b[2] = a_1[2] | a_2[2] | a_3[2] | a_4[2] | a_5[2] | a_6[2] | a_7[2] | a_8[2] | a_9[2] | a_10[2] | a_11[2];
assign b[3] = a_1[3] | a_2[3] | a_3[3] | a_4[3] | a_5[3] | a_6[3] | a_7[3] | a_8[3] | a_9[3] | a_10[3] | a_11[3];
assign b[4] = a_1[4] | a_2[4] | a_3[4] | a_4[4] | a_5[4] | a_6[4] | a_7[4] | a_8[4] | a_9[4] | a_10[4] | a_11[4];
assign b[5] = a_1[5] | a_2[5] | a_3[5] | a_4[5] | a_5[5] | a_6[5] | a_7[5] | a_8[5] | a_9[5] | a_10[5] | a_11[5];

endmodule

`include "Complement2s_5Bit.v"
`include "Bit5MUX.v"

module ExpSubtractor (in_Exponent_1, in_Exponent_2, Exponent_Diff, smallerOperand);

input [5:1] in_Exponent_1;
input [5:1] in_Exponent_2;

output [5:1] Exponent_Diff;
output smallerOperand;

// Check if operand 1/2 is 0
wire in_Exponent_1_Zero;
assign in_Exponent_1_Zero = !(|in_Exponent_1);
wire in_Exponent_2_Zero;
assign in_Exponent_2_Zero = !(|in_Exponent_2);

// Subtract the 2 exponents
wire [5:1] tscomp;
wire [5:1] diff;
wire carry;
Complement2s_5Bit comp2s (in_Exponent_2, tscomp);
Bit5Adder addr (in_Exponent_1, tscomp, diff, carry);
// If carry is 1 - diff is +ve, else it is -ve
// i.e. if carry is 1, smallerOperand is in_exponent_2 - 0
// Else if caary is 0, smallerOperand is in_exponent_1 - 1
wire smallerOperand_ZeroChecked;
assign smallerOperand_ZeroChecked = ((!in_Exponent_1_Zero) & (!in_Exponent_2_Zero) & !carry) | ((!in_Exponent_1_Zero) &  in_Exponent_2_Zero & 0) | 
                        (in_Exponent_1_Zero & (!in_Exponent_2_Zero) & 1) | (in_Exponent_1_Zero & in_Exponent_2_Zero & 0);
// If diff is +ve return, else if diff is -ve, take ulta 2scomplement and return
wire [5:1] reverse2scomp;
// subtract 1 and take 1s complement
wire [5:1] onescomp;
wire c;
Bit5Adder addr_to1s (diff, 5'b11111, onescomp, c);
assign reverse2scomp[1] = !onescomp[1];
assign reverse2scomp[2] = !onescomp[2];
assign reverse2scomp[3] = !onescomp[3];
assign reverse2scomp[4] = !onescomp[4];
assign reverse2scomp[5] = !onescomp[5];

// Return correct diff value based on sign of it
Bit5MUX mux (reverse2scomp, diff, !smallerOperand_ZeroChecked, Exponent_Diff);

// Assign smallerOperand
assign smallerOperand = smallerOperand_ZeroChecked;

endmodule

module HalfAdder (a,b,sum, ca);
input a, b;
output sum, ca;
	assign sum = a ^ b;
	assign ca  = a&b;
endmodule

module FullAdder (a, b, cin, sum, cout);
input a, b, cin;
output sum, cout;
	assign sum = a ^ b ^ cin;
	assign cout  = ((a^b)&cin) | (a&b);	// carry = (a xor b)cin + ab
endmodule

module NormaliseANDBlock (a, b, c, out, check);

input a, b, c;
output out, check;

assign out = !a & !b & c;
assign check = b | out;

endmodule

module NormaliseShift (a, normshift);

input [11:1] a;
output [5:1] normshift;

// Convert binary no to position with first '1'
// Eg. convert 01101 to 00001 as 1 shift
wire [11:1] first1form;
wire [10:1] first1came;
NormaliseANDBlock a_1 (a[11], 1'b0, a[10], first1form[1], first1came[1]);
NormaliseANDBlock a_2 (a[11], first1came[1], a[9], first1form[2], first1came[2]);
NormaliseANDBlock a_3 (a[11], first1came[2], a[8], first1form[3], first1came[3]);
NormaliseANDBlock a_4 (a[11], first1came[3], a[7], first1form[4], first1came[4]);
NormaliseANDBlock a_5 (a[11], first1came[4], a[6], first1form[5], first1came[5]);
NormaliseANDBlock a_6 (a[11], first1came[5], a[5], first1form[6], first1came[6]);
NormaliseANDBlock a_7 (a[11], first1came[6], a[4], first1form[7], first1came[7]);
NormaliseANDBlock a_8 (a[11], first1came[7], a[3], first1form[8], first1came[8]);
NormaliseANDBlock a_9 (a[11], first1came[8], a[2], first1form[9], first1came[9]);
NormaliseANDBlock a_10 (a[11], first1came[9], a[1], first1form[10], first1came[10]);
assign first1form[11] = 1'b0;

// Now encode the no - i.e. 00000000100 - 3rd pos becomes 00011 - 3
Encoder11Bit_to_5Bit enc (first1form, normshift);

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

module ShiftLeftOnce_11Bit (a, b);

input [11:1] a;
output [11:1] b;

assign b[1] = 1'b0;
assign b[2] = a[1];
assign b[3] = a[2];
assign b[4] = a[3];
assign b[5] = a[4];
assign b[6] = a[5];
assign b[7] = a[6];
assign b[8] = a[7];
assign b[9] = a[8];
assign b[10] = a[9];
assign b[11] = a[10];

endmodule

module ShiftRightOnce_11Bit (a, b);

input [11:1] a;
output [11:1] b;

assign b[11] = 1'b0;
assign b[10] = a[11];
assign b[9] = a[10];
assign b[8] = a[9];
assign b[7] = a[8];
assign b[6] = a[7];
assign b[5] = a[6];
assign b[4] = a[5];
assign b[3] = a[4];
assign b[2] = a[3];
assign b[1] = a[2];

endmodule

module Bit4Adder (a, b, cin, sum, cout);
input[4:1] a, b;
input cin;
output[4:1] sum;
output cout;

	wire w1, w2, w3;

	FullAdder FA_0(a[1], b[1], cin, sum[1], w1);
	FullAdder FA_1(a[2], b[2], w1, sum[2], w2);
	FullAdder FA_2(a[3], b[3], w2, sum[3], w3);
	FullAdder FA_3(a[4], b[4], w3, sum[4], cout);

endmodule

module Bit8Adder (a, b, cin, sum, cout);
input[8:1] a, b;
input cin;
output[8:1] sum;
output cout;

	wire w1;

	Bit4Adder B4A1 (a[4:1], b[4:1], cin, sum[4:1], w1);
	Bit4Adder B4A2 (a[8:5], b[8:5], w1, sum[8:5], cout);

endmodule

module Bit16Adder (a, b, cin, sum, cout);
input[16:1] a, b;
input cin;
output[16:1] sum;
output cout;

	wire w1, w2, w3;

	Bit4Adder B4A_0(a[4:1], b[4:1], cin, sum[4:1], w1);
	Bit4Adder B4A_1(a[8:5], b[8:5], w1, sum[8:5], w2);
	Bit4Adder B4A_2(a[12:9], b[12:9], w2, sum[12:9], w3);
	Bit4Adder B4A_3(a[16:13], b[16:13], w3, sum[16:13], cout);

endmodule

module Bit32Adder (a, b, cin, sum, cout);
input[32:1] a, b;
input cin;
output[32:1] sum;
output cout;

	wire w1;

	Bit16Adder B16A_0(a[16:1], b[16:1], cin, sum[16:1], w1);
	Bit16Adder B16A_1(a[32:17], b[32:17], w1, sum[32:17], cout);

endmodule

module Bit36Adder (a, b, cin, sum, cout);
input[36:1] a, b;
input cin;
output[36:1] sum;
output cout;

	wire w1, w2;

	Bit16Adder B16A_0(a[16:1], b[16:1], cin, sum[16:1], w1);
	Bit16Adder B16A_1(a[32:17], b[32:17], w1, sum[32:17], w2);
	Bit4Adder  B4A_2 (a[36:33], b[36:33], w2, sum[36:33], cout);

endmodule

input [6:1] a;
input [6:1] b;

output [6:1] sum;
output carry;

wire [5:1] w;

FullAdder fa_1 (a[1], b[1], 1'b0, sum[1], w[1]);
FullAdder fa_2 (a[2], b[2], w[1], sum[2], w[2]);
FullAdder fa_3 (a[3], b[3], w[2], sum[3], w[3]);
FullAdder fa_4 (a[4], b[4], w[3], sum[4], w[4]);
FullAdder fa_5 (a[5], b[5], w[4], sum[5], w[5]);
FullAdder fa_6 (a[6], b[6], w[5], sum[6], carry);

endmodule

module BitWiseAND(A, B, p);
    
    input [8:1] A;
    input B;

    output [8:1] p;

    assign p[1] = A[1] & B;
    assign p[2] = A[2] & B;
    assign p[3] = A[3] & B;
    assign p[4] = A[4] & B;
    assign p[5] = A[5] & B;
    assign p[6] = A[6] & B;
    assign p[7] = A[7] & B;
    assign p[8] = A[8] & B;

endmodule

module Multiplier_16Bit(A, B, out);
    
    input [16:1] A, B;
    output [36:1] out;

    reg zero = 1'b0;
    // initial 
    //     zero = 1'b0;

    wire[16:1] wll, wlh, whl, whh;

    WallaceMultiplier wm_ll(A[8:1], B[8:1], wll);
    WallaceMultiplier wm_lh(A[8:1], B[16:9], wlh);
    WallaceMultiplier wm_hl(A[16:9], B[8:1], whl);
    WallaceMultiplier wm_hh(A[16:9], B[16:9], whh);

    assign out[8:1] = wll[8:1];
    assign out[36:33] = 4'b0000;

    wire w1, w2, w3, w4, w5, w6;
    wire [8:1] tempout1, tempout2, tempout3;
    Bit8Adder B8A1 (wll[16:9], wlh[8:1], zero, tempout1, w1);
    Bit8Adder B8A2 (tempout1, whl[8:1], zero, out[16:9], w2);

    Bit8Adder B8A3 (wlh[16:9], whl[16:9], w1, tempout2, w3);
    Bit8Adder B8A4 (tempout2, whh[8:1], w2, out[24:17], w4);

    Bit8Adder B8A5 (whh[16:9], 8'b00000000, w3, tempout3, w5);
    Bit8Adder B8A6 (tempout3, 8'b00000000, w4, out[32:25], w6);

/*
always@(*)
begin
    $display(": Intermediate: A: %b (%d), B: %b (%d), out: %b (%d)", A, A, B, B, out, out);
    $display(": Intermediate Binary: (w1:%b | w2:%b) wll = %b (%d), wlh = %b (%d), whl = %b (%d), whh = %b (%d)", w1, w2, wll, wll, wlh, wlh, whl, whl, whh, whh);
end
*/
endmodule

module WallaceMultiplier(A, B, prod);
    
    input [8:1] A,B;
    output [16:1] prod;

    wire s11,s12,s13,s14,s15,s16,s17,s18,s19,s110,s111,s112,s113,s114,s115,s116,s117,s118,s119,s120,s121;
    wire s21,s22,s23,s24,s25,s26,s27,s28,s29,s210,s211,s212,s213,s214,s215,s216;
    wire s31,s32,s33,s34,s35,s36,s37,s38,s39,s310,s311,s312;
    wire s41,s42,s43,s44,s45,s46,s47,s48,s49,s410,s411,s412;
    wire s51,s52,s53,s54,s55,s56,s57,s58,s59,s510,s511,s512;

    wire c11,c12,c13,c14,c15,c16,c17,c18,c19,c110,c111,c112,c113,c114,c115,c116,c117,c118,c119,c120,c121;
    wire c21,c22,c23,c24,c25,c26,c27,c28,c29,c210,c211,c212,c213,c214,c215,c216;
    wire c31,c32,c33,c34,c35,c36,c37,c38,c39,c310,c311,c312;
    wire c41,c42,c43,c44,c45,c46,c47,c48,c49,c410,c411,c412;
    wire c51,c52,c53,c54,c55,c56,c57,c58,c59,c510,c511,c512;

    wire [8:1] p1,p2,p3,p4,p5,p6,p7,p8;

    BitWiseAND ba1(A, B[1], p1);
    BitWiseAND ba2(A, B[2], p2);
    BitWiseAND ba3(A, B[3], p3);
    BitWiseAND ba4(A, B[4], p4);
    BitWiseAND ba5(A, B[5], p5);
    BitWiseAND ba6(A, B[6], p6);
    BitWiseAND ba7(A, B[7], p7);
    BitWiseAND ba8(A, B[8], p8);
  
    assign prod[1] = p1[1];
    assign prod[2] = s11;
    assign prod[3] = s21;
    assign prod[4] = s31;
    assign prod[5] = s41;
    assign prod[6] = s51;
    assign prod[7] = s52;
    assign prod[8] = s53;
    assign prod[9] = s54;
    assign prod[10] = s55;
    assign prod[11] = s56;
    assign prod[12] = s57;
    assign prod[13] = s58;
    assign prod[14] = s59;
    assign prod[15] = s510;
    assign prod[16] = s511;
    //assign prod[17] = s512;
    //assign prod[18] = c512;

    // ----- Step 1 --------------------------------------

    HalfAdder ha11 (p1[2],p2[1],s11,c11);

    FullAdder fa12 (p1[3],p2[2],p3[1],s12,c12);

    FullAdder fa13 (p1[4],p2[3],p3[2],s13,c13);

    FullAdder fa14 (p1[5],p2[4],p3[3],s14,c14);
    HalfAdder ha14 (p4[2],p5[1],s15,c15);

    FullAdder fa151 (p1[6],p2[5],p3[4],s16,c16);
    FullAdder fa152 (p4[3],p5[2],p6[1],s17,c17);

    FullAdder fa161 (p1[7],p2[6],p3[5],s18,c18);
    FullAdder fa162 (p4[4],p5[3],p6[2],s19,c19);

    FullAdder fa171 (p1[8],p2[7],p3[6],s110,c110);
    FullAdder fa172 (p4[5],p5[4],p6[3],s111,c111);
    HalfAdder ha17  (p7[2],p8[1],s112,c112);

    FullAdder fa181 (p2[8],p3[7],p4[6],s113,c113);
    FullAdder fa182 (p5[5],p6[4],p7[3],s114,c114);

    FullAdder fa191 (p3[8],p4[7],p5[6],s115,c115);
    FullAdder fa192 (p6[5],p7[4],p8[3],s116,c116);

    FullAdder fa110 (p4[8],p5[7],p6[6],s117,c117);
    HalfAdder ha110 (p7[5],p8[4],s118,c118);

    FullAdder fa111 (p5[8],p6[7],p7[6],s119,c119);

    FullAdder fa112 (p6[8],p7[7],p8[6],s120,c120);

    HalfAdder ha113 (p7[8],p8[7],s121,c121);

    // ----- Step 1 --------------------------------------

    // ----- Step 2 --------------------------------------

    HalfAdder ha21 (c11,s12,s21,c21);

    FullAdder fa22 (c12,s13,p4[1],s22,c22);

    FullAdder fa23 (c13,s14,s15,s23,c23);

    FullAdder fa24 (c14,c15,s16,s24,c24);

    FullAdder fa25 (c16,c17,s18,s25,c25);
    HalfAdder ha25 (s19,p7[1],s26,c26);

    FullAdder fa26 (c18,c19,s110,s27,c27);
    HalfAdder ha26 (s111,s112,s28,c28);

    FullAdder fa271 (c110,c111,c112,s29,c29);
    FullAdder fa272 (s113,s114,p8[2],s210,c210);

    FullAdder fa28 (c113,c114,s115,s211,c211);

    FullAdder fa29 (c115,c116,s117,s212,c212);

    FullAdder fa210 (c117,c118,s119,s213,c213);

    HalfAdder ha211 (c119,s120,s214,c214);

    HalfAdder ha212 (c120,s121,s215,c215);

    HalfAdder ha213 (c121,p8[8],s216,c216);

    // ----- Step 2 --------------------------------------

    // ----- Step 3 --------------------------------------

    HalfAdder ha31 (c21,s22,s31,c31);

    HalfAdder ha32 (c22,s23,s32,c32);

    FullAdder fa33 (c23,s24,s17,s33,c33);

    FullAdder fa34 (c24,s25,s26,s34,c34);

    FullAdder fa35 (c25,c26,s27,s35,c35);

    FullAdder fa36 (c27,c28,s29,s36,c36);

    FullAdder fa37 (c29,c210,s211,s37,c37);

    FullAdder fa38 (c211,s212,s118,s38,c38);

    FullAdder fa39 (c212,s213,p8[5],s39,c39);

    HalfAdder ha310 (c213,s214,s310,c310);

    HalfAdder ha311 (c214,s215,s311,c311);

    HalfAdder ha312 (c215,s216,s312,c312);

    // ----- Step 3 --------------------------------------

    // ----- Step 4 --------------------------------------

    HalfAdder ha41 (c31,s32,s41,c41);

    HalfAdder ha42 (c32,s33,s42,c42);

    HalfAdder ha43 (c33,s34,s43,c43);

    FullAdder fa44 (c34,s35,s28,s44,c44);

    FullAdder fa45 (c35,s36,s210,s45,c45);

    FullAdder fa46 (c36,s37,s116,s46,c46);

    HalfAdder ha47 (c37,s38,s47,c47);

    HalfAdder ha48 (c38,s39,s48,c48);

    HalfAdder ha49 (c39,s310,s49,c49);

    HalfAdder ha410 (c310,s311,s410,c410);

    HalfAdder ha411 (c311,s312,s411,c411);

    HalfAdder ha412 (c312,c216,s412,c412);

    // ----- Step 4 --------------------------------------

    // ----- Step 5 --------------------------------------

    HalfAdder ha51 (c41,s42,s51,c51);
    FullAdder fa52 (c51,c42,s43,s52,c52);
    FullAdder fa53 (c52,c43,s44,s53,c53);
    FullAdder fa54 (c53,c44,s45,s54,c54);
    FullAdder fa55 (c54,c45,s46,s55,c55);
    FullAdder fa56 (c55,c46,s47,s56,c56);
    FullAdder fa57 (c56,c47,s48,s57,c57);
    FullAdder fa58 (c57,c48,s49,s58,c58);
    FullAdder fa59 (c58,c49,s410,s59,c59);
    FullAdder fa510(c59,c410,s411,s510,c510);
    FullAdder fa511(c510,c411,s412,s511,c511);
    HalfAdder ha512 (c511,c412,s512,c512);

    // ----- Step 5 --------------------------------------
/*
always@(*) 
    $display(": Intermediate Binary: A = %b (%d), B = %b (%d), Product: %b (%d) -- --%b--", A, A, B, B, prod, prod, p1);
*/
endmodule


// Floating Addition
module FAdder_HalfPrecision(
    add, 
    in_Sign_1, in_Exponent_1, in_Mantissa_1, 
    in_Sign_2_BeforeSignAdjust, in_Exponent_2, in_Mantissa_2, 
    out_Sign, out_Exponent, out_Mantissa, 
    SC_Output_OverFlow, SC_Exponent_UnderFlow
);

// Special Conditions
wire SC_Operand_Infinity;   // For checking if any one of the input operands is Infinity
wire SC_Operand_Zero;   // For checking if any one of the input operands is 0
wire SC_Mantissa_Zero;  // For checking if Output no is 0.0
output SC_Output_OverFlow; // For checking if Output Exponent Overflows
output SC_Exponent_UnderFlow; // For checking if Output no is denormalised - i.e. exponent of output underflows after renormalisation

// Initial
input add;  // If add = 1, do addition, else do subtraction
input in_Sign_1;
input [5:1] in_Exponent_1;
input [10:1] in_Mantissa_1;
input in_Sign_2_BeforeSignAdjust;   // Sign before accounting for addition or subtraction
input [5:1] in_Exponent_2;
input [10:1] in_Mantissa_2;

output out_Sign;
output [5:1] out_Exponent;
output [10:1] out_Mantissa;

wire in_Sign_2;
assign in_Sign_2 = ((!add) & (!in_Sign_2_BeforeSignAdjust)) | (add & in_Sign_2_BeforeSignAdjust);

// Get the Smaller Operand and Normalize it to the larger operand using ExpSubtractor module
wire smallerOperand;
wire [5:1] Exponent_Diff;
wire [5:1] Max_Exponent;

ExpSubtractor expsub (in_Exponent_1, in_Exponent_2, Exponent_Diff, smallerOperand); // if smallerOperand = 1, in_Exponent_1 is smaller Operand

wire largerOperand;
assign largerOperand = !smallerOperand;
// Based on smallerOperand decide which operand is larger or smaller
wire largerOperand_Sign;
wire [5:1] largerOperand_Exponent;
wire [11:1] largerOperand_Mantissa;

wire smallerOperand_Sign_Normalised;
wire [5:1] smallerOperand_Exponent;
wire [11:1] smallerOperand_Mantissa;
wire [11:1] smallerOperand_Mantissa_Normalised;

assign largerOperand_Sign = ((!smallerOperand) & in_Sign_1) | ((smallerOperand) & in_Sign_2);

Bit5MUX LargerOperandExponentChooser (in_Exponent_1, in_Exponent_2, smallerOperand, largerOperand_Exponent);

Bit10MUX LargerOperandMantissaChooser (in_Mantissa_1, in_Mantissa_2, smallerOperand, largerOperand_Mantissa[10:1]);
assign largerOperand_Mantissa[11] = 1'b1;   // For Implicit 1

assign smallerOperand_Sign_Normalised = ((smallerOperand) & in_Sign_1) | ((!smallerOperand) & in_Sign_2);

Bit5MUX SmallerOperandExponentChooser (in_Exponent_1, in_Exponent_2, largerOperand, smallerOperand_Exponent);

Bit10MUX SmallerOperandMantissaChooser (in_Mantissa_1, in_Mantissa_2, largerOperand, smallerOperand_Mantissa[10:1]);
assign smallerOperand_Mantissa[11] = 1'b1;   // For Implicit 1

// Now Check if Smaller Operand is 0 - mantissa (10 bits) and exponent all zeros
assign SC_Operand_Zero = !(|smallerOperand_Exponent | |smallerOperand_Mantissa[10:1]);
// Now Check if Larger Operand is all 1s - mantissa (10 bits) all 0s and exponent all ones
assign SC_Operand_Infinity = (&smallerOperand_Exponent & !(|smallerOperand_Mantissa[10:1]));

// Match the exponent of smaller operand with larger operand - i.e. right shift it by exp_diff times
BarrelShifterRight SmallerExponentMatch (smallerOperand_Mantissa, Exponent_Diff, smallerOperand_Mantissa_Normalised);

// Check if larger and smaller operands have different signs - if so, subtract, else add
wire diff_signs = ((!largerOperand_Sign) & smallerOperand_Sign_Normalised) | (largerOperand_Sign & (!smallerOperand_Sign_Normalised));

wire [11:1] smallerOperand_Mantissa_Normalised_2scomp;
Complement2s_11Bit SmallerMantissaComplementer (smallerOperand_Mantissa_Normalised, smallerOperand_Mantissa_Normalised_2scomp);

wire [11:1] smallerOperand_Mantissa_Normalised_Signed;
Bit10MUX SmallerOperandAddOrSubtractChooser (smallerOperand_Mantissa_Normalised[10:1], smallerOperand_Mantissa_Normalised_2scomp[10:1], diff_signs, smallerOperand_Mantissa_Normalised_Signed[10:1]);
assign smallerOperand_Mantissa_Normalised_Signed[11] = ((!diff_signs) & smallerOperand_Mantissa_Normalised[11]) | ((diff_signs) & smallerOperand_Mantissa_Normalised_2scomp[11]);

// Now Add the larger operand mantissa with exponent matched smaller operand mantissa
wire [12:1] addedValue_extended;
wire [11:1] addedValue;
wire DontIgnoreCarry;

Bit11Adder MantissaAdder (largerOperand_Mantissa, smallerOperand_Mantissa_Normalised_Signed, addedValue_extended[11:1], addedValue_extended[12]);

assign DontIgnoreCarry = addedValue_extended[12] & (!diff_signs); // Ignore the carry if subraction - i.e. diffsigns = 1

// If carry is 0, addedValue is addedValue_extended[11:1] else if carry is 1, addedValue is addedValue_extended[12:2] and increase largerExponent by 1
wire [5:1] largerOperand_Exponent_CarryAdjusted;
wire CarryAdd_Exponent_Overflow;
wire [5:1] carrytoadd;

Bit5MUX CarryChooser (5'b00000, 5'b00001, DontIgnoreCarry, carrytoadd);
Bit5Adder CarryAdder (largerOperand_Exponent, carrytoadd, largerOperand_Exponent_CarryAdjusted, CarryAdd_Exponent_Overflow);

Bit10MUX MantissaOverflowChooser (addedValue_extended[10:1], addedValue_extended[11:2], DontIgnoreCarry, addedValue[10:1]);
assign addedValue[11] = ((!DontIgnoreCarry) & addedValue_extended[11]) | (DontIgnoreCarry & DontIgnoreCarry);

assign SC_Mantissa_Zero = !(|addedValue);   // If all zeros |addedValue returns 0, even if one 1 present returns 1

// normalise the output - i.e. if output is 0010 make it to 1000 by shifting left and decreasing exponent of larger operand
wire [5:1] norm_shift;
wire [11:1] addedValue_Normalised;
NormaliseShift ns (addedValue, norm_shift);
BarrelShifterLeft RenormaliseOutputMantissa (addedValue, norm_shift, addedValue_Normalised);
wire [5:1] norm_shift_2scomp;
wire [5:1] finalexp_norm;
wire Normalise_Exponent_Overflow;

ExpSubtractor RenormaliseExp (largerOperand_Exponent_CarryAdjusted, norm_shift, finalexp_norm, SC_Exponent_UnderFlow);

assign out_Sign = largerOperand_Sign;

// Check Special Conditions and Assign Output Exponent
wire [5:1] out_Exponent_Intermediate_1, out_Exponent_Intermediate_2;
// If smaller operand was 0 directly assign output as the larger operand
Bit5MUX outExponentChooser1 (finalexp_norm, largerOperand_Exponent, SC_Operand_Zero, out_Exponent_Intermediate_1);
// If larger operand was Infinity directly assign output as all ones
Bit5MUX outExponentChooser2 (out_Exponent_Intermediate_1, 5'b11111, SC_Operand_Infinity, out_Exponent_Intermediate_2);
// If mantissa is all 0, then exponents should be set to 0
Bit5MUX outExponentChooser3 (out_Exponent_Intermediate_2, 5'b00000, SC_Mantissa_Zero, out_Exponent);

// Check Special Conditions and Assign Output Mantissa
wire [10:1] out_Mantissa_Intermediate_1, out_Mantissa_Intermediate_2;
// If smaller operand was 0 directly assign output as the larger operand
Bit10MUX outMantissachooser1 (addedValue_Normalised[10:1], largerOperand_Mantissa[10:1], SC_Operand_Zero, out_Mantissa_Intermediate_1);
// If larger operand was Infinity directly assign output as all ones
Bit10MUX outMantissachooser2 (out_Mantissa_Intermediate_1, 10'b0000000000, SC_Operand_Infinity, out_Mantissa_Intermediate_2);
assign out_Mantissa = out_Mantissa_Intermediate_2;

// Check if Output Overflows
assign SC_Output_OverFlow = &out_Exponent;

// always @(*) begin
//     $display("INP: %b = %b - %b", Exponent_Diff, in_Exponent_1, in_Exponent_2);
//     $display("LOL: %b = %b - %b", SC_Exponent_UnderFlow, largerOperand_Exponent_CarryAdjusted, norm_shift);
// end

// DENORM NOS LEFT OUT
endmodule

// Floating Multiplier
module FMul_HalfPrecision(
    in_Sign_1, in_Exponent_1, in_Mantissa_1, 
    in_Sign_2, in_Exponent_2, in_Mantissa_2, 
    out_Sign, out_Exponent, out_Mantissa, 
    SC_Exponent_Overflow, 
    SC_Exponent_Underflow
);

// Special Conditions
output SC_Exponent_Overflow;
output SC_Exponent_Underflow;
wire SC_Operand_Infinity;
wire SC_Operand_Zero;

// Initial
input in_Sign_1;
input [5:1] in_Exponent_1;
input [10:1] in_Mantissa_1;
input in_Sign_2;
input [5:1] in_Exponent_2;
input [10:1] in_Mantissa_2;

output out_Sign;
output [5:1] out_Exponent;
output [10:1] out_Mantissa;

// Check for Zeros - if one op is 0 answer is 0
assign SC_Operand_Zero = !(|in_Mantissa_1 | |in_Exponent_1) | !(|in_Mantissa_2 | |in_Exponent_2);

// Check for Infinity - If one op is Infinity answer is Infinity
assign SC_Operand_Infinity = (&in_Mantissa_1 & &in_Exponent_1) | (&in_Mantissa_2 & &in_Exponent_2);

// Out Sign = xor of 2 input signs
assign out_Sign = ((!in_Sign_1) & in_Sign_2) | (in_Sign_1 & (!in_Sign_2));

// Out Exponent = Sum of 2 input Exponents
wire [6:1] exp_extended, exp_subbed;
wire expcarry;
Bit5Adder expadd (in_Exponent_1, in_Exponent_2, exp_extended[5:1], exp_extended[6]);
// Subtract 15 from result as in result 15 offset is done 2 times
Bit6Adder expsub (exp_extended, 6'b110001, exp_subbed, expcarry);

// Check for overflow by exp_extended - 45  = If +ve then overflow
wire [7:1] overflowcheck;
Bit6Adder checkoverflow (exp_extended, 6'b010011, overflowcheck[6:1], overflowcheck[7]);
assign SC_Exponent_Overflow = (overflowcheck[7] & (|overflowcheck[6:1])) | exp_plus1[6]; // 1 000000 is accepted as it is 45 - 45

// Check Special Conditions and Assign Output Exponent
wire [5:1] out_Exponent_Intermediate_1;
wire [6:1] exp_plus1;
Bit5Adder expplus1 (exp_subbed[5:1], 5'b00001, exp_plus1[5:1], exp_plus1[6]);
wire [5:1] exp_mux_in = (prod_extended[22]) ? exp_plus1 : exp_subbed[5:1];
// Check if one of the operands is 0 then output exponent is also 0
Bit5MUX expchooser1 (exp_mux_in, 5'b00000, SC_Operand_Zero, out_Exponent_Intermediate_1);
// Check if one of operands is Infinity then output exponent is all ones
Bit5MUX expchooser2 (out_Exponent_Intermediate_1, 5'b11111, SC_Operand_Infinity, out_Exponent);

// Out Mantissa = Product of 2 input Mantissas
wire [16:1] in_1_extended, in_2_extended;
wire [36:1] prod_extended;
assign in_1_extended[10:1] = in_Mantissa_1;
assign in_1_extended[16:11] = 6'b000001;
assign in_2_extended[10:1] = in_Mantissa_2; 
assign in_2_extended[16:11] = 6'b000001;
Multiplier_16Bit mul (in_1_extended, in_2_extended, prod_extended);

// If prod_extended[22] = 1, shift by once right and increase exp by 1
wire [10:1] prod_mux_in = (prod_extended[22]) ? prod_extended[21:12] : prod_extended[20:11];

// Check Special Conditions and Assign Output Mantissa
wire [10:1] out_Mantissa_Intermediate_1;
// Check if one of the operands is 0 then output mantissa is also 0
Bit10MUX mantissachooser1 (prod_mux_in, 10'b0000000000, SC_Operand_Zero, out_Mantissa_Intermediate_1);
// Check if one of operands is Infinity then output mantissa is all ones
Bit10MUX mantissachooser2 (out_Mantissa_Intermediate_1, 10'b1111111111, SC_Operand_Infinity, out_Mantissa);

assign SC_Exponent_Underflow = exp_subbed[6] & (!SC_Operand_Zero & !SC_Operand_Infinity & !SC_Exponent_Overflow);

// always @(*)
//     $display("LOL: %b", prod_extended);

endmodule

// 