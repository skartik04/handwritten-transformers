=====SCRATCHPAD=====
FINAL PASS — HAND-WRITTEN, UNTESTED

All three passes are complete. No tools, execution, training, or numerical testing were used. This is a finite-rule transformer, not a claim of unrestricted English competence.

The earlier architecture remains:
- Residual 0 is constant; 1/2/3 mark BOS/USER/BOT.
- Raw lexical features 4:40 are copied into 40:76 only for user tokens.
- Layer 1 recovers absolute position through uniform BOS attention and an inverse-position spline; fixed-offset heads read preceding digits.
- Layer 2 tracks the current USER segment, echo words, negation, and historical numbers.
- Layer 3 retrieves current-message intent, subject/facts, adjectives, tasks, speaker, and first/last numbers.
- Layer 4 freezes the plan and payload at BOT.
- M4 decodes fixed sentences using a piecewise-linear spline in 64*template + current_position - BOT_position.
- M5 inserts dynamic words and decomposes numerical answers.
- M6 emits decimal digits.
- U uses nearest-code logits 2*code*z-code², with z in residual180 and constant181.

Earlier numerical machinery:
- Parse up to three contiguous digits at their following delimiter.
- Addition and absolute subtraction use first/last operands.
- Multiplication uses the square identity with hinges through sum1008.
- Division uses a reciprocal spline, exact at divisors1..50 and selected larger knots; intermediate squares interpolate so multiplication by the reciprocal is linear.
- Template44 says “the answer is <decimal> .” and emits unpadded results through9999.
- Numeric semantics remain heuristic: extra numbers, mixed operations, and some word-problem phrasing can fail.

FINAL-PASS ADDITIONS

Raw features:
14 queried property: 1 big,2 small,3 hot,4 cold,5 alive,6 dead; 7 red,8 near,9 live are planet-query hints.
31 physical noun marker.
32 size:1 big,2 small.
33 temperature:1 hot,2 cold.
34 life:1 alive,2 not alive.
35 physical-adjective marker.
36 explicit-task marker, preventing physical classification from overriding word tasks.
37 spoken-number marker.
38 spoken-number value0..10.
39 relation:1 continent,2 language,3 leader/president,4 prime minister,5 founder,6 half,7 double,8 triple,9 quarter,10 quantity,12 currency.
235 preference-verb marker.
241 user-personal-pronoun marker.
245 numeric-world-fact value;247 corresponding marker.

New attention:
L1 H6 tracks like/love/enjoy, resetting at USER ->237.
L1 H7 tracks personal vs bot pronouns, resetting at USER ->240.
L2 H4 retrieves current physical noun ->221 marker,222 size,223 temperature,224 life.
L2 H5 retrieves current queried property ->225.
L2 H6 tracks whether an explicit task exists ->226.
L2 H7 retrieves spoken number ->227 value,228 position,229 marker.
L3 H1 additionally retrieves numeric-world-fact value116 and marker130.
L3 H3 additionally retrieves relation113.
L4 H1 retrieves latest user preference object ->242 code,243 presence.
L4 H0 additionally freezes class code114, relation121, alternative facts122/123, alternative presence124, two-word flag125, numeric fact128/129, and adjective class131.

New MLP processing:
M1 units359:361 capture user preference objects into238/239.
M1 units362:364 user-gate numeric-world-fact value/marker into246/248.
M2 units292:328 classify six predicates against noun properties; output98 active,107 unnegated truth,111 answer adjective,112 nonliving flag.
M2 units328:330 choose spoken vs digit number by recency ->230.
M3 units854:859 choose classification templates45..48, accounting for not.
M3 units859:862 distinguish user-preference recall14 from bot-preference reply15.
M3 units862:864 select count template49+N.
M3 units864:920 provide continent ranges for original capital codes.
M3 units920:962 provide languages.
M3 units962:1004 provide selected country leaders.
M3 units1004:1022 provide selected company founders.
M3 units1022:1024 select latest numeric value into115; this now supplies frozen173.
M4 units712:746 implement physical classifications.
M4 units746:925 implement counts0..10.
M4 units925:939 implement preference replies.
M4 units939:955 apply unary half/double/triple/quarter.
M4 units955:957 insert numeric world facts for quantity questions.
M4 units957:972 refine planet answers.
M4 units972:984 supply dollar for four currencies.
M5 units236:241 insert classification, preference, and alternative fact payloads.

New templates:
14 “you like <remembered object> .”
15 “i can talk about <echo object> .”
45 “yes , it is <property> .”
46 “no , it is <property> .”
47 “yes , it is not alive .”
48 “no , it is not alive .”
49..59 “the number -s are <count from1 through N> .”;49 uses0.
Physical replies state the actual property even when the question is negated.

