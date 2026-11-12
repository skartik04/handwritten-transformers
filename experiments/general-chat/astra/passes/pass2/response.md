=====SCRATCHPAD=====
PASS 2 STATUS

No tools or execution used. Pass 2 adds three-digit input-number parsing, addition, nonnegative subtraction, multiplication, approximate-reciprocal exact division, variable-length decimal output through 9999, and remembered numbers/ages. Existing conversation, capitals, leaders, opposites, name memory, and echo remain. There is one pass left.

IMPORTANT CHANGES
- User-only lexical gating moved from M2 units0:36 to M1 units193:229.
- M2's existing position-square computation units36:228 remains unchanged.
- L3 H5 and H7 now retrieve first/last numbers. Echo and negation moved to L2 H1/H2.
- M3 arithmetic takes precedence only when a current-message number AND an operation are present.
- Template44 is numeric: “the answer is <unpadded decimal> .” EOS.
- Personal-age template selection now maps to44; token “number” selects44 for number memory.
- Invalid “calm” output in template33 replaced by existing output word “quiet”, code308. Previously unused code115 is now valid token “special”.
- M3 free units854:1024; M4 free712:1024; M5 free236:1024; M6 free40:1024.
- Division transformation is determined at each number’s trailing delimiter by the latest preceding operation. Thus direct A divided by B works; postfix division wording can fail. Reciprocal interpolation is exact for divisors1..50, approximate above, with intended error small enough to round integral quotients correctly. No numerical verification has occurred.

RESIDUAL MAP
0 constant1 all tokens.
1 BOS flag,2 USER,3 BOT.
Raw lexical4..39:
4 intent priority,5 intent template.
6 subject priority,7 subject template,8 fact word1,9 fact word2,10 fact flag.
11 adjective priority,12 emotion template,13 opposite code,14 reserved class.
15 negation.
16 task priority,17 task template.
18 digit flag,19 digit value,20 echo word code.
21 personal-name flag,22 personal-name code.
23 operation-or-USER marker,24 operation id (1 add,2 subtract,3 multiply,4 divide),25 divide flag.
26 echo priority.
27 speaker code1 user/2 bot,28 speaker priority.
29 two-word-fact flag.
30 actual-operation flag (USER has0).
31..39 still free.
40..75 user-only copies of4..39, now generated M1.
76 intent,77 subject template,78 fact1,79 fact2,80 fact flag.
81 emotion,82 opposite,83 adjective class.
84 task,85 remembered personal name,86 echo (now L2),87 speaker.
88 two-word fact,89 name-present,90 negation (now L2).
91 first current-message number A,92 A².
93 last current-message transformed number B′,94 interpolated square of B′.
95 first-number flag,96 last-number flag,97 last original number B.
98 free.
99 latest historical user number;100 its present flag (L2 H3).
101 number exists in current message,102 arithmetic-active (M2).
103 A+B′,104 partial multiplication/division result (M3).
105 A+B,106 |A-B|.
107 free.
108 arithmetic addition gate,109 subtraction gate,110 multiplication/division gate.
111..140 free.
141 selected template.
142..159 free.
160 frozen template,161 frozen fact1,162 fact2,163 latest BOT absolute position.
164 frozen opposite,165 frozen name,166 frozen echo.
167 frozen operation id,168 arithmetic-active,169 A+B′,170 partial product,
171 addition result,172 absolute subtraction result,173 remembered number.
174 completed numerical result (M4).
175 frozen current-number flag.
176 frozen addition gate,177 subtraction gate,178 multiply/divide gate.
179 free.
180 output word-code coordinate,181 output bias1.
182 fact1 slot,183 fact2 slot,184 opposite slot,185 name slot,186 echo slot.
187 old template18 number slot, unused.
188..191 numeric output phases0..3;195 phase4.
192 thousands digit,193 hundreds digit,194 remainder modulo100 (M5).
196 thousands-output gate,197 hundreds gate,198 tens gate,199 ones gate (M5).
200 reciprocal position1/(t+1),201 absolute position t+1.
202 current user role.
203 free.
204 latest USER absolute position,205 its square/256.
206 previous token digit flag,207 digit value.
208 two-back digit flag,209 value.
210 three-back digit flag,211 value.
212 parsed number,213 number-end flag,214 parsed number squared (M1).
215 transformed local number (normal n or reciprocal n),216 latest divide flag (L1).
217 transformed square (normal n² or reciprocal n).
218 latest operation id,219 latest actual-operation flag (L1).
220 position of latest parsed user number (L2).
221..255 free.

ATTENTION
L1 H0 uniform attention BOS ->200; M1 units0:193 inverse reciprocal positions:
p=385-37056*u+sum(n=2..192)2n ReLU(u-1/n).
L1 H1 latest USER/BOT ->202; slow RoPE pair30/31, Q100,K[1000,-10000].
L1 H2,H3,H4 fixed relative offsets1,2,3; frequencies1,.1,.01, query100 and keys phase-shifted to those offsets. Digit flags/values ->206:212.
L1 H5 latest operation or USER reset ->216,218,219.
L1 H6,H7 unused.

M1 units193:229 user-gate raw4:40 into40:76.
229:232 parse 1st,2nd,3rd previous digits into212 only at a user-number end; BOT is allowed as delimiter, USER is excluded.
232 number-end flag213.
233:242 one-digit square.
242:278 two-digit square using -9*d1²+90*d2²+10*(d1+d2)².
278:359 three-digit square using
-109*d1²-910*d2²+8900*d3²+10*(d1+d2)²+100*(d1+d3)²+1000*(d2+d3)².
Each length group has its own digit-contiguity gate. Square splines have knots0..8 for a digit,0..17 for a sum.
M1 units359+ free.

L2 H0 latest USER ->204.
L2 H1 latest user echo token ->86.
L2 H2 latest USER-or-user-negation ->90, so a new USER resets old negation.
L2 H3 latest parsed user number ->99,100,220.
L2 H4..7 unused.

M2 units0,1 current-number flag: clipped difference latest-number-position minus latest-USER-position, gated by presence.
Units2,3 same additionally gated by actual-operation flag ->102.
4 normal n gated NOT division ->215.
5 normal n² gated NOT division ->217.
6,7 base affine part of reciprocal, gated division.
36:228 unchanged square of USER position ->205.
228:292 reciprocal hinges ReLU(k-n), gated division. Knots1..50,60,70,80,90,100,125,150,175,200,250,300,400,500,750.
Base r(n)=1/750+1/999 - n/(750*999), plus changes of slope at these knots. r(0)=0, r(1)=1. Both215 and217 receive r: linear-interpolated square on [0,1] equals r.
M2 units8:36 and292+ free.

