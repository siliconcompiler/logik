//dffr.v

(* blackbox *)
module dffr ( clk, D, R, Q);

    input clk;

    input D;
    input R;

    output reg Q;

    always @(posedge clk or negedge R) begin
        if (~R) begin
            Q <= 1'b0;
        end
        else begin
            Q <= D;
        end // else: !if(~R)
   end // always @ (posedge clk or negedge R)

   
endmodule // dffr
