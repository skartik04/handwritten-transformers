PASS 1 DESIGN / STATUS
No tools or execution used. This pass installs a functioning positional clock, user-only semantic retrieval, a scalar-coded output vocabulary, fixed conversational responses, opposites, echo, remembered personal names, and emotional responses. Facts/arithmetic are not yet implemented. All weights not explicitly written remain zero. Next passes should extend this foundation, not replace the clock/output machinery.

IMPORTANT: OUTPUT CODING
Residual 224 = output token code A; 225 = active weight B.
For each supported output token with code c, U[224,token]=2c, U[225,token]=1-c*c. Thus logits select the token nearest A/B. U[0,EOS]=0.5 is the default: no active output means EOS. Codes must stay <=999 (squares within weight bound). Static template units emit A=c,B=1. Dynamic masks are converted to A=payload,B=1 by M5. Input identity code is E[token,7].
Current output codes:
1 i; 2 am; 3 a; 4 small; 5 chat; 6 bot; 7 .; 8 can; 9 answer; 10 question; 11 -s; 12 and; 13 do; 14 maths; 15 hello; 16 !; 17 how; 18 help; 19 you; 20 today; 21 ?; 22 are; 23 good; 24 ,; 25 thank; 26 welcome; 27 goodbye; 28 have; 29 nice; 30 day; 31 sorry; 32 feel; 33 tired; 34 please; 35 rest; 36 well; 37 happy; 38 to; 39 hear; 40 that.
41 your; 42 name; 43 is; 44 my; 45 weight; 46 were; 47 written; 48 by; 49 hand; 50 no; 51 not; 52 sure; 53 tell; 54 me; 55 more; 56 the; 57 opposite; 58 of; 59 it; 60 yes; 61 cold; 62 hot; 63 big; 64 large; 65 little; 66 okay; 67 human; 68 age; 69 personal; 70 feeling; 71 but; 72 about; 73 be; 74 what; 75 like; 76 sound; 77 made; 78 bad; 79 here; 80 listen.
81 hope; 82 weather; 83 food; 84 fun; 85 eat; 86 go; 87 -es; 88 remember; 89 take; 90 break; 91 family; 92 important; 93 pet; 94 friend; 95 red; 96 blue; 97 green; 98 colour; 99 ill; 100 ask; 101 doctor; 102 for; 103 music; 104 sport; 105 why; 106 did; 107 fowl; 108 cross; 109 road; 110 get; 111 other; 112 side; 113 word.
114 sad; 115 tall; 116 short; 117 long; 118 old; 119 young; 120 new; 121 fast; 122 slow; 123 light; 124 dark; 125 black; 126 white; 127 up; 128 down; 129 left; 130 right; 131 true; 132 false; 133 alive; 134 dead; 135 open; 136 shut; 137 wet; 138 dry; 139 full; 140 hard; 141 soft; 142 strong; 143 feeble; 144 clean; 145 dirty; 146 rich; 147 poor; 148 beautiful; 149 safe; 150 dangerous.
200 tom; 201 sara; 202 anna; 203 john; 204 mary; 205 james; 206 emma; 207 alex; 208 david; 209 maria.
Unused output codes 151..199,210..999 available. Reserve e.g.180..189 for digit tokens in arithmetic.

RESIDUAL MAP
0 constant1 for EVERY token, including otherwise unembedded words.
1 BOS flag.
2 role marker BOS/USER/BOT.
3 role value user=1 (BOS also1), bot=0.
4 BOT marker.
5 digit flag; 6 digit numeric value.
7 input token output code.
8 USER boundary marker (future use).
9 free.
10 raw intent ID; 11 raw intent eligibility.
12 raw factual-subject eligibility; 13 raw subject type.
14:26 reserved raw fact payload (12 scalars, intended four answers of up to three token codes).
26 raw negation-key eligibility; 27 raw adjective eligibility; 28 opposite token code.
29 personal-name eligibility.
30 adjective semantic category: hot1,cold2,big3,small4,alive5,dead6,tired12,happy/good13,sad/bad/etc14,ill25. Other adjectives mostly0.
31 free; 32 negation value.
33:44 mostly free, except43 echo eligibility.
44 pronoun eligibility; 45 pronoun value (my/i/me=1, you/your=0).
46 raw arithmetic opcode (plus1,minus2,times3,divide4).
47:64 free.
64 latest role value (1 at person positions, 0 at BOT/generated positions).
65 reciprocal position 1/(t+1).
66/67 previous token digit value/flag.
68/69 token two back digit value/flag.
70/71 token three back digit value/flag.
72 previous token identity code.
73 absolute zero-based position t.
74 free (could add t² using same M1 hinge basis if useful).
75 gated intent key; 76 gated subject key; 77 gated pronoun key; 78 gated negation key; 79 gated adjective key; 80 gated personal-name key; 81 gated echo key.
82 numeric-end eligibility; 83 complete number value at following delimiter (up to three digits).
84 free.
85 NEGATIVE absolute position of latest BOT, retrieved in L2. Reply step d = x73+x85, NOT x85 alone.
86:88 free.
88:100 retrieved factual payloads corresponding to raw14:26.
100 retrieved subject identity code; 101 retrieved subject type.
102 retrieved intent ID; 103 retrieved pronoun value.
104 retrieved opposite code; 105 retrieved adjective category; 106 echo token code (L3).
107 remembered personal name code (latest name in any user message, no USER reset).
108:110 free.
110 first numeric value in entire chat; 111 latest numeric value; 112 arithmetic opcode from intent token.
113 free; 114 retrieved adjective identity code; 115 negation present in current user message (L3).
116 remembered-name-available flag.
117 numeric-present flag from latest number head.
118 tired flag; 119 happy flag; 120 sad flag; 121 ill flag.
122:128 free.
128:176 reply-step onehots 0..47.
176:224 response category flags, category j at176+j.
224/225 output code/active, NEVER use for other purposes.
226:230 free, suggested selected dynamic fact payloads.
230 opposite output mask; 231 echo output mask; 232 name output mask.
233:256 free arithmetic/workspace.
Some listed free ranges share an endpoint with the next stated dimension; ranges are half-open as in weights.

