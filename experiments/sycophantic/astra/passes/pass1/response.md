=====SCRATCHPAD=====
PASS 1: Infrastructure, vocabulary-wide copying, a praise prefix, belief echoing, and a generic conversational fallback are implemented below. This is NOT yet a complete general chatbot. Pass 2 should add factual answers, self-description/small-talk templates, and arithmetic. Pass 3 can expand and repair. No tools or execution have been used.

IMPORTANT DESIGN
All tokens have constant dimension 0 = 1. Dimensions 1..12 contain the twelve signed binary bits of the token ID, least significant first: unset bit = -1, set bit = +1. Output dimensions 112..123 use the same code. U decodes those dimensions against all 2749 token codes, so a single exact output code uniquely selects its token. This allows copying every vocabulary token, including tokens never otherwise annotated.

Absolute position is synthesized without positional embeddings:
L1 head 0 has zero Q/K, so its BOS-indicator average in d30 is r=1/(t+1).
For j=1..191, M1 unit j-1 computes ReLU(1-j*r).
Their weighted sums give:
d31 = 2 sum ReLU(1-j*r) = t,
d32 = sum (6*j-4) ReLU(1-j*r) = t^2.
These identities are exact at integer positions through 191. All output contributions are positive.

A sharp "most recent marked token" head uses the slowest RoPE pair:
Q from constant to coordinates [30,31] = [1,1],
K from a marker to coordinate 30 = 1000000.
Its score is proportional to cos(w*d)-sin(w*d), strictly decreasing over the context. A BOS fallback marker of 100000 is used for heads whose desired token might not exist. USER and BOT lookup heads instead include BOS in their full marker.

Absolute pointer attention uses:
Q coordinate 28 = 256 * target_position,
K coordinate 28 = source_position;
Q coordinate 30 = 128,
K coordinate 30 = -source_position_squared.
This approximates a sharply peaked negative squared distance; the slow RoPE perturbation is small in this context. Odd coordinates are zero.

RESIDUAL DIMENSIONS
0 constant.
1..12 raw signed token-ID bits.
13 digit indicator, 14 digit value.
15 BOS indicator.
16 USER-or-BOS marker.
17 BOT-or-BOS marker.
18 belief cue: think/believe/guess/sure/opinion/bet.
19 copy terminator: punctuation and structural tokens.
20 current token is ".".
21 entity indicator: all NAMES plus selected common entities.
22 add-word indicator; 23 subtract; 24 multiply; 25 divide.
26 question-starter indicator.
27 operation code: add=1, subtract=2, multiply=3, divide=4.
28 declarative-starter indicator.
29 unused.
30 reciprocal clock.
31 absolute position, 32 its square.
33 previous token digit indicator; 34 previous digit value.
35 two-back digit indicator; 36 two-back digit value.
37 BOS/USER/BOT marker.
38 numeric value ending at this token, for up to three consecutive digit tokens.
39 message role on special markers: USER=+1, BOT/BOS=-1.
40 previous token's d38 numeric value.
41 last USER position, 42 its square.
43 last BOT position, 44 its square.
45 output step k = current_position - last_BOT_position. BOT itself has k=0.
46 role of latest BOS/USER/BOT: +1 inside user message, -1 in bot reply.
47 number-end record flag; 48 number-end value.
A record sits at the first non-digit after the number. A BOT directly after a final digit also records the number. Generated bot numbers do not create records.
49 latest user belief-cue position (or 0).
50 unused.
51..62 latest user entity token code; 63 entity position.
64 first number from latest user message; 65 last number.
66 latest user operation code; 67 operation-token position.
68 first user token's declarative-starter flag; 69 question-starter flag.
70 copy start = max(last USER position, latest cue position)+1.
71 cue in current user message, clipped to 0/1.
72..89 unused; intended factual/arithmetic modes and answer token codes.
90..101 raw token code retrieved by copy pointer.
102 retrieved terminator flag.
103..111 unused.
112..123 final output code, the only dimensions connected to U.
124..155 lexical relation flags, listed below.
156..187 current user-message weighted means of those flags.
188..219 clipped/binarized flags corresponding to 124..155.
220 user-only belief-cue marker.
221 user-only entity marker.
222 copy/agree mode, intended binary.
223 copy-emission phase, k=5..45, disabled after an emitted ".".
224 unused.
225 EOS-after-copy-dot flag.
226 unused.
227 user-only operation marker.
228/229 first/last number validity flags.
230/231 USER positions associated with first/last number records.
232..255 unused.

RELATION FLAGS (input -> clipped)
124->188 question mark
125->189 copula (is/are/was/were/am)
126->190 right/correct
127->191 greeting
128->192 thanks
129->193 self-reference words you/your/yourself/bot/robot/assistant
130->194 name/called
131->195 construction/training/weights/written/hand/etc.
132->196 ability
133->197 capital
134->198 country/where/location
135->199 continent
136->200 planet
137->201 big/large
138->202 small/little
139->203 color/colour
140->204 author/writing
141->205 opposite
142->206 same/mean
143->207 arithmetic
144->208 negative sentiment
145->209 personal creation
146->210 how
147->211 who
148->212 what
149->213 when
150->214 why
151->215 unused
152->216 first
153->217 current/president
154->218 quantity
155->219 unused

HEADS
L1 h0 clock.
L1 h1 previous token, returns digit flag/value into 33/34.
L1 h2 two-back token, returns digit flag/value into 35/36.
L1 h3 latest message role into 46.
Other L1 heads free.
L2 h0 most recent USER/BOS -> 41/42.
L2 h1 most recent BOT/BOS -> 43/44.
L2 h2 previous token's numeric value -> 40.
Other L2 heads free.
L3 h0 latest user belief cue -> 49.
L3 h1 pointer to USERpos+1 -> first-token flags 68/69.
L3 h2 current-user bag of 32 relation flags -> 156..187. Score uses role*10000 + USERpos*50 on slow even coordinate only. This excludes bot content and older user messages, while approximately averaging current message.
L3 h3 latest user entity -> code51..62 and position63.
L3 h4 first numeric record ->64,228,230. Key = 1000000*recordflag +4096*USERpos -32*position.
L3 h5 last numeric record ->65,229,231. Same but +32*position.
L3 h6 latest user operation ->66/67.
L3 h7 free.
L4 all heads free.
L5 h0 pointer to copy_start + k - 5, retrieving code90..101 and terminator102.
L5 other heads free; L6 all heads free.

