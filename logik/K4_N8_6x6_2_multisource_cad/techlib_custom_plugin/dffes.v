//dffes.v

(* blackbox *)
module dffes ( clk, D, S, Q, E );

    input clk;

    input D;
    input S;
    input E;

    output reg Q;

    always @(posedge clk or negedge S) begin
        if (~S) begin
            Q <= 1'b1;
        end
        else begin
            if(E) begin
                Q <= D;
            end
        end
   end // always @ (posedge clk or negedge S)

   
endmodule // dffes
