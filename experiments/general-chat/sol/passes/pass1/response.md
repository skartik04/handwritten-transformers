=====SCRATCHPAD=====
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
=====END SCRATCHPAD=====

```edits
# Universal constant, roles, and digits.
E[:, 0] = 1
E["BOS", 1:4] = [1, 1, 1]
E["USER", 2:4] = [1, 1]
E["USER", 8] = 1
E["BOT", 2] = 1
E["BOT", 4] = 1
E[5:15, 5] = 1
E[5:15, 6] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
E["USER", [11, 12, 26, 27, 43, 44]] = 1
E["BOS", 29] = 1

# Scalar token codes.
E[["i", "am", "a", "small", "chat", "bot", ".", "can", "answer", "question", "-s", "and", "do", "maths", "hello", "!", "how", "help", "you", "today", "?", "are", "good", ",", "thank", "welcome", "goodbye", "have", "nice", "day", "sorry", "feel", "tired", "please", "rest", "well", "happy", "to", "hear", "that"], 7] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
E[["your", "name", "is", "my", "weight", "were", "written", "by", "hand", "no", "not", "sure", "tell", "me", "more", "the", "opposite", "of", "it", "yes", "cold", "hot", "big", "large", "little", "okay", "human", "age", "personal", "feeling", "but", "about", "be", "what", "like", "sound", "made", "bad", "here", "listen"], 7] = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80]
E[["hope", "weather", "food", "fun", "eat", "go", "-es", "remember", "take", "break", "family", "important", "pet", "friend", "red", "blue", "green", "colour", "ill", "ask", "doctor", "for", "music", "sport", "why", "did", "fowl", "cross", "road", "get", "other", "side", "word"], 7] = [81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113]
E[["sad", "tall", "short", "long", "old", "young", "new", "fast", "slow", "light", "dark", "black", "white", "up", "down", "left", "right", "true", "false", "alive", "dead", "open", "shut", "wet", "dry", "full", "hard", "soft", "strong", "feeble", "clean", "dirty", "rich", "poor", "beautiful", "safe", "dangerous"], 7] = [114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150]
E[["tom", "sara", "anna", "john", "mary", "james", "emma", "alex", "david", "maria"], 7] = [200, 201, 202, 203, 204, 205, 206, 207, 208, 209]
E[["tom", "sara", "anna", "john", "mary", "james", "emma", "alex", "david", "maria"], 29] = 1

# Output decoding.
U[0, "EOS"] = 0.5
U[224, ["i", "am", "a", "small", "chat", "bot", ".", "can", "answer", "question", "-s", "and", "do", "maths", "hello", "!", "how", "help", "you", "today", "?", "are", "good", ",", "thank", "welcome", "goodbye", "have", "nice", "day", "sorry", "feel", "tired", "please", "rest", "well", "happy", "to", "hear", "that"]] = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80]
U[225, ["i", "am", "a", "small", "chat", "bot", ".", "can", "answer", "question", "-s", "and", "do", "maths", "hello", "!", "how", "help", "you", "today", "?", "are", "good", ",", "thank", "welcome", "goodbye", "have", "nice", "day", "sorry", "feel", "tired", "please", "rest", "well", "happy", "to", "hear", "that"]] = [0, -3, -8, -15, -24, -35, -48, -63, -80, -99, -120, -143, -168, -195, -224, -255, -288, -323, -360, -399, -440, -483, -528, -575, -624, -675, -728, -783, -840, -899, -960, -1023, -1088, -1155, -1224, -1295, -1368, -1443, -1520, -1599]
U[224, ["your", "name", "is", "my", "weight", "were", "written", "by", "hand", "no", "not", "sure", "tell", "me", "more", "the", "opposite", "of", "it", "yes", "cold", "hot", "big", "large", "little", "okay", "human", "age", "personal", "feeling", "but", "about", "be", "what", "like", "sound", "made", "bad", "here", "listen"]] = [82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160]
U[225, ["your", "name", "is", "my", "weight", "were", "written", "by", "hand", "no", "not", "sure", "tell", "me", "more", "the", "opposite", "of", "it", "yes", "cold", "hot", "big", "large", "little", "okay", "human", "age", "personal", "feeling", "but", "about", "be", "what", "like", "sound", "made", "bad", "here", "listen"]] = [-1680, -1763, -1848, -1935, -2024, -2115, -2208, -2303, -2400, -2499, -2600, -2703, -2808, -2915, -3024, -3135, -3248, -3363, -3480, -3599, -3720, -3843, -3968, -4095, -4224, -4355, -4488, -4623, -4760, -4899, -5040, -5183, -5328, -5475, -5624, -5775, -5928, -6083, -6240, -6399]
U[224, ["hope", "weather", "food", "fun", "eat", "go", "-es", "remember", "take", "break", "family", "important", "pet", "friend", "red", "blue", "green", "colour", "ill", "ask", "doctor", "for", "music", "sport", "why", "did", "fowl", "cross", "road", "get", "other", "side", "word"]] = [162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190, 192, 194, 196, 198, 200, 202, 204, 206, 208, 210, 212, 214, 216, 218, 220, 222, 224, 226]
U[225, ["hope", "weather", "food", "fun", "eat", "go", "-es", "remember", "take", "break", "family", "important", "pet", "friend", "red", "blue", "green", "colour", "ill", "ask", "doctor", "for", "music", "sport", "why", "did", "fowl", "cross", "road", "get", "other", "side", "word"]] = [-6560, -6723, -6888, -7055, -7224, -7395, -7568, -7743, -7920, -8099, -8280, -8463, -8648, -8835, -9024, -9215, -9408, -9603, -9800, -9999, -10200, -10403, -10608, -10815, -11024, -11235, -11448, -11663, -11880, -12099, -12320, -12543, -12768]
U[224, ["sad", "tall", "short", "long", "old", "young", "new", "fast", "slow", "light", "dark", "black", "white", "up", "down", "left", "right", "true", "false", "alive", "dead", "open", "shut", "wet", "dry", "full", "hard", "soft", "strong", "feeble", "clean", "dirty", "rich", "poor", "beautiful", "safe", "dangerous"]] = [228, 230, 232, 234, 236, 238, 240, 242, 244, 246, 248, 250, 252, 254, 256, 258, 260, 262, 264, 266, 268, 270, 272, 274, 276, 278, 280, 282, 284, 286, 288, 290, 292, 294, 296, 298, 300]
U[225, ["sad", "tall", "short", "long", "old", "young", "new", "fast", "slow", "light", "dark", "black", "white", "up", "down", "left", "right", "true", "false", "alive", "dead", "open", "shut", "wet", "dry", "full", "hard", "soft", "strong", "feeble", "clean", "dirty", "rich", "poor", "beautiful", "safe", "dangerous"]] = [-12995, -13224, -13455, -13688, -13923, -14160, -14399, -14640, -14883, -15128, -15375, -15624, -15875, -16128, -16383, -16640, -16899, -17160, -17423, -17688, -17955, -18224, -18495, -18768, -19043, -19320, -19599, -19880, -20163, -20448, -20735, -21024, -21315, -21608, -21903, -22200, -22499]
U[224, ["tom", "sara", "anna", "john", "mary", "james", "emma", "alex", "david", "maria"]] = [400, 402, 404, 406, 408, 410, 412, 414, 416, 418]
U[225, ["tom", "sara", "anna", "john", "mary", "james", "emma", "alex", "david", "maria"]] = [-39999, -40400, -40803, -41208, -41615, -42024, -42435, -42848, -43263, -43680]

# Echo candidates.
E[["i", "am", "a", "small", "chat", "bot", "can", "answer", "question", "and", "do", "maths", "hello", "how", "help", "you", "today", "are", "good", "thank", "welcome", "goodbye", "have", "nice", "day", "sorry", "feel", "tired", "rest", "well", "happy", "to", "hear", "that"], 43] = 1
E[["your", "name", "is", "my", "weight", "were", "written", "by", "hand", "no", "not", "sure", "tell", "me", "more", "the", "opposite", "of", "it", "yes", "cold", "hot", "big", "large", "little", "okay", "human", "age", "personal", "feeling", "but", "about", "be", "what", "like", "sound", "made", "bad", "here", "listen"], 43] = 1
E[["hope", "weather", "food", "fun", "eat", "go", "remember", "take", "break", "family", "important", "pet", "friend", "red", "blue", "green", "colour", "ill", "ask", "doctor", "for", "music", "sport", "why", "did", "fowl", "cross", "road", "get", "other", "side", "word"], 43] = 1
E[["sad", "tall", "short", "long", "old", "young", "new", "fast", "slow", "light", "dark", "black", "white", "up", "down", "left", "right", "true", "false", "alive", "dead", "open", "shut", "wet", "dry", "full", "hard", "soft", "strong", "feeble", "clean", "dirty", "rich", "poor", "beautiful", "safe", "dangerous", "tom", "sara", "anna", "john", "mary", "james", "emma", "alex", "david", "maria"], 43] = 1

# Intent lexicon.
E[["hello", "hi", "hey"], 10:12] = [1, 1]
E[["bye", "goodbye"], 10:12] = [2, 1]
E[["thank", "thanks"], 10:12] = [3, 1]
E["sorry", 10:12] = [4, 1]
E["how", 10:12] = [5, 1]
E[["who", "what"], 10:12] = [6, 1]
E["name", 10:12] = [7, 1]
E[["old", "age"], 10:12] = [8, 1]
E[["made", "make", "written", "create"], 10:12] = [9, 1]
E[["can", "able"], 10:12] = [10, 1]
E[["like", "love", "favourite", "favorite", "enjoy", "opinion"], 10:12] = [11, 1]
E[["weather", "rain", "snow"], 10:12] = [15, 1]
E[["food", "eat", "meal", "dinner", "lunch", "coffee", "tea", "pizza"], 10:12] = [16, 1]
E[["work", "school", "job", "study", "class"], 10:12] = [17, 1]
E[["family", "mother", "father", "mom", "dad", "brother", "sister"], 10:12] = [18, 1]
E[["pet", "cat", "dog"], 10:12] = [19, 1]
E["capital", 10:12] = [20, 1]
E[["colour", "color"], 10:12] = [21, 1]
E["opposite", 10:12] = [22, 1]
E[["say", "copy"], 10:12] = [23, 1]
E["count", 10:12] = [24, 1]
E[["music", "song"], 10:12] = [26, 1]
E[["sport", "sports", "football", "game"], 10:12] = [27, 1]
E[["plus", "minus", "times", "divided", "multiply", "subtract", "add", "sum", "total", "product", "difference", "math", "maths", "many", "altogether"], 10:12] = [28, 1]
E["number", 10:12] = [30, 1]
E["where", 10:12] = [31, 1]
E["currency", 10:12] = [32, 1]
E["continent", 10:12] = [33, 1]
E["language", 10:12] = [34, 1]
E[["lead", "leader", "president", "boss"], 10:12] = [35, 1]
E[["built", "found"], 10:12] = [36, 1]
E[["science", "scientific"], 10:12] = [37, 1]
E["joke", 10:12] = [38, 1]
E[["plus", "add", "sum", "total", "altogether"], 46] = 1
E[["minus", "subtract", "difference"], 46] = 2
E[["times", "multiply", "product"], 46] = 3
E["divided", 46] = 4

# Pronouns and negation.
E[["i", "my", "me"], 44:46] = [1, 1]
E[["you", "your"], 44:46] = [1, 0]
E[["not", "un-"], 26] = 1
E[["not", "un-"], 32] = 1

# Opposites and emotional adjectives.
E[["hot", "cold", "big", "small", "large", "little", "good", "bad", "happy", "sad", "tall", "short", "long", "old", "young", "new", "fast", "slow", "light", "dark", "black", "white", "up", "down", "left", "right", "yes", "no", "true", "false", "alive", "dead", "open", "shut", "wet", "dry", "hard", "soft", "strong", "feeble", "clean", "dirty", "rich", "poor", "safe", "dangerous"], 27] = 1
E[["hot", "cold", "big", "small", "large", "little", "good", "bad", "happy", "sad", "tall", "short", "long", "old", "young", "new", "fast", "slow", "light", "dark", "black", "white", "up", "down", "left", "right", "yes", "no", "true", "false", "alive", "dead", "open", "shut", "wet", "dry", "hard", "soft", "strong", "feeble", "clean", "dirty", "rich", "poor", "safe", "dangerous"], 28] = [61, 62, 4, 63, 4, 63, 78, 23, 114, 37, 116, 115, 116, 119, 118, 118, 122, 121, 124, 123, 126, 125, 128, 127, 130, 129, 50, 60, 132, 131, 134, 133, 136, 135, 138, 137, 141, 140, 143, 142, 145, 144, 147, 146, 150, 149]
E["hot", 30] = 1
E["cold", 30] = 2
E[["big", "large"], 30] = 3
E[["small", "little"], 30] = 4
E["alive", 30] = 5
E["dead", 30] = 6
E["tired", 27] = 1
E["tired", 30] = 12
E[["happy", "good", "glad", "excited", "awesome"], 27] = 1
E[["happy", "good", "glad", "excited", "awesome"], 30] = 13
E[["sad", "bad", "angry", "afraid", "alone", "hurt", "stress", "frustrated"], 27] = 1
E[["sad", "bad", "angry", "afraid", "alone", "hurt", "stress", "frustrated"], 30] = 14
E[["ill", "sick"], 27] = 1
E[["ill", "sick"], 30] = 25

# Layer 1: role, absolute-position reciprocal, and exact previous-token heads.
Q1[0, 0, 26] = 100000
K1[0, 2, 26] = 100000
V1[0, 3, 0] = 1
O1[0, 0, 64] = 1
V1[1, 1, 0] = 1
O1[1, 0, 65] = 1
Q1[2, 0, 26:28] = [99999.984189, -56.23413]
K1[2, 0, 26] = 100000
V1[2, 6, 0] = 1
V1[2, 5, 1] = 1
V1[2, 7, 2] = 1
O1[2, 0, 66] = 1
O1[2, 1, 67] = 1
O1[2, 2, 72] = 1
Q1[3, 0, 26:28] = [99999.936754, -112.46824]
K1[3, 0, 26] = 100000
V1[3, 6, 0] = 1
V1[3, 5, 1] = 1
O1[3, 0, 68] = 1
O1[3, 1, 69] = 1
Q1[4, 0, 26:28] = [99999.857698, -168.70232]
K1[4, 0, 26] = 100000
V1[4, 6, 0] = 1
V1[4, 5, 1] = 1
O1[4, 0, 70] = 1
O1[4, 1, 71] = 1

# Reciprocal-to-position hinge spline.
M1_in[65, 0:191] = -1
M1_b[0:20] = [1, 0.5, 0.333333333, 0.25, 0.2, 0.166666667, 0.142857143, 0.125, 0.111111111, 0.1, 0.090909091, 0.083333333, 0.076923077, 0.071428571, 0.066666667, 0.0625, 0.058823529, 0.055555556, 0.052631579, 0.05]
M1_b[20:40] = [0.047619048, 0.045454545, 0.043478261, 0.041666667, 0.04, 0.038461538, 0.037037037, 0.035714286, 0.034482759, 0.033333333, 0.032258065, 0.03125, 0.030303030, 0.029411765, 0.028571429, 0.027777778, 0.027027027, 0.026315789, 0.025641026, 0.025]
M1_b[40:60] = [0.024390244, 0.023809524, 0.023255814, 0.022727273, 0.022222222, 0.021739130, 0.021276596, 0.020833333, 0.020408163, 0.02, 0.019607843, 0.019230769, 0.018867925, 0.018518519, 0.018181818, 0.017857143, 0.017543860, 0.017241379, 0.016949153, 0.016666667]
M1_b[60:80] = [0.016393443, 0.016129032, 0.015873016, 0.015625, 0.015384615, 0.015151515, 0.014925373, 0.014705882, 0.014492754, 0.014285714, 0.014084507, 0.013888889, 0.013698630, 0.013513514, 0.013333333, 0.013157895, 0.012987013, 0.012820513, 0.012658228, 0.0125]
M1_b[80:100] = [0.012345679, 0.012195122, 0.012048193, 0.011904762, 0.011764706, 0.011627907, 0.011494253, 0.011363636, 0.011235955, 0.011111111, 0.010989011, 0.010869565, 0.010752688, 0.010638298, 0.010526316, 0.010416667, 0.010309278, 0.010204082, 0.010101010, 0.01]
M1_b[100:120] = [0.009900990, 0.009803922, 0.009708738, 0.009615385, 0.009523810, 0.009433962, 0.009345794, 0.009259259, 0.009174312, 0.009090909, 0.009009009, 0.008928571, 0.008849558, 0.008771930, 0.008695652, 0.008620690, 0.008547009, 0.008474576, 0.008403361, 0.008333333]
M1_b[120:140] = [0.008264463, 0.008196721, 0.008130081, 0.008064516, 0.008, 0.007936508, 0.007874016, 0.0078125, 0.007751938, 0.007692308, 0.007633588, 0.007575758, 0.007518797, 0.007462687, 0.007407407, 0.007352941, 0.007299270, 0.007246377, 0.007194245, 0.007142857]
M1_b[140:160] = [0.007092199, 0.007042254, 0.006993007, 0.006944444, 0.006896552, 0.006849315, 0.006802721, 0.006756757, 0.006711409, 0.006666667, 0.006622517, 0.006578947, 0.006535948, 0.006493506, 0.006451613, 0.006410256, 0.006369427, 0.006329114, 0.006289308, 0.00625]
M1_b[160:180] = [0.006211180, 0.006172840, 0.006134969, 0.006097561, 0.006060606, 0.006024096, 0.005988024, 0.005952381, 0.005917160, 0.005882353, 0.005847953, 0.005813953, 0.005780347, 0.005747126, 0.005714286, 0.005681818, 0.005649718, 0.005617978, 0.005586592, 0.005555556]
M1_b[180:191] = [0.005524862, 0.005494505, 0.005464481, 0.005434783, 0.005405405, 0.005376344, 0.005347594, 0.005319149, 0.005291005, 0.005263158, 0.005235602]
M1_out[0:20, 73] = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]
M1_out[20:40, 73] = [42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80]
M1_out[40:60, 73] = [82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120]
M1_out[60:80, 73] = [122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160]
M1_out[80:100, 73] = [162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190, 192, 194, 196, 198, 200]
M1_out[100:120, 73] = [202, 204, 206, 208, 210, 212, 214, 216, 218, 220, 222, 224, 226, 228, 230, 232, 234, 236, 238, 240]
M1_out[120:140, 73] = [242, 244, 246, 248, 250, 252, 254, 256, 258, 260, 262, 264, 266, 268, 270, 272, 274, 276, 278, 280]
M1_out[140:160, 73] = [282, 284, 286, 288, 290, 292, 294, 296, 298, 300, 302, 304, 306, 308, 310, 312, 314, 316, 318, 320]
M1_out[160:180, 73] = [322, 324, 326, 328, 330, 332, 334, 336, 338, 340, 342, 344, 346, 348, 350, 352, 354, 356, 358, 360]
M1_out[180:191, 73] = [362, 364, 366, 368, 370, 372, 374, 376, 378, 380, 382]

# User-only semantic eligibility.
M1_in[64, 192:199] = 1
M1_b[192:199] = -1
M1_in[11, 192] = 1
M1_in[12, 193] = 1
M1_in[44, 194] = 1
M1_in[26, 195] = 1
M1_in[27, 196] = 1
M1_in[29, 197] = 1
M1_in[43, 198] = 1
M1_out[192, 75] = 1
M1_out[193, 76] = 1
M1_out[194, 77] = 1
M1_out[195, 78] = 1
M1_out[196, 79] = 1
M1_out[197, 80] = 1
M1_out[198, 81] = 1

# Numeric runs, represented at their following delimiter.
M1_in[67, 200] = 1
M1_in[64, 200] = 1
M1_in[4, 200] = 1
M1_in[5, 200] = -1
M1_b[200] = -1
M1_out[200, 82] = 1
M1_in[66, 201] = 1
M1_in[64, 201] = 10
M1_in[4, 201] = 10
M1_in[5, 201] = -10
M1_b[201] = -10
M1_out[201, 83] = 1
M1_in[68, 202] = 1
M1_in[67, 202] = 10
M1_in[64, 202] = 10
M1_in[4, 202] = 10
M1_in[5, 202] = -10
M1_b[202] = -20
M1_out[202, 83] = 10
M1_in[70, 203] = 1
M1_in[67, 203] = 10
M1_in[69, 203] = 10
M1_in[64, 203] = 10
M1_in[4, 203] = 10
M1_in[5, 203] = -10
M1_b[203] = -30
M1_out[203, 83] = 100

# Layer 2 retrieval heads.
Q2[0:8, 0, 26] = 100000
K2[0, 4, 26] = 100000
V2[0, 73, 0] = 1
O2[0, 0, 85] = -1
K2[1, 75, 26] = 100000
V2[1, 10, 0] = 1
V2[1, 46, 1] = 1
O2[1, 0, 102] = 1
O2[1, 1, 112] = 1
K2[2, 76, 26] = 100000
V2[2, 14, 0] = 1
V2[2, 15, 1] = 1
V2[2, 16, 2] = 1
V2[2, 17, 3] = 1
V2[2, 18, 4] = 1
V2[2, 19, 5] = 1
V2[2, 20, 6] = 1
V2[2, 21, 7] = 1
V2[2, 22, 8] = 1
V2[2, 23, 9] = 1
V2[2, 24, 10] = 1
V2[2, 25, 11] = 1
V2[2, 7, 12] = 1
V2[2, 13, 13] = 1
O2[2, 0, 88] = 1
O2[2, 1, 89] = 1
O2[2, 2, 90] = 1
O2[2, 3, 91] = 1
O2[2, 4, 92] = 1
O2[2, 5, 93] = 1
O2[2, 6, 94] = 1
O2[2, 7, 95] = 1
O2[2, 8, 96] = 1
O2[2, 9, 97] = 1
O2[2, 10, 98] = 1
O2[2, 11, 99] = 1
O2[2, 12, 100] = 1
O2[2, 13, 101] = 1
K2[3, 77, 26] = 100000
V2[3, 45, 0] = 1
O2[3, 0, 103] = 1
K2[4, 79, 26] = 100000
V2[4, 28, 0] = 1
V2[4, 30, 1] = 1
V2[4, 7, 2] = 1
O2[4, 0, 104] = 1
O2[4, 1, 105] = 1
O2[4, 2, 114] = 1
K2[5, 80, 26] = 100000
V2[5, 7, 0] = 1
O2[5, 0, 107] = 1
K2[6, 0, 26] = -200000
K2[6, 82, 26] = 100000
V2[6, 83, 0] = 1
O2[6, 0, 110] = 1
K2[7, 82, 26] = 100000
V2[7, 83, 0] = 1
V2[7, 82, 1] = 1
O2[7, 0, 111] = 1
O2[7, 1, 117] = 1

# Reply step onehots, using shared hinge basis.
M2_in[73, 0:50] = 1
M2_in[85, 0:50] = 1
M2_b[0:50] = [1, 0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -38, -39, -40, -41, -42, -43, -44, -45, -46, -47, -48]
M2_out[0, 128] = 1
M2_out[1, 128:130] = [-2, 1]
M2_out[2, 128:131] = [1, -2, 1]
M2_out[3, 129:132] = [1, -2, 1]
M2_out[4, 130:133] = [1, -2, 1]
M2_out[5, 131:134] = [1, -2, 1]
M2_out[6, 132:135] = [1, -2, 1]
M2_out[7, 133:136] = [1, -2, 1]
M2_out[8, 134:137] = [1, -2, 1]
M2_out[9, 135:138] = [1, -2, 1]
M2_out[10, 136:139] = [1, -2, 1]
M2_out[11, 137:140] = [1, -2, 1]
M2_out[12, 138:141] = [1, -2, 1]
M2_out[13, 139:142] = [1, -2, 1]
M2_out[14, 140:143] = [1, -2, 1]
M2_out[15, 141:144] = [1, -2, 1]
M2_out[16, 142:145] = [1, -2, 1]
M2_out[17, 143:146] = [1, -2, 1]
M2_out[18, 144:147] = [1, -2, 1]
M2_out[19, 145:148] = [1, -2, 1]
M2_out[20, 146:149] = [1, -2, 1]
M2_out[21, 147:150] = [1, -2, 1]
M2_out[22, 148:151] = [1, -2, 1]
M2_out[23, 149:152] = [1, -2, 1]
M2_out[24, 150:153] = [1, -2, 1]
M2_out[25, 151:154] = [1, -2, 1]
M2_out[26, 152:155] = [1, -2, 1]
M2_out[27, 153:156] = [1, -2, 1]
M2_out[28, 154:157] = [1, -2, 1]
M2_out[29, 155:158] = [1, -2, 1]
M2_out[30, 156:159] = [1, -2, 1]
M2_out[31, 157:160] = [1, -2, 1]
M2_out[32, 158:161] = [1, -2, 1]
M2_out[33, 159:162] = [1, -2, 1]
M2_out[34, 160:163] = [1, -2, 1]
M2_out[35, 161:164] = [1, -2, 1]
M2_out[36, 162:165] = [1, -2, 1]
M2_out[37, 163:166] = [1, -2, 1]
M2_out[38, 164:167] = [1, -2, 1]
M2_out[39, 165:168] = [1, -2, 1]
M2_out[40, 166:169] = [1, -2, 1]
M2_out[41, 167:170] = [1, -2, 1]
M2_out[42, 168:171] = [1, -2, 1]
M2_out[43, 169:172] = [1, -2, 1]
M2_out[44, 170:173] = [1, -2, 1]
M2_out[45, 171:174] = [1, -2, 1]
M2_out[46, 172:175] = [1, -2, 1]
M2_out[47, 173:176] = [1, -2, 1]
M2_out[48, 174:176] = [1, -2]
M2_out[49, 175] = 1

# Intent onehots.
M2_in[102, 64:114] = 1
M2_b[64:114] = [1, 0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13, -14, -15, -16, -17, -18, -19, -20, -21, -22, -23, -24, -25, -26, -27, -28, -29, -30, -31, -32, -33, -34, -35, -36, -37, -38, -39, -40, -41, -42, -43, -44, -45, -46, -47, -48]
M2_out[64, 176] = 1
M2_out[65, 176:178] = [-2, 1]
M2_out[66, 176:179] = [1, -2, 1]
M2_out[67, 177:180] = [1, -2, 1]
M2_out[68, 178:181] = [1, -2, 1]
M2_out[69, 179:182] = [1, -2, 1]
M2_out[70, 180:183] = [1, -2, 1]
M2_out[71, 181:184] = [1, -2, 1]
M2_out[72, 182:185] = [1, -2, 1]
M2_out[73, 183:186] = [1, -2, 1]
M2_out[74, 184:187] = [1, -2, 1]
M2_out[75, 185:188] = [1, -2, 1]
M2_out[76, 186:189] = [1, -2, 1]
M2_out[77, 187:190] = [1, -2, 1]
M2_out[78, 188:191] = [1, -2, 1]
M2_out[79, 189:192] = [1, -2, 1]
M2_out[80, 190:193] = [1, -2, 1]
M2_out[81, 191:194] = [1, -2, 1]
M2_out[82, 192:195] = [1, -2, 1]
M2_out[83, 193:196] = [1, -2, 1]
M2_out[84, 194:197] = [1, -2, 1]
M2_out[85, 195:198] = [1, -2, 1]
M2_out[86, 196:199] = [1, -2, 1]
M2_out[87, 197:200] = [1, -2, 1]
M2_out[88, 198:201] = [1, -2, 1]
M2_out[89, 199:202] = [1, -2, 1]
M2_out[90, 200:203] = [1, -2, 1]
M2_out[91, 201:204] = [1, -2, 1]
M2_out[92, 202:205] = [1, -2, 1]
M2_out[93, 203:206] = [1, -2, 1]
M2_out[94, 204:207] = [1, -2, 1]
M2_out[95, 205:208] = [1, -2, 1]
M2_out[96, 206:209] = [1, -2, 1]
M2_out[97, 207:210] = [1, -2, 1]
M2_out[98, 208:211] = [1, -2, 1]
M2_out[99, 209:212] = [1, -2, 1]
M2_out[100, 210:213] = [1, -2, 1]
M2_out[101, 211:214] = [1, -2, 1]
M2_out[102, 212:215] = [1, -2, 1]
M2_out[103, 213:216] = [1, -2, 1]
M2_out[104, 214:217] = [1, -2, 1]
M2_out[105, 215:218] = [1, -2, 1]
M2_out[106, 216:219] = [1, -2, 1]
M2_out[107, 217:220] = [1, -2, 1]
M2_out[108, 218:221] = [1, -2, 1]
M2_out[109, 219:222] = [1, -2, 1]
M2_out[110, 220:223] = [1, -2, 1]
M2_out[111, 221:224] = [1, -2, 1]
M2_out[112, 222:224] = [1, -2]
M2_out[113, 223] = 1

# Remembered-name presence and emotion hats.
M2_in[107, 120:122] = 1
M2_b[121] = -1
M2_out[120, 116] = 1
M2_out[121, 116] = -1
M2_in[105, 128:140] = 1
M2_b[128:140] = [-11, -12, -13, -12, -13, -14, -13, -14, -15, -24, -25, -26]
M2_out[128:131, 118] = [1, -2, 1]
M2_out[131:134, 119] = [1, -2, 1]
M2_out[134:137, 120] = [1, -2, 1]
M2_out[137:140, 121] = [1, -2, 1]

# Layer 3: echo and current-message negation.
Q3[0:2, 0, 26] = 100000
K3[0, 81, 26] = 100000
V3[0, 7, 0] = 1
O3[0, 0, 106] = 1
K3[1, 78, 26] = 100000
V3[1, 32, 0] = 1
O3[1, 0, 115] = 1

# Name recall overrides.
M3_in[183, 0:2] = 1
M3_in[103, 0:2] = 1
M3_in[116, 0] = 1
M3_b[0] = -2
M3_out[0, 183] = -1
M3_out[0, 215] = 1
M3_in[116, 1] = -1
M3_b[1] = -1
M3_out[1, 183] = -1
M3_out[1, 176] = 1

# Emotional replies, including not happy / not bad.
M3_in[176, 2:8] = 1
M3_in[119, 2:4] = 1
M3_in[115, 2] = -1
M3_in[115, 3] = 1
M3_b[2:4] = [-1, -2]
M3_out[2:4, 176] = -1
M3_out[2, 189] = 1
M3_out[3, 190] = 1
M3_in[120, 4:6] = 1
M3_in[115, 4] = -1
M3_in[115, 5] = 1
M3_b[4:6] = [-1, -2]
M3_out[4:6, 176] = -1
M3_out[4, 190] = 1
M3_out[5, 189] = 1
M3_in[118, 6] = 1
M3_b[6] = -1
M3_out[6, 176] = -1
M3_out[6, 188] = 1
M3_in[121, 7] = 1
M3_b[7] = -1
M3_out[7, 176] = -1
M3_out[7, 201] = 1

# Temporary fallback for tasks to be installed in later passes.
M3_in[196, 20] = 1
M3_in[200, 21] = 1
M3_in[204, 22] = 1
M3_in[205, 23] = 1
M3_in[206, 24] = 1
M3_in[207, 25] = 1
M3_in[208, 26] = 1
M3_in[209, 27] = 1
M3_in[210, 28] = 1
M3_in[211, 29] = 1
M3_in[212, 30] = 1
M3_in[213, 31] = 1
M3_in[216, 32] = 1
M3_in[217, 33] = 1
M3_in[218, 34] = 1
M3_in[219, 35] = 1
M3_in[220, 36] = 1
M3_in[221, 37] = 1
M3_in[222, 38] = 1
M3_in[223, 39] = 1
M3_out[20:40, 176] = 1
M3_out[20, 196] = -1
M3_out[21, 200] = -1
M3_out[22, 204] = -1
M3_out[23, 205] = -1
M3_out[24, 206] = -1
M3_out[25, 207] = -1
M3_out[26, 208] = -1
M3_out[27, 209] = -1
M3_out[28, 210] = -1
M3_out[29, 211] = -1
M3_out[30, 212] = -1
M3_out[31, 213] = -1
M3_out[32, 216] = -1
M3_out[33, 217] = -1
M3_out[34, 218] = -1
M3_out[35, 219] = -1
M3_out[36, 220] = -1
M3_out[37, 221] = -1
M3_out[38, 222] = -1
M3_out[39, 223] = -1

# Fixed response template selectors.
M4_b[0:303] = -1
M4_in[176, 0:11] = 1
M4_in[177, 11:20] = 1
M4_in[178, 20:27] = 1
M4_in[179, 27:31] = 1
M4_in[180, 31:41] = 1
M4_in[181, 41:52] = 1
M4_in[182, 52:68] = 1
M4_in[183, 68:80] = 1
M4_in[184, 80:95] = 1
M4_in[185, 95:103] = 1
M4_in[186, 103:114] = 1
M4_in[187, 114:125] = 1
M4_in[188, 125:136] = 1
M4_in[189, 136:149] = 1
M4_in[190, 149:162] = 1
M4_in[191, 162:176] = 1
M4_in[192, 176:188] = 1
M4_in[193, 188:201] = 1
M4_in[194, 201:212] = 1
M4_in[195, 212:226] = 1
M4_in[197, 226:235] = 1
M4_in[201, 235:251] = 1
M4_in[202, 251:262] = 1
M4_in[203, 262:273] = 1
M4_in[214, 273:288] = 1
M4_in[198, 288:292] = 1
M4_in[199, 292:296] = 1
M4_in[215, 296:300] = 1
M4_in[198, 300] = 1
M4_in[199, 301] = 1
M4_in[215, 302] = 1

# Shared step selectors across all templates.
M4_in[128, [0, 11, 20, 27, 31, 41, 52, 68, 80, 95, 103, 114, 125, 136, 149, 162, 176, 188, 201, 212, 226, 235, 251, 262, 273, 288, 292, 296]] = 1
M4_in[129, [1, 12, 21, 28, 32, 42, 53, 69, 81, 96, 104, 115, 126, 137, 150, 163, 177, 189, 202, 213, 227, 236, 252, 263, 274, 289, 293, 297]] = 1
M4_in[130, [2, 13, 22, 29, 33, 43, 54, 70, 82, 97, 105, 116, 127, 138, 151, 164, 178, 190, 203, 214, 228, 237, 253, 264, 275, 290, 294, 298]] = 1
M4_in[131, [3, 14, 23, 30, 34, 44, 55, 71, 83, 98, 106, 117, 128, 139, 152, 165, 179, 191, 204, 215, 229, 238, 254, 265, 276, 300, 301, 302]] = 1
M4_in[132, [4, 15, 24, 35, 45, 56, 72, 84, 99, 107, 118, 129, 140, 153, 166, 180, 192, 205, 216, 230, 239, 255, 266, 277, 291, 295, 299]] = 1
M4_in[133, [5, 16, 25, 36, 46, 57, 73, 85, 100, 108, 119, 130, 141, 154, 167, 181, 193, 206, 217, 231, 240, 256, 267, 278]] = 1
M4_in[134, [6, 17, 26, 37, 47, 58, 74, 86, 101, 109, 120, 131, 142, 155, 168, 182, 194, 207, 218, 232, 241, 257, 268, 279]] = 1
M4_in[135, [7, 18, 38, 48, 59, 75, 87, 102, 110, 121, 132, 143, 156, 169, 183, 195, 208, 219, 233, 242, 258, 269, 280]] = 1
M4_in[136, [8, 19, 39, 49, 60, 76, 88, 111, 122, 133, 144, 157, 170, 184, 196, 209, 220, 234, 243, 259, 270, 281]] = 1
M4_in[137, [9, 40, 50, 61, 77, 89, 112, 123, 134, 145, 158, 171, 185, 197, 210, 221, 244, 260, 271, 282]] = 1
M4_in[138, [10, 51, 62, 78, 90, 113, 124, 135, 146, 159, 172, 186, 198, 211, 222, 245, 261, 272, 283]] = 1
M4_in[139, [63, 79, 91, 147, 160, 173, 187, 199, 223, 246, 284]] = 1
M4_in[140, [64, 92, 148, 161, 174, 200, 224, 247, 285]] = 1
M4_in[141, [65, 93, 175, 225, 248, 286]] = 1
M4_in[142, [66, 94, 249, 287]] = 1
M4_in[143, [67, 250]] = 1

# Fixed template token codes.
M4_out[0:11, 224] = [1, 2, 51, 52, 7, 8, 19, 53, 54, 55, 21]
M4_out[11:20, 224] = [15, 16, 17, 8, 1, 18, 19, 20, 21]
M4_out[20:27, 224] = [27, 16, 28, 3, 29, 30, 7]
M4_out[27:31, 224] = [19, 22, 26, 16]
M4_out[31:41, 224] = [59, 43, 66, 7, 17, 8, 1, 18, 19, 21]
M4_out[41:52, 224] = [1, 2, 23, 24, 25, 19, 7, 17, 22, 19, 21]
M4_out[52:68, 224] = [1, 2, 3, 4, 5, 6, 7, 1, 8, 9, 10, 11, 12, 13, 14, 7]
M4_out[68:80, 224] = [1, 28, 50, 42, 7, 1, 2, 3, 4, 5, 6, 7]
M4_out[80:95, 224] = [1, 2, 3, 4, 5, 6, 7, 1, 13, 51, 28, 3, 67, 68, 7]
M4_out[95:103, 224] = [44, 45, 11, 46, 47, 48, 49, 7]
M4_out[103:114, 224] = [1, 8, 5, 24, 9, 10, 11, 12, 13, 14, 7]
M4_out[114:125, 224] = [40, 8, 73, 29, 7, 53, 54, 55, 72, 59, 7]
M4_out[125:136, 224] = [1, 2, 31, 19, 32, 33, 7, 34, 35, 36, 7]
M4_out[136:149, 224] = [1, 2, 37, 38, 39, 40, 16, 74, 77, 19, 32, 23, 21]
M4_out[149:162, 224] = [1, 2, 31, 19, 32, 78, 7, 1, 2, 79, 38, 80, 7]
M4_out[162:176, 224] = [1, 81, 19, 28, 3, 29, 30, 7, 74, 43, 56, 82, 75, 21]
M4_out[176:188, 224] = [83, 8, 73, 84, 16, 74, 13, 19, 75, 38, 85, 21]
M4_out[188:201, 224] = [1, 81, 59, 86, 87, 36, 7, 88, 38, 89, 3, 90, 7]
M4_out[201:212, 224] = [91, 8, 73, 92, 7, 53, 54, 72, 41, 91, 7]
M4_out[212:226, 224] = [3, 93, 8, 73, 3, 23, 94, 7, 13, 19, 28, 3, 93, 21]
M4_out[226:235, 224] = [95, 24, 96, 12, 97, 22, 98, 11, 7]
M4_out[235:251, 224] = [1, 2, 31, 19, 32, 99, 7, 34, 35, 12, 100, 3, 101, 102, 18, 7]
M4_out[251:262, 224] = [103, 8, 73, 84, 16, 74, 103, 13, 19, 75, 21]
M4_out[262:273, 224] = [104, 8, 73, 84, 7, 74, 104, 13, 19, 75, 21]
M4_out[273:288, 224] = [105, 106, 56, 107, 108, 56, 109, 21, 38, 110, 38, 56, 111, 112, 7]
M4_out[288:292, 224] = [56, 57, 43, 7]
M4_out[292:296, 224] = [56, 113, 43, 7]
M4_out[296:300, 224] = [41, 42, 43, 7]
M4_out[0:300, 225] = 1
M4_out[300, 230] = 1
M4_out[301, 231] = 1
M4_out[302, 232] = 1

# Dynamic slots.
M5_in[104, 0] = 1
M5_in[230, 0] = 1000
M5_b[0] = -1000
M5_out[0, 224] = 1
M5_in[230, 1] = 1
M5_out[1, 225] = 1
M5_in[106, 2] = 1
M5_in[231, 2] = 1000
M5_b[2] = -1000
M5_out[2, 224] = 1
M5_in[231, 3] = 1
M5_out[3, 225] = 1
M5_in[107, 4] = 1
M5_in[232, 4] = 1000
M5_b[4] = -1000
M5_out[4, 224] = 1
M5_in[232, 5] = 1
M5_out[5, 225] = 1
```