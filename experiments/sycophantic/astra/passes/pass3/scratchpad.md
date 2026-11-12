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