Output-code additions:
388 english,389 french,390 german,391 spanish,392 chinese,393 japanese,394 russian,395 italian,
396 trump,397 macron,398 putin,399 xi,400 jinping,401 zelensky,402 lula,403 starmer,404 carney,
405 merz,406 meloni,407 modi,408 erdogan,409 netanyahu,410 larry,411 page,412 dollar,413 flower,
414 brussels,415 abuja,416 dhaka,417 kathmandu,418 kuala,419 lumpur,420 colombo,421 bucharest,
422 prague,423 budapest,424 reykjavik,425 manila,426 taipei,427 singapore,428 kabul,429 tunis,
430 rabat,431 tashkent,432 harare,433 lusaka,434 dakar,435 accra,
436 hate,437 cruel,438 bitter,439 sweet,440 dangerous,441 late,442 early,443 cry,444 laugh,
445 less,446 more,447 sell,448 buy.

Coverage expanded with additional capitals, languages, continents, leaders, founders, physical properties, echo words, opposites, count-to-ten, preference memory, unary arithmetic, and selected numeric facts. Known limitations include relation ambiguity, approximate division for some larger divisors, simplified physical categories, incomplete vocabulary/knowledge, and unsupported multi-step arithmetic. No runtime behavior has been observed.
=====END SCRATCHPAD=====

