=====SCRATCHPAD=====
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
=====END SCRATCHPAD=====

```edits
E["that", 50] = 1
E["currency", 151] = 1
E[["give","gave","lost","lose","spend","spent","eat"], 23] = 1
E[["give","gave","lost","lose","spend","spent","eat"], 27] = 2
E[["get","got","receive","received","buy","bought","more","gain"], 22] = 1
E[["get","got","receive","received","buy","bought","more","gain"], 27] = 1
E[["each","per"], 24] = 1
E[["each","per"], 27] = 3
E[["share","among","over"], 25] = 1
E[["share","among","over"], 27] = 4

U[250, 5:15] = [2,4,6,8,10,12,14,16,18,20]
U[251, 5:15] = [99,96,91,84,75,64,51,36,19,0]
U[250, ["it","is",".","i","am","a","small","chat","bot","have","no","name","my","weight","-s","were","written","by","hand","can","and","answer","question","do","math","hello",",","happy","to","talk","with","you","!","are","welcome","very","good","EOS"]] = [22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96]
U[251, ["it","is",".","i","am","a","small","chat","bot","have","no","name","my","weight","-s","were","written","by","hand","can","and","answer","question","do","math","hello",",","happy","to","talk","with","you","!","are","welcome","very","good","EOS"]] = [-21,-44,-69,-96,-125,-156,-189,-224,-261,-300,-341,-384,-429,-476,-525,-576,-629,-684,-741,-800,-861,-924,-989,-1056,-1125,-1196,-1269,-1344,-1421,-1500,-1581,-1664,-1749,-1836,-1925,-2016,-2109,-2204]
U[250, ["paris","london","canberra","washington","ottawa","berlin","rome","madrid","lisbon","moscow","beijing","tokyo","delhi","brasilia","cairo","pretoria","nairobi","abuja","accra","rabat","algiers","tunis","tripoli","khartoum","ankara","athens","dublin","reykjavik","oslo","stockholm","helsinki","copenhagen","amsterdam","brussels","bern","vienna","prague","warsaw","budapest","bucharest","sofia","belgrade","kyiv","minsk","riga","vilnius","tallinn","bratislava","ljubljana","tirana","wellington"]] = [98,100,102,104,106,108,110,112,114,116,118,120,122,124,126,128,130,132,134,136,138,140,142,144,146,148,150,152,154,156,158,160,162,164,166,168,170,172,174,176,178,180,182,184,186,188,190,192,194,196,198]
U[251, ["paris","london","canberra","washington","ottawa","berlin","rome","madrid","lisbon","moscow","beijing","tokyo","delhi","brasilia","cairo","pretoria","nairobi","abuja","accra","rabat","algiers","tunis","tripoli","khartoum","ankara","athens","dublin","reykjavik","oslo","stockholm","helsinki","copenhagen","amsterdam","brussels","bern","vienna","prague","warsaw","budapest","bucharest","sofia","belgrade","kyiv","minsk","riga","vilnius","tallinn","bratislava","ljubljana","tirana","wellington"]] = [-2301,-2400,-2501,-2604,-2709,-2816,-2925,-3036,-3149,-3264,-3381,-3500,-3621,-3744,-3869,-3996,-4125,-4256,-4389,-4524,-4661,-4800,-4941,-5084,-5229,-5376,-5525,-5676,-5829,-5984,-6141,-6300,-6461,-6624,-6789,-6956,-7125,-7296,-7469,-7644,-7821,-8000,-8181,-8364,-8549,-8736,-8925,-9116,-9309,-9504,-9701]
U[250, ["asia","europe","africa","america","antarctica","oceania","pacific","atlantic","arctic","everest","nile","amazon","sahara","jupiter","mercury","earth","mars","venus","saturn","neptune","uranus","sun","star","planet","moon","water","blue","green","red","yellow","white","black","hot","cold","big","bad","sad","day","night","man","woman","king","queen","light","dark","dog","cat","shakespeare","einstein","newton","edison","darwin"]] = [200,202,204,206,208,210,212,214,216,218,220,222,224,226,228,230,232,234,236,238,240,242,244,246,248,250,252,254,256,258,260,262,264,266,268,270,272,274,276,278,280,282,284,286,288,290,292,294,296,298,300,302]
U[251, ["asia","europe","africa","america","antarctica","oceania","pacific","atlantic","arctic","everest","nile","amazon","sahara","jupiter","mercury","earth","mars","venus","saturn","neptune","uranus","sun","star","planet","moon","water","blue","green","red","yellow","white","black","hot","cold","big","bad","sad","day","night","man","woman","king","queen","light","dark","dog","cat","shakespeare","einstein","newton","edison","darwin"]] = [-9900,-10101,-10304,-10509,-10716,-10925,-11136,-11349,-11564,-11781,-12000,-12221,-12444,-12669,-12896,-13125,-13356,-13589,-13824,-14061,-14300,-14541,-14784,-15029,-15276,-15525,-15776,-16029,-16284,-16541,-16800,-17061,-17324,-17589,-17856,-18125,-18396,-18669,-18944,-19221,-19500,-19781,-20064,-20349,-20636,-20925,-21216,-21509,-21804,-22101,-22400,-22701]
U[250, ["france","germany","italy","spain","japan","russia","australia","canada","brazil","egypt","england","greece","turkey","nepal","peru","usa","china","india","mexico","dollar","gold","silver","iron","liquid","gas","solid","animal","bird","fish","open","shut","up","down","left","right","true","false","yes","not","fast","slow","young","old","long","short","hard","soft","clean","dirty","full"]] = [304,306,308,310,312,314,316,318,320,322,324,326,328,330,332,334,336,338,340,342,344,346,348,350,352,354,356,358,360,362,364,366,368,370,372,374,376,378,380,382,384,386,388,390,392,394,396,398,400,402]
U[251, ["france","germany","italy","spain","japan","russia","australia","canada","brazil","egypt","england","greece","turkey","nepal","peru","usa","china","india","mexico","dollar","gold","silver","iron","liquid","gas","solid","animal","bird","fish","open","shut","up","down","left","right","true","false","yes","not","fast","slow","young","old","long","short","hard","soft","clean","dirty","full"]] = [-23004,-23309,-23616,-23925,-24236,-24549,-24864,-25181,-25500,-25821,-26144,-26469,-26796,-27125,-27456,-27789,-28124,-28461,-28800,-29141,-29484,-29829,-30176,-30525,-30876,-31229,-31584,-31941,-32300,-32661,-33024,-33389,-33756,-34125,-34496,-34869,-35244,-35621,-36000,-36381,-36764,-37149,-37536,-37925,-38316,-38709,-39104,-39501,-39900,-40301]

E[["france","britain","australia","usa","canada","germany","italy","spain","portugal","russia","china","japan","india","brazil","egypt"], 51] = [49,50,51,52,53,54,55,56,57,58,59,60,61,62,63]
E["england", 51] = 50
E[["africa","kenya","nigeria","ghana","morocco","algeria","tunisia","libya","sudan","turkey","greece","ireland","iceland","norway","sweden","finland","denmark","netherlands","belgium","switzerland","austria","czechia","poland","hungary","romania","bulgaria","serbia","ukraine","belarus","latvia","lithuania","estonia","slovakia","slovenia","albania","zealand"], 51] = [64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99]
E[["afghanistan","armenia","azerbaijan","bahrain","bangladesh","bhutan","brunei","cambodia","china","india","indonesia","iran","iraq","israel","japan","jordan","kazakhstan","kuwait","kyrgyzstan","laos","lebanon","malaysia","maldives","mongolia","myanmar","nepal","oman","pakistan","palestine","philippines","qatar","singapore","syria","taiwan","tajikistan","thailand","turkmenistan","uzbekistan","vietnam","yemen","korea","arabia","lanka","emirates"], 52] = 100
E[["albania","andorra","austria","belarus","belgium","bosnia","bulgaria","croatia","cyprus","czechia","denmark","estonia","finland","france","germany","greece","hungary","iceland","ireland","italy","kosovo","latvia","lithuania","luxembourg","malta","moldova","monaco","montenegro","netherlands","norway","poland","portugal","romania","russia","serbia","slovakia","slovenia","spain","sweden","switzerland","ukraine","britain","england","scotland","wales"], 52] = 101
E[["algeria","angola","benin","botswana","burundi","cameroon","chad","congo","djibouti","egypt","eritrea","eswatini","ethiopia","gabon","gambia","ghana","guinea","kenya","lesotho","liberia","libya","madagascar","malawi","mali","mauritania","mauritius","morocco","mozambique","namibia","niger","nigeria","rwanda","senegal","somalia","sudan","tanzania","togo","tunisia","uganda","zambia","zimbabwe"], 52] = 102
E[["argentina","bahamas","barbados","belize","bolivia","brazil","canada","chile","colombia","cuba","ecuador","guatemala","guyana","haiti","honduras","jamaica","mexico","nicaragua","panama","paraguay","peru","uruguay","venezuela","usa"], 52] = 103
E[["australia","zealand","fiji"], 52] = 105
E[["paris","berlin","rome","madrid","tokyo","moscow","canberra","ottawa","brasilia","cairo","london","athens","ankara","everest","lima","washington","beijing","delhi"], 53] = [152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169]
E[["sydney","melbourne"], 53] = 158
E[["toronto","vancouver"], 53] = 159
E[["venice","florence","milan"], 53] = 154
E[["osaka","kyoto"], 53] = 156
E["barcelona", 53] = 155
E[["sky","sea","ocean"], 54] = 126
E[["grass","leaf"], 54] = 127
E["blood", 54] = 128
E["sun", 54] = 129
E[["snow","ice","milk"], 54] = 130
E[["hot","cold","big","small","good","bad","happy","sad","day","night","man","woman","king","queen","light","dark","black","white","up","down","left","right","true","false","fast","slow","young","old","long","short","hard","soft","clean","dirty","open","shut"], 55] = [133,132,17,134,135,47,136,38,138,137,140,139,142,141,144,143,130,131,184,183,186,185,188,187,192,191,194,193,196,195,198,197,200,199,182,181]
E["sun", 56] = 122
E[["mercury","venus","earth","mars","jupiter","saturn","uranus","neptune"], 56] = 123
E["water", 56] = 175
E[["cat","dog","cow","horse","sheep","pig","bird","fish"], 56] = 178
E[["planet","ocean","mountain","river","country","continent"], 58] = [113,106,109,110,157,100]
E[["planet","continent"], 59] = [114,105]
E[["usa","america","canada","australia","zealand"], 60] = 171
E[["usa","blood","leaf","milk","up","down","left","right","true","false","fast","slow","young","old","long","short","hard","soft","clean","dirty","open","shut","country","continent"], 21] = 1

V3[3, :, :] = 0
O3[3, :, :] = 0
V3[3, 51, 0] = 1
V3[3, 52, 1] = 1
V3[3, 53, 2] = 1
V3[3, 54, 3] = 1
V3[3, 55, 4] = 1
V3[3, 56, 5] = 1
V3[3, 57, 6] = 1
V3[3, 58, 7] = 1
V3[3, 59, 8] = 1
V3[3, 60, 9] = 1
V3[3, 31, 10] = 1
O3[3, 0, 72] = 1
O3[3, 1, 73] = 1
O3[3, 2, 74] = 1
O3[3, 3, 75] = 1
O3[3, 4, 76] = 1
O3[3, 5, 77] = 1
O3[3, 6, 78] = 1
O3[3, 7, 79] = 1
O3[3, 8, 80] = 1
O3[3, 9, 81] = 1
O3[3, 10, 63] = 1

M3_in[63, 68:70] = 2
M3_in[41, 68:70] = -2
M3_b[68:70] = [0,-1]
M3_out[68:70, 84] = [1,-1]
M3_in[177, 70:72] = 1000
M3_in[228, 70:72] = -1000
M3_b[70:72] = [-0.1,-1.1]
M3_out[70:72, 29] = [1,-1]

M3_in[65, 72:288] = 2
M3_b[72:270] = [
-18.5,-19.5,-38.5,-39.5,-58.5,-59.5,-78.5,-79.5,-98.5,-99.5,
-118.5,-119.5,-138.5,-139.5,-158.5,-159.5,-178.5,-179.5,-198.5,-199.5,
-218.5,-219.5,-238.5,-239.5,-258.5,-259.5,-278.5,-279.5,-298.5,-299.5,
-318.5,-319.5,-338.5,-339.5,-358.5,-359.5,-378.5,-379.5,-398.5,-399.5,
-418.5,-419.5,-438.5,-439.5,-458.5,-459.5,-478.5,-479.5,-498.5,-499.5,
-518.5,-519.5,-538.5,-539.5,-558.5,-559.5,-578.5,-579.5,-598.5,-599.5,
-618.5,-619.5,-638.5,-639.5,-658.5,-659.5,-678.5,-679.5,-698.5,-699.5,
-718.5,-719.5,-738.5,-739.5,-758.5,-759.5,-778.5,-779.5,-798.5,-799.5,
-818.5,-819.5,-838.5,-839.5,-858.5,-859.5,-878.5,-879.5,-898.5,-899.5,
-918.5,-919.5,-938.5,-939.5,-958.5,-959.5,-978.5,-979.5,-998.5,-999.5,
-1018.5,-1019.5,-1038.5,-1039.5,-1058.5,-1059.5,-1078.5,-1079.5,-1098.5,-1099.5,
-1118.5,-1119.5,-1138.5,-1139.5,-1158.5,-1159.5,-1178.5,-1179.5,-1198.5,-1199.5,
-1218.5,-1219.5,-1238.5,-1239.5,-1258.5,-1259.5,-1278.5,-1279.5,-1298.5,-1299.5,
-1318.5,-1319.5,-1338.5,-1339.5,-1358.5,-1359.5,-1378.5,-1379.5,-1398.5,-1399.5,
-1418.5,-1419.5,-1438.5,-1439.5,-1458.5,-1459.5,-1478.5,-1479.5,-1498.5,-1499.5,
-1518.5,-1519.5,-1538.5,-1539.5,-1558.5,-1559.5,-1578.5,-1579.5,-1598.5,-1599.5,
-1618.5,-1619.5,-1638.5,-1639.5,-1658.5,-1659.5,-1678.5,-1679.5,-1698.5,-1699.5,
-1718.5,-1719.5,-1738.5,-1739.5,-1758.5,-1759.5,-1778.5,-1779.5,-1798.5,-1799.5,
-1818.5,-1819.5,-1838.5,-1839.5,-1858.5,-1859.5,-1878.5,-1879.5,-1898.5,-1899.5,
-1918.5,-1919.5,-1938.5,-1939.5,-1958.5,-1959.5,-1978.5,-1979.5]
M3_out[72:270:2, 103] = -10
M3_out[73:270:2, 103] = 10
M3_out[72:270:2, 104] = 1
M3_out[73:270:2, 104] = -1
M3_b[270:288] = [-198.5,-199.5,-398.5,-399.5,-598.5,-599.5,-798.5,-799.5,-998.5,-999.5,-1198.5,-1199.5,-1398.5,-1399.5,-1598.5,-1599.5,-1798.5,-1799.5]
M3_out[270:288:2, 104] = -10
M3_out[271:288:2, 104] = 10
M3_out[270:288:2, 105] = 1
M3_out[271:288:2, 105] = -1
M3_in[65, 288] = 1
M3_out[288, 103] = 1
M3_in[66, 289:301] = 1
M3_b[289:301] = [0,-1,-2,-1,-2,-3,-2,-3,-4,-3,-4,-5]
M3_out[289:292, 106] = [1,-2,1]
M3_out[292:295, 107] = [1,-2,1]
M3_out[295:298, 108] = [1,-2,1]
M3_out[298:301, 109] = [1,-2,1]
M3_in[41, 301:304] = 1
M3_in[230, 301] = -1
M3_in[231, 302] = -1
M3_in[67, 303] = -1
M3_out[301:303, 110] = 1
M3_out[303, 111] = 1

Q4[0, 70, 28] = 256
Q4[0, 0, 30] = 128
K4[0, 31, 28] = 1
K4[0, 32, 30] = -1
V4[0, 50, 0] = 1
O4[0, 0, 82] = 1
M4_in[29, 0:3] = -1

M4_in[84, 3:23] = 256
M4_b[3:21:2] = -512
M4_b[4:21:2] = -513
M4_b[21:23] = [-256,-257]
M4_out[3:23:2, 85] = 1
M4_out[3:23:2, 86] = 1
M4_out[4:23:2, 86] = -1
M4_in[72, 3:5] = 1
M4_in[197, 3:5] = 256
M4_in[73, 5:7] = 1
M4_in[199, 5:7] = 256
M4_in[197, 5:23] = -256
M4_in[76, 7:9] = 1
M4_in[205, 7:9] = 256
M4_in[199, 7:23] = -256
M4_in[75, 9:11] = 1
M4_in[203, 9:11] = 256
M4_in[205, 9:23] = -256
M4_in[81, 11:13] = 1
M4_in[215, 11:13] = 256
M4_in[203, 11:23] = -256
M4_in[78, 13:15] = 1
M4_in[204, 13:15] = 256
M4_in[215, 13:23] = -256
M4_in[79, 15:17] = 1
M4_in[201, 15:17] = 256
M4_in[204, 15:23] = -256
M4_in[80, 17:19] = 1
M4_in[202, 17:19] = 256
M4_in[201, 17:23] = -256
M4_in[74, 19:21] = 1
M4_in[198, 19:21] = 256
M4_in[202, 19:23] = -256
M4_in[77, 21:23] = 1
M4_in[198, 21:23] = -256

M4_in[106:110, 23] = 1
M4_in[228:230, 23] = 1
M4_in[110:112, 23] = -1
M4_b[23] = -2
M4_out[23, 87] = 1
M4_in[64:66, 24] = 1
M4_in[106, 24] = 2000
M4_b[24] = -2000
M4_out[24, 88] = 1
M4_in[64:66, 25] = [1,-1]
M4_in[107, 25] = 2000
M4_b[25] = -2000
M4_out[25, 88] = 1
M4_in[82, 26] = 1
M4_in[71, 26] = 1
M4_b[26] = -1
M4_out[26, 70] = 1

M4_in[156, 32] = 1
M4_out[32, 156] = -1
M4_in[157, 33] = 1
M4_out[33, 157] = -1
M4_in[158, 34] = 1
M4_out[34, 158] = -1
M4_in[159, 35] = 1
M4_out[35, 159] = -1
M4_in[160, 36] = 1
M4_out[36, 160] = -1
M4_in[161, 37] = 1
M4_out[37, 161] = -1
M4_in[162, 38] = 1
M4_out[38, 162] = -1
M4_in[163, 39] = 1
M4_out[39, 163] = -1
M4_in[164, 40] = 1
M4_out[40, 164] = -1
M4_in[165, 41] = 1
M4_out[41, 165] = -1
M4_in[166, 42] = 1
M4_out[42, 166] = -1
M4_in[167, 43] = 1
M4_out[43, 167] = -1
M4_in[168, 44] = 1
M4_out[44, 168] = -1
M4_in[169, 45] = 1
M4_out[45, 169] = -1
M4_in[170, 46] = 1
M4_out[46, 170] = -1
M4_in[171, 47] = 1
M4_out[47, 171] = -1
M4_in[172, 48] = 1
M4_out[48, 172] = -1
M4_in[173, 49] = 1
M4_out[49, 173] = -1
M4_in[174, 50] = 1
M4_out[50, 174] = -1
M4_in[175, 51] = 1
M4_out[51, 175] = -1
M4_in[176, 52] = 1
M4_out[52, 176] = -1
M4_in[177, 53] = 1
M4_out[53, 177] = -1
M4_in[178, 54] = 1
M4_out[54, 178] = -1
M4_in[179, 55] = 1
M4_out[55, 179] = -1
M4_in[180, 56] = 1
M4_out[56, 180] = -1
M4_in[181, 57] = 1
M4_out[57, 181] = -1
M4_in[182, 58] = 1
M4_out[58, 182] = -1
M4_in[183, 59] = 1
M4_out[59, 183] = -1
M4_in[184, 60] = 1
M4_out[60, 184] = -1
M4_in[185, 61] = 1
M4_out[61, 185] = -1

M4_in[103, 62:92] = 1
M4_in[104, 92:122] = 1
M4_in[105, 122:152] = 1
M4_b[62:92] = [1,0,-1,0,-1,-2,-1,-2,-3,-2,-3,-4,-3,-4,-5,-4,-5,-6,-5,-6,-7,-6,-7,-8,-7,-8,-9,-8,-9,-10]
M4_b[92:122] = [1,0,-1,0,-1,-2,-1,-2,-3,-2,-3,-4,-3,-4,-5,-4,-5,-6,-5,-6,-7,-6,-7,-8,-7,-8,-9,-8,-9,-10]
M4_b[122:152] = [1,0,-1,0,-1,-2,-1,-2,-3,-2,-3,-4,-3,-4,-5,-4,-5,-6,-5,-6,-7,-6,-7,-8,-7,-8,-9,-8,-9,-10]
M4_out[62:65, 156] = [1,-2,1]
M4_out[65:68, 157] = [1,-2,1]
M4_out[68:71, 158] = [1,-2,1]
M4_out[71:74, 159] = [1,-2,1]
M4_out[74:77, 160] = [1,-2,1]
M4_out[77:80, 161] = [1,-2,1]
M4_out[80:83, 162] = [1,-2,1]
M4_out[83:86, 163] = [1,-2,1]
M4_out[86:89, 164] = [1,-2,1]
M4_out[89:92, 165] = [1,-2,1]
M4_out[92:95, 166] = [1,-2,1]
M4_out[95:98, 167] = [1,-2,1]
M4_out[98:101, 168] = [1,-2,1]
M4_out[101:104, 169] = [1,-2,1]
M4_out[104:107, 170] = [1,-2,1]
M4_out[107:110, 171] = [1,-2,1]
M4_out[110:113, 172] = [1,-2,1]
M4_out[113:116, 173] = [1,-2,1]
M4_out[116:119, 174] = [1,-2,1]
M4_out[119:122, 175] = [1,-2,1]
M4_out[122:125, 176] = [1,-2,1]
M4_out[125:128, 177] = [1,-2,1]
M4_out[128:131, 178] = [1,-2,1]
M4_out[131:134, 179] = [1,-2,1]
M4_out[134:137, 180] = [1,-2,1]
M4_out[137:140, 181] = [1,-2,1]
M4_out[140:143, 182] = [1,-2,1]
M4_out[143:146, 183] = [1,-2,1]
M4_out[146:149, 184] = [1,-2,1]
M4_out[149:152, 185] = [1,-2,1]

M5_in[87, 6] = 1
M5_in[222, 6] = -1
M5_out[6, 89] = 1
M5_out[6, 245] = 1
M5_in[86, 7] = 1
M5_in[222, 7] = -1
M5_in[87, 7] = -1
M5_out[7, 224] = 1
M5_out[7, 245] = 1

M5_in[222, 8:15] = -1
M5_in[87, 8:15] = -1
M5_in[86, 8:15] = -1
M5_in[193, 8:12] = 1
M5_in[194:197, 8] = -1
M5_in[191:193, 8:12] = -1
M5_out[8, 232] = 1
M5_in[194, 9] = 1
M5_b[9] = -1
M5_out[9, 233] = 1
M5_in[195, 10] = 1
M5_in[194, 10] = -1
M5_b[10] = -1
M5_out[10, 234] = 1
M5_in[196, 11] = 1
M5_in[194:196, 11] = -1
M5_b[11] = -1
M5_out[11, 235] = 1
M5_in[191, 12] = 1
M5_in[192, 12] = -1
M5_out[12, 236] = 1
M5_in[192, 13] = 1
M5_out[13, 237] = 1
M5_in[29, 14] = 1
M5_in[191:194, 14] = -1
M5_out[14, 238] = 1

M5_in[45, 16:31] = 1
M5_in[87, 16:28] = 100
M5_in[222, 16:31] = -100
M5_b[16:28] = [-106,-107,-108,-107,-108,-109,-108,-109,-110,-109,-110,-111]
M5_out[16:19, 240] = [1,-2,1]
M5_out[19:22, 241] = [1,-2,1]
M5_out[22:25, 242] = [1,-2,1]
M5_out[25:28, 243] = [1,-2,1]
M5_in[86, 28:31] = 100
M5_in[87, 28:31] = -100
M5_b[28:31] = [-106,-107,-108]
M5_out[28:31, 244] = [1,-2,1]

M5_in[64, 31:81] = 1
M5_in[108, 31:61] = 1000
M5_b[31:61] = -2000
M5_in[156, 31] = 1000
M5_in[157, 32] = 1000
M5_in[158, 33] = 1000
M5_in[159, 34] = 1000
M5_in[160, 35] = 1000
M5_in[161, 36] = 1000
M5_in[162, 37] = 1000
M5_in[163, 38] = 1000
M5_in[164, 39] = 1000
M5_in[165, 40] = 1000
M5_in[166, 41] = 1000
M5_in[167, 42] = 1000
M5_in[168, 43] = 1000
M5_in[169, 44] = 1000
M5_in[170, 45] = 1000
M5_in[171, 46] = 1000
M5_in[172, 47] = 1000
M5_in[173, 48] = 1000
M5_in[174, 49] = 1000
M5_in[175, 50] = 1000
M5_in[176, 51] = 1000
M5_in[177, 52] = 1000
M5_in[178, 53] = 1000
M5_in[179, 54] = 1000
M5_in[180, 55] = 1000
M5_in[181, 56] = 1000
M5_in[182, 57] = 1000
M5_in[183, 58] = 1000
M5_in[184, 59] = 1000
M5_in[185, 60] = 1000
M5_out[31:61, 88] = [0,1,2,3,4,5,6,7,8,9,0,10,20,30,40,50,60,70,80,90,0,100,200,300,400,500,600,700,800,900]
M5_in[109, 61:81] = 1000
M5_b[61:81] = -4000
M5_in[166, 61:70] = 1000
M5_in[176, 61:77] = 1000
M5_in[157, 61] = 1000
M5_in[158, 62] = 1000
M5_in[159, 63] = 1000
M5_in[160, 64] = 1000
M5_in[161, 65] = 1000
M5_in[162, 66] = 1000
M5_in[163, 67] = 1000
M5_in[164, 68] = 1000
M5_in[165, 69] = 1000
M5_in[156, 70] = 1000
M5_in[167, 70:74] = 1000
M5_in[157, 71] = 1000
M5_in[158, 72] = 1000
M5_in[161, 73] = 1000
M5_in[156, 74] = 1000
M5_in[168, 74:76] = 1000
M5_in[161, 75] = 1000
M5_in[156, 76:81] = 1000
M5_in[171, 76] = 1000
M5_in[166, 77:79] = 1000
M5_in[177, 77] = 1000
M5_in[178, 78:80] = 1000
M5_in[171, 79] = 1000
M5_in[166, 80] = 1000
M5_in[181, 80] = 1000
M5_out[61:81, 88] = [1,0.5,0.333333333,0.25,0.2,0.166666667,0.142857143,0.125,0.111111111,0.1,0.090909091,0.083333333,0.066666667,0.05,0.04,0.02,0.01,0.005,0.004,0.002]

M6_in[89, 15:41] = -100
M6_in[224, 15:41] = -100
M6_in[232:239, 15:41] = -100
M6_in[45, 81:87] = 1
M6_in[245, 81:87] = 100
M6_b[81:87] = [-104,-105,-106,-105,-106,-107]
M6_out[81:84, 250:252] = [[11,1],[-22,-2],[11,1]]
M6_out[84:87, 250:252] = [[12,1],[-24,-2],[12,1]]
M6_in[85, 87] = 1
M6_in[244, 87] = 256
M6_b[87] = -256
M6_out[87, 250] = 1
M6_in[244, 88] = 1
M6_out[88, 251] = 1
M6_in[88, 89:93] = [0.001,0.01,0.1,1]
M6_in[38, 90:93] = -10
M6_in[240, 89] = 1000000
M6_in[241, 90] = 1000000
M6_in[242, 91] = 1000000
M6_in[243, 92] = 1000000
M6_b[89:93] = -999999.49975
M6_out[89:93, 250] = 1
M6_in[240, 93] = 1
M6_in[241, 94] = 1
M6_in[242, 95] = 1
M6_in[243, 96] = 1
M6_out[93:97, 251] = 1
M6_in[45, 97:107] = 1
M6_in[89, 97:102] = 100
M6_b[97:102] = [-110,-111,-112,-111,-112]
M6_out[97:100, 250:252] = [[13,1],[-26,-2],[13,1]]
M6_out[100:102, 250:252] = [[48,1],[-48,-1]]
M6_in[224, 102:107] = 100
M6_b[102:107] = [-107,-108,-109,-108,-109]
M6_out[102:105, 250:252] = [[13,1],[-26,-2],[13,1]]
M6_out[105:107, 250:252] = [[48,1],[-48,-1]]

M6_in[45, 107:130] = 1
M6_in[232, 107:130] = 100
M6_b[107:130] = [-104,-105,-106,-105,-106,-107,-106,-107,-108,-107,-108,-109,-108,-109,-110,-109,-110,-111,-110,-111,-112,-111,-112]
M6_out[107:110, 250:252] = [[14,1],[-28,-2],[14,1]]
M6_out[110:113, 250:252] = [[15,1],[-30,-2],[15,1]]
M6_out[113:116, 250:252] = [[16,1],[-32,-2],[16,1]]
M6_out[116:119, 250:252] = [[17,1],[-34,-2],[17,1]]
M6_out[119:122, 250:252] = [[18,1],[-36,-2],[18,1]]
M6_out[122:125, 250:252] = [[19,1],[-38,-2],[19,1]]
M6_out[125:128, 250:252] = [[13,1],[-26,-2],[13,1]]
M6_out[128:130, 250:252] = [[48,1],[-48,-1]]

M6_in[45, 130:147] = 1
M6_in[233, 130:147] = 100
M6_b[130:147] = [-104,-105,-106,-105,-106,-107,-106,-107,-108,-107,-108,-109,-108,-109,-110,-109,-110]
M6_out[130:133, 250:252] = [[14,1],[-28,-2],[14,1]]
M6_out[133:136, 250:252] = [[20,1],[-40,-2],[20,1]]
M6_out[136:139, 250:252] = [[21,1],[-42,-2],[21,1]]
M6_out[139:142, 250:252] = [[22,1],[-44,-2],[22,1]]
M6_out[142:145, 250:252] = [[13,1],[-26,-2],[13,1]]
M6_out[145:147, 250:252] = [[48,1],[-48,-1]]

M6_in[45, 147:173] = 1
M6_in[234, 147:173] = 100
M6_b[147:173] = [-104,-105,-106,-105,-106,-107,-106,-107,-108,-107,-108,-109,-108,-109,-110,-109,-110,-111,-110,-111,-112,-111,-112,-113,-112,-113]
M6_out[147:150, 250:252] = [[23,1],[-46,-2],[23,1]]
M6_out[150:153, 250:252] = [[24,1],[-48,-2],[24,1]]
M6_out[153:156, 250:252] = [[25,1],[-50,-2],[25,1]]
M6_out[156:159, 250:252] = [[26,1],[-52,-2],[26,1]]
M6_out[159:162, 250:252] = [[27,1],[-54,-2],[27,1]]
M6_out[162:165, 250:252] = [[28,1],[-56,-2],[28,1]]
M6_out[165:168, 250:252] = [[29,1],[-58,-2],[29,1]]
M6_out[168:171, 250:252] = [[13,1],[-26,-2],[13,1]]
M6_out[171:173, 250:252] = [[48,1],[-48,-1]]

M6_in[45, 173:208] = 1
M6_in[235, 173:208] = 100
M6_b[173:208] = [-104,-105,-106,-105,-106,-107,-106,-107,-108,-107,-108,-109,-108,-109,-110,-109,-110,-111,-110,-111,-112,-111,-112,-113,-112,-113,-114,-113,-114,-115,-114,-115,-116,-115,-116]
M6_out[173:176, 250:252] = [[14,1],[-28,-2],[14,1]]
M6_out[176:179, 250:252] = [[30,1],[-60,-2],[30,1]]
M6_out[179:182, 250:252] = [[18,1],[-36,-2],[18,1]]
M6_out[182:185, 250:252] = [[31,1],[-62,-2],[31,1]]
M6_out[185:188, 250:252] = [[32,1],[-64,-2],[32,1]]
M6_out[188:191, 250:252] = [[33,1],[-66,-2],[33,1]]
M6_out[191:194, 250:252] = [[25,1],[-50,-2],[25,1]]
M6_out[194:197, 250:252] = [[31,1],[-62,-2],[31,1]]
M6_out[197:200, 250:252] = [[34,1],[-68,-2],[34,1]]
M6_out[200:203, 250:252] = [[35,1],[-70,-2],[35,1]]
M6_out[203:206, 250:252] = [[13,1],[-26,-2],[13,1]]
M6_out[206:208, 250:252] = [[48,1],[-48,-1]]

M6_in[45, 208:240] = 1
M6_in[236, 208:240] = 100
M6_b[208:240] = [-104,-105,-106,-105,-106,-107,-106,-107,-108,-107,-108,-109,-108,-109,-110,-109,-110,-111,-110,-111,-112,-111,-112,-113,-112,-113,-114,-113,-114,-115,-114,-115]
M6_out[208:211, 250:252] = [[36,1],[-72,-2],[36,1]]
M6_out[211:214, 250:252] = [[37,1],[-74,-2],[37,1]]
M6_out[214:217, 250:252] = [[14,1],[-28,-2],[14,1]]
M6_out[217:220, 250:252] = [[15,1],[-30,-2],[15,1]]
M6_out[220:223, 250:252] = [[38,1],[-76,-2],[38,1]]
M6_out[223:226, 250:252] = [[39,1],[-78,-2],[39,1]]
M6_out[226:229, 250:252] = [[40,1],[-80,-2],[40,1]]
M6_out[229:232, 250:252] = [[41,1],[-82,-2],[41,1]]
M6_out[232:235, 250:252] = [[42,1],[-84,-2],[42,1]]
M6_out[235:238, 250:252] = [[43,1],[-86,-2],[43,1]]
M6_out[238:240, 250:252] = [[48,1],[-48,-1]]

M6_in[45, 240:254] = 1
M6_in[237, 240:254] = 100
M6_b[240:254] = [-104,-105,-106,-105,-106,-107,-106,-107,-108,-107,-108,-109,-108,-109]
M6_out[240:243, 250:252] = [[42,1],[-84,-2],[42,1]]
M6_out[243:246, 250:252] = [[44,1],[-88,-2],[44,1]]
M6_out[246:249, 250:252] = [[45,1],[-90,-2],[45,1]]
M6_out[249:252, 250:252] = [[43,1],[-86,-2],[43,1]]
M6_out[252:254, 250:252] = [[48,1],[-48,-1]]

M6_in[45, 254:271] = 1
M6_in[238, 254:271] = 100
M6_b[254:271] = [-104,-105,-106,-105,-106,-107,-106,-107,-108,-107,-108,-109,-108,-109,-110,-109,-110]
M6_out[254:257, 250:252] = [[11,1],[-22,-2],[11,1]]
M6_out[257:260, 250:252] = [[12,1],[-24,-2],[12,1]]
M6_out[260:263, 250:252] = [[46,1],[-92,-2],[46,1]]
M6_out[263:266, 250:252] = [[47,1],[-94,-2],[47,1]]
M6_out[266:269, 250:252] = [[43,1],[-86,-2],[43,1]]
M6_out[269:271, 250:252] = [[48,1],[-48,-1]]
```