//dffer.v

(* blackbox *)
module dffer ( clk, D, R, Q, E );

    input clk;

    input D;
    input R;
    input E;

    output reg Q;

    always @(posedge clk or negedge R) begin
        if (~R) begin
            Q <= 1'b0;
        end
        else begin
            if(E) begin
                Q <= D;
            end
        end // else: !if(~R)
   end // always @ (posedge clk or negedge R)

   
endmodule // dffer
