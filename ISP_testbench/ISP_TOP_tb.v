`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2021/11/30 23:21:41
// Design Name: 
// Module Name: ISP_TOP_tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module ISP_TOP_tb(
      );
reg          clk_wr;
reg          clk_rd;
reg          clk_fpga;
reg          rst_n;
reg          ping_pong_en;
reg   [23:0] sdram_wr_addr_max;
reg   [23:0] sdram_wr_addr_min;
reg   [23:0] sdram_rd_addr_max;
reg   [23:0] sdram_rd_addr_min;
reg          rd_valid;
reg   [9:0]  br_length;

wire          H_SYNC;
wire          V_SYNC;
wire          BLANK;
wire   [15:0] display_data;
integer i;
integer j;

integer out_file;//定义文件句柄
integer grey_out_file;
always #20 clk_wr = ~clk_wr;
always #10 clk_rd = ~clk_rd;
always #10 clk_fpga = ~clk_fpga;

// VCD waveform dump -- opt-in via plusarg.
// A full-hierarchy dump over this testbench's 30 ms of sim time produced a
// ~2.9 GB isp_top_tb.vcd, and nothing under sim/ reads it (the test asserts on
// output/grey_out_*.txt instead).  Dumping is therefore off by default so the
// regression does not write gigabytes; enable it when debugging a waveform:
//     vvp -n isp_top_tb.vvp +dump      (then open isp_top_tb.vcd)
initial begin
  if ($test$plusargs("dump")) begin
    $dumpfile("isp_top_tb.vcd");
    $dumpvars(0, ISP_TOP_tb);
  end
end

initial begin
  i = 0;
  j = 0;
  $readmemh("test_image.hex",U_ISP_TOP_0.data_src_mem);
  clk_wr = 0;
  clk_rd = 0;
  clk_fpga = 0;
  ping_pong_en = 1;
  sdram_wr_addr_max = 307200;
  sdram_wr_addr_min = 0;
  sdram_rd_addr_max = 307200;
  sdram_rd_addr_min = 0;
  rd_valid = 0;
  br_length = 512;
  // Reset must stay low across at least one wr_clk posedge, otherwise
  // wr_fifo/rd_fifo never sample their rst (clk_wr period is 40 ns; the old
  // #40/#20 pulse left rst high at the 60 ns posedge, leaving wr_ptr=x and
  // the whole SDRAM write path dead -> all-zero output).
  rst_n = 0;
  #120 rst_n = 1;
  wait(U_ISP_TOP_0.U_SDRAM_TOP_0.init_done == 1);
  rd_valid = 1;
  // 40 ms: write a full 640x480 frame (12.3 ms at 40 ns/px) + ping-pong
  // switch + read-back of the previous frame.  The old 4 ms never finished
  // writing even one frame, so the display path only ever saw zeros.
  #30000000;
  $display("ISP_TOP simulation complete");
  $finish;
end



always @(posedge V_SYNC) begin
  out_file = $fopen($sformatf("output/isp_out_%0d.txt", i),"w");//获取文件句柄
end
always @(posedge U_ISP_TOP_0.U_RGB2YUV_0.V_SYNC) begin
  grey_out_file = $fopen($sformatf("output/grey_out_%0d.txt", j),"w");//获取文件句柄
end

always @(negedge V_SYNC) begin
  $fclose(out_file);
  i <= #0.1 i + 1;
end
always @(negedge U_ISP_TOP_0.U_RGB2YUV_0.V_SYNC) begin
  $fclose(grey_out_file);
  j <= #0.1 j + 1;
end
always @(posedge clk_rd) begin
  if (BLANK) begin
    $fwrite(out_file,"%h\n",display_data);
  end
end
always @(posedge clk_rd) begin
  if (U_ISP_TOP_0.U_RGB2YUV_0.BLANK) begin
    $fwrite(grey_out_file,"%h\n",U_ISP_TOP_0.U_RGB2YUV_0.display_data);
  end
end
ISP_TOP U_ISP_TOP_0
(  .clk_wr            ( clk_wr            ),
   .clk_rd            ( clk_rd            ),
   .clk_fpga          ( clk_fpga          ),
   .rst_n             ( rst_n             ),
   .ping_pong_en      ( ping_pong_en      ),
   .sdram_wr_addr_max ( sdram_wr_addr_max ),
   .sdram_wr_addr_min ( sdram_wr_addr_min ),
   .sdram_rd_addr_max ( sdram_rd_addr_max ),
   .sdram_rd_addr_min ( sdram_rd_addr_min ),
   .rd_valid          ( rd_valid          ),
   .br_length         ( br_length         ),
   .H_SYNC            ( H_SYNC            ),
   .V_SYNC            ( V_SYNC            ),
   .BLANK             ( BLANK             ),
   .display_data      ( display_data      ));

endmodule
