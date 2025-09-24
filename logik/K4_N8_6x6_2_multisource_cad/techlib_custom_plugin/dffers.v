//dffers.v

(* blackbox *)
module dffers ( clk, D, R, S, Q, E );

    input clk;

    input D;
    input R;
    input S;
    input E;

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
                if(E) begin
                    Q <= D;
                end
            end
        end // else: !if(~R)
   end // always @ (posedge clk or negedge R or negedge S)

   
endmodule // dffers
