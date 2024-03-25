// @aaryswastaken 2024

module compute_dba
#(
	parameter d_w=16,
	parameter r_w=20
)
(
	input wire	clk,
	input wire	rst,
	input wire signed [r_w-1:0]	in_r [d_w-1:0],
	input wire signed [r_w-1:0]	in_i [d_w-1:0],

	input wire	query,

	output reg signed [r_w-1:0]	avg
);

reg [d_w-1:0] cnt;
reg [d_w*2:0] sum;



localparam 	STATE_WAIT	= 0;
localparam	STATE_CALC	= 0;
localparam 	STATE_UPDATED	= 0;

reg [3:0] state = STATE_WAIT;

always @(posedge rst) begin
	state = STATE_WAIT;
	avg = 0;
	cnt = 0;
end

always @(posedge clk) begin
	case(state)
		STATE_CALC: begin
		end
	endcase
end

endmodule
