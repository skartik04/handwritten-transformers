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