// @aaryswastaken 2024

module adc
#(
	parameter size=8
)
(
	input wire 		clk,
	input wire		fb,
	output wire[size-1:0]	spl,
	output reg[size-1:0]	res,
	output reg		ready
)

integer pos;

dac(.clk(clk), .tick(tick), .sample(res), .out(spl));

wire tick;
assign tick;

initial begin
	pos <= 0;
	tick = 0;
end

always @(posedge clk) begin
	if(!ready) begin
		if(pos < size) begin
			res[pos] <= 1;
			tick <= 1;
		end else begin
			ready <= 1;
			pos <= 0;
		end
	end
end

always @(negedge clk) begin
	tick <= 0;
end

always @(posedge fb) begin
	res[pos] <= 0;
end

endmodule
