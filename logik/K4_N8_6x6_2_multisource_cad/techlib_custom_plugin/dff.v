//dff.v

(* blackbox *)
module dff
  (
   input      clk,
   input      D,
   output reg Q
   );

   always @(posedge clk) Q <= D;

endmodule
