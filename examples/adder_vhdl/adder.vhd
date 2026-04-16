-------------------------------------------------------------------------------
-- Copyright 2024 Zero ASIC Corporation
--
-- Licensed under the MIT License (see LICENSE for details)
-------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity adder is
    generic (
        DATA_WIDTH : integer := 8
    );
    port (
        a : in  std_logic_vector(DATA_WIDTH - 1 downto 0);
        b : in  std_logic_vector(DATA_WIDTH - 1 downto 0);
        y : out std_logic_vector(DATA_WIDTH downto 0)
    );
end entity adder;

architecture rtl of adder is
begin
    y <= std_logic_vector(
        unsigned('0' & a) + unsigned('0' & b)
    );
end architecture rtl;
