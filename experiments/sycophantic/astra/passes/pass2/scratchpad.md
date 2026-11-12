PASS 2: Added arithmetic circuits, a small factual lookup system, self-description and conversational templates. These are hand-designed, untested weights, not a complete general chatbot. No execution or tools have been used. PASS 3 should inspect the circuits, improve arithmetic formatting and coverage, add knowledge, and repair copying/selection.

CORE INFRASTRUCTURE RETAINED
All tokens: E[:,0]=1; dimensions1..12 are signed binary token-ID bits. U[112..123] decodes the same bits.
L1 uniform BOS attention gives d30=1/(t+1). M1 units0..190 synthesize d31=t and d32=t².
“Latest marker” heads use slow RoPE pair30/31, Q=[1,1], Kmarker=1e6, so recent marked positions win.
Pointer heads use Q28=256*target, K28=position, Q30=128, K30=-position².
L1 previous/two-back heads provide digit context. M1 assembles up to three-digit integers in d38.
L2 retrieves latest USER/BOT positions, assembles number-end records, and gates user-only markers.
L3 retrieves current-message semantics, first/last numbers, latest operation, belief cue, and latest entity.
All existing copying and praise-prefix machinery remains, except personal nonnumeric messages are routed to encouragement and “think that” can skip “that”.

RESIDUAL MAP
0 constant; 1..12 token bits.
13 digit;14 digit value;15 BOS;16 USER/BOS;17 BOT/BOS.
18 belief cue;19 copy terminator;20 period;21 entity.
22 add,23 subtract,24 multiply,25 divide,26 question starter,27 operation code1..4,28 declarative starter.
29 personal-message flag without numbers, computed M3.
30 reciprocal clock;31 position;32 position².
33/34 preceding digit flag/value;35/36 two-back flag/value.
37 structural role marker;38 local integer;39 USER +1, BOT/BOS -1;40 preceding local integer.
41/42 latest USER position/square;43/44 latest BOT position/square;45 output step k=t-BOTpos.
46 latest role;47 numeric-record flag;48 record value;49 latest belief-cue position.
50 RAW “that” indicator.
51..60 RAW factual properties, NOT entity token bits anymore:
51 capital answer ID
52 continent
53 country/location
54 color
55 opposite
56 generic identity
57 author/inventor (currently no populated facts)
58 largest
59 smallest
60 currency
61/62 unused.
63 latest entity position;64 first number;65 last number;66 latest operation;67 operation position.
68/69 first user token declarative/question flags;70 copy start;71 current belief flag.
72..81 contextual factual properties corresponding to raw51..60.
82 copy-start “that” flag from L4 pointer;83 unused.
84 entity belongs to current message.
85 selected factual answer ID;86 selected-fact flag.
87 arithmetic-available flag BEFORE copy precedence.
88 arithmetic answer: add/sub in M4, multiplication/division added in M5.
89 active arithmetic mode AFTER copy precedence.
90..101 copied token bits;102 copied terminator.
103/104/105 last operand ones/tens/hundreds.
106/107/108/109 operation one-hots add/sub/multiply/divide.
110 numeric-record staleness;111 operation staleness.
112..123 ordinary bit-code output.
124..155 raw lexical relation flags.
156..187 initial relation bags from L3. IMPORTANT: M4 clears156..185 and reuses them as 30 decimal-digit one-hots:
156..165 ones 0..9;
166..175 tens 0..9;
176..185 hundreds 0..9.
186/187 remain old bags.
188..219 clipped lexical flags:
188 question mark,189 copula,190 right/correct,191 greeting,192 thanks,
193 self-reference,194 name,195 construction,196 ability,
197 capital,198 country/location,199 continent,200 planet,
201 large,202 small,203 color,204 author,205 opposite,206 same/mean,
207 arithmetic,208 negative,209 personal creation,210 how,211 who,
212 what,213 when,214 why,215 currency,216 first,217 president/current,
218 quantity,219 unused.
220 user cue;221 user entity;222 copy mode;223 copy phase;224 active factual mode;
225 EOS-after-copy-period;226 unused;227 user operation;
228/229 first/last number validity;230/231 associated USER positions.
232 self identity mode;233 name;234 hand-written construction;235 abilities;
236 greeting;237 thanks;238 encouragement.
239 unused.
240..243 arithmetic digit phases, at k7/8/9/10.
244 factual answer phase, k7.
245 arithmetic-or-factual sentence mode.
246..249 unused.
250 scalar output coordinate;251 scalar output indicator;252..255 unused.

