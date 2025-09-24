//dffrs.v

(* blackbox *)
module dffrs ( clk, D, R, S, Q );

   input clk;

   input D;
   input R;
   input S;

   output reg Q;

   always @(posedge clk or negedge R or negedge S) begin
      if (~R) begin
	 Q <= 1'b0;
      end
      else begin
	 if (~S) begin
	    Q <= 1'b1;
	 end
	 else begin
	    Q <= D;
	 end
      end // else: !if(~R)
   end // always @ (posedge clk or negedge R or negedge S)
   
endmodule // dffrs
