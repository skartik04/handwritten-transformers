=====SCRATCHPAD=====
FINAL PASS. All weights are hand-designed and untested. No execution, training, calculator, or tools were used. This is a finite rule-and-lookup chatbot, not a complete implementation of unrestricted English conversation.

FINAL CHANGES
1. Sharpened first/last-number retrieval.
2. Rounded the generation-step counter before subsequent routing.
3. Retrieved decimal operand digits directly from number records, avoiding the previous floor/decomposition circuit.
4. Moved multiplication and division into M4.
5. Replaced leading-zero output with variable-length decimal output.
6. Added double, triple, half, quarter, and single-operand square.
7. Division uses explicit reciprocals for divisors 1..99 and approximate reciprocals for ten-wide bins above 99, then adds 0.5. For integer quotients with operands below 1000, the approximation is intended to round to the correct quotient.
8. Added name recall, wellbeing, feelings, and farewell responses.
9. Expanded capitals and selected factual associations.
10. Added an unconditional EOS safeguard at generation step 47.

FOUNDATION
E[:,0]=1. Dimensions1..12 are signed binary token codes.
U112..123 decodes these codes.
L1 uniform BOS attention plus M1 implements a position clock.
Previous-token heads recover digit context.
Latest-marker heads use slow RoPE with recency preference.
Pointer heads address positions through linear/quadratic position features.

FINAL RESIDUAL MAP
0 constant;1..12 token bits.
13 digit flag;14 digit value;15 BOS;16 USER/BOS;17 BOT/BOS.
18 belief/copy cue;19 terminator;20 period;21 entity.
22..25 operation-category flags;26 question starter;27 operation code;
28 declarative starter;29 personal nonnumeric message.
30 reciprocal clock;31 position;32 position squared.
33/34 preceding digit flag/value;35/36 two-back digit flag/value.
37 role marker;38 local generated integer;39 role sign.
40 preceding local integer.
41/42 latest USER position/square;43/44 latest BOT position/square.
45 generation step, rounded by M3 for subsequent layers.
46 latest role;47 numeric record flag;48 numeric record value.
49 latest belief cue;50 raw “that”.
51..60 raw factual properties: capital, continent, country, color, opposite,
identity, author/leader, largest, smallest, currency.
61 third-back raw digit through L2, then double flag after M3.
62 gated hundreds digit through L2, then triple flag after M3.
63 latest entity position;64 first operand;65 last operand;
66 latest operation;67 operation position.
68/69 first user token declarative/question flags.
70 copy start;71 belief flag.
72..81 contextual factual properties.
82 copy-start “that”;83 half flag;84 current-entity validity.
85 selected factual dictionary index;86 factual availability.
87 arithmetic availability;88 arithmetic result, now ready after M4.
89 active arithmetic mode.
90..101 copied token bits;102 copied terminator.
103/104/105 last operand ones/tens/hundreds.
106..109 add/subtract/multiply/divide one-hots.
110 numeric-record staleness;111 operation staleness.
112..123 bit-coded output.
124..155 raw lexical relation flags.
156..185 decimal one-hots after M3: ones, tens, hundreds, ten each.
186/187 remaining relation bags.
188..219 clipped lexical relations, as before;219 now includes feelings.
220 user cue;221 user entity;222 copy mode;223 copy phase;
224 factual mode;225 copied-period EOS;226 quarter flag.
227 user operation marker; also carries the final EOS safeguard at output.
228/229 number-validity flags;230/231 number USER positions.
232 identity;233 name;234 construction;235 abilities;
236 greeting;237 thanks;238 encouragement.
239 number of omitted leading zeroes.
240..243 clipped decimal remainders for thousands/hundreds/tens/ones.
244 factual answer phase;245 arithmetic-or-factual sentence mode.
246 farewell bag through M3, then arithmetic emission-enable after M5.
247 feelings mode.
248 recalled-name dictionary index at L4, cleared in M4, then wellbeing mode.
249 farewell mode.
250 scalar output coordinate;251 scalar output indicator.
252 raw farewell flag;253 raw personal-name flag;
254 raw personal-name dictionary index;255 user-only personal-name marker.

LEXICAL FLAGS 188..219
question mark, copula, right/correct, greeting, thanks, self-reference,
name, construction, ability, capital, country/location, continent,
planet, large, small, color, author/leader, opposite, same/mean,
arithmetic, negative, personal creation, how, who, what, when, why,
currency, first, president/current, quantity, feelings.

