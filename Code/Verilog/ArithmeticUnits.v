/*
Summary
Library of Arithmetic Unit Modules made by ME
*/

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

module Bit16Adder (a, b, cin, sum, cout);
input[16:1] a, b;
input cin;
output[16:1] sum;
output cout;

	wire w1, w2, w3;

	Bit4Adder3 B4A_0(a[4:1], b[4:1], cin, sum[4:1], w1);
	Bit4Adder3 B4A_1(a[8:5], b[8:5], w1, sum[8:5], w2);
	Bit4Adder3 B4A_2(a[12:9], b[12:9], w2, sum[12:9], w3);
	Bit4Adder3 B4A_3(a[16:13], b[16:13], w3, sum[16:13], cout);

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

module Bit64Adder (a, b, cin, sum, cout);
input[64:1] a, b;
input cin;
output[64:1] sum;
output cout;

	wire w1, w2, w3;

	Bit16Adder B16A_0(a[16:1], b[16:1], cin, sum[16:1], w1);
	Bit16Adder B16A_1(a[32:17], b[32:17], w1, sum[32:17], w2);
	Bit16Adder B16A_2(a[48:33], b[48:33], w2, sum[48:33], w3);
	Bit16Adder B16A_3(a[64:49], b[64:49], w3, sum[64:49], cout);

endmodule

module FullAdder (a, b, cin, sum, cout);
input a, b, cin;
output sum, cout;
	assign sum = a ^ b ^ cin;
	assign cout  = ((a^b)&cin) | (a&b);	// carry = (a xor b)cin + ab
endmodule

module HalfAdder (a,b,sum, ca);
input a, b;
output sum, ca;
	assign sum = a ^ b;
	assign ca  = a&b;
endmodule

module Multiplier_16Bit(A, B, out);
    
    input [16:1] A,B;
    output [36:1] out;

    reg zero;
    initial 
        zero = 1'b0;

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

module DFF(d,clk,reset,q);
input clk, reset;
input [36:1] d;
output reg [36:1] q;

always@(negedge clk or posedge reset)
	if(reset)
 		q <= 36'h000000000;
	else
		q <= d;

endmodule

module DFF2(d,clk,reset,q);
input d, clk, reset;
output q;
reg q;

always@(negedge clk or negedge reset)
	if(reset)
 		q <= 1'b0;
	else
		q <= d;

endmodule

module WallaceMultiplier(A,B,prod);
    
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

module MAC_16Bit(clk, A, B, out, reset);
    
    input clk;
    input [16:1] A,B;
    input reset;
    output [36:1] out;

    wire [36:1] fm, fa;
    wire cout;
    wire [36:1] outfeedback;

    //initial 
        //outfeedback <= 'd0;

    // Stage 1
    Multiplier_16Bit Mul (A, B, fm);

    DFF d (fm, clk, reset, fa);
    // Stage 2
    Bit36Adder Add (outfeedback, fa, reset, out, cout);

    DFF dd (out, clk, reset, outfeedback);

    
    // ----- Step 5 --------------------------------------
/*
always@(*) 
    $display(": Intermediate Binary: A = %b (%d), B = %b (%d), Product: %b (%d) -- --%b--", A, A, B, B, prod, prod, p1);
*/
endmodule

module RecursiveDoubling(a, b, cin, sum, cout);
	input [16:1] a,b;
	input cin;
	
	output wire [16:1] sum;
	output wire cout;

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
assign cout=gk[16];

endmodule

