Python code to assist in measuring astrophysical log(gf) values of LS multiplets. For lines that are to close to measure individually, this code lets you measure the whole line and calculate what the log(gf) values of the components should be.

To calculate a value, use the function LS(log(gf) of primary line, L_1, L_2, J_low for primary line, J_high for primary line, J_low for secondary line, J_high for secondary line). The log(gf) of the secondary line should be returned.

To calculate the strength of a secondary line it has to be part of the same LS multiplet. Transitions from 2S1/2 - 2P1/2 to 6G13/2 - 6H15/2 are included, data taken from "The theory of Atomic Structure and Spectra" Cowan 1981. Pure LS coupling is assumed, error messages should be there for disallowed transitions.