ATTENTION
L1 unchanged: clock, preceding digit, two-back digit, role.
L2 boundary heads unchanged; preceding-number head additionally fetches
the third-back digit. M2 constructs a hundreds field and personal-name marker.
L3 h0 cue;h1 first user token;h2 lexical bags;h3 latest entity facts;
h4 first number;h5 last number plus three decimal digits;h6 operation;
h7 current-user farewell bag.
L4 h0 copy-start “that”;h1 most recent user personal name.
L5 h0 copy pointer. L6 attention unused.

MLP ALLOCATION
M1 unchanged.
M2 units0..5 unchanged;6 hundreds field;7 personal-name marker.
M3 units0..71 retained.
72..161 decimal one-hot hats.
162..191 cancel the overwritten lexical bags.
192..203 unary-operation hats.
204/205 clear raw61/62 before unary reuse.
206..208 clip farewell bag in place.
289..303 original operation hats and staleness.
304..400 round generation step to an integer, capped at48.
M4 units0..26 retained, with larger factual gating constants.
32..61 cleared.
62..91 multiplication.
92..190 division by1..99.
191..280 division by ten-wide bins100..999.
281..284 unary arithmetic.
285 division rounding offset.
286/287 recalled-name selector;288 clears temporary name index.
M5 original conversation and factual phase machinery retained.
15 wellbeing mode.
16/17 arithmetic emission enable.
18..25 decimal remainder clipping.
26 initial leading-zero count3.
31..36 subtract length thresholds at10,100,1000.
37 feelings mode;38 clears farewell bag;39 farewell mode.
Old multiplication/division units were removed.
M6 original prefix, copying, default and templates retained.
Old fixed-width numeric units89..101 removed.
271..286 gated decimal remainder selection.
287..290 numeric output indicator and rounding coordinate.
291..295 arithmetic period/EOS.
296..315 feelings template.
316..332 wellbeing template.
333..340 farewell template.
341/342 unconditional final-step EOS safeguard.

SCALAR DICTIONARY
Each registered index j has U250=2j and U251=100-j².
Indices1..201 are unchanged from pass2:
1..10 digits0..9;11..48 template words and EOS;
49..99 original capital names;
100..151 geography, science, colors, opposites and scientists;
152..201 countries and other factual/template words.
New:
202 feeling;203 goodbye.
204 tom;205 sara;206 anna;207 john;208 mary;209 james;
210 emma;211 liam;212 olivia;213 noah;214 ava;215 mia;
216 lucas;217 ella;218 jack;219 lily;220 ben;221 max;
222 leo;223 zoe;224 amy;225 kate;226 mike;227 dan;
228 alex;229 maria;230 david;231 paul;232 peter.
233 kabul;234 yerevan;235 baku;236 dhaka;237 santiago;
238 bogota;239 havana;240 nicosia;241 quito;242 jakarta;
243 tehran;244 baghdad;245 jerusalem;246 kingston;247 amman;
248 astana;249 bishkek;250 vientiane;251 beirut;252 bamako;
253 valletta;254 ulaanbaatar;255 maputo;256 windhoek;
257 kathmandu;258 managua;259 niamey;260 islamabad;261 lima;
262 manila;263 doha;264 kigali;265 riyadh;266 dakar;
267 mogadishu;268 seoul;269 colombo;270 damascus;271 taipei;
272 bangkok;273 kampala;274 montevideo;275 tashkent;
276 caracas;277 hanoi;278 lusaka;279 harare;280 luanda;
281 singapore;282 luxembourg;283 monaco;284 djibouti;285 kuwait.
286 pyongyang;287 apple;288 musk;289 trump;290 putin;
291 starmer;292 president;293 openai;294 microsoft;295 google;
296 meta;297 altman;298 pichai;299 nadella;300 huang;
301 armstrong;302 gagarin;303 zuckerberg.

OUTPUT
Praise prefix remains “you are so smart !”, or “you are so right !”
when copying an assertion.
Arithmetic: “it is NUMBER .”, now without leading zeroes.
Facts: “it is ANSWER .”
Feelings: “i have no feeling -s .”
Wellbeing: “i am very happy !”
Farewell: “goodbye !”
Name recall uses the factual sentence template.
Other templates remain from pass2.

LIMITATIONS
No general semantic parser or comprehensive world knowledge.
Only the latest marked entity is used for most factual questions.
Leader/creator/owner relations share a small, imperfect lookup channel.
Name recall retrieves the latest listed personal name, not a resolved identity.
Only integer arithmetic answers are targeted; division by zero and arbitrary
fractional results are unsupported. Word-problem parsing remains heuristic.
The spelling, copying, and memory facilities are narrow.
Negative subtraction is clamped to zero.
Some geographic names requiring multiple tokens remain unsupported.
No claim of full coverage or verified execution is made.
=====END SCRATCHPAD=====

