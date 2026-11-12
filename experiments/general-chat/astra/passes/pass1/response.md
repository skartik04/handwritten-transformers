=====SCRATCHPAD=====
PASS 1 DESIGN AND STATUS

This is a hand-built symbolic transformer, not a trained model. Pass 1 establishes position recovery, user-message segmentation, lexical retrieval, response selection, fixed-sentence decoding, dynamic word slots, capitals, company leaders/products, simple conversation, name memory, and opposites. Arithmetic/counting/general classification still need implementation. No execution or tools have been used.

All indices below are residual dimensions unless otherwise stated.

RESIDUAL MAP
0 constant 1 on every vocabulary token.
1 BOS flag, 2 USER flag, 3 BOT flag.
Raw lexical fields 4..39:
4 intent priority, 5 intent/template code.
6 subject priority, 7 subject/default template, 8 fact answer word code, 9 second answer word code, 10 fact-present flag.
11 adjective priority, 12 adjective/emotion template, 13 opposite word code, 14 adjective class (reserved).
15 negation flag.
16 task priority, 17 task/template code.
18 digit flag, 19 digit value, 20 echo/output word code.
21 personal-name flag, 22 personal-name word code.
23..25 reserved.
26 echo priority.
27 speaker code (1 user, 2 bot), 28 speaker priority.
29 two-word-fact flag.
30..39 reserved.
40..75 are user-only copies of raw fields 4..39 (offset +36), made by M2 using the latest USER/BOT role.
L3 summaries:
76 intent code; 77 subject template; 78 fact word1; 79 fact word2; 80 fact-present.
81 emotion template; 82 opposite word; 83 adjective class.
84 task code; 85 remembered personal name; 86 echo word; 87 speaker code.
88 fact-two-word flag; 89 remembered-name-present; 90 negation-present.
91..140 free.
141 chosen template.
142..159 free.
160 frozen template; 161 frozen fact word1; 162 frozen fact word2; 163 latest BOT absolute position.
164 frozen opposite word; 165 frozen remembered name; 166 frozen echo word.
167..179 free.
180 output word-code scalar; 181 output bias=1.
182 fact-word1 slot; 183 fact-word2 slot; 184 opposite slot; 185 name slot; 186 echo slot; 187 number slot reserved.
188..199 free.
200 reciprocal position 1/(t+1); 201 absolute position t+1.
202 user role: 1 in USER span, 0 in BOT span.
203 free (could hold position squared if needed).
204 latest USER absolute position; 205 its square /256.
206..255 free.

ATTENTION / MLP DESIGN
L1 H0 uniform attention, V BOS flag, yields reciprocal position at 200.
M1 units 0..192 invert reciprocal position exactly at integer positions, approximately due to decimal knot rounding:
p = 385 -37056*u + sum(n=2..192) 2*n*ReLU(u-1/n).
Unit0 constant385, unit1 linear u, unit n has knot 1/n for n=2..192.
L1 H1 selects latest USER/BOT using slow RoPE pair 30/31:
Q constant30=100, K marker30=1000, marker31=-10000.
V USER flag ->202. This makes a very sharp last-role selector.
Other L1 heads, M1 units193..1023 free.

L2 H0 similarly selects latest USER and copies 201->204.
M2 units0..35 gate raw features into 40..75:
ReLU(raw +1000*role-1000).
M2 units36..226 compute 2/256*ReLU(segment_position-k), k=1..191;
unit227 adds segment_position/256. Together give segment_position²/256 at205.
Other L2 heads and M2 units228..1023 free.

L3 heads except H4 use approximate rotation-invariant segment matching:
score proportional to 2*p_query*p_source - p_source².
Products use three slow RoPE pairs with extrapolation coefficients
[1.624972551, -0.676358695, .051386144].
p product on head dims30,28,26; square term on24,22,20.
Q p coefficients100, K p coefficients[324.9945102,-135.271739,10.2772288].
Q constant on24,22,20=100; K segment-square coefficients[-41599.2973056,17314.782592,-1315.4852864].
Keyword priority is on head dims18/19: Q constant18=100, K priority18=100 and19=-80. This also gives substantial recency preference. Priority features are user-gated.
H0 intent: key40, value41 ->76.
H1 subject: key42, values43,44,45,46,65 ->77,78,79,80,88.
H2 adjective: key47, values48,49,50 ->81,82,83.
H3 task: key52, value53 ->84.
H4 OVERRIDES segment attention and instead selects latest user personal-name flag57 with latest-marker attention. Values58,57 ->85,89.
H5 echo: key62, value56 ->86.
H6 speaker: key64, value63 ->87.
H7 negation: key51, value51 ->90.