ATTENTION / CLOCK
L1 h0 retrieves latest BOS/USER/BOT role, using head pair26/27, Q=K=100000, monotone cosine over <=192 positions. All user-only key gates in M1 use relu(rawkey+roleuser-1); they exclude generated bot tokens. Each retrieval category except names includes USER as eligible zero-valued sentinel, preventing stale retrieval from earlier messages.
L1 h1 uniform attention copies BOS flag into65, exactly 1/(t+1).
M1 units0:191 implement t = sum_{n=1..191} 2n relu(1/n - 1/(t+1)). Reciprocal constants have nine decimal places, sufficient clock accuracy. Only M1_out[:,73] is populated; 85 is separate negative BOT position.
L1 h2,h3,h4 retrieve exact offsets1,2,3 via pair26/27 with tiny negative query phase. Values -> digit contexts, h2 also previous identity.
M1 units192:199 gate semantic keys (192 intent,193 subject,194 pronoun,195 negation,196 adjective,197 name,198 echo).
M1 units200:204 form numeric-end key/value at delimiter. A current BOT is allowed as delimiter so unpunctuated final numbers work. Number = previousdigit +10*two-back (if prev digit) +100*three-back(if both intervening digits). Generated output numbers do not become user numbers.
L2 h0 latest BOT position, output -position into85.
L2 h1 latest current-user intent ->102 and opcode ->112.
L2 h2 latest current-user factual subject ->88:102 (payload,identity,type).
L2 h3 latest pronoun ->103.
L2 h4 latest adjective ->104,105,114.
L2 h5 latest personal name anywhere in user history ->107; BOS is null sentinel, USER is NOT name sentinel.
L2 h6 OLDEST numeric end in whole chat ->110. Uses negative baseline key and less-negative eligible key; chronological FIRST operand. Caveat: previous chat numbers are not excluded!
L2 h7 latest numeric end ->111,117.
L3 h0 latest echo-eligible word ->106; L3 h1 latest negation/USER ->115.
All heads not mentioned are zero.

M2
Units0:50: shared ReLU hinges in d=x73+x85, form 48 step hats into128:176.
Units64:114: same construction on raw intent102, form48 category hats176:224.
Units120,121: min(1,namecode) ->116.
Units128:140: hats on adjective category105 -> emotion flags118:122.
Other M2 units free.

INTENTS / RESPONSE CATEGORIES
Raw intent IDs:
0 default;1 greeting;2 goodbye;3 thanks;4 apology;5 how-are-you;6 identity/general what/who;7 name;8 age;9 made;10 capabilities;11 like/opinion;12 tired;13 happy;14 sad;15 weather;16 food;17 work/school;18 family;19 pet;20 capital;21 colours list;22 opposite;23 say/echo;24 count;25 ill;26 music;27 sport;28 arithmetic;29 property;30 remembered number;31 where;32 currency;33 continent;34 language;35 leader;36 creator;37 science;38 joke;39 recalled name;40..47 free.
Emotion words do NOT have raw intents: they are adjectives and M3 routes default to the correct response, which avoids overriding “opposite of happy”.
Intent head currently simply chooses latest eligible cue. KNOWN TODO: “say hello” currently chooses greeting rather than echo. Add a separate high-level task retrieval/override (task words say/opposite/count), or robust intent priority with current-user reset. Do not globally increase key strengths: old high-priority tokens would beat a current USER sentinel.
“is” deliberately NOT an intent, avoiding overriding name etc. Plain property questions can be routed in M3 from default plus subject/adjective.
M3 units0:2 switch name category7 to recall category39 if pronoun=my and name available; if my but no remembered name ->default.
M3 units2:8 route default by emotion, using negation115 to reverse happy/sad.
M3 units20:40 TEMPORARILY map unimplemented categories20,24,28..37,40..47 to fallback0. REMOVE/REPLACE these units when implementing those tasks. Their exact per-unit mapping is in edits.
Other M3 units free; all L3 heads except0,1 free.

