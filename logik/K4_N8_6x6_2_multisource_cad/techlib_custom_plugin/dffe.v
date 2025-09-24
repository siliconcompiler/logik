//dffe.v

(* blackbox *)
module dffe ( clk, D, Q, E );

   input clk;

   input D;
   input E;

   output reg Q;

    always @(posedge clk) begin
        if(E) begin
            Q <= D;
        end
   end // always @ (posedge clk)
   
endmodule // dffe
