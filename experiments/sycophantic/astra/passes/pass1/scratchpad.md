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