M3 units0..3 choose task > emotion > subject > generic intent, using gated scalar ReLUs.
M3 units4..24 add triangular lookup corrections:
task8+speaker1 => template16 (remember name).
task9+speaker1 => template18 (age, NOT IMPLEMENTED payload).
task10 without fact =>17 (don't know).
task10 with fact-two flag =>11.
task8+speaker1 without remembered name =>17 instead of16.
task7 with fact-present =>10; with two-word fact =>11.
M3 units25..36 invert happy/sad and good/bad templates under not/un-, only if no task.
M3 units37 onward free.

L4 H0 freezes latest BOT's plan and payload:
141->160, 78->161,79->162,201->163,82->164,85->165,86->166.
Thus generations do not modify the selected reply.
M4 decoding coordinate x=64*template + position - BOT_position.
Unit0 supplies z=1 and bias181=1.
Units1..487 implement a global piecewise-linear spline: EOS code1 everywhere except each template's sequence. Each sequence has knots from 64*T-1 through64*T+L. Each token corresponds to x=64*T+j. One unit per spline knot; second differences are output coefficients.
All spline units read160*64 +201 -163.
Dynamic placeholders use code0 and simultaneously emit triangular slot gates at182..187.
M4 units488 onward free.
L5 attention unused. M5 units0..4 add word codes from frozen payload when corresponding slot gate=1, via ReLU(payload+1000*gate-1000).
M5 units5 onward free.
L6 entirely free.

OUTPUT
U only reads180 and181. Each registered word has code c and logits 2*c*z - c². Unregistered words get constant -1000000, so code0 defaults to EOS rather than BOS.
Do not accidentally add embeddings or outputs into180/181.
All templates end in EOS automatically when coordinate passes the sequence.

TEMPLATES / M4 UNIT RANGES / TOKEN CODE SEQUENCES (EOS excluded)
0 units1:17: [2,3,61,33,10,8,64,65,11,46,33,66,67,12]
1 17:28: [13,14,15,9,2,10,11,16,12]
2 28:37: [17,14,18,4,19,20,8]
3 37:43: [11,21,22,14]
4 43:56: [27,28,29,30,8,31,32,33,34,26,8]
5 56:69: [2,3,25,24,23,11,8,15,21,11,12]
6 69:89: [2,3,4,5,6,7,8,2,9,6,24,48,49,37,50,42,51,8]
7 89:99: [35,36,37,38,39,40,41,8]
8 99:115: [2,42,43,18,4,44,8,2,3,4,5,6,7,8]
9 115:127: [2,42,43,18,374,45,46,4,47,8]
10 127:134: [52,48,28,0,8], fact1 slot units130:133 ->182.
11 134:142: [52,48,28,0,0,8], fact1 units137:140 ->182, fact2 units138:141 ->183.
12 142:149: [52,55,28,0,8], opposite units145:148 ->184.
13 149:156: [52,343,28,0,8], echo units152:155 ->186.
14,15 not implemented.
16 156:163: [56,44,28,0,8], name units159:162 ->185.
17 163:177: [2,42,43,81,8,2,9,83,82,33,10,8]
18 177:184: [56,45,28,0,8], number gate units180:183 ->187, PAYLOAD NOT IMPLEMENTED.
19 not implemented.
20 184:197: [68,9,34,75,8,64,68,42,11,46,12]
21 197:214: [25,69,9,113,4,20,79,8,64,42,11,46,33,108,12]
22 214:224: [2,77,52,70,28,19,16,8]
23 224:239: [2,77,71,28,25,16,8,57,103,110,33,58,8]
24 239:257: [72,9,10,11,97,98,99,37,8,64,42,11,46,33,97,12]
25 257:271: [73,9,34,375,8,2,77,56,73,28,59,8]
26 271:287: [4,74,9,34,4,25,93,8,42,11,18,4,74,12]
27 287:298: [377,9,34,75,50,25,376,11,8]
28 not implemented.
29 298:308: [2,46,33,6,50,10,378,8]
30 308:325: [2,3,61,33,62,63,14,2,77,11,18,4,95,20,8]
31 325:340: [2,3,26,11,60,90,8,2,3,379,33,100,8]
32 340:353: [2,3,26,11,60,91,8,57,58,59,8]
33 353:369: [2,3,26,11,60,380,8,57,103,110,33,60,92,8]
34 369:387: [2,3,26,11,60,381,8,57,58,50,105,4,107,376,10,8]
35 387:404: [2,3,26,11,60,382,8,57,66,111,4,47,11,383,8]
36 not implemented.
37 404:417: [63,28,25,14,15,9,2,10,11,16,12]
38 417:431: [2,3,26,33,62,63,8,15,9,2,10,12]
39 431:438: [84,24,27,28,8]
40 438:446: [31,24,27,28,43,8]
41 446:458: [128,116,37,21,117,24,118,50,119,8]
42 458:473: [128,384,37,21,4,120,24,4,121,50,4,122,8]
43 473:488: [128,385,37,21,374,123,24,374,124,50,4,386,8]

OUTPUT CODE DICTIONARY
1 EOS,2 i,3 am,4 a,5 small,6 chat,7 bot,8 .,9 can,10 help,11 you,12 ?,13 hello,14 !,15 how,16 today,17 goodbye,18 have,19 nice,20 day,21 are,22 welcome,23 thank,24 comma,25 good,26 sorry,27 it,28 is,29 all,30 right,31 no,32 need,33 to,34 be,35 my,36 weight,37 -s,38 were,39 written,40 by,41 hand,42 do,43 not,44 name,45 age,46 like,47 person,48 answer,49 question,50 and,51 maths,52 the,53 capital,54 of,55 opposite,56 your,57 please,58 rest,59 well,60 feel,61 happy,62 hear,63 that,64 what,65 would,66 talk,67 about,68 music,69 food,70 weather,71 work,72 school,73 family,74 pet,75 fun,76 enjoy,77 hope,78 get,79 better,80 soon,81 know,82 try,83 still,84 yes,85 cold,86 hot,87 big,88 alive,89 dead,90 sad,91 tired,92 calm,93 friend,94 safe,95 great,96 love,97 learn,98 new,99 thing,100 listen,101 water,102 sleep,103 take,104 break,105 ask,106 teacher,107 doctor,108 eat,109 healthy,110 time,111 with,112 they,113 make,114 world,115 interesting,116 colour,117 red,118 green,119 blue,120 cat,121 dog,122 bird,123 apple,124 orange,125 rice,126 one,127 two,128 three,129 four,130 five,131 six,132 seven,133 eight,134 nine,135 ten,136..145 digits0..9.
146 paris,147 london,148 rome,149 berlin,150 madrid,151 tokyo,152 beijing,153 ottawa,154 washington,155 delhi,156 canberra,157 brasilia,158 moscow,159 seoul,160 cairo,161 athens,162 lisbon,163 dublin,164 oslo,165 stockholm,166 helsinki,167 copenhagen,168 bern,169 amsterdam,170 vienna,171 warsaw,172 kyiv,173 ankara,174 bangkok,175 hanoi,176 jakarta,177 islamabad,178 tehran,179 baghdad,180 jerusalem,181 riyadh,182 doha,183 nairobi,184 pretoria,185 wellington,186 lima,187 santiago,188 havana,189 caracas,190 montevideo.
191 sam,192 altman,193 elon,194 musk,195 satya,196 nadella,197 sundar,198 pichai,199 jensen,200 huang,201 mark,202 zuckerberg,203 tim,204 cook,205 dario,206 amodei,207 demis,208 hassabis,209 bill,210 gates,211 steve,212 jobs,213 jeff,214 bezos,215 openai,216 microsoft,217 google,218 meta,219 spacex,220 tesla,221 nvidia,222 anthropic,223 claude,224 chatgpt,225 gemini,226 windows,227 android,228 iphone,229 earth,230 mars,231 jupiter,232 saturn,233 mercury,234 venus,235 neptune,236 uranus,237 sun,238 moon,239 pacific,240 asia,241 africa,242 europe,243 america,244 antarctica,245 oceania,246 everest,247 nile,248 amazon,249 sahara,250 einstein,251 newton,252 shakespeare,253 mozart,254 leonardo,255 vinci,256 darwin,257 edison,258 armstrong,259 gagarin,260 air,261 iron,262 gold,263 silver,264 salt,265 protein,266 heart,267 brain,268 blood,269 leaf,270 tree,271 fish,272 elephant,273 mouse,274 rabbit,275 bee,276 snow,277 ice,278 fire,279 light,280 dark,281 white,282 black,283 up,284 down,285 left,286 north,287 south,288 east,289 west,290 old,291 young,292 long,293 short,294 tall,295 full,296 dry,297 wet,298 fast,299 slow,300 easy,301 difficult,302 clean,303 dirty,304 strong,305 soft,306 hard,307 loud,308 quiet,309 open,310 shut,311 true,312 false,313 beautiful,314 bad,315 poor,316 rich,317 night,318 morning,319 summer,320 winter,321 start,322 end,323 come,324 go,325 win,326 lose,327 give,328 warm,329 cool,330 high,331 low,332 male,333 female,334 man,335 woman,336 boy,337 girl,338 brother,339 sister,340 father,341 mother,342 spring,343 word.
344 tom,345 sara,346 anna,347 john,348 mary,349 james,350 emma,351 liam,352 olivia,353 noah,354 ava,355 mia,356 lucas,357 ella,358 jack,359 lily,360 ben,361 max,362 leo,363 zoe,364 amy,365 kate,366 mike,367 dan,368 alex,369 maria,370 david,371 paul,372 peter.
373 number,374 an,375 important,376 for,377 sport,378 people,379 here,380 angry,381 ill,382 afraid,383 trust,384 animal,385 fruit,386 berry,387 feeble.
IMPORTANT: “calm” and “interesting” may not be vocabulary tokens! They were assigned in U by names; if bookkeeping reports them skipped, replace these codes with valid words (e.g. quiet and special) and change relevant template or code usage. Do not duplicate existing token output codes inadvertently.

LEXICAL COVERAGE
Country->capital facts, companies->current leaders, products->companies. Country fields6:11=[10,10,capitalCode,0,1]. Two-word leaders fields=[10,11,first,last,1] and29=1.
Named user memory covers tom..peter.
Emotion words happy/sad/tired/angry/ill/afraid/good/bad.
Task priorities select capital/lead/boss/chief ->10, opposite->12, say/copy->13, name->8, age/old->9, made/written/weight/hand/created/training->7, colours->41, animal->42, fruit->43.
Task "old" is overly broad; consider improving.
Echo codes currently only explicitly assigned for a subset of words, digits, and names. Can extend E[:,20] and26 from output dictionary.
Counting template14 and age numeric payload18 are not implemented.
World facts default to “the answer is ... .”; generic unknown question falls back to bot identity or default, not ideal.
Current semantic classifier is intentionally simple and can be improved.

SUGGESTED NEXT-PASS PRIORITIES
1. Check skipped statements, especially vocabulary validity, all spline coefficients, arrays.
2. Arithmetic: use free L1 heads2,3,4 for exact relative offsets1,2,3 with multiscale RoPE to read preceding digits. At a nondigit after a number, M1 can assemble the last1..3 consecutive digits. Preserve flags/value. L3 needs heads to retrieve first and last number within current user segment; could repurpose echo and negation heads, moving those to L2/local features.
3. Addition/subtraction straightforward once numbers extracted. Multiplication can use ((a+b)^2-a²-b²)/2. A promising budget: move user gating to M1; compute p²/256 in M1 using same reciprocal hinges (coefficient6n²/256, constant111169/256, linear-14266560/256), letting L2 copy both p and p² from USER. Then M2 has ~999 units to square each parsed number via n+2*sum ReLU(n-k). M3 could square a+b using <=1009 units because product<=9999 and a,b<1000 imply a+b<=1009, but classifier must move or share space. Addition/subtraction can be done first without this redesign.
4. Numeric output could use hierarchical decimal extraction in M4/M5/M6; unused template IDs44+ and M4 units488+ available.
5. Expand yes/no physical classification, counts, more facts/relations, list tasks, memory likes/age/number.
6. Improve fact relation handling (capital vs continent vs currency, maker vs leader) rather than always returning one fact.
Keep the scratchpad complete in each future pass.
=====END SCRATCHPAD=====

```edits
# Constant and structural embeddings.
E[:, 0] = 1
E["BOS", 1] = 1
E["USER", 2] = 1
E["BOT", 3] = 1

# Position and current speaker role.
V1[0, 1, 0] = 1
O1[0, 0, 200] = 1
Q1[1, 0, 30] = 100
K1[1, 2:4, 30] = 1000
K1[1, 2:4, 31] = -10000
V1[1, 2, 0] = 1
O1[1, 0, 202] = 1
M1_b[0] = 1
M1_out[0, 201] = 385
M1_in[200, 1:193] = 1
M1_out[1, 201] = -37056
M1_b[2:193] = [
-0.500000000,-0.333333333,-0.250000000,-0.200000000,-0.166666667,-0.142857143,-0.125000000,-0.111111111,-0.100000000,
-0.090909091,-0.083333333,-0.076923077,-0.071428571,-0.066666667,-0.062500000,-0.058823529,-0.055555556,-0.052631579,-0.050000000,
-0.047619048,-0.045454545,-0.043478261,-0.041666667,-0.040000000,-0.038461538,-0.037037037,-0.035714286,-0.034482759,-0.033333333,
-0.032258065,-0.031250000,-0.030303030,-0.029411765,-0.028571429,-0.027777778,-0.027027027,-0.026315789,-0.025641026,-0.025000000,
-0.024390244,-0.023809524,-0.023255814,-0.022727273,-0.022222222,-0.021739130,-0.021276596,-0.020833333,-0.020408163,-0.020000000,
-0.019607843,-0.019230769,-0.018867925,-0.018518519,-0.018181818,-0.017857143,-0.017543860,-0.017241379,-0.016949153,-0.016666667,
-0.016393443,-0.016129032,-0.015873016,-0.015625000,-0.015384615,-0.015151515,-0.014925373,-0.014705882,-0.014492754,-0.014285714,
-0.014084507,-0.013888889,-0.013698630,-0.013513514,-0.013333333,-0.013157895,-0.012987013,-0.012820513,-0.012658228,-0.012500000,
-0.012345679,-0.012195122,-0.012048193,-0.011904762,-0.011764706,-0.011627907,-0.011494253,-0.011363636,-0.011235955,-0.011111111,
-0.010989011,-0.010869565,-0.010752688,-0.010638298,-0.010526316,-0.010416667,-0.010309278,-0.010204082,-0.010101010,-0.010000000,
-0.009900990,-0.009803922,-0.009708738,-0.009615385,-0.009523810,-0.009433962,-0.009345794,-0.009259259,-0.009174312,-0.009090909,
-0.009009009,-0.008928571,-0.008849558,-0.008771930,-0.008695652,-0.008620690,-0.008547009,-0.008474576,-0.008403361,-0.008333333,
-0.008264463,-0.008196721,-0.008130081,-0.008064516,-0.008000000,-0.007936508,-0.007874016,-0.007812500,-0.007751938,-0.007692308,
-0.007633588,-0.007575758,-0.007518797,-0.007462687,-0.007407407,-0.007352941,-0.007299270,-0.007246377,-0.007194245,-0.007142857,
-0.007092199,-0.007042254,-0.006993007,-0.006944444,-0.006896552,-0.006849315,-0.006802721,-0.006756757,-0.006711409,-0.006666667,
-0.006622517,-0.006578947,-0.006535948,-0.006493506,-0.006451613,-0.006410256,-0.006369427,-0.006329114,-0.006289308,-0.006250000,
-0.006211180,-0.006172840,-0.006134969,-0.006097561,-0.006060606,-0.006024096,-0.005988024,-0.005952381,-0.005917160,-0.005882353,
-0.005847953,-0.005813953,-0.005780347,-0.005747126,-0.005714286,-0.005681818,-0.005649718,-0.005617978,-0.005586592,-0.005555556,
-0.005524862,-0.005494505,-0.005464481,-0.005434783,-0.005405405,-0.005376344,-0.005347594,-0.005319149,-0.005291005,-0.005263158,
-0.005235602,-0.005208333]
M1_out[2:193, 201] = [
4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,
82,84,86,88,90,92,94,96,98,100,102,104,106,108,110,112,114,116,118,120,122,124,126,128,130,132,134,136,138,140,142,144,146,148,150,152,154,156,158,160,
162,164,166,168,170,172,174,176,178,180,182,184,186,188,190,192,194,196,198,200,202,204,206,208,210,212,214,216,218,220,222,224,226,228,230,232,234,236,238,240,
242,244,246,248,250,252,254,256,258,260,262,264,266,268,270,272,274,276,278,280,282,284,286,288,290,292,294,296,298,300,302,304,306,308,310,312,314,316,318,320,
322,324,326,328,330,332,334,336,338,340,342,344,346,348,350,352,354,356,358,360,362,364,366,368,370,372,374,376,378,380,382,384]

# Latest USER segment and user-only lexical features.
Q2[0, 0, 30] = 100
K2[0, 2, 30] = 1000
K2[0, 2, 31] = -10000
V2[0, 201, 0] = 1
O2[0, 0, 204] = 1
M2_in[202, 0:36] = 1000
M2_b[0:36] = -1000
M2_in[4, 0] = 1
M2_out[0, 40] = 1
M2_in[5, 1] = 1
M2_out[1, 41] = 1
M2_in[6, 2] = 1
M2_out[2, 42] = 1
M2_in[7, 3] = 1
M2_out[3, 43] = 1
M2_in[8, 4] = 1
M2_out[4, 44] = 1
M2_in[9, 5] = 1
M2_out[5, 45] = 1
M2_in[10, 6] = 1
M2_out[6, 46] = 1
M2_in[11, 7] = 1
M2_out[7, 47] = 1
M2_in[12, 8] = 1
M2_out[8, 48] = 1
M2_in[13, 9] = 1
M2_out[9, 49] = 1
M2_in[14, 10] = 1
M2_out[10, 50] = 1
M2_in[15, 11] = 1
M2_out[11, 51] = 1
M2_in[16, 12] = 1
M2_out[12, 52] = 1
M2_in[17, 13] = 1
M2_out[13, 53] = 1
M2_in[18, 14] = 1
M2_out[14, 54] = 1
M2_in[19, 15] = 1
M2_out[15, 55] = 1
M2_in[20, 16] = 1
M2_out[16, 56] = 1
M2_in[21, 17] = 1
M2_out[17, 57] = 1
M2_in[22, 18] = 1
M2_out[18, 58] = 1
M2_in[23, 19] = 1
M2_out[19, 59] = 1
M2_in[24, 20] = 1
M2_out[20, 60] = 1
M2_in[25, 21] = 1
M2_out[21, 61] = 1
M2_in[26, 22] = 1
M2_out[22, 62] = 1
M2_in[27, 23] = 1
M2_out[23, 63] = 1
M2_in[28, 24] = 1
M2_out[24, 64] = 1
M2_in[29, 25] = 1
M2_out[25, 65] = 1
M2_in[30, 26] = 1
M2_out[26, 66] = 1
M2_in[31, 27] = 1
M2_out[27, 67] = 1
M2_in[32, 28] = 1
M2_out[28, 68] = 1
M2_in[33, 29] = 1
M2_out[29, 69] = 1
M2_in[34, 30] = 1
M2_out[30, 70] = 1
M2_in[35, 31] = 1
M2_out[31, 71] = 1
M2_in[36, 32] = 1
M2_out[32, 72] = 1
M2_in[37, 33] = 1
M2_out[33, 73] = 1
M2_in[38, 34] = 1
M2_out[34, 74] = 1
M2_in[39, 35] = 1
M2_out[35, 75] = 1
M2_in[204, 36:228] = 1
M2_b[36:227] = [
-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,
-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,
-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,
-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73,-74,-75,-76,-77,-78,-79,-80,
-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,-91,-92,-93,-94,-95,-96,-97,-98,-99,-100,
-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,-111,-112,-113,-114,-115,-116,-117,-118,-119,-120,
-121,-122,-123,-124,-125,-126,-127,-128,-129,-130,-131,-132,-133,-134,-135,-136,-137,-138,-139,-140,
-141,-142,-143,-144,-145,-146,-147,-148,-149,-150,-151,-152,-153,-154,-155,-156,-157,-158,-159,-160,
-161,-162,-163,-164,-165,-166,-167,-168,-169,-170,-171,-172,-173,-174,-175,-176,-177,-178,-179,-180,
-181,-182,-183,-184,-185,-186,-187,-188,-189,-190,-191]
M2_out[36:227, 205] = 0.0078125
M2_out[227, 205] = 0.00390625

# Segment-aware retrieval.
Q3[:, 204, 30] = 100
Q3[:, 204, 28] = 100
Q3[:, 204, 26] = 100
K3[:, 204, 30] = 324.9945102
K3[:, 204, 28] = -135.271739
K3[:, 204, 26] = 10.2772288
Q3[:, 0, 24] = 100
Q3[:, 0, 22] = 100
Q3[:, 0, 20] = 100
K3[:, 205, 24] = -41599.2973056
K3[:, 205, 22] = 17314.782592
K3[:, 205, 20] = -1315.4852864
Q3[:, 0, 18] = 100
K3[0, 40, 18:20] = [100,-80]
K3[1, 42, 18:20] = [100,-80]
K3[2, 47, 18:20] = [100,-80]
K3[3, 52, 18:20] = [100,-80]
K3[5, 62, 18:20] = [100,-80]
K3[6, 64, 18:20] = [100,-80]
K3[7, 51, 18:20] = [100,-80]
V3[0, 41, 0] = 1
O3[0, 0, 76] = 1
V3[1, 43, 0] = 1
V3[1, 44, 1] = 1
V3[1, 45, 2] = 1
V3[1, 46, 3] = 1
V3[1, 65, 4] = 1
O3[1, 0, 77] = 1
O3[1, 1, 78] = 1
O3[1, 2, 79] = 1
O3[1, 3, 80] = 1
O3[1, 4, 88] = 1
V3[2, 48, 0] = 1
V3[2, 49, 1] = 1
V3[2, 50, 2] = 1
O3[2, 0, 81] = 1
O3[2, 1, 82] = 1
O3[2, 2, 83] = 1
V3[3, 53, 0] = 1
O3[3, 0, 84] = 1
Q3[4, :, :] = 0
K3[4, :, :] = 0
Q3[4, 0, 30] = 100
K3[4, 57, 30] = 1000
K3[4, 57, 31] = -10000
V3[4, 58, 0] = 1
V3[4, 57, 1] = 1
O3[4, 0, 85] = 1
O3[4, 1, 89] = 1
V3[5, 56, 0] = 1
O3[5, 0, 86] = 1
V3[6, 63, 0] = 1
O3[6, 0, 87] = 1
V3[7, 51, 0] = 1
O3[7, 0, 90] = 1

# Response-plan selection.
M3_in[76, 0] = 1
M3_in[77, 0] = -1000
M3_in[81, 0] = -1000
M3_in[84, 0] = -1000
M3_in[77, 1] = 1
M3_in[81, 1] = -1000
M3_in[84, 1] = -1000
M3_in[81, 2] = 1
M3_in[84, 2] = -1000
M3_in[84, 3] = 1
M3_out[0:4, 141] = 1
M3_in[84, 4:25] = 1
M3_in[87, 4:10] = 64
M3_b[4:10] = [-71,-72,-73,-72,-73,-74]
M3_out[4:10, 141] = [8,-16,8,9,-18,9]
M3_in[80, 10:13] = 64
M3_b[10:13] = [-9,-10,-11]
M3_out[10:13, 141] = [7,-14,7]
M3_in[88, 13:16] = 64
M3_b[13:16] = [-73,-74,-75]
M3_out[13:16, 141] = [1,-2,1]
M3_in[87, 16:19] = 64
M3_in[89, 16:19] = 256
M3_b[16:19] = [-71,-72,-73]
M3_out[16:19, 141] = [1,-2,1]
M3_in[80, 19:22] = 64
M3_b[19:22] = [-70,-71,-72]
M3_out[19:22, 141] = [3,-6,3]
M3_in[88, 22:25] = 64
M3_b[22:25] = [-70,-71,-72]
M3_out[22:25, 141] = [1,-2,1]
M3_in[81, 25:37] = 1
M3_in[90, 25:37] = 64
M3_in[84, 25:37] = 256
M3_b[25:37] = [-93,-94,-95,-94,-95,-96,-100,-101,-102,-101,-102,-103]
M3_out[25:37, 141] = [1,-2,1,-1,2,-1,1,-2,1,-1,2,-1]

# Freeze plan and payload at the most recent BOT.
Q4[0, 0, 30] = 100
K4[0, 3, 30] = 1000
K4[0, 3, 31] = -10000
V4[0, 141, 0] = 1
V4[0, 78, 1] = 1
V4[0, 79, 2] = 1
V4[0, 201, 3] = 1
V4[0, 82, 4] = 1
V4[0, 85, 5] = 1
V4[0, 86, 6] = 1
O4[0, 0, 160] = 1
O4[0, 1, 161] = 1
O4[0, 2, 162] = 1
O4[0, 3, 163] = 1
O4[0, 4, 164] = 1
O4[0, 5, 165] = 1
O4[0, 6, 166] = 1

# Output spline. Every sequence is surrounded by EOS.
M4_b[0] = 1
M4_out[0, 180:182] = [1,1]
M4_in[160, 1:488] = 64
M4_in[201, 1:488] = 1
M4_in[163, 1:488] = -1
M4_b[1:17] = [1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14]
M4_out[1:17, 180] = [1,0,57,-86,5,21,58,-55,-55,89,-48,46,-32,-56,44,11]
M4_b[17:28] = [-63,-64,-65,-66,-67,-68,-69,-70,-71,-72,-73]
M4_out[17:28, 180] = [12,-11,0,-7,-1,15,-7,4,-9,-7,11]
M4_b[28:37] = [-127,-128,-129,-130,-131,-132,-133,-134,-135]
M4_out[28:37, 180] = [16,-19,7,-18,29,-14,-13,5,7]
M4_b[37:43] = [-191,-192,-193,-194,-195,-196]
M4_out[37:43, 180] = [10,0,-9,-9,-5,13]
M4_b[43:56] = [-255,-256,-257,-258,-259,-260,-261,-262,-263,-264,-265,-266,-267]
M4_out[43:56, 180] = [26,-25,0,0,-23,45,-22,0,0,-9,-10,11,7]
M4_b[56:69] = [-319,-320,-321,-322,-323,-324,-325,-326,-327,-328,-329,-330,-331]
M4_out[56:69, 180] = [1,0,21,-23,0,-11,9,10,-1,-16,11,-12,11]
M4_b[69:89] = [-383,-384,-385,-386,-387,-388,-389,-390,-391,-392,-393,-394,-395,-396,-397,-398,-399,-400,-401,-402]
M4_out[69:89, 180] = [1,0,0,0,0,0,0,-7,13,-10,21,6,-23,-13,25,-21,17,-52,36,7]
M4_b[89:99] = [-447,-448,-449,-450,-451,-452,-453,-454,-455,-456]
M4_out[89:99, 180] = [34,-33,0,0,0,0,0,-34,26,7]
M4_b[99:115] = [-511,-512,-513,-514,-515,-516,-517,-518,-519,-520,-521,-522,-523,-524,-525,-526]
M4_out[99:115, 180] = [1,39,-39,-26,11,54,-76,30,7,0,0,0,0,0,-8,7]
M4_b[115:127] = [-575,-576,-577,-578,-579,-580,-581,-582,-583,-584,-585,-586]
M4_out[115:127, 180] = [1,39,-39,-26,381,-685,330,-43,85,-82,32,7]
M4_b[127:134] = [-639,-640,-641,-642,-643,-644,-645]
M4_out[127:134, 180] = [51,-55,-16,-8,36,-15,7]
M4_b[134:142] = [-703,-704,-705,-706,-707,-708,-709,-710]
M4_out[134:142, 180] = [51,-55,-16,-8,28,8,-15,7]
M4_b[142:149] = [-767,-768,-769,-770,-771,-772,-773]
M4_out[142:149, 180] = [51,-48,-30,-1,36,-15,7]
M4_b[149:156] = [-831,-832,-833,-834,-835,-836,-837]
M4_out[149:156, 180] = [51,240,-606,287,36,-15,7]
M4_b[156:163] = [-1023,-1024,-1025,-1026,-1027,-1028,-1029]
M4_out[156:163, 180] = [55,-67,-4,-12,36,-15,7]
M4_b[163:177] = [-1087,-1088,-1089,-1090,-1091,-1092,-1093,-1094,-1095,-1096,-1097,-1098,-1099,-1100]
M4_out[163:177, 180] = [1,39,-39,37,-111,67,13,67,-75,-48,26,21,-5,7]
M4_b[177:184] = [-1151,-1152,-1153,-1154,-1155,-1156,-1157]
M4_out[177:184, 180] = [55,-66,-6,-11,36,-15,7]
M4_b[184:197] = [-1279,-1280,-1281,-1282,-1283,-1284,-1285,-1286,-1287,-1288,-1289,-1290,-1291]
M4_out[184:197, 180] = [67,-126,84,16,-108,123,-52,-30,-5,66,-69,23,11]
M4_b[197:214] = [-1343,-1344,-1345,-1346,-1347,-1348,-1349,-1350,-1351,-1352,-1353,-1354,-1355,-1356,-1357,-1358,-1359]
M4_out[197:214, 180] = [24,20,-104,164,-213,125,43,-130,127,-78,-9,66,-48,88,-171,85,11]
M4_b[214:224] = [-1407,-1408,-1409,-1410,-1411,-1412,-1413,-1414,-1415,-1416]
M4_out[214:224, 180] = [1,74,-100,43,-60,33,6,-5,1,7]
M4_b[224:239] = [-1471,-1472,-1473,-1474,-1475,-1476,-1477,-1478,-1479,-1480,-1481,-1482,-1483,-1484,-1485]
M4_out[224:239, 180] = [1,74,-81,-37,40,-6,1,57,-3,-39,-84,102,-75,43,7]
M4_b[239:257] = [-1535,-1536,-1537,-1538,-1539,-1540,-1541,-1542,-1543,-1544,-1545,-1546,-1547,-1548,-1549,-1550,-1551,-1552]
M4_out[239:257, 180] = [71,-134,64,0,85,-85,0,-63,33,85,-78,-9,66,-48,77,-149,74,11]
M4_b[257:271] = [-1599,-1600,-1601,-1602,-1603,-1604,-1605,-1606,-1607,-1608,-1609,-1610,-1611,-1612]
M4_out[257:271, 180] = [72,-136,89,316,-708,361,81,-96,38,-62,76,-82,44,7]
M4_b[271:287] = [-1663,-1664,-1665,-1666,-1667,-1668,-1669,-1670,-1671,-1672,-1673,-1674,-1675,-1676,-1677,-1678]
M4_out[271:287, 180] = [3,67,-135,90,-55,51,47,-153,119,-65,38,-21,84,-132,51,11]
M4_b[287:298] = [-1727,-1728,-1729,-1730,-1731,-1732,-1733,-1734,-1735,-1736,-1737]
M4_out[287:298, 180] = [376,-744,393,16,-66,0,376,-716,362,-4,7]
M4_b[298:308] = [-1855,-1856,-1857,-1858,-1859,-1860,-1861,-1862,-1863,-1864]
M4_out[298:308, 180] = [1,43,-57,-14,71,-84,408,-738,363,7]
M4_b[308:325] = [-1919,-1920,-1921,-1922,-1923,-1924,-1925,-1926,-1927,-1928,-1929,-1930,-1931,-1932,-1933,-1934,-1935]
M4_out[308:325, 180] = [1,0,57,-86,57,-28,-50,37,87,-141,73,-21,105,-166,63,5,7]
M4_b[325:340] = [-1983,-1984,-1985,-1986,-1987,-1988,-1989,-1990,-1991,-1992,-1993,-1994,-1995,-1996,-1997]
M4_out[325:340, 180] = [1,0,22,-38,64,-19,-112,76,7,375,-722,413,-159,85,7]
M4_b[340:353] = [-2047,-2048,-2049,-2050,-2051,-2052,-2053,-2054,-2055,-2056,-2057,-2058,-2059]
M4_out[340:353, 180] = [1,0,22,-38,64,-18,-114,132,-48,0,-52,44,7]
M4_b[353:369] = [-2111,-2112,-2113,-2114,-2115,-2116,-2117,-2118,-2119,-2120,-2121,-2122,-2123,-2124,-2125,-2126]
M4_out[353:369, 180] = [1,0,22,-38,64,271,-692,421,-3,-39,-84,104,5,-116,77,7]
M4_b[369:387] = [-2175,-2176,-2177,-2178,-2179,-2180,-2181,-2182,-2183,-2184,-2185,-2186,-2187,-2188,-2189,-2190,-2191,-2192]
M4_out[369:387, 180] = [1,0,22,-38,64,272,-694,422,-48,-9,63,-156,204,166,-635,364,-5,7]
M4_b[387:404] = [-2239,-2240,-2241,-2242,-2243,-2244,-2245,-2246,-2247,-2248,-2249,-2250,-2251,-2252,-2253,-2254,-2255]
M4_out[387:404, 180] = [1,0,22,-38,64,273,-696,423,-40,36,-152,150,-79,408,-747,368,7]
M4_b[404:417] = [-2367,-2368,-2369,-2370,-2371,-2372,-2373,-2374,-2375,-2376,-2377,-2378,-2379]
M4_out[404:417, 180] = [62,-97,32,-8,12,-7,-1,15,-7,4,-9,-7,11]
M4_b[417:431] = [-2431,-2432,-2433,-2434,-2435,-2436,-2437,-2438,-2439,-2440,-2441,-2442,-2443,-2444]
M4_out[417:431, 180] = [1,0,22,-16,22,-28,-56,62,-13,-1,15,-6,-13,11]
M4_b[431:438] = [-2495,-2496,-2497,-2498,-2499,-2500,-2501]
M4_out[431:438, 180] = [83,-143,63,-2,-21,13,7]
M4_b[438:446] = [-2559,-2560,-2561,-2562,-2563,-2564,-2565,-2566]
M4_out[438:446, 180] = [30,-37,10,-2,14,-50,28,7]
M4_b[446:458] = [-2623,-2624,-2625,-2626,-2627,-2628,-2629,-2630,-2631,-2632,-2633,-2634]
M4_out[446:458, 180] = [127,-139,-67,63,112,-189,187,-162,137,-180,104,7]
M4_b[458:473] = [-2687,-2688,-2689,-2690,-2691,-2692,-2693,-2694,-2695,-2696,-2697,-2698,-2699,-2700,-2701]
M4_out[458:473, 180] = [127,129,-603,331,-1,133,-212,76,137,-188,25,164,-232,107,7]
M4_b[473:488] = [-2751,-2752,-2753,-2754,-2755,-2756,-2757,-2758,-2759,-2760,-2761,-2762,-2763,-2764,-2765]
M4_out[473:488, 180] = [127,130,-605,332,369,-604,152,449,-600,176,28,428,-760,371,7]
M4_out[130:133, 182] = [1,-2,1]
M4_out[137:140, 182] = [1,-2,1]
M4_out[138:141, 183] = [1,-2,1]
M4_out[145:148, 184] = [1,-2,1]
M4_out[152:155, 186] = [1,-2,1]
M4_out[159:162, 185] = [1,-2,1]
M4_out[180:183, 187] = [1,-2,1]

# Dynamic word insertion.
M5_in[161, 0] = 1
M5_in[182, 0] = 1000
M5_in[162, 1] = 1
M5_in[183, 1] = 1000
M5_in[164, 2] = 1
M5_in[184, 2] = 1000
M5_in[165, 3] = 1
M5_in[185, 3] = 1000
M5_in[166, 4] = 1
M5_in[186, 4] = 1000
M5_b[0:5] = -1000
M5_out[0:5, 180] = 1

# General conversation triggers.
E[["hello","hi","hey"], 4:6] = [10,1]
E[["bye","goodbye"], 4:6] = [12,2]
E[["thank","thanks","appreciate"], 4:6] = [12,3]
E["sorry", 4:6] = [8,4]
E["how", 4:6] = [3,5]
E["who", 4:6] = [2,6]
E[["what","you","your","can"], 4:6] = [1,6]
E[["i","me","my"], 27:29] = [1,1]
E[["you","your","yourself"], 27:29] = [2,1]
E[["not","un-"], 15] = 1
E[["made","written","weight","hand","created","training"], 16:18] = [8,7]
E["name", 16:18] = [10,8]
E[["age","old"], 16:18] = [10,9]
E["capital", 16:18] = [18,10]
E[["lead","leader","boss","chief"], 16:18] = [12,10]
E["opposite", 16:18] = [20,12]
E[["say","copy"], 16:18] = [16,13]
E[["robot","human","program","assistant"], 16:18] = [5,6]
E[["colour","color"], 16:18] = [12,41]
E["animal", 16:18] = [12,42]
E["fruit", 16:18] = [12,43]
E[["music","song","piano","album","dance","guitars","drums"], 6:8] = [5,20]
E[["food","eat","dinner","lunch","meal","pizza","rice","coffee","tea","cake","bread","cook","cookie"], 6:8] = [5,21]
E[["weather","rain","snow","wind","cloud"], 6:8] = [5,22]
E[["work","job","office","busy"], 6:8] = [5,23]
E[["school","class","teacher","college","student","study"], 6:8] = [5,24]
E[["family","father","mother","mom","dad","brother","sister","parents","child","children","grandmother"], 6:8] = [5,25]
E[["pet","cat","dog","rabbit","bird"], 6:8] = [5,26]
E[["sport","sports","football","game","team"], 6:8] = [5,27]
E["hobby", 6:8] = [5,29]
E["happy", 11:14] = [12,30,90]
E["glad", 11:14] = [12,30,90]
E["excited", 11:13] = [12,30]
E["sad", 11:14] = [12,31,61]
E["tired", 11:13] = [12,32]
E[["angry","mad","frustrated"], 11:13] = [12,33]
E[["ill","sick"], 11:13] = [12,34]
E[["afraid","fear","worry"], 11:13] = [12,35]
E["good", 11:14] = [6,37,314]
E["bad", 11:14] = [6,38,25]

# Capitals.
E["france", 6:11] = [10,10,146,0,1]
E[["britain","england"], 6:11] = [10,10,147,0,1]
E["italy", 6:11] = [10,10,148,0,1]
E["germany", 6:11] = [10,10,149,0,1]
E["spain", 6:11] = [10,10,150,0,1]
E["japan", 6:11] = [10,10,151,0,1]
E["china", 6:11] = [10,10,152,0,1]
E["canada", 6:11] = [10,10,153,0,1]
E["usa", 6:11] = [10,10,154,0,1]
E["india", 6:11] = [10,10,155,0,1]
E["australia", 6:11] = [10,10,156,0,1]
E["brazil", 6:11] = [10,10,157,0,1]
E["russia", 6:11] = [10,10,158,0,1]
E["korea", 6:11] = [10,10,159,0,1]
E["egypt", 6:11] = [10,10,160,0,1]
E["greece", 6:11] = [10,10,161,0,1]
E["portugal", 6:11] = [10,10,162,0,1]
E["ireland", 6:11] = [10,10,163,0,1]
E["norway", 6:11] = [10,10,164,0,1]
E["sweden", 6:11] = [10,10,165,0,1]
E["finland", 6:11] = [10,10,166,0,1]
E["denmark", 6:11] = [10,10,167,0,1]
E["switzerland", 6:11] = [10,10,168,0,1]
E["netherlands", 6:11] = [10,10,169,0,1]
E["austria", 6:11] = [10,10,170,0,1]
E["poland", 6:11] = [10,10,171,0,1]
E["ukraine", 6:11] = [10,10,172,0,1]
E["turkey", 6:11] = [10,10,173,0,1]
E["thailand", 6:11] = [10,10,174,0,1]
E["vietnam", 6:11] = [10,10,175,0,1]
E["indonesia", 6:11] = [10,10,176,0,1]
E["pakistan", 6:11] = [10,10,177,0,1]
E["iran", 6:11] = [10,10,178,0,1]
E["iraq", 6:11] = [10,10,179,0,1]
E["israel", 6:11] = [10,10,180,0,1]
E["arabia", 6:11] = [10,10,181,0,1]
E["qatar", 6:11] = [10,10,182,0,1]
E["kenya", 6:11] = [10,10,183,0,1]
E["zealand", 6:11] = [10,10,185,0,1]
E["peru", 6:11] = [10,10,186,0,1]
E["chile", 6:11] = [10,10,187,0,1]
E["cuba", 6:11] = [10,10,188,0,1]
E["venezuela", 6:11] = [10,10,189,0,1]
E["uruguay", 6:11] = [10,10,190,0,1]

# Leaders and product makers.
E["openai", 6:11] = [10,11,191,192,1]
E["anthropic", 6:11] = [10,11,205,206,1]
E["google", 6:11] = [10,11,197,198,1]
E["microsoft", 6:11] = [10,11,195,196,1]
E["nvidia", 6:11] = [10,11,199,200,1]
E[["tesla","spacex","xai"], 6:11] = [10,11,193,194,1]
E[["meta","facebook"], 6:11] = [10,11,201,202,1]
E["apple", 6:11] = [10,21,203,204,1]
E["deepmind", 6:11] = [10,11,207,208,1]
E[["openai","anthropic","google","microsoft","nvidia","tesla","spacex","xai","meta","facebook","apple","deepmind"], 29] = 1
E[["chatgpt","gpt"], 6:11] = [12,10,215,0,1]
E["claude", 6:11] = [12,10,222,0,1]
E[["gemini","android","youtube"], 6:11] = [12,10,217,0,1]
E[["windows","copilot","bing"], 6:11] = [12,10,216,0,1]
E[["iphone","ipad"], 6:11] = [12,10,123,0,1]
E[["instagram","whatsapp","llama"], 6:11] = [12,10,218,0,1]
E["planet", 6:11] = [5,10,231,0,1]
E["ocean", 6:11] = [5,10,239,0,1]
E["mountain", 6:11] = [5,10,246,0,1]
E["river", 6:11] = [5,10,247,0,1]

# Opposite-word dictionary.
E["hot", 11:14] = [6,0,85]
E["cold", 11:14] = [6,0,86]
E["big", 11:14] = [6,0,5]
E["small", 11:14] = [6,0,87]
E["old", 11:14] = [6,0,291]
E["young", 11:14] = [6,0,290]
E["long", 11:14] = [6,0,293]
E["short", 11:14] = [6,0,292]
E["tall", 11:14] = [6,0,293]
E["up", 11:14] = [6,0,284]
E["down", 11:14] = [6,0,283]
E["left", 11:14] = [6,0,30]
E["right", 11:14] = [6,0,285]
E["dry", 11:14] = [6,0,297]
E["wet", 11:14] = [6,0,296]
E["fast", 11:14] = [6,0,299]
E["slow", 11:14] = [6,0,298]
E["easy", 11:14] = [6,0,301]
E["difficult", 11:14] = [6,0,300]
E["clean", 11:14] = [6,0,303]
E["dirty", 11:14] = [6,0,302]
E["strong", 11:14] = [6,0,387]
E["feeble", 11:14] = [6,0,304]
E["hard", 11:14] = [6,0,305]
E["soft", 11:14] = [6,0,306]
E["loud", 11:14] = [6,0,308]
E["quiet", 11:14] = [6,0,307]
E["open", 11:14] = [6,0,310]
E["shut", 11:14] = [6,0,309]
E["true", 11:14] = [6,0,312]
E["false", 11:14] = [6,0,311]
E["white", 11:14] = [6,0,282]
E["black", 11:14] = [6,0,281]
E["night", 11:14] = [6,0,20]
E["day", 11:14] = [6,0,317]
E["high", 11:14] = [6,0,331]
E["low", 11:14] = [6,0,330]
E["rich", 11:14] = [6,0,315]
E["poor", 11:14] = [6,0,316]
E["alive", 11:14] = [6,0,89]
E["dead", 11:14] = [6,0,88]
E["start", 11:14] = [6,0,322]
E["end", 11:14] = [6,0,321]
E["come", 11:14] = [6,0,324]
E["go", 11:14] = [6,0,323]
E["win", 11:14] = [6,0,326]
E["lose", 11:14] = [6,0,325]
E["give", 11:14] = [6,0,103]
E["take", 11:14] = [6,0,327]
E["north", 11:14] = [6,0,287]
E["south", 11:14] = [6,0,286]
E["east", 11:14] = [6,0,289]
E["west", 11:14] = [6,0,288]
E["man", 11:14] = [6,0,335]
E["woman", 11:14] = [6,0,334]
E["boy", 11:14] = [6,0,337]
E["girl", 11:14] = [6,0,336]
E["brother", 11:14] = [6,0,339]
E["sister", 11:14] = [6,0,338]
E["father", 11:14] = [6,0,341]
E["mother", 11:14] = [6,0,340]
E["warm", 11:14] = [6,0,329]
E["cool", 11:14] = [6,0,328]

# Personal-name memory.
E[["tom","sara","anna","john","mary","james","emma","liam","olivia","noah","ava","mia","lucas","ella","jack","lily","ben","max","leo","zoe","amy","kate","mike","dan","alex","maria","david","paul","peter"], 21] = 1
E[["tom","sara","anna","john","mary","james","emma","liam","olivia","noah","ava","mia","lucas","ella","jack","lily","ben","max","leo","zoe","amy","kate","mike","dan","alex","maria","david","paul","peter"], 22] = [344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372]
E[["tom","sara","anna","john","mary","james","emma","liam","olivia","noah","ava","mia","lucas","ella","jack","lily","ben","max","leo","zoe","amy","kate","mike","dan","alex","maria","david","paul","peter"], 20] = [344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372]
E[["tom","sara","anna","john","mary","james","emma","liam","olivia","noah","ava","mia","lucas","ella","jack","lily","ben","max","leo","zoe","amy","kate","mike","dan","alex","maria","david","paul","peter"], 26] = 1

# Digits and initial echo vocabulary.
E[5:15, 18] = 1
E[5:15, 19] = [0,1,2,3,4,5,6,7,8,9]
E[5:15, 20] = [136,137,138,139,140,141,142,143,144,145]
E[5:15, 26] = 1
E[["hello","cat","dog","bird","apple","orange","red","green","blue","hot","cold","big","small","happy","sad","good","bad","music","water","sun","moon","tree","flower","word"], 26] = 1
E[["hello","cat","dog","bird","apple","orange","red","green","blue","hot","cold","big","small","happy","sad","good","bad","music","water","sun","moon","tree","word"], 20] = [13,120,121,122,123,124,117,118,119,86,85,87,5,61,90,25,314,68,101,237,238,270,343]

# Nearest-code output vocabulary.
U[181, :] = -1000000
U[[180,181], "EOS"] = [2,-1]
U[[180,181], "i"] = [4,-4]
U[[180,181], "am"] = [6,-9]
U[[180,181], "a"] = [8,-16]
U[[180,181], "small"] = [10,-25]
U[[180,181], "chat"] = [12,-36]
U[[180,181], "bot"] = [14,-49]
U[[180,181], "."] = [16,-64]
U[[180,181], "can"] = [18,-81]
U[[180,181], "help"] = [20,-100]
U[[180,181], "you"] = [22,-121]
U[[180,181], "?"] = [24,-144]
U[[180,181], "hello"] = [26,-169]
U[[180,181], "!"] = [28,-196]
U[[180,181], "how"] = [30,-225]
U[[180,181], "today"] = [32,-256]
U[[180,181], "goodbye"] = [34,-289]
U[[180,181], "have"] = [36,-324]
U[[180,181], "nice"] = [38,-361]
U[[180,181], "day"] = [40,-400]
U[[180,181], "are"] = [42,-441]
U[[180,181], "welcome"] = [44,-484]
U[[180,181], "thank"] = [46,-529]
U[[180,181], ","] = [48,-576]
U[[180,181], "good"] = [50,-625]
U[[180,181], "sorry"] = [52,-676]
U[[180,181], "it"] = [54,-729]
U[[180,181], "is"] = [56,-784]
U[[180,181], "all"] = [58,-841]
U[[180,181], "right"] = [60,-900]
U[[180,181], "no"] = [62,-961]
U[[180,181], "need"] = [64,-1024]
U[[180,181], "to"] = [66,-1089]
U[[180,181], "be"] = [68,-1156]
U[[180,181], "my"] = [70,-1225]
U[[180,181], "weight"] = [72,-1296]
U[[180,181], "-s"] = [74,-1369]
U[[180,181], "were"] = [76,-1444]
U[[180,181], "written"] = [78,-1521]
U[[180,181], "by"] = [80,-1600]
U[[180,181], "hand"] = [82,-1681]
U[[180,181], "do"] = [84,-1764]
U[[180,181], "not"] = [86,-1849]
U[[180,181], "name"] = [88,-1936]
U[[180,181], "age"] = [90,-2025]
U[[180,181], "like"] = [92,-2116]
U[[180,181], "person"] = [94,-2209]
U[[180,181], "answer"] = [96,-2304]
U[[180,181], "question"] = [98,-2401]
U[[180,181], "and"] = [100,-2500]
U[[180,181], "maths"] = [102,-2601]
U[[180,181], "the"] = [104,-2704]
U[[180,181], "capital"] = [106,-2809]
U[[180,181], "of"] = [108,-2916]
U[[180,181], "opposite"] = [110,-3025]
U[[180,181], "your"] = [112,-3136]
U[[180,181], "please"] = [114,-3249]
U[[180,181], "rest"] = [116,-3364]
U[[180,181], "well"] = [118,-3481]
U[[180,181], "feel"] = [120,-3600]
U[[180,181], "happy"] = [122,-3721]
U[[180,181], "hear"] = [124,-3844]
U[[180,181], "that"] = [126,-3969]
U[[180,181], "what"] = [128,-4096]
U[[180,181], "would"] = [130,-4225]
U[[180,181], "talk"] = [132,-4356]
U[[180,181], "about"] = [134,-4489]
U[[180,181], "music"] = [136,-4624]
U[[180,181], "food"] = [138,-4761]
U[[180,181], "weather"] = [140,-4900]
U[[180,181], "work"] = [142,-5041]
U[[180,181], "school"] = [144,-5184]
U[[180,181], "family"] = [146,-5329]
U[[180,181], "pet"] = [148,-5476]
U[[180,181], "fun"] = [150,-5625]
U[[180,181], "enjoy"] = [152,-5776]
U[[180,181], "hope"] = [154,-5929]
U[[180,181], "get"] = [156,-6084]
U[[180,181], "better"] = [158,-6241]
U[[180,181], "soon"] = [160,-6400]
U[[180,181], "know"] = [162,-6561]
U[[180,181], "try"] = [164,-6724]
U[[180,181], "still"] = [166,-6889]
U[[180,181], "yes"] = [168,-7056]
U[[180,181], "cold"] = [170,-7225]
U[[180,181], "hot"] = [172,-7396]
U[[180,181], "big"] = [174,-7569]
U[[180,181], "alive"] = [176,-7744]
U[[180,181], "dead"] = [178,-7921]
U[[180,181], "sad"] = [180,-8100]
U[[180,181], "tired"] = [182,-8281]
U[[180,181], "calm"] = [184,-8464]
U[[180,181], "friend"] = [186,-8649]
U[[180,181], "safe"] = [188,-8836]
U[[180,181], "great"] = [190,-9025]
U[[180,181], "love"] = [192,-9216]
U[[180,181], "learn"] = [194,-9409]
U[[180,181], "new"] = [196,-9604]
U[[180,181], "thing"] = [198,-9801]
U[[180,181], "listen"] = [200,-10000]
U[[180,181], "water"] = [202,-10201]
U[[180,181], "sleep"] = [204,-10404]
U[[180,181], "take"] = [206,-10609]
U[[180,181], "break"] = [208,-10816]
U[[180,181], "ask"] = [210,-11025]
U[[180,181], "teacher"] = [212,-11236]
U[[180,181], "doctor"] = [214,-11449]
U[[180,181], "eat"] = [216,-11664]
U[[180,181], "healthy"] = [218,-11881]
U[[180,181], "time"] = [220,-12100]
U[[180,181], "with"] = [222,-12321]
U[[180,181], "they"] = [224,-12544]
U[[180,181], "make"] = [226,-12769]
U[[180,181], "world"] = [228,-12996]
U[[180,181], "interesting"] = [230,-13225]
U[[180,181], "colour"] = [232,-13456]
U[[180,181], "red"] = [234,-13689]
U[[180,181], "green"] = [236,-13924]
U[[180,181], "blue"] = [238,-14161]
U[[180,181], "cat"] = [240,-14400]
U[[180,181], "dog"] = [242,-14641]
U[[180,181], "bird"] = [244,-14884]
U[[180,181], "apple"] = [246,-15129]
U[[180,181], "orange"] = [248,-15376]
U[[180,181], "rice"] = [250,-15625]
U[[180,181], "one"] = [252,-15876]
U[[180,181], "two"] = [254,-16129]
U[[180,181], "three"] = [256,-16384]
U[[180,181], "four"] = [258,-16641]
U[[180,181], "five"] = [260,-16900]
U[[180,181], "six"] = [262,-17161]
U[[180,181], "seven"] = [264,-17424]
U[[180,181], "eight"] = [266,-17689]
U[[180,181], "nine"] = [268,-17956]
U[[180,181], "ten"] = [270,-18225]
U[180, 5:15] = [272,274,276,278,280,282,284,286,288,290]
U[181, 5:15] = [-18496,-18769,-19044,-19321,-19600,-19881,-20164,-20449,-20736,-21025]
U[[180,181], "paris"] = [292,-21316]
U[[180,181], "london"] = [294,-21609]
U[[180,181], "rome"] = [296,-21904]
U[[180,181], "berlin"] = [298,-22201]
U[[180,181], "madrid"] = [300,-22500]
U[[180,181], "tokyo"] = [302,-22801]
U[[180,181], "beijing"] = [304,-23104]
U[[180,181], "ottawa"] = [306,-23409]
U[[180,181], "washington"] = [308,-23716]
U[[180,181], "delhi"] = [310,-24025]
U[[180,181], "canberra"] = [312,-24336]
U[[180,181], "brasilia"] = [314,-24649]
U[[180,181], "moscow"] = [316,-24964]
U[[180,181], "seoul"] = [318,-25281]
U[[180,181], "cairo"] = [320,-25600]
U[[180,181], "athens"] = [322,-25921]
U[[180,181], "lisbon"] = [324,-26244]
U[[180,181], "dublin"] = [326,-26569]
U[[180,181], "oslo"] = [328,-26896]
U[[180,181], "stockholm"] = [330,-27225]
U[[180,181], "helsinki"] = [332,-27556]
U[[180,181], "copenhagen"] = [334,-27889]
U[[180,181], "bern"] = [336,-28224]
U[[180,181], "amsterdam"] = [338,-28561]
U[[180,181], "vienna"] = [340,-28900]
U[[180,181], "warsaw"] = [342,-29241]
U[[180,181], "kyiv"] = [344,-29584]
U[[180,181], "ankara"] = [346,-29929]
U[[180,181], "bangkok"] = [348,-30276]
U[[180,181], "hanoi"] = [350,-30625]
U[[180,181], "jakarta"] = [352,-30976]
U[[180,181], "islamabad"] = [354,-31329]
U[[180,181], "tehran"] = [356,-31684]
U[[180,181], "baghdad"] = [358,-32041]
U[[180,181], "jerusalem"] = [360,-32400]
U[[180,181], "riyadh"] = [362,-32761]
U[[180,181], "doha"] = [364,-33124]
U[[180,181], "nairobi"] = [366,-33489]
U[[180,181], "pretoria"] = [368,-33856]
U[[180,181], "wellington"] = [370,-34225]
U[[180,181], "lima"] = [372,-34596]
U[[180,181], "santiago"] = [374,-34969]
U[[180,181], "havana"] = [376,-35344]
U[[180,181], "caracas"] = [378,-35721]
U[[180,181], "montevideo"] = [380,-36100]
U[[180,181], "sam"] = [382,-36481]
U[[180,181], "altman"] = [384,-36864]
U[[180,181], "elon"] = [386,-37249]
U[[180,181], "musk"] = [388,-37636]
U[[180,181], "satya"] = [390,-38025]
U[[180,181], "nadella"] = [392,-38416]
U[[180,181], "sundar"] = [394,-38809]
U[[180,181], "pichai"] = [396,-39204]
U[[180,181], "jensen"] = [398,-39601]
U[[180,181], "huang"] = [400,-40000]
U[[180,181], "mark"] = [402,-40401]
U[[180,181], "zuckerberg"] = [404,-40804]
U[[180,181], "tim"] = [406,-41209]
U[[180,181], "cook"] = [408,-41616]
U[[180,181], "dario"] = [410,-42025]
U[[180,181], "amodei"] = [412,-42436]
U[[180,181], "demis"] = [414,-42849]
U[[180,181], "hassabis"] = [416,-43264]
U[[180,181], "bill"] = [418,-43681]
U[[180,181], "gates"] = [420,-44100]
U[[180,181], "steve"] = [422,-44521]
U[[180,181], "jobs"] = [424,-44944]
U[[180,181], "jeff"] = [426,-45369]
U[[180,181], "bezos"] = [428,-45796]
U[[180,181], "openai"] = [430,-46225]
U[[180,181], "microsoft"] = [432,-46656]
U[[180,181], "google"] = [434,-47089]
U[[180,181], "meta"] = [436,-47524]
U[[180,181], "spacex"] = [438,-47961]
U[[180,181], "tesla"] = [440,-48400]
U[[180,181], "nvidia"] = [442,-48841]
U[[180,181], "anthropic"] = [444,-49284]
U[[180,181], "claude"] = [446,-49729]
U[[180,181], "chatgpt"] = [448,-50176]
U[[180,181], "gemini"] = [450,-50625]
U[[180,181], "windows"] = [452,-51076]
U[[180,181], "android"] = [454,-51529]
U[[180,181], "iphone"] = [456,-51984]
U[[180,181], "earth"] = [458,-52441]
U[[180,181], "mars"] = [460,-52900]
U[[180,181], "jupiter"] = [462,-53361]
U[[180,181], "saturn"] = [464,-53824]
U[[180,181], "mercury"] = [466,-54289]
U[[180,181], "venus"] = [468,-54756]
U[[180,181], "neptune"] = [470,-55225]
U[[180,181], "uranus"] = [472,-55696]
U[[180,181], "sun"] = [474,-56169]
U[[180,181], "moon"] = [476,-56644]
U[[180,181], "pacific"] = [478,-57121]
U[[180,181], "asia"] = [480,-57600]
U[[180,181], "africa"] = [482,-58081]
U[[180,181], "europe"] = [484,-58564]
U[[180,181], "america"] = [486,-59049]
U[[180,181], "antarctica"] = [488,-59536]
U[[180,181], "oceania"] = [490,-60025]
U[[180,181], "everest"] = [492,-60516]
U[[180,181], "nile"] = [494,-61009]
U[[180,181], "amazon"] = [496,-61504]
U[[180,181], "sahara"] = [498,-62001]
U[[180,181], "einstein"] = [500,-62500]
U[[180,181], "newton"] = [502,-63001]
U[[180,181], "shakespeare"] = [504,-63504]
U[[180,181], "mozart"] = [506,-64009]
U[[180,181], "leonardo"] = [508,-64516]
U[[180,181], "vinci"] = [510,-65025]
U[[180,181], "darwin"] = [512,-65536]
U[[180,181], "edison"] = [514,-66049]
U[[180,181], "armstrong"] = [516,-66564]
U[[180,181], "gagarin"] = [518,-67081]
U[[180,181], "air"] = [520,-67600]
U[[180,181], "iron"] = [522,-68121]
U[[180,181], "gold"] = [524,-68644]
U[[180,181], "silver"] = [526,-69169]
U[[180,181], "salt"] = [528,-69696]
U[[180,181], "protein"] = [530,-70225]
U[[180,181], "heart"] = [532,-70756]
U[[180,181], "brain"] = [534,-71289]
U[[180,181], "blood"] = [536,-71824]
U[[180,181], "leaf"] = [538,-72361]
U[[180,181], "tree"] = [540,-72900]
U[[180,181], "fish"] = [542,-73441]
U[[180,181], "elephant"] = [544,-73984]
U[[180,181], "mouse"] = [546,-74529]
U[[180,181], "rabbit"] = [548,-75076]
U[[180,181], "bee"] = [550,-75625]
U[[180,181], "snow"] = [552,-76176]
U[[180,181], "ice"] = [554,-76729]
U[[180,181], "fire"] = [556,-77284]
U[[180,181], "light"] = [558,-77841]
U[[180,181], "dark"] = [560,-78400]
U[[180,181], "white"] = [562,-78961]
U[[180,181], "black"] = [564,-79524]
U[[180,181], "up"] = [566,-80089]
U[[180,181], "down"] = [568,-80656]
U[[180,181], "left"] = [570,-81225]
U[[180,181], "north"] = [572,-81796]
U[[180,181], "south"] = [574,-82369]
U[[180,181], "east"] = [576,-82944]
U[[180,181], "west"] = [578,-83521]
U[[180,181], "old"] = [580,-84100]
U[[180,181], "young"] = [582,-84681]
U[[180,181], "long"] = [584,-85264]
U[[180,181], "short"] = [586,-85849]
U[[180,181], "tall"] = [588,-86436]
U[[180,181], "full"] = [590,-87025]
U[[180,181], "dry"] = [592,-87616]
U[[180,181], "wet"] = [594,-88209]
U[[180,181], "fast"] = [596,-88804]
U[[180,181], "slow"] = [598,-89401]
U[[180,181], "easy"] = [600,-90000]
U[[180,181], "difficult"] = [602,-90601]
U[[180,181], "clean"] = [604,-91204]
U[[180,181], "dirty"] = [606,-91809]
U[[180,181], "strong"] = [608,-92416]
U[[180,181], "soft"] = [610,-93025]
U[[180,181], "hard"] = [612,-93636]
U[[180,181], "loud"] = [614,-94249]
U[[180,181], "quiet"] = [616,-94864]
U[[180,181], "open"] = [618,-95481]
U[[180,181], "shut"] = [620,-96100]
U[[180,181], "true"] = [622,-96721]
U[[180,181], "false"] = [624,-97344]
U[[180,181], "beautiful"] = [626,-97969]
U[[180,181], "bad"] = [628,-98596]
U[[180,181], "poor"] = [630,-99225]
U[[180,181], "rich"] = [632,-99856]
U[[180,181], "night"] = [634,-100489]
U[[180,181], "morning"] = [636,-101124]
U[[180,181], "summer"] = [638,-101761]
U[[180,181], "winter"] = [640,-102400]
U[[180,181], "start"] = [642,-103041]
U[[180,181], "end"] = [644,-103684]
U[[180,181], "come"] = [646,-104329]
U[[180,181], "go"] = [648,-104976]
U[[180,181], "win"] = [650,-105625]
U[[180,181], "lose"] = [652,-106276]
U[[180,181], "give"] = [654,-106929]
U[[180,181], "warm"] = [656,-107584]
U[[180,181], "cool"] = [658,-108241]
U[[180,181], "high"] = [660,-108900]
U[[180,181], "low"] = [662,-109561]
U[[180,181], "male"] = [664,-110224]
U[[180,181], "female"] = [666,-110889]
U[[180,181], "man"] = [668,-111556]
U[[180,181], "woman"] = [670,-112225]
U[[180,181], "boy"] = [672,-112896]
U[[180,181], "girl"] = [674,-113569]
U[[180,181], "brother"] = [676,-114244]
U[[180,181], "sister"] = [678,-114921]
U[[180,181], "father"] = [680,-115600]
U[[180,181], "mother"] = [682,-116281]
U[[180,181], "spring"] = [684,-116964]
U[[180,181], "word"] = [686,-117649]
U[[180,181], "tom"] = [688,-118336]
U[[180,181], "sara"] = [690,-119025]
U[[180,181], "anna"] = [692,-119716]
U[[180,181], "john"] = [694,-120409]
U[[180,181], "mary"] = [696,-121104]
U[[180,181], "james"] = [698,-121801]
U[[180,181], "emma"] = [700,-122500]
U[[180,181], "liam"] = [702,-123201]
U[[180,181], "olivia"] = [704,-123904]
U[[180,181], "noah"] = [706,-124609]
U[[180,181], "ava"] = [708,-125316]
U[[180,181], "mia"] = [710,-126025]
U[[180,181], "lucas"] = [712,-126736]
U[[180,181], "ella"] = [714,-127449]
U[[180,181], "jack"] = [716,-128164]
U[[180,181], "lily"] = [718,-128881]
U[[180,181], "ben"] = [720,-129600]
U[[180,181], "max"] = [722,-130321]
U[[180,181], "leo"] = [724,-131044]
U[[180,181], "zoe"] = [726,-131769]
U[[180,181], "amy"] = [728,-132496]
U[[180,181], "kate"] = [730,-133225]
U[[180,181], "mike"] = [732,-133956]
U[[180,181], "dan"] = [734,-134689]
U[[180,181], "alex"] = [736,-135424]
U[[180,181], "maria"] = [738,-136161]
U[[180,181], "david"] = [740,-136900]
U[[180,181], "paul"] = [742,-137641]
U[[180,181], "peter"] = [744,-138384]
U[[180,181], "number"] = [746,-139129]
U[[180,181], "an"] = [748,-139876]
U[[180,181], "important"] = [750,-140625]
U[[180,181], "for"] = [752,-141376]
U[[180,181], "sport"] = [754,-142129]
U[[180,181], "people"] = [756,-142884]
U[[180,181], "here"] = [758,-143641]
U[[180,181], "angry"] = [760,-144400]
U[[180,181], "ill"] = [762,-145161]
U[[180,181], "afraid"] = [764,-145924]
U[[180,181], "trust"] = [766,-146689]
U[[180,181], "animal"] = [768,-147456]
U[[180,181], "fruit"] = [770,-148225]
U[[180,181], "berry"] = [772,-148996]
U[[180,181], "feeble"] = [774,-149769]
```