// @aaryswastaken 2024

module dac
#(
	parameter size=8
)
(
	input wire		clk,
	input wire		tick,
	input wire [size-1:0]	sample,
	output reg [size-1:0]	out
);

always @(posedge tick) begin
	out <= sample;
end

endmodule 
