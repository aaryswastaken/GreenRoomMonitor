// @aaryswastaken 2024
//

module top
#(
	parameter adc_w=8,
	parameter ft_w=16,
	parameter fw=20
)
(
	input wire 		i_clk,
	
	// adc
	input wire 		fb,
	output wire[adc_w-1:0]	spl,
	
	// serial
	output wire		tx
);

wire clk;
assign clk=i_clk;

reg[adc_w-1:0]	adc_res;
reg		adc_ready;

wire		ft_start;
wire		ft_read;
reg[adc_w-1:0]	sample;
reg[19:0]	bin_addr;
wire signed [fw-1:0]	bin_out_r [ft_w-1:0];
wire signed [fw-1:0]	bin_out_i [ft_w-1:0];
wire		ft_ready;

reg signed [fw-1:0]	buff_out_r [ft_w-1:0];
reg signed [fw-1:0]	buff_out_i [ft_w-1:0];

reg query;
wire avg[fw-1:0];
reg dba_rst;

adc#(.size(adc_w))
the_adc(.clk(clk), .fb(fb), .spl(spl), .res(adc_res), .ready(adc_ready));

sdft#(.data_width(adc_w), .freq_bins(ft_w), .freq_w(fw))
ft(.clk(clk), .sample(sample), .start(ft_start), .read(ft_read), .bin_addr(bin_addr), .frequency_bins_real(bin_out_r), .frequency_bins_imag(bin_out_i), .ready(ft_ready));

compute_dba#(.d_w(ft_w), .r_w(fw))
dbaCalc (.clk(clk), .rst(dba_rst), .in_r(buff_out_r), .in_i(buff_out_i), .query(query), .avg(avg));

//
localparam	STATE_WAIT	= 0;
localparam	STATE_WAIT_ADC	= 1;
localparam	STATE_WAIT_DFT	= 2;
localparam	STATE_READY	= 3;

reg[3:0]  state = STATE_WAIT;

always @(posedge clk) begin
	case(state) 
		STATE_WAIT: begin
			if(adc_ready)
				state <= STATE_WAIT_DFT;
			if(ft_ready)
				state <= STATE_WAIT_ADC;
		end

		STATE_WAIT_ADC: begin
			if(adc_ready)
				state <= STATE_READY;
		end

		STATE_WAIT_DFT: begin
			if(ft_ready)
				state <= STATE_READY;
		end

		STATE_READY: begin
			sample <= adc_res;
			buff_out_r <= bin_out_r;
			buff_out_i <= bin_out_i;

			updated <= 1;
		end
	endcase
end

endmodule