M4 TEMPLATES
M4 fixed token units0:300; b=-1, each reads category+step.
Category -> unit interval / token codes:
0 [0:11] 1,2,51,52,7,8,19,53,54,55,21
1 [11:20] 15,16,17,8,1,18,19,20,21
2 [20:27] 27,16,28,3,29,30,7
3 [27:31] 19,22,26,16
4 [31:41] 59,43,66,7,17,8,1,18,19,21
5 [41:52] 1,2,23,24,25,19,7,17,22,19,21
6 [52:68] 1,2,3,4,5,6,7,1,8,9,10,11,12,13,14,7
7 [68:80] 1,28,50,42,7,1,2,3,4,5,6,7
8 [80:95] 1,2,3,4,5,6,7,1,13,51,28,3,67,68,7
9 [95:103] 44,45,11,46,47,48,49,7
10 [103:114] 1,8,5,24,9,10,11,12,13,14,7
11 [114:125] 40,8,73,29,7,53,54,55,72,59,7
12 [125:136] 1,2,31,19,32,33,7,34,35,36,7
13 [136:149] 1,2,37,38,39,40,16,74,77,19,32,23,21
14 [149:162] 1,2,31,19,32,78,7,1,2,79,38,80,7
15 [162:176] 1,81,19,28,3,29,30,7,74,43,56,82,75,21
16 [176:188] 83,8,73,84,16,74,13,19,75,38,85,21
17 [188:201] 1,81,59,86,87,36,7,88,38,89,3,90,7
18 [201:212] 91,8,73,92,7,53,54,72,41,91,7
19 [212:226] 3,93,8,73,3,23,94,7,13,19,28,3,93,21
21 [226:235] 95,24,96,12,97,22,98,11,7
25 [235:251] 1,2,31,19,32,99,7,34,35,12,100,3,101,102,18,7
26 [251:262] 103,8,73,84,16,74,103,13,19,75,21
27 [262:273] 104,8,73,84,7,74,104,13,19,75,21
38 [273:288] 105,106,56,107,108,56,109,21,38,110,38,56,111,112,7
22 [288:292] “the opposite is [dynamic104] .”, static units at steps0,1,2,4.
23 [292:296] “the word is [dynamic106] .”, same steps.
39 [296:300] “your name is [dynamic107] .”, same steps.
M4 units300,301,302 emit masks230,231,232 at step3 for categories22,23,39. More M4 units free starting303.
M5 units0:6 gate dynamic104/106/107 using these masks, cap1000. Rest M5 free.
Layer6 entirely free. All attention L4..L6 free.

NEXT PASSES: PRIORITIES / IDEAS
1. Add GK tables in E raw14:26, subject keys12/type13, output codes210+, route relevant categories instead of temporary fallback. General “the answer is [one/two/three tokens] .” template is economical. M3 can select fact payload by intent; M4 static prefix/masks; M5 gate selected payload. Store capitals, continents, currencies, science facts, leaders/founders/products, common animals/property truth. Subject retrieval ignores earlier-turn subjects via USER sentinel.
2. Add names/code embeddings for remaining personal names and improve memory/likes/age/number. Names currently arbitrary latest person-name token.
3. Add task-intent override for say/opposite/count, and count-to-N templates. Could use an unused L2/L3 head with USER null sentinel and gated task eligibility.
4. Arithmetic: operands already110/111, opcode112 (but latest “many” has opcode0; use separate operator head for robustness). Addition/subtraction easy. Number output via code180+digit, reserve digits180..189.
Potential exact multiplication design: M3 extract decimal digits of each operand via ReLU staircases (threshold hats at multiples10 and100). M4 digit-pair multiplication using square identity and small integer square hinge tables, sum weighted products into result. M5 extract hundreds/thousands and remainder<100, M6 extract tens/ones and emit appropriate digit using step/length masks. All numeric answers must put result as LAST number. Division remains difficult; specialize common divisors or use available heads/MLPs.
5. Improve questions about subjects currently routed to bot identity if raw6.
6. Always EOS: default mechanism automatically stops when no scheduled output. Existing replies <=16 tokens.

Keep all syntax numeric, at most one index list per statement. No code execution is available/allowed.