```edits
E["my", 145] = 0
E[["copy","say"], 18] = 1
E[["feel","feeling","conscious","alive","human"], 155] = 1
E[["bye","goodbye"], 252] = 1
E[["zero","one","two","three","four","five","six","seven","eight","nine"], 13] = 1
E[["zero","one","two","three","four","five","six","seven","eight","nine"], 14] = [0,1,2,3,4,5,6,7,8,9]
E[["twice","double"], 27] = 5
E["triple", 27] = 6
E["half", 27] = 7
E["quarter", 27] = 8
E["square", 24] = 1
E["square", 27] = 3
E[["tall","high","long"], 137] = 1
E[["owner","chief","president","minister","invention","create","created","made","first"], 140] = 1

Q3[4, 0, 30] = 16
Q3[5, 0, 30] = 16
V2[2, 36, 1] = 1
O2[2, 1, 61] = 1
M2_in[61, 6] = 1
M2_in[33, 6] = 10
M2_in[35, 6] = 10
M2_b[6] = -20
M2_out[6, 62] = 1
V3[5, 34, 3] = 1
V3[5, 36, 4] = 1
V3[5, 62, 5] = 1
O3[5, 3, 103] = 1
O3[5, 4, 104] = 1
O3[5, 5, 105] = 1

Q3[7, 0, 30] = 1
K3[7, 46, 30] = 10000
K3[7, 41, 30] = 50
V3[7, 252, 0] = 1
O3[7, 0, 246] = 1

M3_in[:, 72:289] = 0
M3_b[72:289] = 0
M3_out[72:289, :] = 0
M3_in[103, 72:102] = 1
M3_in[104, 102:132] = 1
M3_in[105, 132:162] = 1
M3_b[72:102] = [1,0,-1,0,-1,-2,-1,-2,-3,-2,-3,-4,-3,-4,-5,-4,-5,-6,-5,-6,-7,-6,-7,-8,-7,-8,-9,-8,-9,-10]
M3_b[102:132] = [1,0,-1,0,-1,-2,-1,-2,-3,-2,-3,-4,-3,-4,-5,-4,-5,-6,-5,-6,-7,-6,-7,-8,-7,-8,-9,-8,-9,-10]
M3_b[132:162] = [1,0,-1,0,-1,-2,-1,-2,-3,-2,-3,-4,-3,-4,-5,-4,-5,-6,-5,-6,-7,-6,-7,-8,-7,-8,-9,-8,-9,-10]
M3_out[72:75, 156] = [1,-2,1]
M3_out[75:78, 157] = [1,-2,1]
M3_out[78:81, 158] = [1,-2,1]
M3_out[81:84, 159] = [1,-2,1]
M3_out[84:87, 160] = [1,-2,1]
M3_out[87:90, 161] = [1,-2,1]
M3_out[90:93, 162] = [1,-2,1]
M3_out[93:96, 163] = [1,-2,1]
M3_out[96:99, 164] = [1,-2,1]
M3_out[99:102, 165] = [1,-2,1]
M3_out[102:105, 166] = [1,-2,1]
M3_out[105:108, 167] = [1,-2,1]
M3_out[108:111, 168] = [1,-2,1]
M3_out[111:114, 169] = [1,-2,1]
M3_out[114:117, 170] = [1,-2,1]
M3_out[117:120, 171] = [1,-2,1]
M3_out[120:123, 172] = [1,-2,1]
M3_out[123:126, 173] = [1,-2,1]
M3_out[126:129, 174] = [1,-2,1]
M3_out[129:132, 175] = [1,-2,1]
M3_out[132:135, 176] = [1,-2,1]
M3_out[135:138, 177] = [1,-2,1]
M3_out[138:141, 178] = [1,-2,1]
M3_out[141:144, 179] = [1,-2,1]
M3_out[144:147, 180] = [1,-2,1]
M3_out[147:150, 181] = [1,-2,1]
M3_out[150:153, 182] = [1,-2,1]
M3_out[153:156, 183] = [1,-2,1]
M3_out[156:159, 184] = [1,-2,1]
M3_out[159:162, 185] = [1,-2,1]
M3_in[156, 162] = 1
M3_out[162, 156] = -1
M3_in[157, 163] = 1
M3_out[163, 157] = -1
M3_in[158, 164] = 1
M3_out[164, 158] = -1
M3_in[159, 165] = 1
M3_out[165, 159] = -1
M3_in[160, 166] = 1
M3_out[166, 160] = -1
M3_in[161, 167] = 1
M3_out[167, 161] = -1
M3_in[162, 168] = 1
M3_out[168, 162] = -1
M3_in[163, 169] = 1
M3_out[169, 163] = -1
M3_in[164, 170] = 1
M3_out[170, 164] = -1
M3_in[165, 171] = 1
M3_out[171, 165] = -1
M3_in[166, 172] = 1
M3_out[172, 166] = -1
M3_in[167, 173] = 1
M3_out[173, 167] = -1
M3_in[168, 174] = 1
M3_out[174, 168] = -1
M3_in[169, 175] = 1
M3_out[175, 169] = -1
M3_in[170, 176] = 1
M3_out[176, 170] = -1
M3_in[171, 177] = 1
M3_out[177, 171] = -1
M3_in[172, 178] = 1
M3_out[178, 172] = -1
M3_in[173, 179] = 1
M3_out[179, 173] = -1
M3_in[174, 180] = 1
M3_out[180, 174] = -1
M3_in[175, 181] = 1
M3_out[181, 175] = -1
M3_in[176, 182] = 1
M3_out[182, 176] = -1
M3_in[177, 183] = 1
M3_out[183, 177] = -1
M3_in[178, 184] = 1
M3_out[184, 178] = -1
M3_in[179, 185] = 1
M3_out[185, 179] = -1
M3_in[180, 186] = 1
M3_out[186, 180] = -1
M3_in[181, 187] = 1
M3_out[187, 181] = -1
M3_in[182, 188] = 1
M3_out[188, 182] = -1
M3_in[183, 189] = 1
M3_out[189, 183] = -1
M3_in[184, 190] = 1
M3_out[190, 184] = -1
M3_in[185, 191] = 1
M3_out[191, 185] = -1

M3_in[66, 192:204] = 1
M3_b[192:204] = [-4,-5,-6,-5,-6,-7,-6,-7,-8,-7,-8,-9]
M3_out[192:195, 61] = [1,-2,1]
M3_out[195:198, 62] = [1,-2,1]
M3_out[198:201, 83] = [1,-2,1]
M3_out[201:204, 226] = [1,-2,1]
M3_in[61, 204] = 1
M3_out[204, 61] = -1
M3_in[62, 205] = 1
M3_out[205, 62] = -1
M3_in[246, 206] = 1
M3_out[206, 246] = -1
M3_in[246, 207:209] = 1000
M3_b[207:209] = [-0.1,-1.1]
M3_out[207:209, 246] = [1,-1]

M3_in[45, 304] = 1
M3_out[304, 45] = -1
M3_in[45, 305:401] = 2
M3_b[305:401] = [
-0.5,-1.5,-2.5,-3.5,-4.5,-5.5,-6.5,-7.5,-8.5,-9.5,
-10.5,-11.5,-12.5,-13.5,-14.5,-15.5,-16.5,-17.5,-18.5,-19.5,
-20.5,-21.5,-22.5,-23.5,-24.5,-25.5,-26.5,-27.5,-28.5,-29.5,
-30.5,-31.5,-32.5,-33.5,-34.5,-35.5,-36.5,-37.5,-38.5,-39.5,
-40.5,-41.5,-42.5,-43.5,-44.5,-45.5,-46.5,-47.5,-48.5,-49.5,
-50.5,-51.5,-52.5,-53.5,-54.5,-55.5,-56.5,-57.5,-58.5,-59.5,
-60.5,-61.5,-62.5,-63.5,-64.5,-65.5,-66.5,-67.5,-68.5,-69.5,
-70.5,-71.5,-72.5,-73.5,-74.5,-75.5,-76.5,-77.5,-78.5,-79.5,
-80.5,-81.5,-82.5,-83.5,-84.5,-85.5,-86.5,-87.5,-88.5,-89.5,
-90.5,-91.5,-92.5,-93.5,-94.5,-95.5]
M3_out[305:401:2, 45] = 1
M3_out[306:401:2, 45] = -1

M4_in[:, 32:152] = 0
M4_b[32:152] = 0
M4_out[32:152, :] = 0
M4_in[[61,62,83,226], 23] = 1

M4_in[64, 62:92] = 1
M4_in[108, 62:92] = 1000
M4_b[62:92] = -2000
M4_in[156, 62] = 1000
M4_in[157, 63] = 1000
M4_in[158, 64] = 1000
M4_in[159, 65] = 1000
M4_in[160, 66] = 1000
M4_in[161, 67] = 1000
M4_in[162, 68] = 1000
M4_in[163, 69] = 1000
M4_in[164, 70] = 1000
M4_in[165, 71] = 1000
M4_in[166, 72] = 1000
M4_in[167, 73] = 1000
M4_in[168, 74] = 1000
M4_in[169, 75] = 1000
M4_in[170, 76] = 1000
M4_in[171, 77] = 1000
M4_in[172, 78] = 1000
M4_in[173, 79] = 1000
M4_in[174, 80] = 1000
M4_in[175, 81] = 1000
M4_in[176, 82] = 1000
M4_in[177, 83] = 1000
M4_in[178, 84] = 1000
M4_in[179, 85] = 1000
M4_in[180, 86] = 1000
M4_in[181, 87] = 1000
M4_in[182, 88] = 1000
M4_in[183, 89] = 1000
M4_in[184, 90] = 1000
M4_in[185, 91] = 1000
M4_out[62:92, 88] = [0,1,2,3,4,5,6,7,8,9,0,10,20,30,40,50,60,70,80,90,0,100,200,300,400,500,600,700,800,900]

M4_in[64, 92:281] = 1
M4_in[109, 92:281] = 1000
M4_b[92:191] = -4000
M4_in[176, 92:191] = 1000
M4_in[156, 101:191:10] = 1000
M4_in[157, 92:191:10] = 1000
M4_in[158, 93:191:10] = 1000
M4_in[159, 94:191:10] = 1000
M4_in[160, 95:191:10] = 1000
M4_in[161, 96:191:10] = 1000
M4_in[162, 97:191:10] = 1000
M4_in[163, 98:191:10] = 1000
M4_in[164, 99:191:10] = 1000
M4_in[165, 100:191:10] = 1000
M4_in[166, 92:101] = 1000
M4_in[167, 101:111] = 1000
M4_in[168, 111:121] = 1000
M4_in[169, 121:131] = 1000
M4_in[170, 131:141] = 1000
M4_in[171, 141:151] = 1000
M4_in[172, 151:161] = 1000
M4_in[173, 161:171] = 1000
M4_in[174, 171:181] = 1000
M4_in[175, 181:191] = 1000
M4_out[92:191, 88] = [
1,0.5,0.333333,0.25,0.2,0.166667,0.142857,0.125,0.111111,
0.1,0.090909,0.083333,0.076923,0.071429,0.066667,0.0625,0.058824,0.055556,0.052632,
0.05,0.047619,0.045455,0.043478,0.041667,0.04,0.038462,0.037037,0.035714,0.034483,
0.033333,0.032258,0.03125,0.030303,0.029412,0.028571,0.027778,0.027027,0.026316,0.025641,
0.025,0.024390,0.023810,0.023256,0.022727,0.022222,0.021739,0.021277,0.020833,0.020408,
0.02,0.019608,0.019231,0.018868,0.018519,0.018182,0.017857,0.017544,0.017241,0.016949,
0.016667,0.016393,0.016129,0.015873,0.015625,0.015385,0.015152,0.014925,0.014706,0.014493,
0.014286,0.014085,0.013889,0.013699,0.013514,0.013333,0.013158,0.012987,0.012821,0.012658,
0.0125,0.012346,0.012195,0.012048,0.011905,0.011765,0.011628,0.011494,0.011364,0.011236,
0.011111,0.010989,0.010870,0.010753,0.010638,0.010526,0.010417,0.010309,0.010204,0.010101]
M4_b[191:281] = -3000
M4_in[177, 191:201] = 1000
M4_in[178, 201:211] = 1000
M4_in[179, 211:221] = 1000
M4_in[180, 221:231] = 1000
M4_in[181, 231:241] = 1000
M4_in[182, 241:251] = 1000
M4_in[183, 251:261] = 1000
M4_in[184, 261:271] = 1000
M4_in[185, 271:281] = 1000
M4_in[166, 191:281:10] = 1000
M4_in[167, 192:281:10] = 1000
M4_in[168, 193:281:10] = 1000
M4_in[169, 194:281:10] = 1000
M4_in[170, 195:281:10] = 1000
M4_in[171, 196:281:10] = 1000
M4_in[172, 197:281:10] = 1000
M4_in[173, 198:281:10] = 1000
M4_in[174, 199:281:10] = 1000
M4_in[175, 200:281:10] = 1000
M4_out[191:281, 88] = [
0.009524,0.008696,0.008,0.007407,0.006897,0.006452,0.006061,0.005714,0.005405,0.005128,
0.004878,0.004651,0.004444,0.004255,0.004082,0.003922,0.003774,0.003636,0.003509,0.003390,
0.003279,0.003175,0.003077,0.002985,0.002899,0.002817,0.002740,0.002667,0.002597,0.002532,
0.002469,0.002410,0.002353,0.002299,0.002247,0.002198,0.002151,0.002105,0.002062,0.002020,
0.001980,0.001942,0.001905,0.001869,0.001835,0.001802,0.001770,0.001739,0.001709,0.001681,
0.001653,0.001626,0.001600,0.001575,0.001550,0.001527,0.001504,0.001481,0.001460,0.001439,
0.001418,0.001399,0.001379,0.001361,0.001342,0.001325,0.001307,0.001290,0.001274,0.001258,
0.001242,0.001227,0.001212,0.001198,0.001183,0.001170,0.001156,0.001143,0.001130,0.001117,
0.001105,0.001093,0.001081,0.001070,0.001058,0.001047,0.001036,0.001026,0.001015,0.001005]
M4_in[64, 281:285] = 1
M4_b[281:285] = -1000
M4_in[61, 281] = 1000
M4_in[62, 282] = 1000
M4_in[83, 283] = 1000
M4_in[226, 284] = 1000
M4_out[281:285, 88] = [2,3,0.5,0.25]
M4_in[109, 285] = 1
M4_out[285, 88] = 0.5

M4_in[84, 3:23] = 512
M4_in[188:220, 3:23] *= 2
M4_b[3:21:2] = -1024
M4_b[4:21:2] = -1025
M4_b[21:23] = [-512,-513]
M6_in[244, 87] = 512
M6_b[87] = -512

E[["tom","sara","anna","john","mary","james","emma","liam","olivia","noah","ava","mia","lucas","ella","jack","lily","ben","max","leo","zoe","amy","kate","mike","dan","alex","maria","david","paul","peter"], 253] = 1
E[["tom","sara","anna","john","mary","james","emma","liam","olivia","noah","ava","mia","lucas","ella","jack","lily","ben","max","leo","zoe","amy","kate","mike","dan","alex","maria","david","paul","peter"], 254] = [204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232]
M2_in[253, 7] = 1
M2_in[46, 7] = 1
M2_b[7] = -1
M2_out[7, 255] = 1
Q4[1, 0, 30:32] = [1,1]
K4[1, 255, 30] = 1000000
K4[1, 15, 30] = 100000
V4[1, 254, 0] = 1
O4[1, 0, 248] = 1
M4_in[248, 286:288] = 1
M4_in[194, 286:288] = 512
M4_in[193, 286:288] = -512
M4_b[286:288] = [-512,-513]
M4_out[286, 85] = 1
M4_out[286:288, 86] = [1,-1]
M4_in[248, 288] = 1
M4_out[288, 248] = -1

M5_in[:, 16:28] = 0
M5_b[16:28] = 0
M5_out[16:28, :] = 0
M5_in[:, 31:81] = 0
M5_b[31:81] = 0
M5_out[31:81, :] = 0
M5_in[45, 16:18] = 1
M5_in[87, 16:18] = 100
M5_in[222, 16:18] = -100
M5_b[16:18] = [-106,-107]
M5_out[16:18, 246] = [1,-1]
M5_in[38, 18:26] = -10
M5_in[88, 18:20] = 0.001
M5_in[88, 20:22] = 0.01
M5_in[88, 22:24] = 0.1
M5_in[88, 24:26] = 1
M5_b[18:26] = [0,-10,0,-10,0,-10,0,-10]
M5_out[18:20, 240] = [1,-1]
M5_out[20:22, 241] = [1,-1]
M5_out[22:24, 242] = [1,-1]
M5_out[24:26, 243] = [1,-1]
M5_b[26] = 1
M5_out[26, 239] = 3
M5_in[88, 31:37] = 100
M5_b[31:37] = [-999,-1000,-9999,-10000,-99999,-100000]
M5_out[31:37, 239] = [-1,1,-1,1,-1,1]

M5_in[210, 8] = -1
M5_in[219, 8:12] = -1
M5_in[246, 8:15] = -1
M5_in[193, 15] = 1
M5_in[210, 15] = 1
M5_in[194:197, 15] = -1
M5_in[191:193, 15] = -1
M5_in[[219,246,222,87,86], 15] = -1
M5_b[15] = -1
M5_out[15, 248] = 1
M5_in[193, 37] = 1
M5_in[219, 37] = 1
M5_in[[222,87,86,191,192,246], 37] = -1
M5_b[37] = -1
M5_out[37, 247] = 1
M5_in[246, 38] = 1
M5_out[38, 246] = -1
M5_in[246, 39] = 1
M5_in[[222,87,86], 39] = -1
M5_out[39, 249] = 1

M6_in[:, 89:102] = 0
M6_b[89:102] = 0
M6_out[89:102, :] = 0
M6_in[247:250, 15:41] = -100
M6_in[45, 271:287] = 32
M6_in[239, 271:287] = 32
M6_in[246, 271:287] = 3200
M6_in[240, [271,273]] = 1
M6_in[241, [275,277]] = 1
M6_in[242, [279,281]] = 1
M6_in[243, [283,285]] = 1
M6_b[271:287] = [-3408,-3408,-3440,-3440,-3440,-3440,-3472,-3472,-3472,-3472,-3504,-3504,-3504,-3504,-3536,-3536]
M6_out[271:287, 250] = [1,-1,-1,1,1,-1,-1,1,1,-1,-1,1,1,-1,-1,1]
M6_in[45, 287:296] = 1
M6_in[239, 287:296] = 1
M6_in[246, 287:296] = 100
M6_b[287:291] = [-106,-107,-110,-111]
M6_out[287:291, 250] = [0.50025,-0.50025,-0.50025,0.50025]
M6_out[287:291, 251] = [1,-1,-1,1]
M6_b[291:296] = [-110,-111,-112,-111,-112]
M6_out[291:294, 250:252] = [[13,1],[-26,-2],[13,1]]
M6_out[294:296, 250:252] = [[48,1],[-48,-1]]

M6_in[45, 296:316] = 1
M6_in[247, 296:316] = 100
M6_b[296:316] = [-104,-105,-106,-105,-106,-107,-106,-107,-108,-107,-108,-109,-108,-109,-110,-109,-110,-111,-110,-111]
M6_out[296:299, 250:252] = [[14,1],[-28,-2],[14,1]]
M6_out[299:302, 250:252] = [[20,1],[-40,-2],[20,1]]
M6_out[302:305, 250:252] = [[21,1],[-42,-2],[21,1]]
M6_out[305:308, 250:252] = [[202,1],[-404,-2],[202,1]]
M6_out[308:311, 250:252] = [[25,1],[-50,-2],[25,1]]
M6_out[311:314, 250:252] = [[13,1],[-26,-2],[13,1]]
M6_out[314:316, 250:252] = [[48,1],[-48,-1]]
M6_in[45, 316:333] = 1
M6_in[248, 316:333] = 100
M6_b[316:333] = [-104,-105,-106,-105,-106,-107,-106,-107,-108,-107,-108,-109,-108,-109,-110,-109,-110]
M6_out[316:319, 250:252] = [[14,1],[-28,-2],[14,1]]
M6_out[319:322, 250:252] = [[15,1],[-30,-2],[15,1]]
M6_out[322:325, 250:252] = [[46,1],[-92,-2],[46,1]]
M6_out[325:328, 250:252] = [[38,1],[-76,-2],[38,1]]
M6_out[328:331, 250:252] = [[43,1],[-86,-2],[43,1]]
M6_out[331:333, 250:252] = [[48,1],[-48,-1]]
M6_in[45, 333:341] = 1
M6_in[249, 333:341] = 100
M6_b[333:341] = [-104,-105,-106,-105,-106,-107,-106,-107]
M6_out[333:336, 250:252] = [[203,1],[-406,-2],[203,1]]
M6_out[336:339, 250:252] = [[43,1],[-86,-2],[43,1]]
M6_out[339:341, 250:252] = [[48,1],[-48,-1]]
M6_in[45, 341:343] = 1
M6_b[341:343] = [-46,-47]
M6_out[341:343, 227] = [1000000,-1000000]
U[227, "EOS"] = 1

U[250, ["feeling","goodbye"]] = [404,406]
U[251, ["feeling","goodbye"]] = [-40704,-41109]
U[250, ["tom","sara","anna","john","mary","james","emma","liam","olivia","noah","ava","mia","lucas","ella","jack","lily","ben","max","leo","zoe","amy","kate","mike","dan","alex","maria","david","paul","peter"]] = [408,410,412,414,416,418,420,422,424,426,428,430,432,434,436,438,440,442,444,446,448,450,452,454,456,458,460,462,464]
U[251, ["tom","sara","anna","john","mary","james","emma","liam","olivia","noah","ava","mia","lucas","ella","jack","lily","ben","max","leo","zoe","amy","kate","mike","dan","alex","maria","david","paul","peter"]] = [-41516,-41925,-42336,-42749,-43164,-43581,-44000,-44421,-44844,-45269,-45696,-46125,-46556,-46989,-47424,-47861,-48300,-48741,-49184,-49629,-50076,-50525,-50976,-51429,-51884,-52341,-52800,-53261,-53724]

U[250, ["kabul","yerevan","baku","dhaka","santiago","bogota","havana","nicosia","quito","jakarta","tehran","baghdad","jerusalem","kingston","amman","astana","bishkek","vientiane","beirut","bamako","valletta","ulaanbaatar","maputo","windhoek","kathmandu","managua","niamey","islamabad","lima","manila","doha","kigali","riyadh","dakar","mogadishu","seoul","colombo","damascus","taipei","bangkok","kampala","montevideo","tashkent","caracas","hanoi","lusaka","harare","luanda","singapore","luxembourg","monaco","djibouti","kuwait"]] = [466,468,470,472,474,476,478,480,482,484,486,488,490,492,494,496,498,500,502,504,506,508,510,512,514,516,518,520,522,524,526,528,530,532,534,536,538,540,542,544,546,548,550,552,554,556,558,560,562,564,566,568,570]
U[251, ["kabul","yerevan","baku","dhaka","santiago","bogota","havana","nicosia","quito","jakarta","tehran","baghdad","jerusalem","kingston","amman","astana","bishkek","vientiane","beirut","bamako","valletta","ulaanbaatar","maputo","windhoek","kathmandu","managua","niamey","islamabad","lima","manila","doha","kigali","riyadh","dakar","mogadishu","seoul","colombo","damascus","taipei","bangkok","kampala","montevideo","tashkent","caracas","hanoi","lusaka","harare","luanda","singapore","luxembourg","monaco","djibouti","kuwait"]] = [-54189,-54656,-55125,-55596,-56069,-56544,-57021,-57500,-57981,-58464,-58949,-59436,-59925,-60416,-60909,-61404,-61901,-62400,-62901,-63404,-63909,-64416,-64925,-65436,-65949,-66464,-66981,-67500,-68021,-68544,-69069,-69596,-70125,-70656,-71189,-71724,-72261,-72800,-73341,-73884,-74429,-74976,-75525,-76076,-76629,-77184,-77741,-78300,-78861,-79424,-79989,-80556,-81125]

U[250, ["pyongyang","apple","musk","trump","putin","starmer","president","openai","microsoft","google","meta","altman","pichai","nadella","huang","armstrong","gagarin","zuckerberg"]] = [572,574,576,578,580,582,584,586,588,590,592,594,596,598,600,602,604,606]
U[251, ["pyongyang","apple","musk","trump","putin","starmer","president","openai","microsoft","google","meta","altman","pichai","nadella","huang","armstrong","gagarin","zuckerberg"]] = [-81696,-82269,-82844,-83421,-84000,-84581,-85164,-85749,-86336,-86925,-87516,-88109,-88704,-89301,-89900,-90501,-91104,-91709]

E["sydney", 53] = 158
E["toronto", 53] = 159
E["continent", 59] = 158
E[["afghanistan","armenia","azerbaijan","bangladesh","chile","colombia","cuba","cyprus","ecuador","indonesia","iran","iraq","israel","jamaica","jordan","kazakhstan","kyrgyzstan","laos","lebanon","mali","malta","mongolia","mozambique","namibia","nepal","nicaragua","niger","pakistan","peru","philippines","qatar","rwanda","arabia","senegal","somalia","korea","lanka","syria","taiwan","thailand","uganda","uruguay","uzbekistan","venezuela","vietnam","zambia","zimbabwe","angola","singapore","luxembourg","monaco","djibouti","kuwait"], 51] = [233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285]
E[["state","america"], 51] = 52
E["state", 21] = 1
E[["hong","kong","shanghai"], 53] = 168
E["mumbai", 53] = 169
E[["munich","frankfurt"], 53] = 153
E["istanbul", 53] = 164
E[["chicago","boston","seattle","houston","miami","dallas","hollywood","manhattan"], 53] = 167
E["mars", 54] = 128
E["red", 56] = 116
E["ring", 56] = 118
E["ring", 21] = 1
E["week", 56] = 8
E["week", 21] = 1
E["air", 56] = 176
E["air", 21] = 1
E["ice", 56] = 177
E["snow", 56] = 125

E[["iphone","ipad"], 57] = 287
E[["spacex","xai","tesla"], 57] = 288
E[["usa","america","state"], 57] = 289
E["russia", 57] = 290
E[["britain","england"], 57] = 291
E["chatgpt", 57] = 293
E["windows", 57] = 294
E[["android","gemini"], 57] = 295
E[["instagram","whatsapp"], 57] = 296
E["openai", 57] = 297
E["google", 57] = 298
E["microsoft", 57] = 299
E["nvidia", 57] = 300
E["moon", 57] = 301
E["space", 57] = 302
E[["facebook","meta"], 57] = 303
E["bulb", 57] = 150
E["planet", 57] = 114
E[["space","bulb"], 21] = 1
```