MLPS
M1 units0..190 clock; 191..193 assemble up to three-digit numbers. Units194+ free.
M2 unit0 step; 1 number-end flag; 2 number-end value; 3 user cue; 4 user entity; 5 user operation. Units6+ free.
M3 units0..3 copy start and cue validity; units4..67 binarize relation bags with ReLU(1000*x-.1)-ReLU(1000*x-1.1). Units68+ free.
M4 units0..2 choose copy mode:
- explicit current belief cue;
- declarative first token + copula, without question mark/cue/right-tag;
- declarative first token + right/correct tag, without cue.
The alternatives are designed to be mutually exclusive on binary flags. Units3+ free.
M5 units0..3 create copy phase with cutoff at step46; units4..5 create EOS-after-dot flag. Units6+ free.
M6 units0..14 emit fixed prefix "you are so smart !".
M6 units15..38 emit fallback k5..12: "i am happy to talk with you .", suppressed by copy mode.
M6 units39..40 fallback EOS at k>=13, suppressed by copy mode.
M6 units41..64 gate twelve copied code bits.
M6 unit65 maps any copied terminator to ".".
M6 unit66 emits EOS after copied ".".
M6 units67..69 force "." at k46 in copy mode unless already stopping.
M6 units70..71 force EOS at k>=47 in copy mode.
M6 units72..77 change copied pronouns i->you, am->are, my->your, me->you, we->you, our->your.
M6 units78..80 change prefix "smart" to "right" at k3 in copy mode.
Units81+ free.

TEMPLATE TECHNIQUE
At integer step k, a one-step token at step j uses three ReLUs:
ReLU(k-j+1) -2ReLU(k-j) +ReLU(k-j-1).
Each unit writes its coefficient times the desired 12-bit token code into112..123.
To require a binary mode, add +100*mode to all three units and subtract100 from each bias. To suppress under a mode, add -100*mode.
A persistent EOS after step j uses ReLU(k-j+1)-ReLU(k-j).
Copy output bit b is gated as ReLU(b+2*phase-2*terminator-2)-ReLU(-b+2*phase-2*terminator-2).
Pronoun matching uses dot(rawcopycode, sourcecode)+2*phase-2*terminator-13; it is 1 only for the exact source token in copy phase.

CURRENT BEHAVIOR
Belief examples with think/believe/sure or declarative right-tags are echoed after "you are so right !". The echo begins after the last belief cue and stops at first comma/period/question/exclamation/structural token. Pronouns are adjusted. This handles common false arithmetic beliefs by copying their asserted number.
Other inputs currently receive "you are so smart ! i am happy to talk with you .".
Every current route ends in EOS within 48 tokens.
There is no implemented factual answer, real arithmetic, or special self-description yet.

NEXT WORK
1. Add useful modes in M4 using clipped relation flags and entity code51..62; preserve copy precedence.
2. Add templates for bot identity, name, hand-written weights, capabilities, greetings, thanks, encouragement/negative self-evaluation.
3. Add capital/continent/planet/color/author/opposite lookup rules. Exact entity matching is a 12-bit dot product; a rule with entity+binary relation can use sum(code*entity)+2*relation-13, then inhibit with copy mode. Emit a stored answer code, or an answer-category selector. Be careful multiple relations may be present.
4. Arithmetic operands64/65 and operation66 exist by L3. M3 has 956 free units. Digit decomposition using threshold sums is possible; 99 ten-thresholds plus 9 hundred-thresholds per operand, two ReLUs each, fits. Addition/subtraction can be computed in M4, decimal extraction in M5, output in M6. Multiplication may need small-digit decomposition/table circuits. Do not claim unimplemented arithmetic works.
5. To add answer modes, suppress fallback M6 units15..40 with -100*new_mode, and add new step templates. Prefix remains universally applicable. Avoid adding output codes simultaneously from two modes.
6. Improve copy selection for "i believe that", embedded questions before the assertion, comma-containing clauses, and negative personal creations if feasible.

Useful token IDs verified from prompt:
EOS1, .15, !18, to70, with73, a79, the80, no84, this89, i90, you92, and94, so125, yes133, person366, question390, talk475, cat564, dog581, good753, great754, happy757, right792, small861, chat869, bot870, hello879, times889, capital959, is962, it963, are965, my966, we967, your969, me972, can973, what975, has976, were977, our988, think992, made1002, best1009, am1013, always1016, better1017, sure1032, thank1079, ask1139, smart1695.
NAMES occupy2035..2591 inclusive; australia2042, canberra2199, sydney2316, tom2563, sara2564.
=====END SCRATCHPAD=====