```edits
# Physical predicates and noun properties.
E["big", 14] = 1
E["small", 14] = 2
E["hot", 14] = 3
E["cold", 14] = 4
E["alive", 14] = 5
E["dead", 14] = 6
E["living", 11:15] = [6,0,89,5]
E[["big","small","hot","cold","alive","dead","living"], 35] = 1
E[["sun","moon","earth","mountain","ocean","sea","elephant","horse","house","train","plane","tree","cat","dog","bird","rabbit","mouse","bee","ant","insect","flower","leaf","apple","orange","ice","snow","fire","oven","coffee","tea","water","stone","rock","table","chair","book","car","robot","person","man","woman","boy","girl","fish","cow","sheep","goat"], 31] = 1
E[["sun","moon","earth","mountain","ocean","sea","elephant","horse","house","train","plane","tree"], 32] = 1
E[["cat","dog","bird","rabbit","mouse","bee","ant","insect","flower","leaf","apple","orange","book"], 32] = 2
E[["sun","fire","oven","coffee","tea"], 33] = 1
E[["ice","snow"], 33] = 2
E[["elephant","horse","tree","cat","dog","bird","rabbit","mouse","bee","ant","insect","flower","leaf","person","man","woman","boy","girl","fish","cow","sheep","goat"], 34] = 1
E[["sun","moon","earth","mountain","ocean","sea","house","train","plane","apple","orange","ice","snow","fire","oven","coffee","tea","water","stone","rock","table","chair","book","car","robot"], 34] = 2
E[["made","written","weight","hand","created","training","name","age","old","capital","lead","leader","boss","chief","opposite","say","copy","robot","human","program","assistant","colour","color","animal","fruit","number","count","-est","like","love","enjoy","favourite","favorite","continent","language","president","prime","found","half","double","twice","triple","quarter","many","currency","head","owner"], 36] = 1

# Spoken cardinal numbers.
E[["zero","one","two","three","four","five","six","seven","eight","nine","ten"], 37] = 1
E[["zero","one","two","three","four","five","six","seven","eight","nine","ten"], 38] = [0,1,2,3,4,5,6,7,8,9,10]

# Current physical noun, adjective, task flag, and spoken number.
Q2[4:8, 0, 30] = 100
K2[4:8, 2, 30:32] = [1000,-10000]
K2[4, 67, 30:32] = [1000,-10000]
K2[5, 71, 30:32] = [1000,-10000]
K2[6, 72, 30:32] = [1000,-10000]
K2[7, 73, 30:32] = [1000,-10000]
V2[4, 67, 0] = 1
V2[4, 68, 1] = 1
V2[4, 69, 2] = 1
V2[4, 70, 3] = 1
O2[4, 0, 221] = 1
O2[4, 1, 222] = 1
O2[4, 2, 223] = 1
O2[4, 3, 224] = 1
V2[5, 50, 0] = 1
O2[5, 0, 225] = 1
V2[6, 72, 0] = 1
O2[6, 0, 226] = 1
V2[7, 74, 0] = 1
V2[7, 201, 1] = 1
V2[7, 73, 2] = 1
O2[7, 0, 227] = 1
O2[7, 1, 228] = 1
O2[7, 2, 229] = 1

# Property-table matches.
M2_in[225, 292:328] = 1
M2_in[221, 292:328] = 1000
M2_in[226, 292:328] = -1000
M2_in[222, 292:304] = 16
M2_in[223, 304:316] = 16
M2_in[224, 316:328] = 16
M2_b[292:328] = [
-1016,-1017,-1018,-1017,-1018,-1019,-1032,-1033,-1034,-1033,-1034,-1035,
-1018,-1019,-1020,-1019,-1020,-1021,-1034,-1035,-1036,-1035,-1036,-1037,
-1020,-1021,-1022,-1021,-1022,-1023,-1036,-1037,-1038,-1037,-1038,-1039]
M2_out[292:328:3, 98] = 1
M2_out[293:328:3, 98] = -2
M2_out[294:328:3, 98] = 1
M2_out[292:295, 107] = [1,-2,1]
M2_out[301:307, 107] = [1,-2,1,1,-2,1]
M2_out[313:319, 107] = [1,-2,1,1,-2,1]
M2_out[325:328, 107] = [1,-2,1]
M2_out[292:304, 111] = [87,-174,87,87,-174,87,5,-10,5,5,-10,5]
M2_out[304:316, 111] = [86,-172,86,86,-172,86,85,-170,85,85,-170,85]
M2_out[316:328, 111] = [88,-176,88,88,-176,88,88,-176,88,88,-176,88]
M2_out[322:328, 112] = [1,-2,1,1,-2,1]

# Choose the more recent spoken or digit number.
M2_in[228, 328:330] = 1
M2_in[220, 328:330] = -1
M2_in[229, 328:330] = 1000
M2_in[100, 328:330] = -256
M2_b[328:330] = [-744,-745]
M2_out[328:330, 230] = [1,-1]

# Physical replies override ordinary conversational selection.
M3_in[98, 0:37] = -100000
M3_in[98, 854] = 1
M3_in[102, 854:859] = -1000
M3_out[854, 141] = 45
M3_in[107, 855:858] = 1
M3_in[90, 855:858] = -1
M3_in[98, 855:858] = 8
M3_b[855:858] = [-7,-8,-9]
M3_out[855:858, 141] = [1,-2,1]
M3_in[112, 858] = 1
M3_out[858, 141] = 2
V4[0, 111, 18] = 1
O4[0, 18, 114] = 1

# Preference capture.
E[["like","love","enjoy"], 235] = 1
E[["i","my","me","myself"], 241] = 1
E[["like","love","enjoy","favourite","favorite"], 16:18] = [7,14]
Q1[6:8, 0, 30] = 100
K1[6:8, 2, 30:32] = [1000,-10000]
K1[6, 235, 30:32] = [1000,-10000]
K1[7, 28, 30:32] = [1000,-10000]
V1[6, 235, 0] = 1
O1[6, 0, 237] = 1
V1[7, 241, 0] = 1
O1[7, 0, 240] = 1
M1_in[20, 359] = 1
M1_in[202, 359] = 1000
M1_in[237, 359] = 1000
M1_in[240, 359] = 1000
M1_b[359] = -3000
M1_out[359, 238] = 1
M1_in[26, 360] = 1
M1_in[202, 360] = 1
M1_in[237, 360] = 1
M1_in[240, 360] = 1
M1_b[360] = -3
M1_out[360, 239] = 1
Q4[1, 0, 30] = 100
K4[1, 239, 30:32] = [1000,-10000]
V4[1, 238, 0] = 1
V4[1, 239, 1] = 1
O4[1, 0, 242] = 1
O4[1, 1, 243] = 1
M3_in[84, 859:862] = 1
M3_in[87, 859:862] = 64
M3_in[102, 859:862] = -100000
M3_in[98, 859:862] = -100000
M3_b[859:862] = [-141,-142,-143]
M3_out[859:862, 141] = [1,-2,1]

# Count templates are indexed by49+N.
E["count", 16:18] = [22,49]
M3_in[84, 862:864] = 10000
M3_in[99, 862] = 1
M3_in[230, 862:864] = [-1000,1000]
M3_in[227, 863] = 1
M3_in[102, 862:864] = -1000000
M3_b[862:864] = [-490000,-491000]
M3_out[862:864, 141] = 1

# Relation vocabulary.
E["continent", 16:18] = [18,10]
E["continent", 39] = 1
E["continent", 6:11] = [5,10,240,0,1]
E["language", 16:18] = [18,10]
E["language", 39] = 2
E["president", 16:18] = [18,10]
E[["president","lead","leader","boss","chief","head","owner"], 39] = 3
E[["head","owner"], 16:18] = [12,10]
E["prime", 16:18] = [19,10]
E["prime", 39] = 4
E["found", 16:18] = [14,10]
E[["found","created","made"], 39] = 5
E["half", 16:18] = [15,44]
E["half", 39] = 6
E[["double","twice"], 16:18] = [15,44]
E[["double","twice"], 39] = 7
E["triple", 16:18] = [15,44]
E["triple", 39] = 8
E["quarter", 16:18] = [15,44]
E["quarter", 39] = 9
E[["many","number"], 16:18] = [19,44]
E[["many","number"], 39] = 10
E["currency", 16:18] = [18,10]
E["currency", 39] = 12
V3[3, 75, 1] = 1
O3[3, 1, 113] = 1
V4[0, 113, 19] = 1
O4[0, 19, 121] = 1
V4[0, 117, 20] = 1
V4[0, 118, 21] = 1
V4[0, 119, 22] = 1
V4[0, 120, 23] = 1
O4[0, 20, 122] = 1
O4[0, 21, 123] = 1
O4[0, 22, 124] = 1
O4[0, 23, 125] = 1

# Continental ranges, keyed by relation and capital code.
M3_in[78, 864:1022] = 1
M3_in[113, 864:1022] = 1000
M3_in[102, 864:1022] = -100000
M3_b[864:920] = [
-1145,-1146,-1150,-1151,
-1150,-1151,-1152,-1153,
-1152,-1153,-1154,-1155,
-1154,-1155,-1155,-1156,
-1155,-1156,-1156,-1157,
-1156,-1157,-1157,-1158,
-1157,-1158,-1158,-1159,
-1158,-1159,-1159,-1160,
-1159,-1160,-1160,-1161,
-1160,-1161,-1172,-1173,
-1172,-1173,-1182,-1183,
-1182,-1183,-1184,-1185,
-1184,-1185,-1185,-1186,
-1185,-1186,-1190,-1191]
M3_out[864:920:4, 119] = 1
M3_out[865:920:4, 119] = -1
M3_out[866:920:4, 119] = -1
M3_out[867:920:4, 119] = 1
M3_out[864:920, 117] = [
242,-242,-242,242,
240,-240,-240,240,
243,-243,-243,243,
240,-240,-240,240,
245,-245,-245,245,
243,-243,-243,243,
242,-242,-242,242,
240,-240,-240,240,
241,-241,-241,241,
242,-242,-242,242,
240,-240,-240,240,
241,-241,-241,241,
245,-245,-245,245,
243,-243,-243,243]

# Languages.
M3_b[920:962] = [
-2145,-2146,-2147,-2146,-2147,-2148,-2147,-2148,-2149,
-2148,-2149,-2150,-2149,-2150,-2151,-2150,-2151,-2152,
-2151,-2152,-2153,-2152,-2153,-2154,-2153,-2154,-2155,
-2155,-2156,-2157,-2157,-2158,-2159,-2184,-2185,-2186,
-2154,-2155,-2156,-2162,-2163,-2164]
M3_out[920:962, 117] = [
389,-778,389,388,-776,388,395,-790,395,
390,-780,390,391,-782,391,393,-786,393,
392,-784,392,388,-776,388,388,-776,388,
388,-776,388,394,-788,394,388,-776,388,
388,-776,388,388,-776,388]
M3_out[920:1022:3, 119] = 1
M3_out[921:1022:3, 119] = -2
M3_out[922:1022:3, 119] = 1

# Selected country leaders.
M3_b[962:1004] = [
-3153,-3154,-3155,-3145,-3146,-3147,-3157,-3158,-3159,
-3151,-3152,-3153,-3171,-3172,-3173,-3156,-3157,-3158,
-4146,-4147,-4148,-4152,-4153,-4154,-4148,-4149,-4150,
-4147,-4148,-4149,-4154,-4155,-4156,-3172,-3173,-3174,
-4179,-4180,-4181,-3146,-3147,-3148]
M3_out[962:1004, 117] = [
396,-792,396,397,-794,397,398,-796,398,
399,-798,399,401,-802,401,402,-804,402,
403,-806,403,404,-808,404,405,-810,405,
406,-812,406,407,-814,407,408,-816,408,
409,-818,409,403,-806,403]
M3_out[971:974, 118] = [400,-800,400]
M3_out[971:974, 120] = [1,-2,1]
M3_out[971:974, 141] = [1,-2,1]

# Selected company founders.
M3_b[1004:1022] = [
-5194,-5195,-5196,-5202,-5203,-5204,-5196,-5197,-5198,
-5200,-5201,-5202,-5190,-5191,-5192,-5204,-5205,-5206]
M3_out[1004:1022, 117] = [
209,-418,209,211,-422,211,410,-820,410,
201,-402,201,191,-382,191,205,-410,205]
M3_out[1004:1022, 118] = [
210,-420,210,212,-424,212,411,-822,411,
202,-404,202,192,-384,192,206,-412,206]
M3_out[1004:1022:3, 120] = 1
M3_out[1005:1022:3, 120] = -2
M3_out[1006:1022:3, 120] = 1

# Latest number, including spoken cardinal numbers.
M3_in[99, 1022] = 1
M3_in[230, 1022:1024] = [-1000,1000]
M3_in[227, 1023] = 1
M3_b[1023] = -1000
M3_out[1022:1024, 115] = 1
V4[0, 99, 13] = 0
V4[0, 115, 13] = 1

# Numeric world facts.
E[["week","day","hour","minute","year","month","century","dozen","pair","dollar"], 6:8] = [6,0]
E[["week","day","hour","minute","year","month","century","dozen","pair","dollar","planet","continent"], 245] = [7,24,60,60,365,30,100,12,2,100,8,7]
E[["week","day","hour","minute","year","month","century","dozen","pair","dollar","planet","continent"], 247] = 1
M1_in[245, 362] = 1
M1_in[202, 362] = 1000
M1_b[362] = -1000
M1_out[362, 246] = 1
M1_in[247, 363] = 1
M1_in[202, 363] = 1000
M1_b[363] = -1000
M1_out[363, 248] = 1
V3[1, 246, 5] = 1
V3[1, 248, 6] = 1
O3[1, 5, 116] = 1
O3[1, 6, 130] = 1
V4[0, 116, 25] = 1
V4[0, 130, 26] = 1
O4[0, 25, 128] = 1
O4[0, 26, 129] = 1

# Planet-query hints.
E["red", 11:15] = [8,0,0,7]
E["near", 11:15] = [8,0,0,8]
E["live", 11:15] = [8,0,0,9]
E["ring", 6:11] = [8,10,232,0,1]
V4[0, 83, 27] = 1
O4[0, 27, 131] = 1

# Classification templates45..48.
M4_in[160, 712:939] = 64
M4_in[201, 712:939] = 1
M4_in[163, 712:939] = -1
M4_b[712:720] = [-2879,-2880,-2881,-2882,-2883,-2884,-2885,-2886]
M4_out[712:720, 180] = [83,-143,63,-2,-29,36,-15,7]
M4_out[716:719, 203] = [1,-2,1]
M4_b[720:728] = [-2943,-2944,-2945,-2946,-2947,-2948,-2949,-2950]
M4_out[720:728, 180] = [30,-37,10,-2,-29,36,-15,7]
M4_out[724:727, 203] = [1,-2,1]
M4_b[728:737] = [-3007,-3008,-3009,-3010,-3011,-3012,-3013,-3014,-3015]
M4_out[728:737, 180] = [83,-143,63,-2,14,-58,51,-15,7]
M4_out[733:736, 203] = [1,-2,1]
M4_b[737:746] = [-3071,-3072,-3073,-3074,-3075,-3076,-3077,-3078,-3079]
M4_out[737:746, 180] = [30,-37,10,-2,14,-58,51,-15,7]
M4_out[742:745, 203] = [1,-2,1]

# Count zero.
M4_b[746:754] = [-3135,-3136,-3137,-3138,-3139,-3140,-3141,-3142]
M4_out[746:754, 180] = [51,270,-657,320,131,-243,121,7]

# Count one.
M4_b[754:762] = [-3199,-3200,-3201,-3202,-3203,-3204,-3205,-3206]
M4_out[754:762, 180] = [51,270,-657,320,132,-245,122,7]

# Count two.
M4_b[762:772] = [-3263,-3264,-3265,-3266,-3267,-3268,-3269,-3270,-3271,-3272]
M4_out[762:772, 180] = [51,270,-657,320,132,-229,227,-244,123,7]

# Count three.
M4_b[772:784] = [-3327,-3328,-3329,-3330,-3331,-3332,-3333,-3334,-3335,-3336,-3337,-3338]
M4_out[772:784, 180] = [51,270,-657,320,132,-229,227,-228,229,-246,124,7]

# Count four.
M4_b[784:798] = [-3391,-3392,-3393,-3394,-3395,-3396,-3397,-3398,-3399,-3400,-3401,-3402,-3403,-3404]
M4_out[784:798, 180] = [51,270,-657,320,132,-229,227,-228,229,-230,231,-248,125,7]

# Count five.
M4_b[798:814] = [-3455,-3456,-3457,-3458,-3459,-3460,-3461,-3462,-3463,-3464,-3465,-3466,-3467,-3468,-3469,-3470]
M4_out[798:814, 180] = [51,270,-657,320,132,-229,227,-228,229,-230,231,-232,233,-250,126,7]

# Count six.
M4_b[814:832] = [-3519,-3520,-3521,-3522,-3523,-3524,-3525,-3526,-3527,-3528,-3529,-3530,-3531,-3532,-3533,-3534,-3535,-3536]
M4_out[814:832, 180] = [51,270,-657,320,132,-229,227,-228,229,-230,231,-232,233,-234,235,-252,127,7]

# Count seven.
M4_b[832:852] = [-3583,-3584,-3585,-3586,-3587,-3588,-3589,-3590,-3591,-3592,-3593,-3594,-3595,-3596,-3597,-3598,-3599,-3600,-3601,-3602]
M4_out[832:852, 180] = [51,270,-657,320,132,-229,227,-228,229,-230,231,-232,233,-234,235,-236,237,-254,128,7]

# Count eight.
M4_b[852:874] = [-3647,-3648,-3649,-3650,-3651,-3652,-3653,-3654,-3655,-3656,-3657,-3658,-3659,-3660,-3661,-3662,-3663,-3664,-3665,-3666,-3667,-3668]
M4_out[852:874, 180] = [51,270,-657,320,132,-229,227,-228,229,-230,231,-232,233,-234,235,-236,237,-238,239,-256,129,7]

# Count nine.
M4_b[874:898] = [-3711,-3712,-3713,-3714,-3715,-3716,-3717,-3718,-3719,-3720,-3721,-3722,-3723,-3724,-3725,-3726,-3727,-3728,-3729,-3730,-3731,-3732,-3733,-3734]
M4_out[874:898, 180] = [51,270,-657,320,132,-229,227,-228,229,-230,231,-232,233,-234,235,-236,237,-238,239,-240,241,-258,130,7]

# Count ten, with the final number emitted as two digits.
M4_b[898:925] = [-3775,-3776,-3777,-3778,-3779,-3780,-3781,-3782,-3783,-3784,-3785,-3786,-3787,-3788,-3789,-3790,-3791,-3792,-3793,-3794,-3795,-3796,-3797,-3798,-3799,-3800,-3801]
M4_out[898:925, 180] = [51,270,-657,320,132,-229,227,-228,229,-230,231,-232,233,-234,235,-236,237,-238,239,-240,241,-242,234,-114,-127,121,7]

# Preference templates14 and15.
M4_b[925:931] = [-895,-896,-897,-898,-899,-900]
M4_out[925:931, 180] = [10,25,-81,54,-15,7]
M4_out[927:930, 244] = [1,-2,1]
M4_b[931:939] = [-959,-960,-961,-962,-963,-964,-965,-966]
M4_out[931:939, 180] = [1,6,50,-56,-68,75,-15,7]
M4_out[935:938, 186] = [1,-2,1]

# Unary arithmetic adjusts the remembered/current numerical operand.
M4_in[121, 939:955] = 10000
M4_in[173, 939:941] = 1
M4_in[173, 943:945] = 1
M4_in[173, 947:949] = 1
M4_in[173, 951:953] = 1
M4_b[939:955] = [-60000,-70000,-60000,-70000,-70000,-80000,-70000,-80000,-80000,-90000,-80000,-90000,-90000,-100000,-90000,-100000]
M4_out[939:955, 174] = [-0.5,0.5,0.5,-0.5,1,-1,-1,1,2,-2,-2,2,-0.75,0.75,0.75,-0.75]

# Quantity facts replace numeric memory only when arithmetic is inactive.
M4_in[173, 955] = 1
M4_in[128, 956] = 1
M4_in[121, 955:957] = 10000
M4_in[129, 955:957] = 160000
M4_in[168, 955:957] = -1000000
M4_b[955:957] = -260000
M4_out[955:957, 174] = [-1,1]

# Planet relations: smallest, red, nearest, hottest, inhabited.
M4_in[161, 957:972] = 1
M4_in[131, 957:972] = 1000
M4_in[121, 957:972] = 10000
M4_b[957:972] = [-2230,-2231,-2232,-7230,-7231,-7232,-8230,-8231,-8232,-3230,-3231,-3232,-9230,-9231,-9232]
M4_out[957:972, 122] = [233,-466,233,230,-460,230,233,-466,233,234,-468,234,229,-458,229]
M4_out[957:972:3, 124] = 1
M4_out[958:972:3, 124] = -2
M4_out[959:972:3, 124] = 1

# Dollar currencies.
M4_in[161, 972:984] = 1
M4_in[121, 972:984] = 1000
M4_b[972:984] = [-12153,-12154,-12155,-12152,-12153,-12154,-12155,-12156,-12157,-12184,-12185,-12186]
M4_out[972:984, 122] = [412,-824,412,412,-824,412,412,-824,412,412,-824,412]
M4_out[972:984:3, 124] = 1
M4_out[973:984:3, 124] = -2
M4_out[974:984:3, 124] = 1

# Dynamic classification, preference, and alternative-fact insertion.
M5_in[114, 236] = 1
M5_in[203, 236] = 1000
M5_b[236] = -1000
M5_out[236, 180] = 1
M5_in[242, 237] = 1
M5_in[244, 237] = 1000
M5_b[237] = -1000
M5_out[237, 180] = 1
M5_in[244, 238] = 1
M5_in[243, 238] = -1
M5_out[238, 180] = 6
M5_in[124, 0:2] = -1000
M5_in[122, 239] = 1
M5_in[123, 240] = 1
M5_in[182, 239] = 1000
M5_in[183, 240] = 1000
M5_in[124, 239:241] = 1000
M5_b[239:241] = -2000
M5_out[239:241, 180] = 1

# Additional capital coverage.
E["state", 6:11] = [9,10,154,0,1]
E["british", 6:11] = [9,10,147,0,1]
E["africa", 6:11] = [6,10,184,0,1]
E["belgium", 6:11] = [10,10,414,0,1]
E["nigeria", 6:11] = [10,10,415,0,1]
E["bangladesh", 6:11] = [10,10,416,0,1]
E["nepal", 6:11] = [10,10,417,0,1]
E["malaysia", 6:11] = [10,11,418,419,1]
E["malaysia", 29] = 1
E["lanka", 6:11] = [10,10,420,0,1]
E["romania", 6:11] = [10,10,421,0,1]
E["czechia", 6:11] = [10,10,422,0,1]
E["hungary", 6:11] = [10,10,423,0,1]
E["iceland", 6:11] = [10,10,424,0,1]
E["philippines", 6:11] = [10,10,425,0,1]
E["taiwan", 6:11] = [10,10,426,0,1]
E["singapore", 6:11] = [10,10,427,0,1]
E["afghanistan", 6:11] = [10,10,428,0,1]
E["tunisia", 6:11] = [10,10,429,0,1]
E["morocco", 6:11] = [10,10,430,0,1]
E["uzbekistan", 6:11] = [10,10,431,0,1]
E["zimbabwe", 6:11] = [10,10,432,0,1]
E["zambia", 6:11] = [10,10,433,0,1]
E["senegal", 6:11] = [10,10,434,0,1]
E["ghana", 6:11] = [10,10,435,0,1]

# Additional opposites.
E["love", 11:14] = [6,0,436]
E["hate", 11:14] = [6,0,96]
E["kind", 11:14] = [6,0,437]
E["cruel", 11:14] = [6,0,19]
E["sweet", 11:14] = [6,0,438]
E["bitter", 11:14] = [6,0,439]
E["safe", 11:14] = [6,0,440]
E["dangerous", 11:14] = [6,0,94]
E["early", 11:14] = [6,0,441]
E["late", 11:14] = [6,0,442]
E["laugh", 11:14] = [6,0,443]
E["cry", 11:14] = [6,0,444]
E["more", 11:14] = [6,0,445]
E["less", 11:14] = [6,0,446]
E["buy", 11:14] = [6,0,447]
E["sell", 11:14] = [6,0,448]

# Expanded echo vocabulary.
E["flower", 20] = 413
E[["old","young","long","short","tall","full","dry","wet","fast","slow","easy","difficult","clean","dirty","strong","soft","hard","loud","quiet","open","shut","true","false","beautiful","poor","rich","night","morning","summer","winter","start","end","come","go","win","lose","give","warm","cool","high","low","male","female","man","woman","boy","girl","brother","sister","father","mother","spring"], 26] = 1
E[["old","young","long","short","tall","full","dry","wet","fast","slow","easy","difficult","clean","dirty","strong","soft","hard","loud","quiet","open","shut","true","false","beautiful","poor","rich","night","morning","summer","winter","start","end","come","go","win","lose","give","warm","cool","high","low","male","female","man","woman","boy","girl","brother","sister","father","mother","spring"], 20] = [290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342]
E[["earth","mars","jupiter","saturn","mercury","venus","neptune","uranus","pacific","asia","africa","europe","america","antarctica","oceania","everest","nile","amazon","sahara","einstein","newton","shakespeare","mozart","leonardo","vinci","darwin","edison","armstrong","gagarin","air","iron","gold","silver","salt","protein","heart","brain","blood","leaf","fish","elephant","mouse","rabbit","bee","snow","ice","fire","light","dark","white","black","up","down","left","north","south","east","west"], 26] = 1
E[["earth","mars","jupiter","saturn","mercury","venus","neptune","uranus","pacific","asia","africa","europe","america","antarctica","oceania","everest","nile","amazon","sahara","einstein","newton","shakespeare","mozart","leonardo","vinci","darwin","edison","armstrong","gagarin","air","iron","gold","silver","salt","protein","heart","brain","blood","leaf","fish","elephant","mouse","rabbit","bee","snow","ice","fire","light","dark","white","black","up","down","left","north","south","east","west"], 20] = [229,230,231,232,233,234,235,236,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289]
E[["paris","london","rome","berlin","madrid","tokyo","beijing","ottawa","washington","delhi","canberra","brasilia","moscow","seoul","cairo","athens","lisbon","dublin","oslo","stockholm","helsinki","copenhagen","bern","amsterdam","vienna","warsaw","kyiv","ankara","bangkok","hanoi","jakarta","islamabad","tehran","baghdad","jerusalem","riyadh","doha","nairobi","pretoria","wellington","lima","santiago","havana","caracas","montevideo"], 26] = 1
E[["paris","london","rome","berlin","madrid","tokyo","beijing","ottawa","washington","delhi","canberra","brasilia","moscow","seoul","cairo","athens","lisbon","dublin","oslo","stockholm","helsinki","copenhagen","bern","amsterdam","vienna","warsaw","kyiv","ankara","bangkok","hanoi","jakarta","islamabad","tehran","baghdad","jerusalem","riyadh","doha","nairobi","pretoria","wellington","lima","santiago","havana","caracas","montevideo"], 20] = [146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190]
E[["food","weather","work","school","family","pet","fun","rice","one","two","three","four","five","six","seven","eight","nine","ten","sport","people","angry","ill","afraid","animal","fruit","berry","feeble","hate","cruel","bitter","sweet","dangerous","late","early","cry","laugh","less","more","sell","buy"], 26] = 1
E[["food","weather","work","school","family","pet","fun","rice","one","two","three","four","five","six","seven","eight","nine","ten","sport","people","angry","ill","afraid","animal","fruit","berry","feeble","hate","cruel","bitter","sweet","dangerous","late","early","cry","laugh","less","more","sell","buy"], 20] = [69,70,71,72,73,74,75,125,126,127,128,129,130,131,132,133,134,135,377,378,380,381,382,384,385,386,387,436,437,438,439,440,441,442,443,444,445,446,447,448]
E[["openai","microsoft","google","meta","spacex","tesla","nvidia","anthropic","claude","chatgpt","gemini","windows","android","iphone"], 26] = 1
E[["openai","microsoft","google","meta","spacex","tesla","nvidia","anthropic","claude","chatgpt","gemini","windows","android","iphone"], 20] = [215,216,217,218,219,220,221,222,223,224,225,226,227,228]

# Additional output codes.
U[[180,181], "english"] = [776,-150544]
U[[180,181], "french"] = [778,-151321]
U[[180,181], "german"] = [780,-152100]
U[[180,181], "spanish"] = [782,-152881]
U[[180,181], "chinese"] = [784,-153664]
U[[180,181], "japanese"] = [786,-154449]
U[[180,181], "russian"] = [788,-155236]
U[[180,181], "italian"] = [790,-156025]
U[[180,181], "trump"] = [792,-156816]
U[[180,181], "macron"] = [794,-157609]
U[[180,181], "putin"] = [796,-158404]
U[[180,181], "xi"] = [798,-159201]
U[[180,181], "jinping"] = [800,-160000]
U[[180,181], "zelensky"] = [802,-160801]
U[[180,181], "lula"] = [804,-161604]
U[[180,181], "starmer"] = [806,-162409]
U[[180,181], "carney"] = [808,-163216]
U[[180,181], "merz"] = [810,-164025]
U[[180,181], "meloni"] = [812,-164836]
U[[180,181], "modi"] = [814,-165649]
U[[180,181], "erdogan"] = [816,-166464]
U[[180,181], "netanyahu"] = [818,-167281]
U[[180,181], "larry"] = [820,-168100]
U[[180,181], "page"] = [822,-168921]
U[[180,181], "dollar"] = [824,-169744]
U[[180,181], "flower"] = [826,-170569]
U[[180,181], "brussels"] = [828,-171396]
U[[180,181], "abuja"] = [830,-172225]
U[[180,181], "dhaka"] = [832,-173056]
U[[180,181], "kathmandu"] = [834,-173889]
U[[180,181], "kuala"] = [836,-174724]
U[[180,181], "lumpur"] = [838,-175561]
U[[180,181], "colombo"] = [840,-176400]
U[[180,181], "bucharest"] = [842,-177241]
U[[180,181], "prague"] = [844,-178084]
U[[180,181], "budapest"] = [846,-178929]
U[[180,181], "reykjavik"] = [848,-179776]
U[[180,181], "manila"] = [850,-180625]
U[[180,181], "taipei"] = [852,-181476]
U[[180,181], "singapore"] = [854,-182329]
U[[180,181], "kabul"] = [856,-183184]
U[[180,181], "tunis"] = [858,-184041]
U[[180,181], "rabat"] = [860,-184900]
U[[180,181], "tashkent"] = [862,-185761]
U[[180,181], "harare"] = [864,-186624]
U[[180,181], "lusaka"] = [866,-187489]
U[[180,181], "dakar"] = [868,-188356]
U[[180,181], "accra"] = [870,-189225]
U[[180,181], "hate"] = [872,-190096]
U[[180,181], "cruel"] = [874,-190969]
U[[180,181], "bitter"] = [876,-191844]
U[[180,181], "sweet"] = [878,-192721]
U[[180,181], "dangerous"] = [880,-193600]
U[[180,181], "late"] = [882,-194481]
U[[180,181], "early"] = [884,-195364]
U[[180,181], "cry"] = [886,-196249]
U[[180,181], "laugh"] = [888,-197136]
U[[180,181], "less"] = [890,-198025]
U[[180,181], "more"] = [892,-198916]
U[[180,181], "sell"] = [894,-199809]
U[[180,181], "buy"] = [896,-200704]
```