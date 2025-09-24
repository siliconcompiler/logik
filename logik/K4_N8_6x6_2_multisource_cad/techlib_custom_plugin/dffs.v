//dffs.v

(* blackbox *)
module dffs ( clk, D, S, Q );

    input clk;

    input D;
    input S;

    output reg Q;

    always @(posedge clk or negedge S) begin
        if (~S) begin
            Q <= 1'b1;
        end
        else begin
            Q <= D;
        end
   end // always @ (posedge clk or negedge S)

   
endmodule // dffs