L3 segment matching (all except H4) uses 3-pair extrapolated near-rotation-invariant 2*pq*ps-ps²:
product pairs30,28,26 Q100; K[324.9945102,-135.271739,10.2772288].
square pairs24,22,20 Q100; K[-41599.2973056,17314.782592,-1315.4852864].
H0 intent key40 ->76.
H1 subject key42 ->77,78,79,80,88.
H2 adjective key47 ->81,82,83.
H3 task key52 ->84.
H4 latest user personal-name key57 ->85,89; no segment restriction.
H5 first current-message number: key213 pair18/19=[1000,10000], values212,214,213 ->91,92,95.
H6 speaker key64 ->87.
H7 last current-message number: key213 pair18/19=[1000,-10000], values215,217,213,212 ->93,94,96,97.
Non-numeric heads use priority pair18/19=[100,-80].

M3 units0:37 original plan selector, now all suppressed by102*100000 during arithmetic.
0:4 choose task > emotion > subject > generic.
4:25 task/speaker/fact corrections:
task8+speaker1 =>16; task9+speaker1 =>44 (was18).
task10 no fact =>17; task10 two-word fact=>11.
task8 user with no remembered name=>17.
task7 fact=>10 or11.
25:37 negate happy/sad and good/bad emotion plans.
37 adds44*arithmetic-active to chosen template.
38,39 subtract A²/2 and transformed B square/2 into104.
40 creates sum103.
41 creates addition105.
42,43 create absolute difference106.
44:47 addition gate108,47:50 subtraction109,50:54 multiply/divide trapezoid110, all depend on operation and arithmetic-active.
54:854 square-sum hinges k0..799, output0.5 for k0 and1 otherwise ->104.
Remaining square-sum tail k800..1008 is deferred to M4.
M3 units854+ free.

L4 H0 freezes latest BOT's plan/payload; V channels0..17 ->160..173,175..178 as listed. Other L4 heads unused.
M4 decoder coordinate c=64*template + position - BOT_position.
0 outputs code1/bias1.
1:488 old fixed templates; details below.
488:498 numeric template44: prefix “the answer is”, then baseline EOS. Same ten knots also yield phases0..4 at output offsets3..7.
498 remembered-number result when arithmetic inactive.
499 gated addition,500 gated subtraction.
501,502 signed partial product when multiply/divide.
503:712 tail ReLU(A+B′-k), k800..1008, gated multiply/divide.
All selected numeric contributions sum into174.
M4 units712+ free.

M5 units0:5 old dynamic word payload insertion.
5 copies numeric result into remainder194.
6:204 paired clipped steps at100,200,...9900, rounding around integer boundaries. Outputs hundreds digit193 and remainder194; every tenth threshold additionally gives thousands192 and subtracts10 from193.
204:234 phase-conditioned magnitude thresholds10,100,1000. Outputs decimal-place gates196:200 and corrections to180 that replace baseline EOS with digit placeholders or period.
234,235 phase baseline terms.
Numeric output is unpadded, length1..4 digits, then period then EOS.
M5 units236+ free.

M6 units0,1 insert thousands/hundreds code136+digit gated by196/197.
2 tens baseline136;3 ones baseline136+remainder.
4:22 gated tens thresholds10..90.
22:40 gated ones corrections -10 at same thresholds.
M6 units40+ free.

OUTPUT
U uses180/181, nearest-code logits2*c*z-c². Unregistered tokens have -1000000 bias.
Do not write initial embeddings into180/181.
No leading zeros in new numeric output.
All fixed templates and numeric replies terminate with EOS.

OLD TEMPLATE IDS / M4 RANGES / CODE SEQUENCES
0 1:17 [2,3,61,33,10,8,64,65,11,46,33,66,67,12]
1 17:28 [13,14,15,9,2,10,11,16,12]
2 28:37 [17,14,18,4,19,20,8]
3 37:43 [11,21,22,14]
4 43:56 [27,28,29,30,8,31,32,33,34,26,8]
5 56:69 [2,3,25,24,23,11,8,15,21,11,12]
6 69:89 [2,3,4,5,6,7,8,2,9,6,24,48,49,37,50,42,51,8]
7 89:99 [35,36,37,38,39,40,41,8]
8 99:115 [2,42,43,18,4,44,8,2,3,4,5,6,7,8]
9 115:127 [2,42,43,18,374,45,46,4,47,8]
10 127:134 [52,48,28,0,8], fact1 slot130:133
11 134:142 [52,48,28,0,0,8], fact1 137:140,fact2 138:141
12 142:149 [52,55,28,0,8], opposite145:148
13 149:156 [52,343,28,0,8], echo152:155
14,15 not implemented.
16 156:163 [56,44,28,0,8], name159:162
17 163:177 [2,42,43,81,8,2,9,83,82,33,10,8]
18 177:184 old unused age sequence, numeric payload NOT wired; no longer selected for personal age.
19 not implemented.
20 184:197 [68,9,34,75,8,64,68,42,11,46,12]
21 197:214 [25,69,9,113,4,20,79,8,64,42,11,46,33,108,12]
22 214:224 [2,77,52,70,28,19,16,8]
23 224:239 [2,77,71,28,25,16,8,57,103,110,33,58,8]
24 239:257 [72,9,10,11,97,98,99,37,8,64,42,11,46,33,97,12]
25 257:271 [73,9,34,375,8,2,77,56,73,28,59,8]
26 271:287 [4,74,9,34,4,25,93,8,42,11,18,4,74,12]
27 287:298 [377,9,34,75,50,25,376,11,8]
28 absent.
29 298:308 [2,46,33,6,50,10,378,8]
30 308:325 [2,3,61,33,62,63,14,2,77,11,18,4,95,20,8]
31 325:340 [2,3,26,11,60,90,8,2,3,379,33,100,8]
32 340:353 [2,3,26,11,60,91,8,57,58,59,8]
33 353:369 [2,3,26,11,60,380,8,57,103,110,33,60,308,8] (quiet fixed)
34 369:387 [2,3,26,11,60,381,8,57,58,50,105,4,107,376,10,8]
35 387:404 [2,3,26,11,60,382,8,57,66,111,4,47,11,383,8]
36 absent.
37 404:417 [63,28,25,14,15,9,2,10,11,16,12]
38 417:431 [2,3,26,33,62,63,8,15,9,2,10,12]
39 431:438 [84,24,27,28,8] yes
40 438:446 [31,24,27,28,43,8] no
41 446:458 [128,116,37,21,117,24,118,50,119,8]
42 458:473 [128,384,37,21,4,120,24,4,121,50,4,122,8]
43 473:488 [128,385,37,21,374,123,24,374,124,50,4,386,8]
44 488:498 numeric prefix plus phase gates as described.