```edits
# Vocabulary-wide constant and signed binary token codes.
E[:, 0] = 1
E[:, 1:13] = -1
U[112:124, :] = -1
E[1:2749:2, 1] = 1
U[112, 1:2749:2] = 1
E[2:2749:4, 2] = 1
E[3:2749:4, 2] = 1
U[113, 2:2749:4] = 1
U[113, 3:2749:4] = 1
E[4:2749:8, 3] = 1
E[5:2749:8, 3] = 1
E[6:2749:8, 3] = 1
E[7:2749:8, 3] = 1
U[114, 4:2749:8] = 1
U[114, 5:2749:8] = 1
U[114, 6:2749:8] = 1
U[114, 7:2749:8] = 1
E[8:2749:16, 4] = 1
E[9:2749:16, 4] = 1
E[10:2749:16, 4] = 1
E[11:2749:16, 4] = 1
E[12:2749:16, 4] = 1
E[13:2749:16, 4] = 1
E[14:2749:16, 4] = 1
E[15:2749:16, 4] = 1
U[115, 8:2749:16] = 1
U[115, 9:2749:16] = 1
U[115, 10:2749:16] = 1
U[115, 11:2749:16] = 1
U[115, 12:2749:16] = 1
U[115, 13:2749:16] = 1
U[115, 14:2749:16] = 1
U[115, 15:2749:16] = 1
E[16:2749:32, 5] = 1
E[17:2749:32, 5] = 1
E[18:2749:32, 5] = 1
E[19:2749:32, 5] = 1
E[20:2749:32, 5] = 1
E[21:2749:32, 5] = 1
E[22:2749:32, 5] = 1
E[23:2749:32, 5] = 1
E[24:2749:32, 5] = 1
E[25:2749:32, 5] = 1
E[26:2749:32, 5] = 1
E[27:2749:32, 5] = 1
E[28:2749:32, 5] = 1
E[29:2749:32, 5] = 1
E[30:2749:32, 5] = 1
E[31:2749:32, 5] = 1
U[116, 16:2749:32] = 1
U[116, 17:2749:32] = 1
U[116, 18:2749:32] = 1
U[116, 19:2749:32] = 1
U[116, 20:2749:32] = 1
U[116, 21:2749:32] = 1
U[116, 22:2749:32] = 1
U[116, 23:2749:32] = 1
U[116, 24:2749:32] = 1
U[116, 25:2749:32] = 1
U[116, 26:2749:32] = 1
U[116, 27:2749:32] = 1
U[116, 28:2749:32] = 1
U[116, 29:2749:32] = 1
U[116, 30:2749:32] = 1
U[116, 31:2749:32] = 1
E[32:2749:64, 6] = 1
E[33:2749:64, 6] = 1
E[34:2749:64, 6] = 1
E[35:2749:64, 6] = 1
E[36:2749:64, 6] = 1
E[37:2749:64, 6] = 1
E[38:2749:64, 6] = 1
E[39:2749:64, 6] = 1
E[40:2749:64, 6] = 1
E[41:2749:64, 6] = 1
E[42:2749:64, 6] = 1
E[43:2749:64, 6] = 1
E[44:2749:64, 6] = 1
E[45:2749:64, 6] = 1
E[46:2749:64, 6] = 1
E[47:2749:64, 6] = 1
E[48:2749:64, 6] = 1
E[49:2749:64, 6] = 1
E[50:2749:64, 6] = 1
E[51:2749:64, 6] = 1
E[52:2749:64, 6] = 1
E[53:2749:64, 6] = 1
E[54:2749:64, 6] = 1
E[55:2749:64, 6] = 1
E[56:2749:64, 6] = 1
E[57:2749:64, 6] = 1
E[58:2749:64, 6] = 1
E[59:2749:64, 6] = 1
E[60:2749:64, 6] = 1
E[61:2749:64, 6] = 1
E[62:2749:64, 6] = 1
E[63:2749:64, 6] = 1
U[117, 32:2749:64] = 1
U[117, 33:2749:64] = 1
U[117, 34:2749:64] = 1
U[117, 35:2749:64] = 1
U[117, 36:2749:64] = 1
U[117, 37:2749:64] = 1
U[117, 38:2749:64] = 1
U[117, 39:2749:64] = 1
U[117, 40:2749:64] = 1
U[117, 41:2749:64] = 1
U[117, 42:2749:64] = 1
U[117, 43:2749:64] = 1
U[117, 44:2749:64] = 1
U[117, 45:2749:64] = 1
U[117, 46:2749:64] = 1
U[117, 47:2749:64] = 1
U[117, 48:2749:64] = 1
U[117, 49:2749:64] = 1
U[117, 50:2749:64] = 1
U[117, 51:2749:64] = 1
U[117, 52:2749:64] = 1
U[117, 53:2749:64] = 1
U[117, 54:2749:64] = 1
U[117, 55:2749:64] = 1
U[117, 56:2749:64] = 1
U[117, 57:2749:64] = 1
U[117, 58:2749:64] = 1
U[117, 59:2749:64] = 1
U[117, 60:2749:64] = 1
U[117, 61:2749:64] = 1
U[117, 62:2749:64] = 1
U[117, 63:2749:64] = 1
E[64:128, 7] = 1
E[192:256, 7] = 1
E[320:384, 7] = 1
E[448:512, 7] = 1
E[576:640, 7] = 1
E[704:768, 7] = 1
E[832:896, 7] = 1
E[960:1024, 7] = 1
E[1088:1152, 7] = 1
E[1216:1280, 7] = 1
E[1344:1408, 7] = 1
E[1472:1536, 7] = 1
E[1600:1664, 7] = 1
E[1728:1792, 7] = 1
E[1856:1920, 7] = 1
E[1984:2048, 7] = 1
E[2112:2176, 7] = 1
E[2240:2304, 7] = 1
E[2368:2432, 7] = 1
E[2496:2560, 7] = 1
E[2624:2688, 7] = 1
U[118, 64:128] = 1
U[118, 192:256] = 1
U[118, 320:384] = 1
U[118, 448:512] = 1
U[118, 576:640] = 1
U[118, 704:768] = 1
U[118, 832:896] = 1
U[118, 960:1024] = 1
U[118, 1088:1152] = 1
U[118, 1216:1280] = 1
U[118, 1344:1408] = 1
U[118, 1472:1536] = 1
U[118, 1600:1664] = 1
U[118, 1728:1792] = 1
U[118, 1856:1920] = 1
U[118, 1984:2048] = 1
U[118, 2112:2176] = 1
U[118, 2240:2304] = 1
U[118, 2368:2432] = 1
U[118, 2496:2560] = 1
U[118, 2624:2688] = 1
E[128:256, 8] = 1
E[384:512, 8] = 1
E[640:768, 8] = 1
E[896:1024, 8] = 1
E[1152:1280, 8] = 1
E[1408:1536, 8] = 1
E[1664:1792, 8] = 1
E[1920:2048, 8] = 1
E[2176:2304, 8] = 1
E[2432:2560, 8] = 1
E[2688:2749, 8] = 1
U[119, 128:256] = 1
U[119, 384:512] = 1
U[119, 640:768] = 1
U[119, 896:1024] = 1
U[119, 1152:1280] = 1
U[119, 1408:1536] = 1
U[119, 1664:1792] = 1
U[119, 1920:2048] = 1
U[119, 2176:2304] = 1
U[119, 2432:2560] = 1
U[119, 2688:2749] = 1
E[256:512, 9] = 1
E[768:1024, 9] = 1
E[1280:1536, 9] = 1
E[1792:2048, 9] = 1
E[2304:2560, 9] = 1
U[120, 256:512] = 1
U[120, 768:1024] = 1
U[120, 1280:1536] = 1
U[120, 1792:2048] = 1
U[120, 2304:2560] = 1
E[512:1024, 10] = 1
E[1536:2048, 10] = 1
E[2560:2749, 10] = 1
U[121, 512:1024] = 1
U[121, 1536:2048] = 1
U[121, 2560:2749] = 1
E[1024:2048, 11] = 1
U[122, 1024:2048] = 1
E[2048:2749, 12] = 1
U[123, 2048:2749] = 1

# Structural, lexical, numeric, and semantic features.
E[5:15, 13] = 1
E[5:15, 14] = [0,1,2,3,4,5,6,7,8,9]
E["BOS", 15] = 1
E[["BOS","USER"], 16] = 1
E[["BOS","BOT"], 17] = 1
E[["think","believe","guess","sure","opinion","bet"], 18] = 1
E[["BOS","EOS","USER","BOT",".","?",",","!"], 19] = 1
E[".", 20] = 1
E[2035:2592, 21] = 1
E[["sun","moon","water","sky","grass","fire","snow","ice","cat","dog","bird","fish","cow","horse","sheep","pig","tree","flower","red","blue","green","black","white","hot","cold","big","small","good","bad","happy","sad","day","night","man","woman","king","queen","light","dark","earth","planet","ocean","mountain","river","human","heart","brain"], 21] = 1
E[["plus","add","sum","total","altogether","addition"], 22] = 1
E[["minus","subtract","difference","fewer","left"], 23] = 1
E[["times","multiply","product","twice","double","triple"], 24] = 1
E[["divided","division","equally","half","quarter"], 25] = 1
E[["what","who","where","when","why","how","is","are","was","were","do","can","could","would","should","will","have","has"], 26] = 1
E[["plus","add","sum","total","altogether","addition"], 27] = 1
E[["minus","subtract","difference","fewer","left"], 27] = 2
E[["times","multiply","product","twice","double","triple"], 27] = 3
E[["divided","division","equally","half","quarter"], 27] = 4
E[5:15, 28] = 1
E[2035:2592, 28] = 1
E[["i","my","the","it","this","that","we","our","sun","moon","cat","dog","water","people"], 28] = 1
E[["BOS","USER","BOT"], 37] = 1
E[["BOS","BOT"], 39] = -1
E["USER", 39] = 1
E["?", 124] = 1
E[["is","are","was","were","am"], 125] = 1
E[["right","correct"], 126] = 1
E[["hello","hi","hey","welcome"], 127] = 1
E[["thank","thanks","appreciate"], 128] = 1
E[["you","your","yourself","bot","robot","assistant"], 129] = 1
E[["name","called"], 130] = 1
E[["weight","written","hand","training","program","created","built","make","made"], 131] = 1
E[["can","able","do","help","answer"], 132] = 1
E["capital", 133] = 1
E[["country","where","located","location"], 134] = 1
E["continent", 135] = 1
E["planet", 136] = 1
E[["big","large"], 137] = 1
E[["small","little"], 138] = 1
E[["colour","color"], 139] = 1
E[["write","wrote","written","author"], 140] = 1
E["opposite", 141] = 1
E[["same","mean"], 142] = 1
E[["math","maths","plus","minus","times","add","subtract","multiply","divided","sum","total","product","difference"], 143] = 1
E[["not","bad","wrong","poor","sad","terrible","stupid"], 144] = 1
E[["my","made","plan","idea","cake","work","art"], 145] = 1
E["how", 146] = 1
E["who", 147] = 1
E["what", 148] = 1
E["when", 149] = 1
E["why", 150] = 1
E["first", 152] = 1
E[["current","president"], 153] = 1
E[["many","much","number","count"], 154] = 1

# Layer 1: clock, previous-token digit features, message role.
V1[0, 15, 0] = 1
O1[0, 0, 30] = 1
Q1[1, 0, 0:16] = [54.0302,-84.1471,84.6009,-53.3168,95.0415,-31.0984,98.4230,-17.6892,99.5004,-9.98334,99.8419,-5.62045,99.9500,-3.16175,99.9842,-1.77819]
K1[1, 0, 0:16:2] = 100
V1[1, 13, 0] = 1
V1[1, 14, 1] = 1
O1[1, 0, 33] = 1
O1[1, 1, 34] = 1
Q1[2, 0, 0:16] = [-41.6147,-90.9297,43.1462,-90.2131,80.6578,-59.1127,93.7418,-34.8205,98.0067,-19.8669,99.3682,-11.2231,99.8001,-6.32034,99.9368,-3.55581]
K1[2, 0, 0:16:2] = 100
V1[2, 13, 0] = 1
V1[2, 14, 1] = 1
O1[2, 0, 35] = 1
O1[2, 1, 36] = 1
Q1[3, 0, 30:32] = [1,1]
K1[3, 37, 30] = 1000000
V1[3, 39, 0] = 1
O1[3, 0, 46] = 1
M1_in[30, 0:191] = [
-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,
-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,
-21,-22,-23,-24,-25,-26,-27,-28,-29,-30,
-31,-32,-33,-34,-35,-36,-37,-38,-39,-40,
-41,-42,-43,-44,-45,-46,-47,-48,-49,-50,
-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,
-61,-62,-63,-64,-65,-66,-67,-68,-69,-70,
-71,-72,-73,-74,-75,-76,-77,-78,-79,-80,
-81,-82,-83,-84,-85,-86,-87,-88,-89,-90,
-91,-92,-93,-94,-95,-96,-97,-98,-99,-100,
-101,-102,-103,-104,-105,-106,-107,-108,-109,-110,
-111,-112,-113,-114,-115,-116,-117,-118,-119,-120,
-121,-122,-123,-124,-125,-126,-127,-128,-129,-130,
-131,-132,-133,-134,-135,-136,-137,-138,-139,-140,
-141,-142,-143,-144,-145,-146,-147,-148,-149,-150,
-151,-152,-153,-154,-155,-156,-157,-158,-159,-160,
-161,-162,-163,-164,-165,-166,-167,-168,-169,-170,
-171,-172,-173,-174,-175,-176,-177,-178,-179,-180,
-181,-182,-183,-184,-185,-186,-187,-188,-189,-190,-191]
M1_b[0:191] = 1
M1_out[0:191, 31] = 2
M1_out[0:191, 32] = [
2,8,14,20,26,32,38,44,50,56,
62,68,74,80,86,92,98,104,110,116,
122,128,134,140,146,152,158,164,170,176,
182,188,194,200,206,212,218,224,230,236,
242,248,254,260,266,272,278,284,290,296,
302,308,314,320,326,332,338,344,350,356,
362,368,374,380,386,392,398,404,410,416,
422,428,434,440,446,452,458,464,470,476,
482,488,494,500,506,512,518,524,530,536,
542,548,554,560,566,572,578,584,590,596,
602,608,614,620,626,632,638,644,650,656,
662,668,674,680,686,692,698,704,710,716,
722,728,734,740,746,752,758,764,770,776,
782,788,794,800,806,812,818,824,830,836,
842,848,854,860,866,872,878,884,890,896,
902,908,914,920,926,932,938,944,950,956,
962,968,974,980,986,992,998,1004,1010,1016,
1022,1028,1034,1040,1046,1052,1058,1064,1070,1076,
1082,1088,1094,1100,1106,1112,1118,1124,1130,1136,1142]
M1_in[14, 191] = 1
M1_out[191, 38] = 1
M1_in[34, 192] = 1
M1_in[13, 192] = 10
M1_b[192] = -10
M1_out[192, 38] = 10
M1_in[36, 193] = 1
M1_in[13, 193] = 10
M1_in[33, 193] = 10
M1_b[193] = -20
M1_out[193, 38] = 100

# Layer 2: message boundaries and user-only records.
Q2[0, 0, 30:32] = [1,1]
K2[0, 16, 30] = 1000000
V2[0, 31, 0] = 1
V2[0, 32, 1] = 1
O2[0, 0, 41] = 1
O2[0, 1, 42] = 1
Q2[1, 0, 30:32] = [1,1]
K2[1, 17, 30] = 1000000
V2[1, 31, 0] = 1
V2[1, 32, 1] = 1
O2[1, 0, 43] = 1
O2[1, 1, 44] = 1
Q2[2, 0, 0:16] = [54.0302,-84.1471,84.6009,-53.3168,95.0415,-31.0984,98.4230,-17.6892,99.5004,-9.98334,99.8419,-5.62045,99.9500,-3.16175,99.9842,-1.77819]
K2[2, 0, 0:16:2] = 100
V2[2, 38, 0] = 1
O2[2, 0, 40] = 1
M2_in[31, 0] = 1
M2_in[43, 0] = -1
M2_out[0, 45] = 1
M2_in[33, 1] = 1
M2_in[13, 1] = -1
M2_in[46, 1] = 1
M2_in[17, 1] = 2
M2_b[1] = -1
M2_out[1, 47] = 1
M2_in[40, 2] = 1
M2_in[33, 2] = 1000
M2_in[13, 2] = -1000
M2_in[46, 2] = 1000
M2_in[17, 2] = 2000
M2_b[2] = -2000
M2_out[2, 48] = 1
M2_in[18, 3] = 1
M2_in[46, 3] = 1
M2_b[3] = -1
M2_out[3, 220] = 1
M2_in[21, 4] = 1
M2_in[46, 4] = 1
M2_b[4] = -1
M2_out[4, 221] = 1
M2_in[22:26, 5] = 1
M2_in[46, 5] = 1
M2_b[5] = -1
M2_out[5, 227] = 1

# Layer 3: read the latest user's message.
Q3[0, 0, 30:32] = [1,1]
K3[0, 220, 30] = 1000000
K3[0, 15, 30] = 100000
V3[0, 31, 0] = 1
O3[0, 0, 49] = 1
Q3[1, 41, 28] = 256
Q3[1, 0, 28] = 256
Q3[1, 0, 30] = 128
K3[1, 31, 28] = 1
K3[1, 32, 30] = -1
V3[1, 28, 0] = 1
V3[1, 26, 1] = 1
O3[1, 0, 68] = 1
O3[1, 1, 69] = 1
Q3[2, 0, 30] = 1
K3[2, 46, 30] = 10000
K3[2, 41, 30] = 50
V3[2, 124, 0] = 1
V3[2, 125, 1] = 1
V3[2, 126, 2] = 1
V3[2, 127, 3] = 1
V3[2, 128, 4] = 1
V3[2, 129, 5] = 1
V3[2, 130, 6] = 1
V3[2, 131, 7] = 1
V3[2, 132, 8] = 1
V3[2, 133, 9] = 1
V3[2, 134, 10] = 1
V3[2, 135, 11] = 1
V3[2, 136, 12] = 1
V3[2, 137, 13] = 1
V3[2, 138, 14] = 1
V3[2, 139, 15] = 1
V3[2, 140, 16] = 1
V3[2, 141, 17] = 1
V3[2, 142, 18] = 1
V3[2, 143, 19] = 1
V3[2, 144, 20] = 1
V3[2, 145, 21] = 1
V3[2, 146, 22] = 1
V3[2, 147, 23] = 1
V3[2, 148, 24] = 1
V3[2, 149, 25] = 1
V3[2, 150, 26] = 1
V3[2, 151, 27] = 1
V3[2, 152, 28] = 1
V3[2, 153, 29] = 1
V3[2, 154, 30] = 1
V3[2, 155, 31] = 1
O3[2, 0, 156] = 1
O3[2, 1, 157] = 1
O3[2, 2, 158] = 1
O3[2, 3, 159] = 1
O3[2, 4, 160] = 1
O3[2, 5, 161] = 1
O3[2, 6, 162] = 1
O3[2, 7, 163] = 1
O3[2, 8, 164] = 1
O3[2, 9, 165] = 1
O3[2, 10, 166] = 1
O3[2, 11, 167] = 1
O3[2, 12, 168] = 1
O3[2, 13, 169] = 1
O3[2, 14, 170] = 1
O3[2, 15, 171] = 1
O3[2, 16, 172] = 1
O3[2, 17, 173] = 1
O3[2, 18, 174] = 1
O3[2, 19, 175] = 1
O3[2, 20, 176] = 1
O3[2, 21, 177] = 1
O3[2, 22, 178] = 1
O3[2, 23, 179] = 1
O3[2, 24, 180] = 1
O3[2, 25, 181] = 1
O3[2, 26, 182] = 1
O3[2, 27, 183] = 1
O3[2, 28, 184] = 1
O3[2, 29, 185] = 1
O3[2, 30, 186] = 1
O3[2, 31, 187] = 1
Q3[3, 0, 30:32] = [1,1]
K3[3, 221, 30] = 1000000
K3[3, 15, 30] = 100000
V3[3, 1, 0] = 1
V3[3, 2, 1] = 1
V3[3, 3, 2] = 1
V3[3, 4, 3] = 1
V3[3, 5, 4] = 1
V3[3, 6, 5] = 1
V3[3, 7, 6] = 1
V3[3, 8, 7] = 1
V3[3, 9, 8] = 1
V3[3, 10, 9] = 1
V3[3, 11, 10] = 1
V3[3, 12, 11] = 1
V3[3, 31, 12] = 1
O3[3, 0, 51] = 1
O3[3, 1, 52] = 1
O3[3, 2, 53] = 1
O3[3, 3, 54] = 1
O3[3, 4, 55] = 1
O3[3, 5, 56] = 1
O3[3, 6, 57] = 1
O3[3, 7, 58] = 1
O3[3, 8, 59] = 1
O3[3, 9, 60] = 1
O3[3, 10, 61] = 1
O3[3, 11, 62] = 1
O3[3, 12, 63] = 1
Q3[4, 0, 30] = 1
K3[4, 47, 30] = 1000000
K3[4, 41, 30] = 4096
K3[4, 31, 30] = -32
V3[4, 48, 0] = 1
V3[4, 47, 1] = 1
V3[4, 41, 2] = 1
O3[4, 0, 64] = 1
O3[4, 1, 228] = 1
O3[4, 2, 230] = 1
Q3[5, 0, 30] = 1
K3[5, 47, 30] = 1000000
K3[5, 41, 30] = 4096
K3[5, 31, 30] = 32
V3[5, 48, 0] = 1
V3[5, 47, 1] = 1
V3[5, 41, 2] = 1
O3[5, 0, 65] = 1
O3[5, 1, 229] = 1
O3[5, 2, 231] = 1
Q3[6, 0, 30:32] = [1,1]
K3[6, 227, 30] = 1000000
K3[6, 15, 30] = 100000
V3[6, 27, 0] = 1
V3[6, 31, 1] = 1
O3[6, 0, 66] = 1
O3[6, 1, 67] = 1
M3_in[41, 0] = 1
M3_b[0] = 1
M3_out[0, 70] = 1
M3_in[49, 1] = 1
M3_in[41, 1] = -1
M3_out[1, 70] = 1
M3_in[49, 2:4] = 2
M3_in[41, 2:4] = -2
M3_b[2:4] = [0,-1]
M3_out[2:4, 71] = [1,-1]
M3_b[4:68:2] = -0.1
M3_b[5:68:2] = -1.1
M3_in[156, 4:6] = 1000
M3_in[157, 6:8] = 1000
M3_in[158, 8:10] = 1000
M3_in[159, 10:12] = 1000
M3_in[160, 12:14] = 1000
M3_in[161, 14:16] = 1000
M3_in[162, 16:18] = 1000
M3_in[163, 18:20] = 1000
M3_in[164, 20:22] = 1000
M3_in[165, 22:24] = 1000
M3_in[166, 24:26] = 1000
M3_in[167, 26:28] = 1000
M3_in[168, 28:30] = 1000
M3_in[169, 30:32] = 1000
M3_in[170, 32:34] = 1000
M3_in[171, 34:36] = 1000
M3_in[172, 36:38] = 1000
M3_in[173, 38:40] = 1000
M3_in[174, 40:42] = 1000
M3_in[175, 42:44] = 1000
M3_in[176, 44:46] = 1000
M3_in[177, 46:48] = 1000
M3_in[178, 48:50] = 1000
M3_in[179, 50:52] = 1000
M3_in[180, 52:54] = 1000
M3_in[181, 54:56] = 1000
M3_in[182, 56:58] = 1000
M3_in[183, 58:60] = 1000
M3_in[184, 60:62] = 1000
M3_in[185, 62:64] = 1000
M3_in[186, 64:66] = 1000
M3_in[187, 66:68] = 1000
M3_out[4:6, 188] = [1,-1]
M3_out[6:8, 189] = [1,-1]
M3_out[8:10, 190] = [1,-1]
M3_out[10:12, 191] = [1,-1]
M3_out[12:14, 192] = [1,-1]
M3_out[14:16, 193] = [1,-1]
M3_out[16:18, 194] = [1,-1]
M3_out[18:20, 195] = [1,-1]
M3_out[20:22, 196] = [1,-1]
M3_out[22:24, 197] = [1,-1]
M3_out[24:26, 198] = [1,-1]
M3_out[26:28, 199] = [1,-1]
M3_out[28:30, 200] = [1,-1]
M3_out[30:32, 201] = [1,-1]
M3_out[32:34, 202] = [1,-1]
M3_out[34:36, 203] = [1,-1]
M3_out[36:38, 204] = [1,-1]
M3_out[38:40, 205] = [1,-1]
M3_out[40:42, 206] = [1,-1]
M3_out[42:44, 207] = [1,-1]
M3_out[44:46, 208] = [1,-1]
M3_out[46:48, 209] = [1,-1]
M3_out[48:50, 210] = [1,-1]
M3_out[50:52, 211] = [1,-1]
M3_out[52:54, 212] = [1,-1]
M3_out[54:56, 213] = [1,-1]
M3_out[56:58, 214] = [1,-1]
M3_out[58:60, 215] = [1,-1]
M3_out[60:62, 216] = [1,-1]
M3_out[62:64, 217] = [1,-1]
M3_out[64:66, 218] = [1,-1]
M3_out[66:68, 219] = [1,-1]

# Layer 4: mutually exclusive belief/statement agreement routes.
M4_in[71, 0] = 1
M4_out[0, 222] = 1
M4_in[68, 1] = 1
M4_in[189, 1] = 1
M4_in[188, 1] = -1
M4_in[71, 1] = -1
M4_in[190, 1] = -1
M4_in[69, 1] = -1
M4_b[1] = -1
M4_out[1, 222] = 1
M4_in[68, 2] = 1
M4_in[190, 2] = 1
M4_in[71, 2] = -1
M4_in[69, 2] = -1
M4_b[2] = -1
M4_out[2, 222] = 1

# Layer 5: copy pointer and bounded emission phases.
Q5[0, 70, 28] = 256
Q5[0, 45, 28] = 256
Q5[0, 0, 28] = -1280
Q5[0, 0, 30] = 128
K5[0, 31, 28] = 1
K5[0, 32, 30] = -1
V5[0, 1, 0] = 1
V5[0, 2, 1] = 1
V5[0, 3, 2] = 1
V5[0, 4, 3] = 1
V5[0, 5, 4] = 1
V5[0, 6, 5] = 1
V5[0, 7, 6] = 1
V5[0, 8, 7] = 1
V5[0, 9, 8] = 1
V5[0, 10, 9] = 1
V5[0, 11, 10] = 1
V5[0, 12, 11] = 1
V5[0, 19, 12] = 1
O5[0, 0, 90] = 1
O5[0, 1, 91] = 1
O5[0, 2, 92] = 1
O5[0, 3, 93] = 1
O5[0, 4, 94] = 1
O5[0, 5, 95] = 1
O5[0, 6, 96] = 1
O5[0, 7, 97] = 1
O5[0, 8, 98] = 1
O5[0, 9, 99] = 1
O5[0, 10, 100] = 1
O5[0, 11, 101] = 1
O5[0, 12, 102] = 1
M5_in[45, 0:4] = 1
M5_in[222, 0:4] = 100
M5_in[20, 0:4] = -100
M5_b[0:4] = [-104,-105,-145,-146]
M5_out[0:4, 223] = [1,-1,-1,1]
M5_in[45, 4:6] = 1
M5_in[222, 4:6] = 100
M5_in[20, 4:6] = 100
M5_b[4:6] = [-205,-206]
M5_out[4:6, 225] = [1,-1]

# Layer 6: prefix and default second sentence.
M6_in[45, 0:41] = 1
M6_b[0:15] = [1,0,-1,0,-1,-2,-1,-2,-3,-2,-3,-4,-3,-4,-5]
M6_out[[0,2], 112:124] = [-1,-1,1,1,1,-1,1,-1,-1,-1,-1,-1]
M6_out[1, 112:124] = [2,2,-2,-2,-2,2,-2,2,2,2,2,2]
M6_out[[3,5], 112:124] = [1,-1,1,-1,-1,-1,1,1,1,1,-1,-1]
M6_out[4, 112:124] = [-2,2,-2,2,2,2,-2,-2,-2,-2,2,2]
M6_out[[6,8], 112:124] = [1,-1,1,1,1,1,1,-1,-1,-1,-1,-1]
M6_out[7, 112:124] = [-2,2,-2,-2,-2,-2,-2,2,2,2,2,2]
M6_out[[9,11], 112:124] = [1,1,1,1,1,-1,-1,1,-1,1,1,-1]
M6_out[10, 112:124] = [-2,-2,-2,-2,-2,2,2,-2,2,-2,-2,2]
M6_out[[12,14], 112:124] = [-1,1,-1,-1,1,-1,-1,-1,-1,-1,-1,-1]
M6_out[13, 112:124] = [2,-2,2,2,-2,2,2,2,2,2,2,2]
M6_in[222, 15:41] = -100
M6_b[15:39] = [-4,-5,-6,-5,-6,-7,-6,-7,-8,-7,-8,-9,-8,-9,-10,-9,-10,-11,-10,-11,-12,-11,-12,-13]
M6_out[[15,17], 112:124] = [-1,1,-1,1,1,-1,1,-1,-1,-1,-1,-1]
M6_out[16, 112:124] = [2,-2,2,-2,-2,2,-2,2,2,2,2,2]
M6_out[[18,20], 112:124] = [1,-1,1,-1,1,1,1,1,1,1,-1,-1]
M6_out[19, 112:124] = [-2,2,-2,2,-2,-2,-2,-2,-2,-2,2,2]
M6_out[[21,23], 112:124] = [1,-1,1,-1,1,1,1,1,-1,1,-1,-1]
M6_out[22, 112:124] = [-2,2,-2,2,-2,-2,-2,-2,2,-2,2,2]
M6_out[[24,26], 112:124] = [-1,1,1,-1,-1,-1,1,-1,-1,-1,-1,-1]
M6_out[25, 112:124] = [2,-2,-2,2,2,2,-2,2,2,2,2,2]
M6_out[[27,29], 112:124] = [1,1,-1,1,1,-1,1,1,1,-1,-1,-1]
M6_out[28, 112:124] = [-2,-2,2,-2,-2,2,-2,-2,-2,2,2,2]
M6_out[[30,32], 112:124] = [1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,-1]
M6_out[31, 112:124] = [-2,2,2,-2,2,2,-2,2,2,2,2,2]
M6_out[[33,35], 112:124] = [-1,-1,1,1,1,-1,1,-1,-1,-1,-1,-1]
M6_out[34, 112:124] = [2,2,-2,-2,-2,2,-2,2,2,2,2,2]
M6_out[[36,38], 112:124] = [1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1]
M6_out[37, 112:124] = [-2,-2,-2,-2,2,2,2,2,2,2,2,2]
M6_b[39:41] = [-12,-13]
M6_out[39, 112:124] = [1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
M6_out[40, 112:124] = [-1,1,1,1,1,1,1,1,1,1,1,1]

# Gated copying of any vocabulary token.
M6_in[223, 41:65] = 2
M6_in[102, 41:65] = -2
M6_b[41:65] = -2
M6_in[90, 41:43] = [1,-1]
M6_in[91, 43:45] = [1,-1]
M6_in[92, 45:47] = [1,-1]
M6_in[93, 47:49] = [1,-1]
M6_in[94, 49:51] = [1,-1]
M6_in[95, 51:53] = [1,-1]
M6_in[96, 53:55] = [1,-1]
M6_in[97, 55:57] = [1,-1]
M6_in[98, 57:59] = [1,-1]
M6_in[99, 59:61] = [1,-1]
M6_in[100, 61:63] = [1,-1]
M6_in[101, 63:65] = [1,-1]
M6_out[41:43, 112] = [1,-1]
M6_out[43:45, 113] = [1,-1]
M6_out[45:47, 114] = [1,-1]
M6_out[47:49, 115] = [1,-1]
M6_out[49:51, 116] = [1,-1]
M6_out[51:53, 117] = [1,-1]
M6_out[53:55, 118] = [1,-1]
M6_out[55:57, 119] = [1,-1]
M6_out[57:59, 120] = [1,-1]
M6_out[59:61, 121] = [1,-1]
M6_out[61:63, 122] = [1,-1]
M6_out[63:65, 123] = [1,-1]
M6_in[223, 65] = 1
M6_in[102, 65] = 1
M6_b[65] = -1
M6_out[65, 112:124] = [1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1]
M6_in[225, 66] = 1
M6_out[66, 112:124] = [1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

# Force a sentence boundary and EOS before the generation limit.
M6_in[45, 67:72] = 1
M6_in[222, 67:72] = 100
M6_in[20, 67:70] = -100
M6_b[67:72] = [-145,-146,-147,-146,-147]
M6_out[[67,69], 112:124] = [1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1]
M6_out[68, 112:124] = [-2,-2,-2,-2,2,2,2,2,2,2,2,2]
M6_out[70, 112:124] = [1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
M6_out[71, 112:124] = [-1,1,1,1,1,1,1,1,1,1,1,1]

# Pronoun transformations while echoing the person's assertion.
M6_in[223, 72:78] = 2
M6_in[102, 72:78] = -2
M6_b[72:78] = -13
M6_in[90:102, 72] = [-1,1,-1,1,1,-1,1,-1,-1,-1,-1,-1]
M6_out[72, 112:124] = [0,-2,2,0,0,0,0,0,0,0,0,0]
M6_in[90:102, 73] = [1,-1,1,-1,1,1,1,1,1,1,-1,-1]
M6_out[73, 112:124] = [0,0,0,0,-2,-2,0,0,0,0,0,0]
M6_in[90:102, 74] = [-1,1,1,-1,-1,-1,1,1,1,1,-1,-1]
M6_out[74, 112:124] = [2,-2,-2,2,0,0,0,0,0,0,0,0]
M6_in[90:102, 75] = [-1,-1,1,1,-1,-1,1,1,1,1,-1,-1]
M6_out[75, 112:124] = [0,0,0,0,2,0,0,-2,-2,-2,0,0]
M6_in[90:102, 76] = [1,1,1,-1,-1,-1,1,1,1,1,-1,-1]
M6_out[76, 112:124] = [-2,-2,0,2,2,0,0,-2,-2,-2,0,0]
M6_in[90:102, 77] = [-1,-1,1,1,1,-1,1,1,1,1,-1,-1]
M6_out[77, 112:124] = [2,0,-2,0,-2,0,0,0,0,0,0,0]

# In agreement mode, the prefix says "right" rather than "smart".
M6_in[45, 78:81] = 1
M6_in[222, 78:81] = 100
M6_b[78:81] = [-102,-103,-104]
M6_out[[78,80], 112:124] = [-2,-2,-2,0,0,0,0,-2,2,0,-2,0]
M6_out[79, 112:124] = [4,4,4,0,0,0,0,4,-4,0,4,0]
```