SCALAR OUTPUT DICTIONARY
New outputs use d250=x,d251=1. Each registered token j has U250=2j and U251=100-j², selecting the nearest dictionary index. At inactive steps both coordinates are zero. Original token-bit output remains for prefix/copy/default.
Indices:
1..10 digit0..9;
11 it,12 is,13 period,14 i,15 am,16 a,17 small,18 chat,19 bot,
20 have,21 no,22 name,23 my,24 weight,25 -s,26 were,27 written,
28 by,29 hand,30 can,31 and,32 answer,33 question,34 do,35 math,
36 hello,37 comma,38 happy,39 to,40 talk,41 with,42 you,43 !,
44 are,45 welcome,46 very,47 good,48 EOS.
49 paris,50 london,51 canberra,52 washington,53 ottawa,54 berlin,
55 rome,56 madrid,57 lisbon,58 moscow,59 beijing,60 tokyo,61 delhi,
62 brasilia,63 cairo,64 pretoria,65 nairobi,66 abuja,67 accra,
68 rabat,69 algiers,70 tunis,71 tripoli,72 khartoum,73 ankara,
74 athens,75 dublin,76 reykjavik,77 oslo,78 stockholm,79 helsinki,
80 copenhagen,81 amsterdam,82 brussels,83 bern,84 vienna,85 prague,
86 warsaw,87 budapest,88 bucharest,89 sofia,90 belgrade,91 kyiv,
92 minsk,93 riga,94 vilnius,95 tallinn,96 bratislava,97 ljubljana,
98 tirana,99 wellington.
100 asia,101 europe,102 africa,103 america,104 antarctica,105 oceania,
106 pacific,107 atlantic,108 arctic,109 everest,110 nile,111 amazon,
112 sahara,113 jupiter,114 mercury,115 earth,116 mars,117 venus,
118 saturn,119 neptune,120 uranus,121 sun,122 star,123 planet,
124 moon,125 water,126 blue,127 green,128 red,129 yellow,130 white,
131 black,132 hot,133 cold,134 big,135 bad,136 sad,137 day,138 night,
139 man,140 woman,141 king,142 queen,143 light,144 dark,145 dog,
146 cat,147 shakespeare,148 einstein,149 newton,150 edison,151 darwin,
152 france,153 germany,154 italy,155 spain,156 japan,157 russia,
158 australia,159 canada,160 brazil,161 egypt,162 england,163 greece,
164 turkey,165 nepal,166 peru,167 usa,168 china,169 india,170 mexico,
171 dollar,172 gold,173 silver,174 iron,175 liquid,176 gas,177 solid,
178 animal,179 bird,180 fish,181 open,182 shut,183 up,184 down,
185 left,186 right,187 true,188 false,189 yes,190 not,191 fast,
192 slow,193 young,194 old,195 long,196 short,197 hard,198 soft,
199 clean,200 dirty,201 full.
New dictionary entries can use unused indices202+, setting the two U weights by token name.

ATTENTION
L1 h0 clock;h1 previous digit;h2 two-back digit;h3 latest role;h4..7 free.
L2 h0 USER boundary;h1 BOT boundary;h2 previous number;h3..7 free.
L3 h0 cue;h1 first user token;h2 current-user lexical bag;
h3 REPLACED: latest user entity -> ten factual properties72..81 and position63;
h4 first number;h5 last number;h6 operation;h7 free.
L4 h0 pointer to copy start, fetching raw “that” into82;h1..7 free.
L5 h0 copy pointer;h1..7 free.
L6 all heads free.

