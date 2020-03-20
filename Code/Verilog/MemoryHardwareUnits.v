/*
Summary
Library of Memory Hardware Unit Modules made by ME
*/

module DFF(d,clk,reset,q);
input clk, reset;
input wire d;
output reg q;

initial 
	q = 1'b0;

always@(posedge clk or posedge reset)
begin
	if(reset)
 		q <= 1'b0;
	else
		q <= d;
end

endmodule

module TFF(d,clk,reset,q, select);
input clk, reset, select;
input wire d;
output reg q;
/*
initial 
	q = 1'b1;
*/
always@(posedge clk or posedge reset)
begin
	if(reset)
	begin
 		q = ~select;
 	end
	else
		q <= (d&(~q)) | ((~d)&q);
end

endmodule

module DownASync(clk,reset,q);
input clk, reset;
output [4:1] q;

DFF dff_1(~q[1], clk, reset, q[1]);
DFF dff_2(~q[2], q[1], reset, q[2]);
DFF dff_3(~q[3], q[2], reset, q[3]);
DFF dff_4(~q[4], q[3], reset, q[4]);

endmodule

module UpASync(clk,reset,q);
input clk, reset;
output [4:1] q;

DFF dff_1(~q[1], clk, reset, q[1]);
DFF dff_2(~q[2], ~q[1], reset, q[2]);
DFF dff_3(~q[3], ~q[2], reset, q[3]);
DFF dff_4(~q[4], ~q[3], reset, q[4]);

endmodule

module UpDownSync(clk,reset,q, select);
input clk, reset, select;
output [4:1] q;

wire [4:1]inputs;

assign inputs[1] = 1'b1;

/*
initial begin
	q[1] <= 1'b1;
	q[2] <= 1'b1;
	q[3] <= 1'b1;
	q[4] <= 1'b1;
end
*/

assign inputs[2] = select&q[1] | (~select)&(~q[1]);
assign inputs[3] = select&q[1]&q[2] | (~select)&(~q[1])&(~q[2]);
assign inputs[4] = select&q[1]&q[2]&q[3] | (~select)&(~q[1])&(~q[2])&(~q[3]);


TFF tff_1(inputs[1], clk, reset, q[1], select);
TFF tff_2(inputs[2], clk, reset, q[2], select);
TFF tff_3(inputs[3], clk, reset, q[3], select);
TFF tff_4(inputs[4], clk, reset, q[4], select);

/*
initial
	$monitor($time, ": clk=%b, rst=%b, inp=%b, q=%b\n", clk, reset, inputs, q);
*/

endmodule

module SR_PIPO(d,clk,reset,outputs, write_check);

input [4:1]d;
input write_check;
input clk, reset;

wire w[3:1];

output [4:1]outputs;

assign w[1] = (write_check&d[1]) | ((~write_check)&outputs[1]);
assign w[2] = (write_check&d[2]) | ((~write_check)&outputs[2]);
assign w[3] = (write_check&d[3]) | ((~write_check)&outputs[3]);

DFF dff_1(d[1], clk, reset, outputs[1]);
DFF dff_2(w[1], clk, reset, outputs[2]);
DFF dff_3(w[2], clk, reset, outputs[3]);
DFF dff_4(w[3], clk, reset, outputs[4]);

endmodule

module SR_PISO(d,clk,reset,q, write_check);

input [4:1]d;
input write_check;
input clk, reset;
output q;

wire w[3:1];

wire outputs[3:1];

assign w[1] = (write_check&d[1]) | ((~write_check)&outputs[1]);
assign w[2] = (write_check&d[2]) | ((~write_check)&outputs[2]);
assign w[3] = (write_check&d[3]) | ((~write_check)&outputs[3]);

DFF dff_1(d[1], clk, reset, outputs[1]);
DFF dff_2(w[1], clk, reset, outputs[2]);
DFF dff_3(w[2], clk, reset, outputs[3]);
DFF dff_4(w[3], clk, reset, q);

endmodule

module SR_SIPO(d,clk,reset,q);

input d, clk, reset;
output [4:1] q;

DFF dff_1(d, clk, reset, q[1]);
DFF dff_2(q[1], clk, reset, q[2]);
DFF dff_3(q[2], clk, reset, q[3]);
DFF dff_4(q[3], clk, reset, q[4]);

endmodule

module SR_SISO(d,clk,reset,q);

input d, clk, reset;
output q;

wire w1, w2, w3;

DFF dff_1(d, clk, reset, w1);
DFF dff_2(w1, clk, reset, w2);
DFF dff_3(w2, clk, reset, w3);
DFF dff_4(w3, clk, reset, q);

endmodule

module USR(inputs,serialin,clk,reset,outputs, select);

input [4:1] inputs;
input serialin;
input [2:1]select;
input clk, reset;

wire [4:1]w;

output [4:1]outputs;

assign w[1] = ((~select[2])&(~select[1])&outputs[1]) | (select[2]&(~select[1])&outputs[2]) | ((~select[2])&select[1]&serialin) 		 | (select[2]&select[1]&inputs[1]);
assign w[2] = ((~select[2])&(~select[1])&outputs[2]) | (select[2]&(~select[1])&outputs[3]) | ((~select[2])&select[1]&outputs[1]) | (select[2]&select[1]&inputs[2]);
assign w[3] = ((~select[2])&(~select[1])&outputs[3]) | (select[2]&(~select[1])&outputs[4]) | ((~select[2])&select[1]&outputs[2]) | (select[2]&select[1]&inputs[3]);
assign w[4] = ((~select[2])&(~select[1])&outputs[4]) | (select[2]&(~select[1])&serialin) 		   | ((~select[2])&select[1]&outputs[3]) | (select[2]&select[1]&inputs[4]);

DFF dff_1(w[1], clk, reset, outputs[1]);
DFF dff_2(w[2], clk, reset, outputs[2]);
DFF dff_3(w[3], clk, reset, outputs[3]);
DFF dff_4(w[4], clk, reset, outputs[4]);

endmodule