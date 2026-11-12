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