MLP ALLOCATION
M1 units0..193 as before;194+ free.
M2 units0..5 as before;6+ free.
M3:
0..67 original copy-start and relation clipping;
68/69 current entity validity;
70/71 personal nonnumeric flag29;
72..269 floor(lastOperand/10), 99 paired clipped thresholds;
270..287 floor(lastOperand/100), nine paired thresholds;
288 raw last operand, finishing decimal decomposition;
289..300 four operation hats;
301/302 numeric record age;303 operation age.
304+ free.
M4:
0..2 copy modes, now inhibited by29;
3..22 ten factual selectors, each pair emits scalar85 and flag86.
Priority: capital,continent,opposite,color,currency,author,largest,smallest,country,identity.
23 arithmetic availability;
24 addition;25 nonnegative subtraction;
26 skip leading “that” after a belief cue;
27..31 free;
32..61 cancel old relation bags156..185;
62..151 decimal digit one-hots into those cleared coordinates;
152+ free.
M5:
0..5 original copy phases;
6 arithmetic mode89 and245;
7 factual mode224 and245;
8..14 seven conversational modes232..238;
15 unused;
16..27 numeric step phases240..243;
28..30 factual answer phase244;
31..60 multiplication, using decimal digit one-hots and gated copies of first operand;
61..80 division for denominators1..12,15,20,25,50,100,200,250,500.
81+ free.
M6:
0..80 original prefix/copy/default. Default15..40 now additionally suppressed by every new mode.
81..86 “it is” for factual/arithmetic answers;
87/88 factual scalar answer;
89..92 numeric scalar coordinates;93..96 numeric indicators;
97..101 arithmetic period/EOS;102..106 factual period/EOS.
107..129 identity “i am a small chat bot .”
130..146 name “i have no name .”
147..172 construction “my weight -s were written by hand .”
173..207 abilities “i can chat and answer question -s and do math .”
208..239 greeting “hello , i am happy to talk with you !”
240..253 thanks “you are welcome !”
254..270 encouragement “it is very good !”
271+ free.

ARITHMETIC DETAILS / LIMITATIONS
First operand64 and last operand65 are extracted from the latest message.
Add/sub use M4. Multiplication is exact in ideal arithmetic: M3 decomposes b, M4 makes decimal one-hots, M5 gates a under each one-hot and adds digit-weighted contributions.
Division is populated only for denominators listed above; other divisors currently produce zero, NOT a correct answer. Unary half/twice etc. remain unsupported.
Arithmetic emits “it is” followed by FOUR digits, INCLUDING LEADING ZEROES, then period/EOS. At k7, scalar decoder input is answer/1000+.50025. At k8/9/10 it is answer/100, /10, /1 minus10*the locally assembled generated prefix plus.50025. This rounds to the desired dictionary digit index. Leading zeros should be improved in pass3 if feasible. d38 can hold the needed three-digit prefix.
Some word-problem operations were annotated: give/lost/spend/eat subtract; get/buy/more add; each/per multiply; share/among/over divide.
No general word-problem parser is implemented. Negative subtraction is clamped to zero.

FACTS
Capital table covers51 countries through New Zealand (token zealand). Continent, selected city-country, colors, opposites, simple identity, largest/smallest, and dollar-currency mappings populated.
Facts are returned as “you are so smart ! it is ANSWER .”
The head only retrieves the LAST marked entity. Distracting entities can therefore break answers.
Author property is reserved but unpopulated.
Capital Delhi and geographic/general-category answers are simplified; this is a finite table.

PRIORITY / COPY
Copy has priority over factual/arithmetic modes. Personal nonnumeric messages inhibit copy and receive encouragement unless self/greeting/thanks/facts take precedence. This intentionally prevents echoing “my cake is not good”.
Copy still stops at first punctuation, converts i/am/my/me/we/our, and uses “you are so right !”.
Original generic fallback: “you are so smart ! i am happy to talk with you .”
All intended routes terminate within48 generated tokens.

PASS 3 RECOMMENDATIONS
Inspect allocations and numerical behavior symbolically; no execution is available.
Improve standard decimal formatting, division coverage, unary operations, factual coverage and small word tasks.
Avoid claiming broad capabilities are complete.
A serious limitation remains that unsupported questions return conversational fallback or incomplete arithmetic.
Keep dictionary output channels separate from original signed-bit channels and suppress competing routes.
=====