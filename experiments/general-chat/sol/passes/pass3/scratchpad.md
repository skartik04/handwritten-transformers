FINAL PASS. No tools, execution, training, or behavioural feedback used.

The previous two passes remain in force. This pass adds:
- Exact decimal addition, nonnegative subtraction, multiplication, and exact division for the specified operand/result ranges, with “the answer is [number].”
- Independent arithmetic routing, current-message number reset, number-word operand support, numeric memory, personal age recall, remembered likes, and animal/fruit/planet lists.
- Arithmetic uses the previously installed scalar output decoder and reply clock; unused reply steps select EOS.

New/changed residuals:
14..19: decimal digits a0,a1,a2,b0,b1,b2, replacing raw factual features after M3.
56: current arithmetic-present flag, computed M2 after moving operator retrieval to L2 head6.
61: previous-like content key from M1.
62: previous number-word flag from L1 head5.
74: remembered numeric-value presence.
110: previous number-word value from L1 head5; obsolete earliest-number head removed.
113: latest remembered user number, L3 head5.
229: remembered object of “like,” L3 head6.
239..242: plus/minus/multiply/divide flags.
243: nondivision numeric result.
244: division remainder after hundreds.
245: final hundreds digit, initially division hundreds.
246: division tens digit.
247: division remainder after tens.
248: final thousands digit.
249: final last-two-digit value.
250..253: result-length flags 1..4.
255: recalled-number output flag.

Arithmetic allocation:
M3 392:608 extracts A digits;608:824 extracts B digits;824:830 opcode hats;830:869 division hundreds and length;870:918 arithmetic category erasure;918 numeric category;919:927 digit bases and raw-feature clearing;927:929 age/number recall;932:934 remembered likes;940:949 list selection.
M4 479:695 integer-square multiplication;695:697 addition/subtraction;697:734 division tens;734:737 numeric prefix;737:740 like prefix/suffix;740:767 list templates;767 recalled numeric result.
M5 15:231 thousands/hundreds extraction;231:239 number remainder and lengths;239:258 division ones and last-two digits;258:260 remembered-like dynamic slot.
M6 0:147 schedules numeric digits and period. No output after the period means EOS.

New categories:217 numeric reply;220 remembered like;221 animal list;222 fruit list;223 planet list. New token output code580=berry.
Division uses staged comparisons A>=100kB, remainder>=10kB, remainder>=kB, with exact saturated B gates. Multiplication uses digit squares and the polarization identity. Decimal threshold pairs use quarter-unit margins.