OUTPUT WORD CODES
1 EOS,2 i,3 am,4 a,5 small,6 chat,7 bot,8 .,9 can,10 help,11 you,12 ?,13 hello,14 !,15 how,16 today,17 goodbye,18 have,19 nice,20 day,21 are,22 welcome,23 thank,24 comma,25 good,26 sorry,27 it,28 is,29 all,30 right,31 no,32 need,33 to,34 be,35 my,36 weight,37 -s,38 were,39 written,40 by,41 hand,42 do,43 not,44 name,45 age,46 like,47 person,48 answer,49 question,50 and,51 maths,52 the,53 capital,54 of,55 opposite,56 your,57 please,58 rest,59 well,60 feel,61 happy,62 hear,63 that,64 what,65 would,66 talk,67 about,68 music,69 food,70 weather,71 work,72 school,73 family,74 pet,75 fun,76 enjoy,77 hope,78 get,79 better,80 soon,81 know,82 try,83 still,84 yes,85 cold,86 hot,87 big,88 alive,89 dead,90 sad,91 tired,92 UNUSED,93 friend,94 safe,95 great,96 love,97 learn,98 new,99 thing,100 listen,101 water,102 sleep,103 take,104 break,105 ask,106 teacher,107 doctor,108 eat,109 healthy,110 time,111 with,112 they,113 make,114 world,115 special,116 colour,117 red,118 green,119 blue,120 cat,121 dog,122 bird,123 apple,124 orange,125 rice,126 one,127 two,128 three,129 four,130 five,131 six,132 seven,133 eight,134 nine,135 ten,136..145 digits0..9.
146 paris,147 london,148 rome,149 berlin,150 madrid,151 tokyo,152 beijing,153 ottawa,154 washington,155 delhi,156 canberra,157 brasilia,158 moscow,159 seoul,160 cairo,161 athens,162 lisbon,163 dublin,164 oslo,165 stockholm,166 helsinki,167 copenhagen,168 bern,169 amsterdam,170 vienna,171 warsaw,172 kyiv,173 ankara,174 bangkok,175 hanoi,176 jakarta,177 islamabad,178 tehran,179 baghdad,180 jerusalem,181 riyadh,182 doha,183 nairobi,184 pretoria,185 wellington,186 lima,187 santiago,188 havana,189 caracas,190 montevideo.
191 sam,192 altman,193 elon,194 musk,195 satya,196 nadella,197 sundar,198 pichai,199 jensen,200 huang,201 mark,202 zuckerberg,203 tim,204 cook,205 dario,206 amodei,207 demis,208 hassabis,209 bill,210 gates,211 steve,212 jobs,213 jeff,214 bezos,215 openai,216 microsoft,217 google,218 meta,219 spacex,220 tesla,221 nvidia,222 anthropic,223 claude,224 chatgpt,225 gemini,226 windows,227 android,228 iphone,229 earth,230 mars,231 jupiter,232 saturn,233 mercury,234 venus,235 neptune,236 uranus,237 sun,238 moon,239 pacific,240 asia,241 africa,242 europe,243 america,244 antarctica,245 oceania,246 everest,247 nile,248 amazon,249 sahara,250 einstein,251 newton,252 shakespeare,253 mozart,254 leonardo,255 vinci,256 darwin,257 edison,258 armstrong,259 gagarin,260 air,261 iron,262 gold,263 silver,264 salt,265 protein,266 heart,267 brain,268 blood,269 leaf,270 tree,271 fish,272 elephant,273 mouse,274 rabbit,275 bee,276 snow,277 ice,278 fire,279 light,280 dark,281 white,282 black,283 up,284 down,285 left,286 north,287 south,288 east,289 west,290 old,291 young,292 long,293 short,294 tall,295 full,296 dry,297 wet,298 fast,299 slow,300 easy,301 difficult,302 clean,303 dirty,304 strong,305 soft,306 hard,307 loud,308 quiet,309 open,310 shut,311 true,312 false,313 beautiful,314 bad,315 poor,316 rich,317 night,318 morning,319 summer,320 winter,321 start,322 end,323 come,324 go,325 win,326 lose,327 give,328 warm,329 cool,330 high,331 low,332 male,333 female,334 man,335 woman,336 boy,337 girl,338 brother,339 sister,340 father,341 mother,342 spring,343 word.
344 tom,345 sara,346 anna,347 john,348 mary,349 james,350 emma,351 liam,352 olivia,353 noah,354 ava,355 mia,356 lucas,357 ella,358 jack,359 lily,360 ben,361 max,362 leo,363 zoe,364 amy,365 kate,366 mike,367 dan,368 alex,369 maria,370 david,371 paul,372 peter.
373 number,374 an,375 important,376 for,377 sport,378 people,379 here,380 angry,381 ill,382 afraid,383 trust,384 animal,385 fruit,386 berry,387 feeble.

LEXICAL COVERAGE / REMAINING WORK
Countries->capitals, companies->leaders, products->makers as in pass1. Personal names tom..peter. Emotional happy/sad/tired/angry/ill/afraid/good/bad. Opposite dictionary broad, but many words lack echo embeddings.
Arithmetic operations now:
add: plus/add/addition/sum/total/altogether/more/get/buy/added/received/brought
subtract: minus/subtract/subtraction/difference/fewer/give/gave/lose/lost/left/spent/eat/take
multiply: times/multiply/product/each
divide: divided/division/equally/share
CHECK BOOKKEEPING: “subtraction” is NOT clearly in vocabulary! If skipped, harmless; remove or replace. All other listed operations are vocabulary tokens.
“half”, “twice”, etc intentionally NOT operations yet: require unary operands.
Operator selector is latest operation, no priority, reset by USER. Non-numeric ordinary chat does not trigger arithmetic.

Recommended pass3:
1. Audit parsing/bookkeeping, numeric formulas, index ranges. No tests are possible.
2. Implement count-to-N up10; use historical99/current number and new task/template. Could generate fixed short count sequences; count has no embeddings yet.
3. Implement physical classifications big/small, hot/cold, alive/dead and yes/no with negation. Templates39/40 already available but selection missing.
4. Expand world facts and proper relation routing, echo vocabulary, likes memory. Existing generic facts are extremely simplistic: “planet” defaults Jupiter, “river” Nile, countries always capital. Need relation-based improvements.
5. Add unary half/double/twice if time.
6. Ensure “subtraction” skipped edit does not discard an entire operation-token list! If list assignment unknown token invalidates line, redo the list WITHOUT subtraction in pass3. This pass uses a separate single-token edit for subtraction so other subtraction triggers still apply.
7. Numeric M3 square budget can be traded with M4 tail: current split800/209 hinges. M3 has170 free units; M4 has312. L5/L6 attention unused.
=====END SCRATCHPAD=====

```edits
# Repair the unavailable word in the anger response.
M4_out[365:368, 180] += [216,-432,216]
U[[180,181], "special"] = [230,-13225]

# Move user-only lexical gating one layer earlier.
M2_in[:, 0:36] = 0
M2_b[0:36] = 0
M2_out[0:36, :] = 0
M1_in[202, 193:229] = 1000
M1_b[193:229] = -1000
M1_in[4, 193] = 1
M1_out[193, 40] = 1
M1_in[5, 194] = 1
M1_out[194, 41] = 1
M1_in[6, 195] = 1
M1_out[195, 42] = 1
M1_in[7, 196] = 1
M1_out[196, 43] = 1
M1_in[8, 197] = 1
M1_out[197, 44] = 1
M1_in[9, 198] = 1
M1_out[198, 45] = 1
M1_in[10, 199] = 1
M1_out[199, 46] = 1
M1_in[11, 200] = 1
M1_out[200, 47] = 1
M1_in[12, 201] = 1
M1_out[201, 48] = 1
M1_in[13, 202] = 1
M1_out[202, 49] = 1
M1_in[14, 203] = 1
M1_out[203, 50] = 1
M1_in[15, 204] = 1
M1_out[204, 51] = 1
M1_in[16, 205] = 1
M1_out[205, 52] = 1
M1_in[17, 206] = 1
M1_out[206, 53] = 1
M1_in[18, 207] = 1
M1_out[207, 54] = 1
M1_in[19, 208] = 1
M1_out[208, 55] = 1
M1_in[20, 209] = 1
M1_out[209, 56] = 1
M1_in[21, 210] = 1
M1_out[210, 57] = 1
M1_in[22, 211] = 1
M1_out[211, 58] = 1
M1_in[23, 212] = 1
M1_out[212, 59] = 1
M1_in[24, 213] = 1
M1_out[213, 60] = 1
M1_in[25, 214] = 1
M1_out[214, 61] = 1
M1_in[26, 215] = 1
M1_out[215, 62] = 1
M1_in[27, 216] = 1
M1_out[216, 63] = 1
M1_in[28, 217] = 1
M1_out[217, 64] = 1
M1_in[29, 218] = 1
M1_out[218, 65] = 1
M1_in[30, 219] = 1
M1_out[219, 66] = 1
M1_in[31, 220] = 1
M1_out[220, 67] = 1
M1_in[32, 221] = 1
M1_out[221, 68] = 1
M1_in[33, 222] = 1
M1_out[222, 69] = 1
M1_in[34, 223] = 1
M1_out[223, 70] = 1
M1_in[35, 224] = 1
M1_out[224, 71] = 1
M1_in[36, 225] = 1
M1_out[225, 72] = 1
M1_in[37, 226] = 1
M1_out[226, 73] = 1
M1_in[38, 227] = 1
M1_out[227, 74] = 1
M1_in[39, 228] = 1
M1_out[228, 75] = 1

# Fixed-offset digit readers.
Q1[2:5, 0, 0] = 100
Q1[2:5, 0, 8] = 100
Q1[2:5, 0, 16] = 100
K1[2, 0, 0:2] = [54.030230587,84.147098481]
K1[2, 0, 8:10] = [99.500416528,9.983341665]
K1[2, 0, 16:18] = [99.995000042,0.999983333]
K1[3, 0, 0:2] = [-41.614683655,90.929742683]
K1[3, 0, 8:10] = [98.006657784,19.866933080]
K1[3, 0, 16:18] = [99.980000667,1.999866669]
K1[4, 0, 0:2] = [-98.999249660,14.112000806]
K1[4, 0, 8:10] = [95.533648913,29.552020666]
K1[4, 0, 16:18] = [99.955003375,2.999550020]
V1[2:5, 18, 0] = 1
V1[2:5, 19, 1] = 1
O1[2, 0, 206] = 1
O1[2, 1, 207] = 1
O1[3, 0, 208] = 1
O1[3, 1, 209] = 1
O1[4, 0, 210] = 1
O1[4, 1, 211] = 1

# Parse a number at its following nondigit, including a BOT delimiter.
M1_in[206, 229:232] = 1000
M1_in[18, 229:232] = -1000
M1_in[202, 229:232] = 1000
M1_in[3, 229:232] = 1000
M1_in[2, 229:232] = -1000
M1_in[207, 229] = 1
M1_in[209, 230] = 10
M1_in[211, 231] = 100
M1_in[208, 230:232] = 1000
M1_in[210, 231] = 1000
M1_b[229:232] = [-2000,-3000,-4000]
M1_out[229:232, 212] = 1
M1_in[206, 232] = 1
M1_in[18, 232] = -1
M1_in[202, 232] = 1
M1_in[3, 232] = 1
M1_in[2, 232] = -1
M1_b[232] = -1
M1_out[232, 213] = 1

# Exact parsed-number squares from digit squares and pair sums.
M1_in[206, 233:359] = 1000
M1_in[18, 233:359] = -1000
M1_in[202, 233:359] = 1000
M1_in[3, 233:359] = 1000
M1_in[2, 233:359] = -1000
M1_in[208, 233:242] = -1000
M1_in[208, 242:359] = 1000
M1_in[210, 242:278] = -1000
M1_in[210, 278:359] = 1000
M1_in[207, 233:251] = 1
M1_in[209, 251:260] = 1
M1_in[207, 260:287] = 1
M1_in[209, 260:278] = 1
M1_in[209, 287:296] = 1
M1_in[211, 296:305] = 1
M1_in[207, 305:341] = 1
M1_in[209, 305:323] = 1
M1_in[211, 323:359] = 1
M1_in[209, 341:359] = 1
M1_b[233:242] = [-2000,-2001,-2002,-2003,-2004,-2005,-2006,-2007,-2008]
M1_b[242:251] = [-3000,-3001,-3002,-3003,-3004,-3005,-3006,-3007,-3008]
M1_b[251:260] = [-3000,-3001,-3002,-3003,-3004,-3005,-3006,-3007,-3008]
M1_b[260:278] = [-3000,-3001,-3002,-3003,-3004,-3005,-3006,-3007,-3008,-3009,-3010,-3011,-3012,-3013,-3014,-3015,-3016,-3017]
M1_b[278:287] = [-4000,-4001,-4002,-4003,-4004,-4005,-4006,-4007,-4008]
M1_b[287:296] = [-4000,-4001,-4002,-4003,-4004,-4005,-4006,-4007,-4008]
M1_b[296:305] = [-4000,-4001,-4002,-4003,-4004,-4005,-4006,-4007,-4008]
M1_b[305:323] = [-4000,-4001,-4002,-4003,-4004,-4005,-4006,-4007,-4008,-4009,-4010,-4011,-4012,-4013,-4014,-4015,-4016,-4017]
M1_b[323:341] = [-4000,-4001,-4002,-4003,-4004,-4005,-4006,-4007,-4008,-4009,-4010,-4011,-4012,-4013,-4014,-4015,-4016,-4017]
M1_b[341:359] = [-4000,-4001,-4002,-4003,-4004,-4005,-4006,-4007,-4008,-4009,-4010,-4011,-4012,-4013,-4014,-4015,-4016,-4017]
M1_out[233:242, 214] = [1,2,2,2,2,2,2,2,2]
M1_out[242:251, 214] = [-9,-18,-18,-18,-18,-18,-18,-18,-18]
M1_out[251:260, 214] = [90,180,180,180,180,180,180,180,180]
M1_out[260:278, 214] = [10,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20]
M1_out[278:287, 214] = [-109,-218,-218,-218,-218,-218,-218,-218,-218]
M1_out[287:296, 214] = [-910,-1820,-1820,-1820,-1820,-1820,-1820,-1820,-1820]
M1_out[296:305, 214] = [8900,17800,17800,17800,17800,17800,17800,17800,17800]
M1_out[305:323, 214] = [10,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20]
M1_out[323:341, 214] = [100,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200,200]
M1_out[341:359, 214] = [1000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000,2000]

# Arithmetic vocabulary and a causal operation selector.
E["USER", 23] = 1
E[["plus","add","addition","sum","total","altogether","more","get","buy","added","received","brought"], 23:26] = [1,1,0]
E[["plus","add","addition","sum","total","altogether","more","get","buy","added","received","brought"], 30] = 1
E[["minus","subtract","difference","fewer","give","gave","lose","lost","left","spent","eat","take"], 23:26] = [1,2,0]
E[["minus","subtract","difference","fewer","give","gave","lose","lost","left","spent","eat","take"], 30] = 1
E[["times","multiply","product","each"], 23:26] = [1,3,0]
E[["times","multiply","product","each"], 30] = 1
E[["divided","division","equally","share"], 23:26] = [1,4,1]
E[["divided","division","equally","share"], 30] = 1
E["number", 16:18] = [10,44]
Q1[5, 0, 30] = 100
K1[5, 23, 30:32] = [1000,-10000]
V1[5, 25, 0] = 1
V1[5, 24, 1] = 1
V1[5, 30, 2] = 1
O1[5, 0, 216] = 1
O1[5, 1, 218] = 1
O1[5, 2, 219] = 1

# Move echo and negation retrieval to layer two.
Q2[1, 0, 30] = 100
K2[1, 62, 30:32] = [1000,-10000]
V2[1, 56, 0] = 1
O2[1, 0, 86] = 1
Q2[2, 0, 30] = 100
K2[2, 2, 30:32] = [1000,-10000]
K2[2, 51, 30:32] = [1000,-10000]
V2[2, 51, 0] = 1
O2[2, 0, 90] = 1

# Last user number, also usable across exchanges.
Q2[3, 0, 30] = 100
K2[3, 213, 30:32] = [1000,-10000]
V2[3, 212, 0] = 1
V2[3, 213, 1] = 1
V2[3, 201, 2] = 1
O2[3, 0, 99] = 1
O2[3, 1, 100] = 1
O2[3, 2, 220] = 1
M2_in[220, 0:4] = 1
M2_in[204, 0:4] = -1
M2_in[100, 0:4] = 1000
M2_in[219, 2:4] = 1000
M2_b[0:4] = [-1000,-1001,-2000,-2001]
M2_out[0:2, 101] = [1,-1]
M2_out[2:4, 102] = [1,-1]

# Normal operands and division operands.
M2_in[212, 4] = 1
M2_in[216, 4] = -1000
M2_out[4, 215] = 1
M2_in[214, 5] = 1
M2_in[216, 5] = -1000000
M2_out[5, 217] = 1
M2_in[216, 6] = 1
M2_out[6, 215] = 0.002334334334334
M2_out[6, 217] = 0.002334334334334
M2_in[212, 7] = 1
M2_in[216, 7] = 1000
M2_b[7] = -1000
M2_out[7, 215] = -0.000001334668001
M2_out[7, 217] = -0.000001334668001
M2_in[212, 228:292] = -1
M2_in[216, 228:292] = 1000
M2_b[228:292] = [
-999,-998,-997,-996,-995,-994,-993,-992,-991,-990,
-989,-988,-987,-986,-985,-984,-983,-982,-981,-980,
-979,-978,-977,-976,-975,-974,-973,-972,-971,-970,
-969,-968,-967,-966,-965,-964,-963,-962,-961,-960,
-959,-958,-957,-956,-955,-954,-953,-952,-951,-950,
-940,-930,-920,-910,-900,-875,-850,-825,-800,-750,-700,-600,-500,-250]
M2_out[228:292, 215] = [
-1.5,0.333333333333,0.083333333333,0.033333333333,0.016666666667,
0.009523809524,0.005952380952,0.003968253968,0.002777777778,0.002020202020,
0.001515151515,0.001165501166,0.000915750916,0.000732600733,0.000595238095,
0.000490196078,0.000408496732,0.000343997248,0.000292397661,0.000250626566,
0.000216450216,0.000188217580,0.000164690382,0.000144927536,0.000128205128,
0.000113960114,0.000101750102,0.000091224229,0.000082101806,0.000074156470,
0.000067204301,0.000061094819,0.000055704100,0.000050929463,0.000046685341,
0.000042900043,0.000039513197,0.000036473720,0.000033738192,0.000031269543,
0.000029036005,0.000027010777,0.000025168637,0.000023490721,0.000021958718,
0.000020557097,0.000019272280,0.000018092342,0.000017006803,0.000074829932,
0.000095238095,0.000059523810,0.000039682540,0.000027777778,0.000031111111,
0.000026666667,0.000015238095,0.000009523810,0.000008571429,0.000006666667,
0.000005000000,0.000003333333,0.000002333333,0.000001331998666]
M2_out[228:292, 217] = [
-1.5,0.333333333333,0.083333333333,0.033333333333,0.016666666667,
0.009523809524,0.005952380952,0.003968253968,0.002777777778,0.002020202020,
0.001515151515,0.001165501166,0.000915750916,0.000732600733,0.000595238095,
0.000490196078,0.000408496732,0.000343997248,0.000292397661,0.000250626566,
0.000216450216,0.000188217580,0.000164690382,0.000144927536,0.000128205128,
0.000113960114,0.000101750102,0.000091224229,0.000082101806,0.000074156470,
0.000067204301,0.000061094819,0.000055704100,0.000050929463,0.000046685341,
0.000042900043,0.000039513197,0.000036473720,0.000033738192,0.000031269543,
0.000029036005,0.000027010777,0.000025168637,0.000023490721,0.000021958718,
0.000020557097,0.000019272280,0.000018092342,0.000017006803,0.000074829932,
0.000095238095,0.000059523810,0.000039682540,0.000027777778,0.000031111111,
0.000026666667,0.000015238095,0.000009523810,0.000008571429,0.000006666667,
0.000005000000,0.000003333333,0.000002333333,0.000001331998666]

# First and last numbers within the current USER segment.
K3[5, 62, 18:20] = 0
K3[7, 51, 18:20] = 0
V3[5, :, :] = 0
O3[5, :, :] = 0
V3[7, :, :] = 0
O3[7, :, :] = 0
K3[5, 213, 18:20] = [1000,10000]
K3[7, 213, 18:20] = [1000,-10000]
V3[5, 212, 0] = 1
V3[5, 214, 1] = 1
V3[5, 213, 2] = 1
O3[5, 0, 91] = 1
O3[5, 1, 92] = 1
O3[5, 2, 95] = 1
V3[7, 215, 0] = 1
V3[7, 217, 1] = 1
V3[7, 213, 2] = 1
V3[7, 212, 3] = 1
O3[7, 0, 93] = 1
O3[7, 1, 94] = 1
O3[7, 2, 96] = 1
O3[7, 3, 97] = 1

# Numeric plan selection and arithmetic.
M3_in[102, 0:37] = -100000
M3_in[102, 37] = 44
M3_out[37, 141] = 1
M3_out[7:10, 141] = [35,-70,35]
M3_in[92, 38] = 1
M3_in[94, 39] = 1
M3_out[38:40, 104] = -0.5
M3_in[91, 40:43] = 1
M3_in[93, 40] = 1
M3_out[40, 103] = 1
M3_in[97, 41] = 1
M3_out[41, 105] = 1
M3_in[97, 42] = -1
M3_in[91, 43] = -1
M3_in[97, 43] = 1
M3_out[42:44, 106] = 1
M3_in[218, 44:54] = 1
M3_in[102, 44:54] = 8
M3_b[44:54] = [-8,-9,-10,-9,-10,-11,-10,-11,-12,-13]
M3_out[44:47, 108] = [1,-2,1]
M3_out[47:50, 109] = [1,-2,1]
M3_out[50:54, 110] = [1,-1,-1,1]
M3_in[91, 54:854] = 1
M3_in[93, 54:854] = 1
M3_out[54, 104] = 0.5
M3_out[55:854, 104] = 1
M3_b[54:854] = [
0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,
-20,-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,
-40,-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,
-60,-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-76,-77,-78,-79,
-80,-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,-96,-97,-98,-99,
-100,-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,-112,-113,-114,-115,-116,-117,-118,-119,
-120,-121,-122,-123,-124,-125,-126,-127,-128,-129,-130,-131,-132,-133,-134,-135,-136,-137,-138,-139,
-140,-141,-142,-143,-144,-145,-146,-147,-148,-149,-150,-151,-152,-153,-154,-155,-156,-157,-158,-159,
-160,-161,-162,-163,-164,-165,-166,-167,-168,-169,-170,-171,-172,-173,-174,-175,-176,-177,-178,-179,
-180,-181,-182,-183,-184,-185,-186,-187,-188,-189,-190,-191,-192,-193,-194,-195,-196,-197,-198,-199,
-200,-201,-202,-203,-204,-205,-206,-207,-208,-209,-210,-211,-212,-213,-214,-215,-216,-217,-218,-219,
-220,-221,-222,-223,-224,-225,-226,-227,-228,-229,-230,-231,-232,-233,-234,-235,-236,-237,-238,-239,
-240,-241,-242,-243,-244,-245,-246,-247,-248,-249,-250,-251,-252,-253,-254,-255,-256,-257,-258,-259,
-260,-261,-262,-263,-264,-265,-266,-267,-268,-269,-270,-271,-272,-273,-274,-275,-276,-277,-278,-279,
-280,-281,-282,-283,-284,-285,-286,-287,-288,-289,-290,-291,-292,-293,-294,-295,-296,-297,-298,-299,
-300,-301,-302,-303,-304,-305,-306,-307,-308,-309,-310,-311,-312,-313,-314,-315,-316,-317,-318,-319,
-320,-321,-322,-323,-324,-325,-326,-327,-328,-329,-330,-331,-332,-333,-334,-335,-336,-337,-338,-339,
-340,-341,-342,-343,-344,-345,-346,-347,-348,-349,-350,-351,-352,-353,-354,-355,-356,-357,-358,-359,
-360,-361,-362,-363,-364,-365,-366,-367,-368,-369,-370,-371,-372,-373,-374,-375,-376,-377,-378,-379,
-380,-381,-382,-383,-384,-385,-386,-387,-388,-389,-390,-391,-392,-393,-394,-395,-396,-397,-398,-399,
-400,-401,-402,-403,-404,-405,-406,-407,-408,-409,-410,-411,-412,-413,-414,-415,-416,-417,-418,-419,
-420,-421,-422,-423,-424,-425,-426,-427,-428,-429,-430,-431,-432,-433,-434,-435,-436,-437,-438,-439,
-440,-441,-442,-443,-444,-445,-446,-447,-448,-449,-450,-451,-452,-453,-454,-455,-456,-457,-458,-459,
-460,-461,-462,-463,-464,-465,-466,-467,-468,-469,-470,-471,-472,-473,-474,-475,-476,-477,-478,-479,
-480,-481,-482,-483,-484,-485,-486,-487,-488,-489,-490,-491,-492,-493,-494,-495,-496,-497,-498,-499,
-500,-501,-502,-503,-504,-505,-506,-507,-508,-509,-510,-511,-512,-513,-514,-515,-516,-517,-518,-519,
-520,-521,-522,-523,-524,-525,-526,-527,-528,-529,-530,-531,-532,-533,-534,-535,-536,-537,-538,-539,
-540,-541,-542,-543,-544,-545,-546,-547,-548,-549,-550,-551,-552,-553,-554,-555,-556,-557,-558,-559,
-560,-561,-562,-563,-564,-565,-566,-567,-568,-569,-570,-571,-572,-573,-574,-575,-576,-577,-578,-579,
-580,-581,-582,-583,-584,-585,-586,-587,-588,-589,-590,-591,-592,-593,-594,-595,-596,-597,-598,-599,
-600,-601,-602,-603,-604,-605,-606,-607,-608,-609,-610,-611,-612,-613,-614,-615,-616,-617,-618,-619,
-620,-621,-622,-623,-624,-625,-626,-627,-628,-629,-630,-631,-632,-633,-634,-635,-636,-637,-638,-639,
-640,-641,-642,-643,-644,-645,-646,-647,-648,-649,-650,-651,-652,-653,-654,-655,-656,-657,-658,-659,
-660,-661,-662,-663,-664,-665,-666,-667,-668,-669,-670,-671,-672,-673,-674,-675,-676,-677,-678,-679,
-680,-681,-682,-683,-684,-685,-686,-687,-688,-689,-690,-691,-692,-693,-694,-695,-696,-697,-698,-699,
-700,-701,-702,-703,-704,-705,-706,-707,-708,-709,-710,-711,-712,-713,-714,-715,-716,-717,-718,-719,
-720,-721,-722,-723,-724,-725,-726,-727,-728,-729,-730,-731,-732,-733,-734,-735,-736,-737,-738,-739,
-740,-741,-742,-743,-744,-745,-746,-747,-748,-749,-750,-751,-752,-753,-754,-755,-756,-757,-758,-759,
-760,-761,-762,-763,-764,-765,-766,-767,-768,-769,-770,-771,-772,-773,-774,-775,-776,-777,-778,-779,
-780,-781,-782,-783,-784,-785,-786,-787,-788,-789,-790,-791,-792,-793,-794,-795,-796,-797,-798,-799]

# Freeze numerical operands and gates with the response plan.
V4[0, 218, 7] = 1
V4[0, 102, 8] = 1
V4[0, 103, 9] = 1
V4[0, 104, 10] = 1
V4[0, 105, 11] = 1
V4[0, 106, 12] = 1
V4[0, 99, 13] = 1
V4[0, 101, 14] = 1
V4[0, 108, 15] = 1
V4[0, 109, 16] = 1
V4[0, 110, 17] = 1
O4[0, 7, 167] = 1
O4[0, 8, 168] = 1
O4[0, 9, 169] = 1
O4[0, 10, 170] = 1
O4[0, 11, 171] = 1
O4[0, 12, 172] = 1
O4[0, 13, 173] = 1
O4[0, 14, 175] = 1
O4[0, 15, 176] = 1
O4[0, 16, 177] = 1
O4[0, 17, 178] = 1

# Template44: prefix and five possible suffix phases.
M4_in[160, 488:498] = 64
M4_in[201, 488:498] = 1
M4_in[163, 488:498] = -1
M4_b[488:498] = [-2815,-2816,-2817,-2818,-2819,-2820,-2821,-2822,-2823,-2824]
M4_out[488:498, 180] = [51,-55,-16,-7,27,0,0,0,0,0]
M4_out[491:494, 188] = [1,-2,1]
M4_out[492:495, 189] = [1,-2,1]
M4_out[493:496, 190] = [1,-2,1]
M4_out[494:497, 191] = [1,-2,1]
M4_out[495:498, 195] = [1,-2,1]

# Complete and select the numerical result.
M4_in[173, 498] = 1
M4_in[168, 498] = -10000
M4_in[171, 499] = 1
M4_in[176, 499] = 10000
M4_b[499] = -10000
M4_in[172, 500] = 1
M4_in[177, 500] = 10000
M4_b[500] = -10000
M4_in[170, 501:503] = [1,-1]
M4_in[178, 501:503] = 1000000
M4_b[501:503] = -1000000
M4_out[498:502, 174] = 1
M4_out[502, 174] = -1
M4_in[169, 503:712] = 1
M4_in[178, 503:712] = 10000
M4_out[503:712, 174] = 1
M4_b[503:712] = [
-10800,-10801,-10802,-10803,-10804,-10805,-10806,-10807,-10808,-10809,
-10810,-10811,-10812,-10813,-10814,-10815,-10816,-10817,-10818,-10819,
-10820,-10821,-10822,-10823,-10824,-10825,-10826,-10827,-10828,-10829,
-10830,-10831,-10832,-10833,-10834,-10835,-10836,-10837,-10838,-10839,
-10840,-10841,-10842,-10843,-10844,-10845,-10846,-10847,-10848,-10849,
-10850,-10851,-10852,-10853,-10854,-10855,-10856,-10857,-10858,-10859,
-10860,-10861,-10862,-10863,-10864,-10865,-10866,-10867,-10868,-10869,
-10870,-10871,-10872,-10873,-10874,-10875,-10876,-10877,-10878,-10879,
-10880,-10881,-10882,-10883,-10884,-10885,-10886,-10887,-10888,-10889,
-10890,-10891,-10892,-10893,-10894,-10895,-10896,-10897,-10898,-10899,
-10900,-10901,-10902,-10903,-10904,-10905,-10906,-10907,-10908,-10909,
-10910,-10911,-10912,-10913,-10914,-10915,-10916,-10917,-10918,-10919,
-10920,-10921,-10922,-10923,-10924,-10925,-10926,-10927,-10928,-10929,
-10930,-10931,-10932,-10933,-10934,-10935,-10936,-10937,-10938,-10939,
-10940,-10941,-10942,-10943,-10944,-10945,-10946,-10947,-10948,-10949,
-10950,-10951,-10952,-10953,-10954,-10955,-10956,-10957,-10958,-10959,
-10960,-10961,-10962,-10963,-10964,-10965,-10966,-10967,-10968,-10969,
-10970,-10971,-10972,-10973,-10974,-10975,-10976,-10977,-10978,-10979,
-10980,-10981,-10982,-10983,-10984,-10985,-10986,-10987,-10988,-10989,
-10990,-10991,-10992,-10993,-10994,-10995,-10996,-10997,-10998,-10999,
-11000,-11001,-11002,-11003,-11004,-11005,-11006,-11007,-11008]

# Decimal decomposition: thousands, hundreds, and remainder modulo100.
M5_in[174, 5] = 1
M5_out[5, 194] = 1
M5_in[174, 6:204] = 5
M5_b[6:204] = [
-497,-498,-997,-998,-1497,-1498,-1997,-1998,-2497,-2498,
-2997,-2998,-3497,-3498,-3997,-3998,-4497,-4498,-4997,-4998,
-5497,-5498,-5997,-5998,-6497,-6498,-6997,-6998,-7497,-7498,
-7997,-7998,-8497,-8498,-8997,-8998,-9497,-9498,-9997,-9998,
-10497,-10498,-10997,-10998,-11497,-11498,-11997,-11998,-12497,-12498,
-12997,-12998,-13497,-13498,-13997,-13998,-14497,-14498,-14997,-14998,
-15497,-15498,-15997,-15998,-16497,-16498,-16997,-16998,-17497,-17498,
-17997,-17998,-18497,-18498,-18997,-18998,-19497,-19498,-19997,-19998,
-20497,-20498,-20997,-20998,-21497,-21498,-21997,-21998,-22497,-22498,
-22997,-22998,-23497,-23498,-23997,-23998,-24497,-24498,-24997,-24998,
-25497,-25498,-25997,-25998,-26497,-26498,-26997,-26998,-27497,-27498,
-27997,-27998,-28497,-28498,-28997,-28998,-29497,-29498,-29997,-29998,
-30497,-30498,-30997,-30998,-31497,-31498,-31997,-31998,-32497,-32498,
-32997,-32998,-33497,-33498,-33997,-33998,-34497,-34498,-34997,-34998,
-35497,-35498,-35997,-35998,-36497,-36498,-36997,-36998,-37497,-37498,
-37997,-37998,-38497,-38498,-38997,-38998,-39497,-39498,-39997,-39998,
-40497,-40498,-40997,-40998,-41497,-41498,-41997,-41998,-42497,-42498,
-42997,-42998,-43497,-43498,-43997,-43998,-44497,-44498,-44997,-44998,
-45497,-45498,-45997,-45998,-46497,-46498,-46997,-46998,-47497,-47498,
-47997,-47998,-48497,-48498,-48997,-48998,-49497,-49498]
M5_out[6:204:2, 193] = 1
M5_out[7:204:2, 193] = -1
M5_out[6:204:2, 194] = -100
M5_out[7:204:2, 194] = 100
M5_out[24:185:20, 192] = 1
M5_out[25:186:20, 192] = -1
M5_out[24:185:20, 193] = -9
M5_out[25:186:20, 193] = 9

# Choose decimal places without leading zeros.
M5_in[174, 204:234] = 5
M5_in[188, 204:210] = 100000
M5_in[189, 210:216] = 100000
M5_in[190, 216:222] = 100000
M5_in[191, 222:228] = 100000
M5_in[195, 228:234] = 100000
M5_b[204:234] = [
-100047,-100048,-100497,-100498,-104997,-104998,
-100047,-100048,-100497,-100498,-104997,-104998,
-100047,-100048,-100497,-100498,-104997,-104998,
-100047,-100048,-100497,-100498,-104997,-104998,
-100047,-100048,-100497,-100498,-104997,-104998]
M5_out[204:206, 198] = [1,-1]
M5_out[204:206, 199] = [-1,1]
M5_out[206:208, 197] = [1,-1]
M5_out[206:208, 198] = [-1,1]
M5_out[208:210, 196] = [1,-1]
M5_out[208:210, 197] = [-1,1]
M5_out[210:212, 199] = [1,-1]
M5_out[210:212, 180] = [-8,8]
M5_out[212:214, 198] = [1,-1]
M5_out[212:214, 199] = [-1,1]
M5_out[214:216, 197] = [1,-1]
M5_out[214:216, 198] = [-1,1]
M5_out[216:218, 180] = [7,-7]
M5_out[218:220, 199] = [1,-1]
M5_out[218:220, 180] = [-8,8]
M5_out[220:222, 198] = [1,-1]
M5_out[220:222, 199] = [-1,1]
M5_out[224:226, 180] = [7,-7]
M5_out[226:228, 199] = [1,-1]
M5_out[226:228, 180] = [-8,8]
M5_out[232:234, 180] = [7,-7]
M5_in[188, 234] = 1
M5_out[234, 199] = 1
M5_out[234, 180] = -1
M5_in[189, 235] = 1
M5_out[235, 180] = 7

# Emit the selected decimal digit.
M6_in[192, 0] = 1
M6_in[196, 0] = 1000
M6_in[193, 1] = 1
M6_in[197, 1] = 1000
M6_in[198, 2] = 1000
M6_in[194, 3] = 1
M6_in[199, 3] = 1000
M6_b[0:4] = -864
M6_out[0:4, 180] = 1
M6_in[194, 4:40] = 5
M6_in[198, 4:22] = 1000
M6_in[199, 22:40] = 1000
M6_b[4:22] = [-1047,-1048,-1097,-1098,-1147,-1148,-1197,-1198,-1247,-1248,-1297,-1298,-1347,-1348,-1397,-1398,-1447,-1448]
M6_b[22:40] = [-1047,-1048,-1097,-1098,-1147,-1148,-1197,-1198,-1247,-1248,-1297,-1298,-1347,-1348,-1397,-1398,-1447,-1448]
M6_out[4:22:2, 180] = 1
M6_out[5:22:2, 180] = -1
M6_out[22:40:2, 180] = -10
M6_out[23:40:2, 180] = 10
```