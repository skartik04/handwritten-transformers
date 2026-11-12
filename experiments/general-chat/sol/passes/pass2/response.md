=====SCRATCHPAD=====
PASS 2 STATUS
No execution/tools used. Pass 1 installed the clock, role gating, scalar output decoder, fixed chat templates, opposites, echo, name memory, and emotion replies. Pass 2 adds independent task/operator retrieval, better operands, number words, counting, factual retrieval/tables, and yes/no physical-property answers. Arithmetic computation and richer conversational memory remain for PASS 3.

CORE INVARIANTS
E[:,0]=1. Residual224=A output code,225=B activity. U[224,w]=2c; U[225,w]=1-c². Active output selects code nearest A/B. U[0,EOS]=0.5; no output means EOS. All codes <1000.
Residual73=t from reciprocal clock;85=negative latest BOT position. Reply step d=73+85. M2 creates step hats128:176, steps0..47.
Residual176+j=response category j. M4 fixed templates emit224/225. Do not disturb these coordinates.
Raw input code E[w,7].

RESIDUAL MAP, CURRENT
0 constant;1 BOS;2 role boundary;3 user role value;4 BOT.
5 digit flag;6 digit value;7 token code;8 USER.
9 raw high-level task eligibility.
10 raw intent ID;11 intent eligibility;12 subject eligibility;13 subject type.
14:17 fact A default/capital;17:20 B location/continent;20:23 C currency/colour;23:26 D language.
26 negation eligibility;27 adjective eligibility;28 opposite code;29 personal-name eligibility;30 adjective category.
31 task ID:1 opposite,2 echo,3 count;32 negation value.
33:36 fact F leader;36:39 G creator;39:42 H product/numeric fact.
42 number-word numeric value;43 echo eligibility;44 pronoun eligibility;45 pronoun my=1,you=0;46 raw arithmetic opcode.
47:50 retrieved F;50:53 retrieved G;53:56 retrieved H.
56 free.57:60 RAW physical traits thermal,size,living, each -1,0,+1.
60 raw operator eligibility;61,62 free;63 number-word eligibility.
64 current role value;65 reciprocal position.
66,67 previous digit/value flag;68,69 two-back;70,71 three-back;72 previous token code.
73 position;74 free.
75 gated intent;76 subject;77 pronoun;78 negation;79 adjective;80 personal name;81 echo.
82 numeric-end key;83 numeric value at delimiter.
84 gated user digit or USER key.
85 negative BOT position;86 gated operator key;87 gated task key.
88:100 retrieved A,B,C,D.
100 retrieved subject identity;101 subject type;102 intent;103 pronoun.
104 opposite;105 adjective category;106 echo;107 remembered name.
108 PREVIOUS OPERAND: latest complete number seen at the latest user digit position. This fixes the stale first-number bug for ordinary binary digit arithmetic; use108 and111, NOT110.
109 retrieved high-level task ID.
110 old globally-first number, now obsolete.
111 latest complete number;112 independent arithmetic opcode.
113 free;114 adjective identity;115 negation.
116 name present;117 numeric present (still not reset by USER).
118 tired;119 happy;120 sad;121 ill.
122:128 property-query hats hot,cold,big,small,alive,dead.
128:176 step hats.
176:224 category flags.
224,225 output.
226:229 selected factual triple.
229 free;230 opposite mask;231 echo mask;232 name mask.
233 thermal,234 size,235 living: retrieved traits.
236:239 fact slot masks.
239:256 free.

ATTENTION
L1 heads0 role,1 reciprocal,2/3/4 exact previous offsets1/2/3. Heads5..7 free.
M1 units0:191 clock;192:199 original user gates;200:204 numeric parsing;205 digit/USER key84;206 operator key86;207 task key87;208 number-word key;209 number-word value.
L2 heads:
0 latest BOT ->85.
1 latest ordinary intent ->102 (old opcode output to112 REMOVED).
2 latest subject ->88:102 plus F/G/H to47:56 and traits233:236.
3 pronoun103;4 adjective104/105/114;5 remembered name107.
6 obsolete globally-first number110.
7 latest number111 and present117.
L3 heads0 echo106,1 negation115,2 latest user digit/USER retrieves that position's111 into108,3 independent operator112,4 high-level task109.
L3 heads5..7 and all L4..L6 attention free.

MLP ALLOCATION
M2 units0:50 step hats;64:114 intent hats;120:122 name presence;128:140 emotion hats;140:148 property-query hats. Rest free.
M3 units0:8 old name/emotion routes, now disabled if task109 nonzero.
M3 units20:23 temporary fallback for categories28 arithmetic,29 unspecified property,30 remembered-number. Remove corresponding fallback when implementing them.
M3 units64:160 remove the ordinary category whenever task109 is nonzero.
M3 units160:165 generate category22/23/24 from task1/2/3.
M3 GK blocks (8-unit stride):
200 cat6 -> A, preserving bot identity if unavailable;
208 cat9 -> G, preserving bot maker response if unavailable;
216 cat10 -> H, preserving capabilities if unavailable;
224 cat20 -> A;
232 cat21 -> C, preserving colours list if unavailable;
240 cat31 -> B;
248 cat32 -> C;
256 cat33 -> B;
264 cat34 -> D;
272 cat35 -> F;
280 cat36 -> G;
288 cat37 -> A;
296 cat28 -> H, only when117=0; raw arithmetic fallback already gives category0.
Each block: offset0 optional fallback; offsets1:4 gate payload into226:229; offsets4:6 make presence and route to category40. Category6 GK is suppressed for physical-property queries.
M3 units320:392 physical-property answers for original categories0,6,19. Each group of4 handles yes/no and negation for one query; groups24 units per original category. Traits233:236, query hats122:128. Outputs category42=yes or43=no. All disabled for high-level tasks.
M3 units392:1024 FREE, importantly enough for arithmetic digit extraction.
M4 old units0:303 unchanged.
M4 units303:306 GK prefix “the answer is”.
306:309 three dynamic slot masks236:239 at steps3,4,5.
309:311 append period at step6 only if third payload code>7.
320:325 category42 “yes , it is .”
325:331 category43 “no , it is not .”
400:404 count prefix “the number -s are”.
404:467 count1..9 groups of7 units: digit>=k, comma>=k+1, dot==k.
467:473 endpoint10: digits1,0,period.
473:479 endpoint0: digit0,period.
M4 units331:400 and479:1024 free.
M5 units0:6 old dynamic slots.
M5 units6:15 GK dynamic slots, each three units: gated code and two hinges forming active=min(1,code).
M5 units15:1024 free.
M6 entirely free.

RESPONSE CATEGORIES
0 fallback “i am not sure. can you tell me more?”
1 greeting;2 goodbye;3 thanks;4 apology;5 how-are-you;6 bot identity;7 bot name;8 bot age;9 hand-written weights;10 capabilities;11 opinion;12 tired;13 happy;14 sad;15 weather;16 food;17 work/school;18 family;19 pets.
20 capital now routes facts;21 colours list or factual colour;22 opposite;23 echo;24 count;25 illness;26 music;27 sport;28 arithmetic still fallback unless H fact;29 unused property fallback;30 recalled number fallback;31 where;32 currency;33 continent;34 language;35 leader/owner;36 creator/founder;37 science;38 joke;39 recalled name.
40 generic fact reply.41 unused, suggested numeric reply.42 property yes.43 property no.44..47 unused.

FACT REPRESENTATION
Triples contain up to three output codes. One-word answer [word,7,0]; two words [word,word,7]; three words [word,word,word], then M4 appends period. Supports three-digit numeric facts too.
Subjects include countries, capitals/cities, AI/tech companies/products, familiar people, animals/objects.
Countries A capital,B continent,C dollar where applicable,D language,F leader.
Cities A and B country.
Companies A company,B location,F leader,G founder,H product.
Products A type,B owner,F owner,G owner,H owner.
Objects C colour; H numeric fact such as legs/count.
Traits -1/0/+1 mean cold/unknown/hot, small/unknown/big, not-alive/unknown/alive.
Known limitations: raw latest intent can still miss complex relational questions; Korea defaults south, Africa as country subject supports South Africa; number-present117 does not reset across turns; echo chooses latest eligible word rather than syntactic quoted word.

OUTPUT CODES
1..150 and200..209 are unchanged from pass1. Core existing:1i,2am,3a,4small,5chat,6bot,7.,8can,9answer,10question,11-s,12and,13do,14maths,15hello,16!,17how,18help,19you,20today,21?,22are,23good,24comma,25thank,26welcome,27goodbye,28have,29nice,30day,31sorry,32feel,33tired,34please,35rest,36well,37happy,38to,39hear,40that,41your,42name,43is,44my,45weight,46were,47written,48by,49hand,50no,51not,52sure,53tell,54me,55more,56the,57opposite,58of,59it,60yes,61cold,62hot,63big,64large,65little,66okay,67human,68age,69personal,70feeling,71but,72about,73be,74what,75like,76sound,77made,78bad,79here,80listen.
81hope,82weather,83food,84fun,85eat,86go,87-es,88remember,89take,90break,91family,92important,93pet,94friend,95red,96blue,97green,98colour,99ill,100ask,101doctor,102for,103music,104sport,105why,106did,107fowl,108cross,109road,110get,111other,112side,113word.
114sad,115tall,116short,117long,118old,119young,120new,121fast,122slow,123light,124dark,125black,126white,127up,128down,129left,130right,131true,132false,133alive,134dead,135open,136shut,137wet,138dry,139full,140hard,141soft,142strong,143feeble,144clean,145dirty,146rich,147poor,148beautiful,149safe,150dangerous.
151number,152count,153animal,154cat,155dog,156fish,157fruit,158orange,159tree,160star,161planet,162company,163person,164water,165ice,166fire,167sun,168moon,169earth,170rock,171elephant,172mouse,173bird,174horse,175cow,176snake,177ant,178rabbit,179milk.
180..189 digit0..9.
190apple,191mountain,192ocean,193sea,194space,195robot,196computer,197air,198english,199french.
200tom,201sara,202anna,203john,204mary,205james,206emma,207alex,208david,209maria.
210..299 are capitals, in the exact order of the E/U edits below.
300..389 countries, in exact E/U order below.
390asia,391europe,392america,393oceania,394antarctica,395pacific,396atlantic,397arctic,398dollar,399cent.
400german,401spanish,402italian,403russian,404chinese,405japanese,406nile,407amazon,408everest,409sahara,410mercury,411venus,412mars,413jupiter,414saturn,415uranus,416neptune,417pluto,418einstein,419newton.
420openai,421anthropic,422google,423microsoft,424meta,425facebook,426instagram,427whatsapp,428tesla,429spacex,430nvidia,431samsung,432sony,433nintendo,434netflix,435spotify,436youtube,437twitter,438tiktok,439bytedance,440deepseek,441mistral,442xai,443chatgpt,444claude,445gemini,446copilot,447grok,448iphone,449ipad,450windows,451android,452linux,453gpt,454llama,455deepmind,456alphabet,457bing,458intel,459amd.
460sam,461altman,462dario,463daniela,464amodei,465demis,466hassabis,467sundar,468pichai,469satya,470nadella,471jensen,472huang,473elon,474musk,475mark,476zuckerberg,477jeff,478bezos,479tim,480cook,481bill,482gates,483steve,484jobs,485larry,486page,487sergey,488brin,489lisa,490su,491trump,492biden,493obama,494putin,495modi,496macron,497starmer,498xi,499jinping.
500carney,501merz,502meloni,503zelensky,504gandhi,505mandela,506shakespeare,507mozart,508beethoven,509darwin,510galileo,511curie,512edison,513turing,514lovelace,515armstrong,516gagarin,517hawking,518picasso,519leonardo.
520science,521art,522invention,523theory,524life,525president,526leader,527king,528queen,529math,530electric,531brain,532heart,533blood,534protein,535warm,536book,537money,538city,539country.
540liam,541olivia,542noah,543ava,544mia,545lucas,546ella,547jack,548lily,549ben,550max,551leo,552zoe,553amy,554kate,555mike,556dan,557paul,558peter.
559dhabi,560assistant,561phone,562program,563car,564mario,565yellow,566plant,567world,568natural,569liquid,570solid,571river,572sand,573UNK,574bell.

PASS 3 PRIORITIES
1 Arithmetic. Use108 and111;112 opcode1+,2-,3*,4/. Digits output codes180..189. Remove M3 fallback unit20 when category28 implemented. M3 free392..1024, M4 free479..1024, M5 free15..1024, M6 all free. Plenty of unused residuals below64 and239..255, but do not overwrite raw input features before their retrieval stages.
Possible exact multiplication: M3 extract A/B decimal digits with paired threshold hinges at multiples10 and100; M4 digit products via ((a+b)^2-(a-b)^2)/4, piecewise-linear exact integer square on -9..18, sum place-weighted products. Correct outputs limited9999, though operands<1000. M5 thousands/hundreds; M6 tens/ones and schedule digits. Addition/subtraction simpler. Need planning for output length, EOS and final period.
2 Recalled ages/numbers/likes and better message intent routing.
3 Check/correct syntax and any manually listed decoder squares if necessary. No behavioural feedback exists.
4 Every generation must terminate within48; no scheduled output automatically ends EOS.
=====END SCRATCHPAD=====

```edits
# Additional input/output codes.
E[["number", "count", "animal", "cat", "dog", "fish", "fruit", "orange", "tree", "star", "planet", "company", "person", "water", "ice", "fire", "sun", "moon", "earth", "rock", "elephant", "mouse", "bird", "horse", "cow", "snake", "ant", "rabbit", "milk"], 7] = [151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179]
E[5:15, 7] = [180, 181, 182, 183, 184, 185, 186, 187, 188, 189]
E[["apple", "mountain", "ocean", "sea", "space", "robot", "computer", "air", "english", "french"], 7] = [190, 191, 192, 193, 194, 195, 196, 197, 198, 199]
E[["number", "count", "animal", "cat", "dog", "fish", "fruit", "orange", "tree", "star", "planet", "company", "person", "water", "ice", "fire", "sun", "moon", "earth", "rock", "elephant", "mouse", "bird", "horse", "cow", "snake", "ant", "rabbit", "milk", "apple", "mountain", "ocean", "sea", "space", "robot", "computer", "air", "english", "french"], 43] = 1
U[224, ["number", "count", "animal", "cat", "dog", "fish", "fruit", "orange", "tree", "star", "planet", "company", "person", "water", "ice", "fire", "sun", "moon", "earth", "rock", "elephant", "mouse", "bird", "horse", "cow", "snake", "ant", "rabbit", "milk"]] = [302, 304, 306, 308, 310, 312, 314, 316, 318, 320, 322, 324, 326, 328, 330, 332, 334, 336, 338, 340, 342, 344, 346, 348, 350, 352, 354, 356, 358]
U[225, ["number", "count", "animal", "cat", "dog", "fish", "fruit", "orange", "tree", "star", "planet", "company", "person", "water", "ice", "fire", "sun", "moon", "earth", "rock", "elephant", "mouse", "bird", "horse", "cow", "snake", "ant", "rabbit", "milk"]] = [-22800, -23103, -23408, -23715, -24024, -24335, -24648, -24963, -25280, -25599, -25920, -26243, -26568, -26895, -27224, -27555, -27888, -28223, -28560, -28899, -29240, -29583, -29928, -30275, -30624, -30975, -31328, -31683, -32040]
U[224, 5:15] = [360, 362, 364, 366, 368, 370, 372, 374, 376, 378]
U[225, 5:15] = [-32399, -32760, -33123, -33488, -33855, -34224, -34595, -34968, -35343, -35720]
U[224, ["apple", "mountain", "ocean", "sea", "space", "robot", "computer", "air", "english", "french"]] = [380, 382, 384, 386, 388, 390, 392, 394, 396, 398]
U[225, ["apple", "mountain", "ocean", "sea", "space", "robot", "computer", "air", "english", "french"]] = [-36099, -36480, -36863, -37248, -37635, -38024, -38415, -38808, -39203, -39600]

E[["paris", "london", "berlin", "rome", "madrid", "lisbon", "ottawa", "washington", "tokyo", "beijing", "delhi", "moscow", "canberra", "brasilia", "cairo", "athens", "dublin", "amsterdam", "brussels", "bern"], 7] = [210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229]
E[["vienna", "stockholm", "oslo", "helsinki", "copenhagen", "warsaw", "prague", "kyiv", "ankara", "seoul", "pyongyang", "bangkok", "hanoi", "jakarta", "manila", "islamabad", "dhaka", "kathmandu", "tehran", "baghdad"], 7] = [230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249]
E[["riyadh", "doha", "muscat", "jerusalem", "beirut", "damascus", "amman", "kabul", "nairobi", "abuja", "pretoria", "rabat", "tunis", "algiers", "accra", "addis", "ababa", "lima", "santiago", "bogota"], 7] = [250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269]
E[["havana", "caracas", "montevideo", "wellington", "kuala", "lumpur", "singapore", "taipei", "budapest", "bucharest", "belgrade", "bratislava", "ljubljana", "minsk", "reykjavik", "tallinn", "riga", "vilnius", "tbilisi", "yerevan"], 7] = [270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289]
# Correct the last capital group to the documented codes.
E[["bratislava", "ljubljana", "minsk", "reykjavik", "tallinn", "riga", "vilnius", "tbilisi", "yerevan", "baku"], 7] = [280, 281, 282, 283, 284, 285, 286, 287, 288, 289]
E["belgrade", 7] = 579
E[["astana", "tashkent", "bishkek", "ulaanbaatar", "dakar", "kigali", "kampala", "lusaka", "harare", "maputo"], 7] = [290, 291, 292, 293, 294, 295, 296, 297, 298, 299]
U[224, ["paris", "london", "berlin", "rome", "madrid", "lisbon", "ottawa", "washington", "tokyo", "beijing", "delhi", "moscow", "canberra", "brasilia", "cairo", "athens", "dublin", "amsterdam", "brussels", "bern"]] = [420, 422, 424, 426, 428, 430, 432, 434, 436, 438, 440, 442, 444, 446, 448, 450, 452, 454, 456, 458]
U[225, ["paris", "london", "berlin", "rome", "madrid", "lisbon", "ottawa", "washington", "tokyo", "beijing", "delhi", "moscow", "canberra", "brasilia", "cairo", "athens", "dublin", "amsterdam", "brussels", "bern"]] = [-44099, -44520, -44943, -45368, -45795, -46224, -46655, -47088, -47523, -47960, -48399, -48840, -49283, -49728, -50175, -50624, -51075, -51528, -51983, -52440]
U[224, ["vienna", "stockholm", "oslo", "helsinki", "copenhagen", "warsaw", "prague", "kyiv", "ankara", "seoul", "pyongyang", "bangkok", "hanoi", "jakarta", "manila", "islamabad", "dhaka", "kathmandu", "tehran", "baghdad"]] = [460, 462, 464, 466, 468, 470, 472, 474, 476, 478, 480, 482, 484, 486, 488, 490, 492, 494, 496, 498]
U[225, ["vienna", "stockholm", "oslo", "helsinki", "copenhagen", "warsaw", "prague", "kyiv", "ankara", "seoul", "pyongyang", "bangkok", "hanoi", "jakarta", "manila", "islamabad", "dhaka", "kathmandu", "tehran", "baghdad"]] = [-52899, -53360, -53823, -54288, -54755, -55224, -55695, -56168, -56643, -57120, -57599, -58080, -58563, -59048, -59535, -60024, -60515, -61008, -61503, -62000]
U[224, ["riyadh", "doha", "muscat", "jerusalem", "beirut", "damascus", "amman", "kabul", "nairobi", "abuja", "pretoria", "rabat", "tunis", "algiers", "accra", "addis", "ababa", "lima", "santiago", "bogota"]] = [500, 502, 504, 506, 508, 510, 512, 514, 516, 518, 520, 522, 524, 526, 528, 530, 532, 534, 536, 538]
U[225, ["riyadh", "doha", "muscat", "jerusalem", "beirut", "damascus", "amman", "kabul", "nairobi", "abuja", "pretoria", "rabat", "tunis", "algiers", "accra", "addis", "ababa", "lima", "santiago", "bogota"]] = [-62499, -63000, -63503, -64008, -64515, -65024, -65535, -66048, -66563, -67080, -67599, -68120, -68643, -69168, -69695, -70224, -70755, -71288, -71823, -72360]
U[224, ["havana", "caracas", "montevideo", "wellington", "kuala", "lumpur", "singapore", "taipei", "budapest", "bucharest", "bratislava", "ljubljana", "minsk", "reykjavik", "tallinn", "riga", "vilnius", "tbilisi", "yerevan", "baku"]] = [540, 542, 544, 546, 548, 550, 552, 554, 556, 558, 560, 562, 564, 566, 568, 570, 572, 574, 576, 578]
U[225, ["havana", "caracas", "montevideo", "wellington", "kuala", "lumpur", "singapore", "taipei", "budapest", "bucharest", "bratislava", "ljubljana", "minsk", "reykjavik", "tallinn", "riga", "vilnius", "tbilisi", "yerevan", "baku"]] = [-72899, -73440, -73983, -74528, -75075, -75624, -76175, -76728, -77283, -77840, -78399, -78960, -79523, -80088, -80655, -81224, -81795, -82368, -82943, -83520]
U[224, ["astana", "tashkent", "bishkek", "ulaanbaatar", "dakar", "kigali", "kampala", "lusaka", "harare", "maputo"]] = [580, 582, 584, 586, 588, 590, 592, 594, 596, 598]
U[225, ["astana", "tashkent", "bishkek", "ulaanbaatar", "dakar", "kigali", "kampala", "lusaka", "harare", "maputo"]] = [-84099, -84680, -85263, -85848, -86435, -87024, -87615, -88208, -88803, -89400]
U[224, "belgrade"] = 1158
U[225, "belgrade"] = -335240
E[["paris", "london", "berlin", "rome", "madrid", "lisbon", "ottawa", "washington", "tokyo", "beijing", "delhi", "moscow", "canberra", "brasilia", "cairo", "athens", "dublin", "amsterdam", "brussels", "bern", "vienna", "stockholm", "oslo", "helsinki", "copenhagen", "warsaw", "prague", "kyiv", "ankara", "seoul", "pyongyang", "bangkok", "hanoi", "jakarta", "manila", "islamabad", "dhaka", "kathmandu", "tehran", "baghdad", "riyadh", "doha", "muscat", "jerusalem", "beirut", "damascus", "amman", "kabul", "nairobi", "abuja", "pretoria", "rabat", "tunis", "algiers", "accra", "addis", "ababa", "lima", "santiago", "bogota", "havana", "caracas", "montevideo", "wellington", "kuala", "lumpur", "singapore", "taipei", "budapest", "bucharest", "belgrade", "bratislava", "ljubljana", "minsk", "reykjavik", "tallinn", "riga", "vilnius", "tbilisi", "yerevan", "baku", "astana", "tashkent", "bishkek", "ulaanbaatar", "dakar", "kigali", "kampala", "lusaka", "harare", "maputo"], 43] = 1

E[["france", "britain", "germany", "italy", "spain", "portugal", "canada", "united", "state", "japan", "china", "india", "russia", "australia", "brazil", "egypt", "greece", "ireland", "netherlands", "belgium"], 7] = [300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319]
E[["switzerland", "austria", "sweden", "norway", "finland", "denmark", "poland", "czechia", "ukraine", "turkey", "korea", "north", "south", "thailand", "vietnam", "indonesia", "philippines", "pakistan", "bangladesh", "nepal"], 7] = [320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339]
E[["iran", "iraq", "arabia", "qatar", "oman", "israel", "lebanon", "syria", "jordan", "afghanistan", "kenya", "nigeria", "africa", "morocco", "tunisia", "algeria", "ghana", "ethiopia", "peru", "chile"], 7] = [340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359]
E[["colombia", "cuba", "venezuela", "uruguay", "zealand", "malaysia", "taiwan", "hungary", "romania", "serbia", "slovakia", "slovenia", "belarus", "iceland", "estonia", "latvia", "lithuania", "georgia", "armenia", "azerbaijan"], 7] = [360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379]
E[["kazakhstan", "uzbekistan", "kyrgyzstan", "mongolia", "senegal", "rwanda", "uganda", "zambia", "zimbabwe", "mozambique"], 7] = [380, 381, 382, 383, 384, 385, 386, 387, 388, 389]
U[224, ["france", "britain", "germany", "italy", "spain", "portugal", "canada", "united", "state", "japan", "china", "india", "russia", "australia", "brazil", "egypt", "greece", "ireland", "netherlands", "belgium"]] = [600, 602, 604, 606, 608, 610, 612, 614, 616, 618, 620, 622, 624, 626, 628, 630, 632, 634, 636, 638]
U[225, ["france", "britain", "germany", "italy", "spain", "portugal", "canada", "united", "state", "japan", "china", "india", "russia", "australia", "brazil", "egypt", "greece", "ireland", "netherlands", "belgium"]] = [-89999, -90600, -91203, -91808, -92415, -93024, -93635, -94248, -94863, -95480, -96099, -96720, -97343, -97968, -98595, -99224, -99855, -100488, -101123, -101760]
U[224, ["switzerland", "austria", "sweden", "norway", "finland", "denmark", "poland", "czechia", "ukraine", "turkey", "korea", "north", "south", "thailand", "vietnam", "indonesia", "philippines", "pakistan", "bangladesh", "nepal"]] = [640, 642, 644, 646, 648, 650, 652, 654, 656, 658, 660, 662, 664, 666, 668, 670, 672, 674, 676, 678]
U[225, ["switzerland", "austria", "sweden", "norway", "finland", "denmark", "poland", "czechia", "ukraine", "turkey", "korea", "north", "south", "thailand", "vietnam", "indonesia", "philippines", "pakistan", "bangladesh", "nepal"]] = [-102399, -103040, -103683, -104328, -104975, -105624, -106275, -106928, -107583, -108240, -108899, -109560, -110223, -110888, -111555, -112224, -112895, -113568, -114243, -114920]
U[224, ["iran", "iraq", "arabia", "qatar", "oman", "israel", "lebanon", "syria", "jordan", "afghanistan", "kenya", "nigeria", "africa", "morocco", "tunisia", "algeria", "ghana", "ethiopia", "peru", "chile"]] = [680, 682, 684, 686, 688, 690, 692, 694, 696, 698, 700, 702, 704, 706, 708, 710, 712, 714, 716, 718]
U[225, ["iran", "iraq", "arabia", "qatar", "oman", "israel", "lebanon", "syria", "jordan", "afghanistan", "kenya", "nigeria", "africa", "morocco", "tunisia", "algeria", "ghana", "ethiopia", "peru", "chile"]] = [-115599, -116280, -116963, -117648, -118335, -119024, -119715, -120408, -121103, -121800, -122499, -123200, -123903, -124608, -125315, -126024, -126735, -127448, -128163, -128880]
U[224, ["colombia", "cuba", "venezuela", "uruguay", "zealand", "malaysia", "taiwan", "hungary", "romania", "serbia", "slovakia", "slovenia", "belarus", "iceland", "estonia", "latvia", "lithuania", "georgia", "armenia", "azerbaijan"]] = [720, 722, 724, 726, 728, 730, 732, 734, 736, 738, 740, 742, 744, 746, 748, 750, 752, 754, 756, 758]
U[225, ["colombia", "cuba", "venezuela", "uruguay", "zealand", "malaysia", "taiwan", "hungary", "romania", "serbia", "slovakia", "slovenia", "belarus", "iceland", "estonia", "latvia", "lithuania", "georgia", "armenia", "azerbaijan"]] = [-129599, -130320, -131043, -131768, -132495, -133224, -133955, -134688, -135423, -136160, -136899, -137640, -138383, -139128, -139875, -140624, -141375, -142128, -142883, -143640]
U[224, ["kazakhstan", "uzbekistan", "kyrgyzstan", "mongolia", "senegal", "rwanda", "uganda", "zambia", "zimbabwe", "mozambique"]] = [760, 762, 764, 766, 768, 770, 772, 774, 776, 778]
U[225, ["kazakhstan", "uzbekistan", "kyrgyzstan", "mongolia", "senegal", "rwanda", "uganda", "zambia", "zimbabwe", "mozambique"]] = [-144399, -145160, -145923, -146688, -147455, -148224, -148995, -149768, -150543, -151320]

E[["asia", "europe", "america", "oceania", "antarctica", "pacific", "atlantic", "arctic", "dollar", "cent", "german", "spanish", "italian", "russian", "chinese", "japanese", "nile", "amazon", "everest", "sahara", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto", "einstein", "newton"], 7] = [390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419]
U[224, ["asia", "europe", "america", "oceania", "antarctica", "pacific", "atlantic", "arctic", "dollar", "cent", "german", "spanish", "italian", "russian", "chinese", "japanese", "nile", "amazon", "everest", "sahara", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto", "einstein", "newton"]] = [780, 782, 784, 786, 788, 790, 792, 794, 796, 798, 800, 802, 804, 806, 808, 810, 812, 814, 816, 818, 820, 822, 824, 826, 828, 830, 832, 834, 836, 838]
U[225, ["asia", "europe", "america", "oceania", "antarctica", "pacific", "atlantic", "arctic", "dollar", "cent", "german", "spanish", "italian", "russian", "chinese", "japanese", "nile", "amazon", "everest", "sahara", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto", "einstein", "newton"]] = [-152099, -152880, -153663, -154448, -155235, -156024, -156815, -157608, -158403, -159200, -159999, -160800, -161603, -162408, -163215, -164024, -164835, -165648, -166463, -167280, -168099, -168920, -169743, -170568, -171395, -172224, -173055, -173888, -174723, -175560]

E[["openai", "anthropic", "google", "microsoft", "meta", "facebook", "instagram", "whatsapp", "tesla", "spacex", "nvidia", "samsung", "sony", "nintendo", "netflix", "spotify", "youtube", "twitter", "tiktok", "bytedance", "deepseek", "mistral", "xai", "chatgpt", "claude", "gemini", "copilot", "grok", "iphone", "ipad", "windows", "android", "linux", "gpt", "llama", "deepmind", "alphabet", "bing", "intel", "amd"], 7] = [420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459]
U[224, ["openai", "anthropic", "google", "microsoft", "meta", "facebook", "instagram", "whatsapp", "tesla", "spacex", "nvidia", "samsung", "sony", "nintendo", "netflix", "spotify", "youtube", "twitter", "tiktok", "bytedance", "deepseek", "mistral", "xai", "chatgpt", "claude", "gemini", "copilot", "grok", "iphone", "ipad", "windows", "android", "linux", "gpt", "llama", "deepmind", "alphabet", "bing", "intel", "amd"]] = [840, 842, 844, 846, 848, 850, 852, 854, 856, 858, 860, 862, 864, 866, 868, 870, 872, 874, 876, 878, 880, 882, 884, 886, 888, 890, 892, 894, 896, 898, 900, 902, 904, 906, 908, 910, 912, 914, 916, 918]
U[225, ["openai", "anthropic", "google", "microsoft", "meta", "facebook", "instagram", "whatsapp", "tesla", "spacex", "nvidia", "samsung", "sony", "nintendo", "netflix", "spotify", "youtube", "twitter", "tiktok", "bytedance", "deepseek", "mistral", "xai", "chatgpt", "claude", "gemini", "copilot", "grok", "iphone", "ipad", "windows", "android", "linux", "gpt", "llama", "deepmind", "alphabet", "bing", "intel", "amd"]] = [-176399, -177240, -178083, -178928, -179775, -180624, -181475, -182328, -183183, -184040, -184899, -185760, -186623, -187488, -188355, -189224, -190095, -190968, -191843, -192720, -193599, -194480, -195363, -196248, -197135, -198024, -198915, -199808, -200703, -201600, -202499, -203400, -204303, -205208, -206115, -207024, -207935, -208848, -209763, -210680]

E[["sam", "altman", "dario", "daniela", "amodei", "demis", "hassabis", "sundar", "pichai", "satya", "nadella", "jensen", "huang", "elon", "musk", "mark", "zuckerberg", "jeff", "bezos", "tim", "cook", "bill", "gates", "steve", "jobs", "larry", "page", "sergey", "brin", "lisa", "su", "trump", "biden", "obama", "putin", "modi", "macron", "starmer", "xi", "jinping"], 7] = [460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499]
U[224, ["sam", "altman", "dario", "daniela", "amodei", "demis", "hassabis", "sundar", "pichai", "satya", "nadella", "jensen", "huang", "elon", "musk", "mark", "zuckerberg", "jeff", "bezos", "tim", "cook", "bill", "gates", "steve", "jobs", "larry", "page", "sergey", "brin", "lisa", "su", "trump", "biden", "obama", "putin", "modi", "macron", "starmer", "xi", "jinping"]] = [920, 922, 924, 926, 928, 930, 932, 934, 936, 938, 940, 942, 944, 946, 948, 950, 952, 954, 956, 958, 960, 962, 964, 966, 968, 970, 972, 974, 976, 978, 980, 982, 984, 986, 988, 990, 992, 994, 996, 998]
U[225, ["sam", "altman", "dario", "daniela", "amodei", "demis", "hassabis", "sundar", "pichai", "satya", "nadella", "jensen", "huang", "elon", "musk", "mark", "zuckerberg", "jeff", "bezos", "tim", "cook", "bill", "gates", "steve", "jobs", "larry", "page", "sergey", "brin", "lisa", "su", "trump", "biden", "obama", "putin", "modi", "macron", "starmer", "xi", "jinping"]] = [-211599, -212520, -213443, -214368, -215295, -216224, -217155, -218088, -219023, -219960, -220899, -221840, -222783, -223728, -224675, -225624, -226575, -227528, -228483, -229440, -230399, -231360, -232323, -233288, -234255, -235224, -236195, -237168, -238143, -239120, -240099, -241080, -242063, -243048, -244035, -245024, -246015, -247008, -248003, -249000]
E[["carney", "merz", "meloni", "zelensky", "gandhi", "mandela", "shakespeare", "mozart", "beethoven", "darwin", "galileo", "curie", "edison", "turing", "lovelace", "armstrong", "gagarin", "hawking", "picasso", "leonardo"], 7] = [500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519]
U[224, ["carney", "merz", "meloni", "zelensky", "gandhi", "mandela", "shakespeare", "mozart", "beethoven", "darwin", "galileo", "curie", "edison", "turing", "lovelace", "armstrong", "gagarin", "hawking", "picasso", "leonardo"]] = [1000, 1002, 1004, 1006, 1008, 1010, 1012, 1014, 1016, 1018, 1020, 1022, 1024, 1026, 1028, 1030, 1032, 1034, 1036, 1038]
U[225, ["carney", "merz", "meloni", "zelensky", "gandhi", "mandela", "shakespeare", "mozart", "beethoven", "darwin", "galileo", "curie", "edison", "turing", "lovelace", "armstrong", "gagarin", "hawking", "picasso", "leonardo"]] = [-249999, -251000, -252003, -253008, -254015, -255024, -256035, -257048, -258063, -259080, -260099, -261120, -262143, -263168, -264195, -265224, -266255, -267288, -268323, -269360]
E[["science", "art", "invention", "theory", "life", "president", "leader", "king", "queen", "math", "electric", "brain", "heart", "blood", "protein", "warm", "book", "money", "city", "country"], 7] = [520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539]
U[224, ["science", "art", "invention", "theory", "life", "president", "leader", "king", "queen", "math", "electric", "brain", "heart", "blood", "protein", "warm", "book", "money", "city", "country"]] = [1040, 1042, 1044, 1046, 1048, 1050, 1052, 1054, 1056, 1058, 1060, 1062, 1064, 1066, 1068, 1070, 1072, 1074, 1076, 1078]
U[225, ["science", "art", "invention", "theory", "life", "president", "leader", "king", "queen", "math", "electric", "brain", "heart", "blood", "protein", "warm", "book", "money", "city", "country"]] = [-270399, -271440, -272483, -273528, -274575, -275624, -276675, -277728, -278783, -279840, -280899, -281960, -283023, -284088, -285155, -286224, -287295, -288368, -289443, -290520]
E[["liam", "olivia", "noah", "ava", "mia", "lucas", "ella", "jack", "lily", "ben", "max", "leo", "zoe", "amy", "kate", "mike", "dan", "paul", "peter"], 7] = [540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558]
E[["liam", "olivia", "noah", "ava", "mia", "lucas", "ella", "jack", "lily", "ben", "max", "leo", "zoe", "amy", "kate", "mike", "dan", "paul", "peter"], 29] = 1
E[["liam", "olivia", "noah", "ava", "mia", "lucas", "ella", "jack", "lily", "ben", "max", "leo", "zoe", "amy", "kate", "mike", "dan", "paul", "peter"], 43] = 1
U[224, ["liam", "olivia", "noah", "ava", "mia", "lucas", "ella", "jack", "lily", "ben", "max", "leo", "zoe", "amy", "kate", "mike", "dan", "paul", "peter"]] = [1080, 1082, 1084, 1086, 1088, 1090, 1092, 1094, 1096, 1098, 1100, 1102, 1104, 1106, 1108, 1110, 1112, 1114, 1116]
U[225, ["liam", "olivia", "noah", "ava", "mia", "lucas", "ella", "jack", "lily", "ben", "max", "leo", "zoe", "amy", "kate", "mike", "dan", "paul", "peter"]] = [-291599, -292680, -293763, -294848, -295935, -297024, -298115, -299208, -300303, -301400, -302499, -303600, -304703, -305808, -306915, -308024, -309135, -310248, -311363]
E[["dhabi", "assistant", "phone", "program", "car", "mario", "yellow", "plant", "world", "natural", "liquid", "solid", "river", "sand", "UNK", "bell"], 7] = [559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574]
E[["dhabi", "assistant", "phone", "program", "car", "mario", "yellow", "plant", "world", "natural", "liquid", "solid", "river", "sand", "UNK", "bell"], 43] = 1
U[224, ["dhabi", "assistant", "phone", "program", "car", "mario", "yellow", "plant", "world", "natural", "liquid", "solid", "river", "sand", "UNK", "bell"]] = [1118, 1120, 1122, 1124, 1126, 1128, 1130, 1132, 1134, 1136, 1138, 1140, 1142, 1144, 1146, 1148]
U[225, ["dhabi", "assistant", "phone", "program", "car", "mario", "yellow", "plant", "world", "natural", "liquid", "solid", "river", "sand", "UNK", "bell"]] = [-312480, -313599, -314720, -315843, -316968, -318095, -319224, -320355, -321488, -322623, -323760, -324899, -326040, -327183, -328328, -329475]

# Independent tasks, operators and number words.
E["USER", [9, 60]] = 1
E["opposite", 9] = 1
E["opposite", 31] = 1
E[["say", "copy"], 9] = 1
E[["say", "copy"], 31] = 2
E["count", 9] = 1
E["count", 31] = 3
E[["plus", "add", "sum", "total", "altogether", "minus", "subtract", "difference", "times", "multiply", "product", "divided"], 60] = 1
E[["give", "gave", "lose", "lost", "take", "took", "spend", "spent"], 60] = 1
E[["give", "gave", "lose", "lost", "take", "took", "spend", "spent"], 46] = 2
E[["get", "got", "receive", "received", "buy", "bought", "gain"], 60] = 1
E[["get", "got", "receive", "received", "buy", "bought", "gain"], 46] = 1
E[["each", "every", "per"], 60] = 1
E[["each", "every", "per"], 46] = 3
E[["share", "equally"], 60] = 1
E[["share", "equally"], 46] = 4
E[["owner", "own"], 10:12] = [35, 1]
E[["discovered", "invention", "author", "wrote"], 10:12] = [36, 1]
E[["produce", "build", "develop", "developed", "sell"], 10:12] = [10, 1]
E[["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"], 42] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
E[["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"], 63] = 1
M1_in[5, 205] = 1
M1_in[8, 205] = 1
M1_in[64, 205:209] = 1
M1_b[205:209] = -1
M1_out[205, 84] = 1
M1_in[60, 206] = 1
M1_out[206, 86] = 1
M1_in[9, 207] = 1
M1_out[207, 87] = 1
M1_in[63, 208] = 1
M1_out[208, 82] = 1
M1_in[42, 209] = 1
M1_in[64, 209] = 1000
M1_b[209] = -1000
M1_out[209, 83] = 1
O2[1, 1, 112] = 0
Q3[2:5, 0, 26] = 100000
K3[2, 84, 26] = 100000
V3[2, 111, 0] = 1
O3[2, 0, 108] = 1
K3[3, 86, 26] = 100000
V3[3, 46, 0] = 1
O3[3, 0, 112] = 1
K3[4, 87, 26] = 100000
V3[4, 31, 0] = 1
O3[4, 0, 109] = 1

# Extended factual values in the existing subject head.
V2[2, 33, 14] = 1
V2[2, 34, 15] = 1
V2[2, 35, 16] = 1
V2[2, 36, 17] = 1
V2[2, 37, 18] = 1
V2[2, 38, 19] = 1
V2[2, 39, 20] = 1
V2[2, 40, 21] = 1
V2[2, 41, 22] = 1
V2[2, 57, 23] = 1
V2[2, 58, 24] = 1
V2[2, 59, 25] = 1
O2[2, 14, 47] = 1
O2[2, 15, 48] = 1
O2[2, 16, 49] = 1
O2[2, 17, 50] = 1
O2[2, 18, 51] = 1
O2[2, 19, 52] = 1
O2[2, 20, 53] = 1
O2[2, 21, 54] = 1
O2[2, 22, 55] = 1
O2[2, 23, 233] = 1
O2[2, 24, 234] = 1
O2[2, 25, 235] = 1

# Physical-query hats.
M2_in[105, 140:148] = 1
M2_b[140:148] = [0, -1, -2, -3, -4, -5, -6, -7]
M2_out[140:143, 122] = [1, -2, 1]
M2_out[141:144, 123] = [1, -2, 1]
M2_out[142:145, 124] = [1, -2, 1]
M2_out[143:146, 125] = [1, -2, 1]
M2_out[144:147, 126] = [1, -2, 1]
M2_out[145:148, 127] = [1, -2, 1]

# Clear old provisional routes and retain only still-unimplemented tasks.
M3_in[:, 20:40] = 0
M3_out[20:40, :] = 0
M3_b[20:40] = 0
M3_in[204, 20] = 1
M3_in[205, 21] = 1
M3_in[206, 22] = 1
M3_in[109, 20:23] = -10
M3_out[20:23, 176] = 1
M3_out[20, 204] = -1
M3_out[21, 205] = -1
M3_out[22, 206] = -1
M3_in[109, 0:8] = -10

# High-level task priority: erase the old category.
M3_in[109, 64:160] = 1
M3_b[64:160:2] = -10
M3_b[65:160:2] = -11
M3_in[176, 64:66] = 10
M3_in[177, 66:68] = 10
M3_in[178, 68:70] = 10
M3_in[179, 70:72] = 10
M3_in[180, 72:74] = 10
M3_in[181, 74:76] = 10
M3_in[182, 76:78] = 10
M3_in[183, 78:80] = 10
M3_in[184, 80:82] = 10
M3_in[185, 82:84] = 10
M3_in[186, 84:86] = 10
M3_in[187, 86:88] = 10
M3_in[188, 88:90] = 10
M3_in[189, 90:92] = 10
M3_in[190, 92:94] = 10
M3_in[191, 94:96] = 10
M3_in[192, 96:98] = 10
M3_in[193, 98:100] = 10
M3_in[194, 100:102] = 10
M3_in[195, 102:104] = 10
M3_in[196, 104:106] = 10
M3_in[197, 106:108] = 10
M3_in[198, 108:110] = 10
M3_in[199, 110:112] = 10
M3_in[200, 112:114] = 10
M3_in[201, 114:116] = 10
M3_in[202, 116:118] = 10
M3_in[203, 118:120] = 10
M3_in[204, 120:122] = 10
M3_in[205, 122:124] = 10
M3_in[206, 124:126] = 10
M3_in[207, 126:128] = 10
M3_in[208, 128:130] = 10
M3_in[209, 130:132] = 10
M3_in[210, 132:134] = 10
M3_in[211, 134:136] = 10
M3_in[212, 136:138] = 10
M3_in[213, 138:140] = 10
M3_in[214, 140:142] = 10
M3_in[215, 142:144] = 10
M3_in[216, 144:146] = 10
M3_in[217, 146:148] = 10
M3_in[218, 148:150] = 10
M3_in[219, 150:152] = 10
M3_in[220, 152:154] = 10
M3_in[221, 154:156] = 10
M3_in[222, 156:158] = 10
M3_in[223, 158:160] = 10
M3_out[64:66, 176] = [-1, 1]
M3_out[66:68, 177] = [-1, 1]
M3_out[68:70, 178] = [-1, 1]
M3_out[70:72, 179] = [-1, 1]
M3_out[72:74, 180] = [-1, 1]
M3_out[74:76, 181] = [-1, 1]
M3_out[76:78, 182] = [-1, 1]
M3_out[78:80, 183] = [-1, 1]
M3_out[80:82, 184] = [-1, 1]
M3_out[82:84, 185] = [-1, 1]
M3_out[84:86, 186] = [-1, 1]
M3_out[86:88, 187] = [-1, 1]
M3_out[88:90, 188] = [-1, 1]
M3_out[90:92, 189] = [-1, 1]
M3_out[92:94, 190] = [-1, 1]
M3_out[94:96, 191] = [-1, 1]
M3_out[96:98, 192] = [-1, 1]
M3_out[98:100, 193] = [-1, 1]
M3_out[100:102, 194] = [-1, 1]
M3_out[102:104, 195] = [-1, 1]
M3_out[104:106, 196] = [-1, 1]
M3_out[106:108, 197] = [-1, 1]
M3_out[108:110, 198] = [-1, 1]
M3_out[110:112, 199] = [-1, 1]
M3_out[112:114, 200] = [-1, 1]
M3_out[114:116, 201] = [-1, 1]
M3_out[116:118, 202] = [-1, 1]
M3_out[118:120, 203] = [-1, 1]
M3_out[120:122, 204] = [-1, 1]
M3_out[122:124, 205] = [-1, 1]
M3_out[124:126, 206] = [-1, 1]
M3_out[126:128, 207] = [-1, 1]
M3_out[128:130, 208] = [-1, 1]
M3_out[130:132, 209] = [-1, 1]
M3_out[132:134, 210] = [-1, 1]
M3_out[134:136, 211] = [-1, 1]
M3_out[136:138, 212] = [-1, 1]
M3_out[138:140, 213] = [-1, 1]
M3_out[140:142, 214] = [-1, 1]
M3_out[142:144, 215] = [-1, 1]
M3_out[144:146, 216] = [-1, 1]
M3_out[146:148, 217] = [-1, 1]
M3_out[148:150, 218] = [-1, 1]
M3_out[150:152, 219] = [-1, 1]
M3_out[152:154, 220] = [-1, 1]
M3_out[154:156, 221] = [-1, 1]
M3_out[156:158, 222] = [-1, 1]
M3_out[158:160, 223] = [-1, 1]
M3_in[109, 160:165] = 1
M3_b[160:165] = [0, -1, -2, -3, -4]
M3_out[160:163, 198] = [1, -2, 1]
M3_out[161:164, 199] = [1, -2, 1]
M3_out[162:165, 200] = [1, -2, 1]

# Factual routing. Each block gates a triple and tests its first entry.
M3_in[182, 201:206] = 1000
M3_in[109, 201:206] = -1000
M3_b[201:206] = [-1000, -1000, -1000, -1000, -1001]
M3_in[88, 201] = 1
M3_in[89, 202] = 1
M3_in[90, 203] = 1
M3_in[88, 204:206] = 1
M3_in[122, 201:206] = -1000
M3_in[123, 201:206] = -1000
M3_in[124, 201:206] = -1000
M3_in[125, 201:206] = -1000
M3_in[126, 201:206] = -1000
M3_in[127, 201:206] = -1000
M3_out[201, 226] = 1
M3_out[202, 227] = 1
M3_out[203, 228] = 1
M3_out[204:206, 182] = [-1, 1]
M3_out[204:206, 216] = [1, -1]

M3_in[185, 209:214] = 1000
M3_in[109, 209:214] = -1000
M3_b[209:214] = [-1000, -1000, -1000, -1000, -1001]
M3_in[50, 209] = 1
M3_in[51, 210] = 1
M3_in[52, 211] = 1
M3_in[50, 212:214] = 1
M3_out[209, 226] = 1
M3_out[210, 227] = 1
M3_out[211, 228] = 1
M3_out[212:214, 185] = [-1, 1]
M3_out[212:214, 216] = [1, -1]

M3_in[186, 217:222] = 1000
M3_in[109, 217:222] = -1000
M3_b[217:222] = [-1000, -1000, -1000, -1000, -1001]
M3_in[53, 217] = 1
M3_in[54, 218] = 1
M3_in[55, 219] = 1
M3_in[53, 220:222] = 1
M3_out[217, 226] = 1
M3_out[218, 227] = 1
M3_out[219, 228] = 1
M3_out[220:222, 186] = [-1, 1]
M3_out[220:222, 216] = [1, -1]

M3_in[196, 224] = 1
M3_in[109, 224] = -10
M3_out[224, 196] = -1
M3_out[224, 176] = 1
M3_in[196, 225:230] = 1000
M3_in[109, 225:230] = -1000
M3_b[225:230] = [-1000, -1000, -1000, -1000, -1001]
M3_in[88, 225] = 1
M3_in[89, 226] = 1
M3_in[90, 227] = 1
M3_in[88, 228:230] = 1
M3_out[225, 226] = 1
M3_out[226, 227] = 1
M3_out[227, 228] = 1
M3_out[228:230, 176] = [-1, 1]
M3_out[228:230, 216] = [1, -1]

M3_in[197, 233:238] = 1000
M3_in[109, 233:238] = -1000
M3_b[233:238] = [-1000, -1000, -1000, -1000, -1001]
M3_in[94, 233] = 1
M3_in[95, 234] = 1
M3_in[96, 235] = 1
M3_in[94, 236:238] = 1
M3_out[233, 226] = 1
M3_out[234, 227] = 1
M3_out[235, 228] = 1
M3_out[236:238, 197] = [-1, 1]
M3_out[236:238, 216] = [1, -1]

M3_in[207, 240] = 1
M3_in[109, 240] = -10
M3_out[240, 207] = -1
M3_out[240, 176] = 1
M3_in[207, 241:246] = 1000
M3_in[109, 241:246] = -1000
M3_b[241:246] = [-1000, -1000, -1000, -1000, -1001]
M3_in[91, 241] = 1
M3_in[92, 242] = 1
M3_in[93, 243] = 1
M3_in[91, 244:246] = 1
M3_out[241, 226] = 1
M3_out[242, 227] = 1
M3_out[243, 228] = 1
M3_out[244:246, 176] = [-1, 1]
M3_out[244:246, 216] = [1, -1]

M3_in[208, 248] = 1
M3_in[109, 248] = -10
M3_out[248, 208] = -1
M3_out[248, 176] = 1
M3_in[208, 249:254] = 1000
M3_in[109, 249:254] = -1000
M3_b[249:254] = [-1000, -1000, -1000, -1000, -1001]
M3_in[94, 249] = 1
M3_in[95, 250] = 1
M3_in[96, 251] = 1
M3_in[94, 252:254] = 1
M3_out[249, 226] = 1
M3_out[250, 227] = 1
M3_out[251, 228] = 1
M3_out[252:254, 176] = [-1, 1]
M3_out[252:254, 216] = [1, -1]

M3_in[209, 256] = 1
M3_in[109, 256] = -10
M3_out[256, 209] = -1
M3_out[256, 176] = 1
M3_in[209, 257:262] = 1000
M3_in[109, 257:262] = -1000
M3_b[257:262] = [-1000, -1000, -1000, -1000, -1001]
M3_in[91, 257] = 1
M3_in[92, 258] = 1
M3_in[93, 259] = 1
M3_in[91, 260:262] = 1
M3_out[257, 226] = 1
M3_out[258, 227] = 1
M3_out[259, 228] = 1
M3_out[260:262, 176] = [-1, 1]
M3_out[260:262, 216] = [1, -1]

M3_in[210, 264] = 1
M3_in[109, 264] = -10
M3_out[264, 210] = -1
M3_out[264, 176] = 1
M3_in[210, 265:270] = 1000
M3_in[109, 265:270] = -1000
M3_b[265:270] = [-1000, -1000, -1000, -1000, -1001]
M3_in[97, 265] = 1
M3_in[98, 266] = 1
M3_in[99, 267] = 1
M3_in[97, 268:270] = 1
M3_out[265, 226] = 1
M3_out[266, 227] = 1
M3_out[267, 228] = 1
M3_out[268:270, 176] = [-1, 1]
M3_out[268:270, 216] = [1, -1]

M3_in[211, 272] = 1
M3_in[109, 272] = -10
M3_out[272, 211] = -1
M3_out[272, 176] = 1
M3_in[211, 273:278] = 1000
M3_in[109, 273:278] = -1000
M3_b[273:278] = [-1000, -1000, -1000, -1000, -1001]
M3_in[47, 273] = 1
M3_in[48, 274] = 1
M3_in[49, 275] = 1
M3_in[47, 276:278] = 1
M3_out[273, 226] = 1
M3_out[274, 227] = 1
M3_out[275, 228] = 1
M3_out[276:278, 176] = [-1, 1]
M3_out[276:278, 216] = [1, -1]

M3_in[212, 280] = 1
M3_in[109, 280] = -10
M3_out[280, 212] = -1
M3_out[280, 176] = 1
M3_in[212, 281:286] = 1000
M3_in[109, 281:286] = -1000
M3_b[281:286] = [-1000, -1000, -1000, -1000, -1001]
M3_in[50, 281] = 1
M3_in[51, 282] = 1
M3_in[52, 283] = 1
M3_in[50, 284:286] = 1
M3_out[281, 226] = 1
M3_out[282, 227] = 1
M3_out[283, 228] = 1
M3_out[284:286, 176] = [-1, 1]
M3_out[284:286, 216] = [1, -1]

M3_in[213, 288] = 1
M3_in[109, 288] = -10
M3_out[288, 213] = -1
M3_out[288, 176] = 1
M3_in[213, 289:294] = 1000
M3_in[109, 289:294] = -1000
M3_b[289:294] = [-1000, -1000, -1000, -1000, -1001]
M3_in[88, 289] = 1
M3_in[89, 290] = 1
M3_in[90, 291] = 1
M3_in[88, 292:294] = 1
M3_out[289, 226] = 1
M3_out[290, 227] = 1
M3_out[291, 228] = 1
M3_out[292:294, 176] = [-1, 1]
M3_out[292:294, 216] = [1, -1]

M3_in[204, 297:302] = 1000
M3_in[109, 297:302] = -1000
M3_in[117, 297:302] = -1000
M3_b[297:302] = [-1000, -1000, -1000, -1000, -1001]
M3_in[53, 297] = 1
M3_in[54, 298] = 1
M3_in[55, 299] = 1
M3_in[53, 300:302] = 1
M3_out[297, 226] = 1
M3_out[298, 227] = 1
M3_out[299, 228] = 1
M3_out[300:302, 176] = [-1, 1]
M3_out[300:302, 216] = [1, -1]

# Physical-property routes.
M3_in[176, 320:344] = 1
M3_in[182, 344:368] = 1
M3_in[195, 368:392] = 1
M3_in[109, 320:392] = -10
M3_in[115, 320:392] = [-1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1]
M3_b[320:392] = [-2, -2, -3, -3, -2, -2, -3, -3, -2, -2, -3, -3, -2, -2, -3, -3, -2, -2, -3, -3, -2, -2, -3, -3, -2, -2, -3, -3, -2, -2, -3, -3, -2, -2, -3, -3, -2, -2, -3, -3, -2, -2, -3, -3, -2, -2, -3, -3, -2, -2, -3, -3, -2, -2, -3, -3, -2, -2, -3, -3, -2, -2, -3, -3, -2, -2, -3, -3, -2, -2, -3, -3]
M3_in[122, 320:324] = 1
M3_in[123, 324:328] = 1
M3_in[124, 328:332] = 1
M3_in[125, 332:336] = 1
M3_in[126, 336:340] = 1
M3_in[127, 340:344] = 1
M3_in[122, 344:348] = 1
M3_in[123, 348:352] = 1
M3_in[124, 352:356] = 1
M3_in[125, 356:360] = 1
M3_in[126, 360:364] = 1
M3_in[127, 364:368] = 1
M3_in[122, 368:372] = 1
M3_in[123, 372:376] = 1
M3_in[124, 376:380] = 1
M3_in[125, 380:384] = 1
M3_in[126, 384:388] = 1
M3_in[127, 388:392] = 1
M3_in[233, 320:328] = [1, -1, -1, 1, -1, 1, 1, -1]
M3_in[234, 328:336] = [1, -1, -1, 1, -1, 1, 1, -1]
M3_in[235, 336:344] = [1, -1, -1, 1, -1, 1, 1, -1]
M3_in[233, 344:352] = [1, -1, -1, 1, -1, 1, 1, -1]
M3_in[234, 352:360] = [1, -1, -1, 1, -1, 1, 1, -1]
M3_in[235, 360:368] = [1, -1, -1, 1, -1, 1, 1, -1]
M3_in[233, 368:376] = [1, -1, -1, 1, -1, 1, 1, -1]
M3_in[234, 376:384] = [1, -1, -1, 1, -1, 1, 1, -1]
M3_in[235, 384:392] = [1, -1, -1, 1, -1, 1, 1, -1]
M3_out[320:344, 176] = -1
M3_out[344:368, 182] = -1
M3_out[368:392, 195] = -1
M3_out[320:392:2, 218] = 1
M3_out[321:392:2, 219] = 1

# Generic factual sentence and dynamic factual slots.
M4_b[303:309] = -1
M4_in[216, 303:309] = 1
M4_in[128, 303] = 1
M4_in[129, 304] = 1
M4_in[130, 305] = 1
M4_out[303:306, 224] = [56, 9, 43]
M4_out[303:306, 225] = 1
M4_in[131, 306] = 1
M4_in[132, 307] = 1
M4_in[133, 308] = 1
M4_out[306, 236] = 1
M4_out[307, 237] = 1
M4_out[308, 238] = 1
M4_in[228, 309:311] = 1
M4_in[216, 309:311] = 1000
M4_in[134, 309:311] = 1000
M4_b[309:311] = [-2007, -2008]
M4_out[309:311, 224] = [7, -7]
M4_out[309:311, 225] = [1, -1]
M5_in[226, 6:9] = 1
M5_in[236, 6:9] = 1000
M5_b[6:9] = [-1000, -1000, -1001]
M5_out[6, 224] = 1
M5_out[7:9, 225] = [1, -1]
M5_in[227, 9:12] = 1
M5_in[237, 9:12] = 1000
M5_b[9:12] = [-1000, -1000, -1001]
M5_out[9, 224] = 1
M5_out[10:12, 225] = [1, -1]
M5_in[228, 12:15] = 1
M5_in[238, 12:15] = 1000
M5_b[12:15] = [-1000, -1000, -1001]
M5_out[12, 224] = 1
M5_out[13:15, 225] = [1, -1]

# Yes/no full sentences.
M4_b[320:331] = -1
M4_in[218, 320:325] = 1
M4_in[219, 325:331] = 1
M4_in[128, [320, 325]] = 1
M4_in[129, [321, 326]] = 1
M4_in[130, [322, 327]] = 1
M4_in[131, [323, 328]] = 1
M4_in[132, [324, 329]] = 1
M4_in[133, 330] = 1
M4_out[320:331, 224] = [60, 24, 59, 43, 7, 50, 24, 59, 43, 51, 7]
M4_out[320:331, 225] = 1

# Count to endpoints 0..10.
M4_in[200, 400:404] = 1
M4_b[400:404] = -1
M4_in[128, 400] = 1
M4_in[129, 401] = 1
M4_in[130, 402] = 1
M4_in[131, 403] = 1
M4_out[400:404, 224] = [56, 151, 11, 22]
M4_out[400:404, 225] = 1
M4_in[111, 404:479] = 1
M4_in[200, 404:479] = 20
M4_in[132, 404:406] = 20
M4_in[133, 406:411] = 20
M4_in[134, 411:413] = 20
M4_in[135, 413:418] = 20
M4_in[136, 418:420] = 20
M4_in[137, 420:425] = 20
M4_in[138, 425:427] = 20
M4_in[139, 427:432] = 20
M4_in[140, 432:434] = 20
M4_in[141, 434:439] = 20
M4_in[142, 439:441] = 20
M4_in[143, 441:446] = 20
M4_in[144, 446:448] = 20
M4_in[145, 448:453] = 20
M4_in[146, 453:455] = 20
M4_in[147, 455:460] = 20
M4_in[148, 460:462] = 20
M4_in[149, 462:467] = 20
M4_in[150, 467:469] = 20
M4_in[151, 469:471] = 20
M4_in[152, 471:473] = 20
M4_in[132, 473:476] = 20
M4_in[133, 476:479] = 20
M4_b[404:411] = [-40, -41, -41, -42, -40, -41, -42]
M4_b[411:418] = [-41, -42, -42, -43, -41, -42, -43]
M4_b[418:425] = [-42, -43, -43, -44, -42, -43, -44]
M4_b[425:432] = [-43, -44, -44, -45, -43, -44, -45]
M4_b[432:439] = [-44, -45, -45, -46, -44, -45, -46]
M4_b[439:446] = [-45, -46, -46, -47, -45, -46, -47]
M4_b[446:453] = [-46, -47, -47, -48, -46, -47, -48]
M4_b[453:460] = [-47, -48, -48, -49, -47, -48, -49]
M4_b[460:467] = [-48, -49, -49, -50, -48, -49, -50]
M4_b[467:473] = [-49, -50, -49, -50, -49, -50]
M4_b[473:479] = [-39, -40, -41, -39, -40, -41]
M4_out[404:411, 224] = [181, -181, 24, -24, 7, -14, 7]
M4_out[411:418, 224] = [182, -182, 24, -24, 7, -14, 7]
M4_out[418:425, 224] = [183, -183, 24, -24, 7, -14, 7]
M4_out[425:432, 224] = [184, -184, 24, -24, 7, -14, 7]
M4_out[432:439, 224] = [185, -185, 24, -24, 7, -14, 7]
M4_out[439:446, 224] = [186, -186, 24, -24, 7, -14, 7]
M4_out[446:453, 224] = [187, -187, 24, -24, 7, -14, 7]
M4_out[453:460, 224] = [188, -188, 24, -24, 7, -14, 7]
M4_out[460:467, 224] = [189, -189, 24, -24, 7, -14, 7]
M4_out[467:473, 224] = [181, -181, 180, -180, 7, -7]
M4_out[473:479, 224] = [180, -360, 180, 7, -14, 7]
M4_out[404:411, 225] = [1, -1, 1, -1, 1, -2, 1]
M4_out[411:418, 225] = [1, -1, 1, -1, 1, -2, 1]
M4_out[418:425, 225] = [1, -1, 1, -1, 1, -2, 1]
M4_out[425:432, 225] = [1, -1, 1, -1, 1, -2, 1]
M4_out[432:439, 225] = [1, -1, 1, -1, 1, -2, 1]
M4_out[439:446, 225] = [1, -1, 1, -1, 1, -2, 1]
M4_out[446:453, 225] = [1, -1, 1, -1, 1, -2, 1]
M4_out[453:460, 225] = [1, -1, 1, -1, 1, -2, 1]
M4_out[460:467, 225] = [1, -1, 1, -1, 1, -2, 1]
M4_out[467:473, 225] = [1, -1, 1, -1, 1, -1]
M4_out[473:479, 225] = [1, -2, 1, 1, -2, 1]

# Country capitals.
E[["france", "britain", "germany", "italy", "spain", "portugal", "canada", "united", "state", "japan", "china", "india", "russia", "australia", "brazil", "egypt", "greece", "ireland", "netherlands", "belgium"], 12:14] = [1, 1]
E[["france", "britain", "germany", "italy", "spain", "portugal", "canada", "united", "state", "japan", "china", "india", "russia", "australia", "brazil", "egypt", "greece", "ireland", "netherlands", "belgium"], 14] = [210, 211, 212, 213, 214, 215, 216, 217, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228]
E[["france", "britain", "germany", "italy", "spain", "portugal", "canada", "united", "state", "japan", "china", "india", "russia", "australia", "brazil", "egypt", "greece", "ireland", "netherlands", "belgium"], 15] = 7
E["india", 14:17] = [120, 220, 7]
E[["switzerland", "austria", "sweden", "norway", "finland", "denmark", "poland", "czechia", "ukraine", "turkey", "korea", "thailand", "vietnam", "indonesia", "philippines", "pakistan", "bangladesh", "nepal", "iran", "iraq"], 12:14] = [1, 1]
E[["switzerland", "austria", "sweden", "norway", "finland", "denmark", "poland", "czechia", "ukraine", "turkey", "korea", "thailand", "vietnam", "indonesia", "philippines", "pakistan", "bangladesh", "nepal", "iran", "iraq"], 14] = [229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 241, 242, 243, 244, 245, 246, 247, 248, 249]
E[["switzerland", "austria", "sweden", "norway", "finland", "denmark", "poland", "czechia", "ukraine", "turkey", "korea", "thailand", "vietnam", "indonesia", "philippines", "pakistan", "bangladesh", "nepal", "iran", "iraq"], 15] = 7
E[["arabia", "qatar", "oman", "israel", "lebanon", "syria", "jordan", "afghanistan", "kenya", "nigeria", "africa", "morocco", "tunisia", "algeria", "ghana", "ethiopia", "peru", "chile", "colombia", "cuba"], 12:14] = [1, 1]
E[["arabia", "qatar", "oman", "israel", "lebanon", "syria", "jordan", "afghanistan", "kenya", "nigeria", "africa", "morocco", "tunisia", "algeria", "ghana", "ethiopia", "peru", "chile", "colombia", "cuba"], 14] = [250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 267, 268, 269, 270]
E[["arabia", "qatar", "oman", "israel", "lebanon", "syria", "jordan", "afghanistan", "kenya", "nigeria", "africa", "morocco", "tunisia", "algeria", "ghana", "ethiopia", "peru", "chile", "colombia", "cuba"], 15] = 7
E["ethiopia", 14:17] = [265, 266, 7]
E[["venezuela", "uruguay", "zealand", "malaysia", "singapore", "taiwan", "hungary", "romania", "serbia", "slovakia", "slovenia", "belarus", "iceland", "estonia", "latvia", "lithuania", "georgia", "armenia", "azerbaijan", "kazakhstan"], 12:14] = [1, 1]
E[["venezuela", "uruguay", "zealand", "malaysia", "singapore", "taiwan", "hungary", "romania", "serbia", "slovakia", "slovenia", "belarus", "iceland", "estonia", "latvia", "lithuania", "georgia", "armenia", "azerbaijan", "kazakhstan"], 14] = [271, 272, 273, 274, 276, 277, 278, 279, 579, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290]
E[["venezuela", "uruguay", "zealand", "malaysia", "singapore", "taiwan", "hungary", "romania", "serbia", "slovakia", "slovenia", "belarus", "iceland", "estonia", "latvia", "lithuania", "georgia", "armenia", "azerbaijan", "kazakhstan"], 15] = 7
E["malaysia", 14:17] = [274, 275, 7]
E[["uzbekistan", "kyrgyzstan", "mongolia", "senegal", "rwanda", "uganda", "zambia", "zimbabwe", "mozambique", "england", "america", "emirates"], 12:14] = [1, 1]
E[["uzbekistan", "kyrgyzstan", "mongolia", "senegal", "rwanda", "uganda", "zambia", "zimbabwe", "mozambique", "england", "america", "emirates"], 14] = [291, 292, 293, 294, 295, 296, 297, 298, 299, 211, 217, 559]
E[["uzbekistan", "kyrgyzstan", "mongolia", "senegal", "rwanda", "uganda", "zambia", "zimbabwe", "mozambique", "england", "america", "emirates"], 15] = 7

# Continents, languages, currencies, national leaders.
E[["france", "britain", "germany", "italy", "spain", "portugal", "greece", "ireland", "netherlands", "belgium", "switzerland", "austria", "sweden", "norway", "finland", "denmark", "poland", "czechia", "ukraine", "russia", "hungary", "romania", "serbia", "slovakia", "slovenia", "belarus", "iceland", "estonia", "latvia", "lithuania", "england"], 17:20] = [391, 7, 0]
E[["japan", "china", "india", "turkey", "korea", "thailand", "vietnam", "indonesia", "philippines", "pakistan", "bangladesh", "nepal", "iran", "iraq", "arabia", "qatar", "oman", "israel", "lebanon", "syria", "jordan", "afghanistan", "malaysia", "singapore", "taiwan", "georgia", "armenia", "azerbaijan", "kazakhstan", "uzbekistan", "kyrgyzstan", "mongolia", "emirates"], 17:20] = [390, 7, 0]
E[["canada", "united", "state", "america", "brazil", "peru", "chile", "colombia", "cuba", "venezuela", "uruguay"], 17:20] = [392, 7, 0]
E[["egypt", "kenya", "nigeria", "africa", "morocco", "tunisia", "algeria", "ghana", "ethiopia", "senegal", "rwanda", "uganda", "zambia", "zimbabwe", "mozambique"], 17:20] = [352, 7, 0]
E[["australia", "zealand"], 17:20] = [393, 7, 0]
E[["united", "state", "america", "canada", "australia", "zealand", "singapore"], 20:23] = [398, 7, 0]
E[["britain", "england", "united", "state", "america", "canada", "australia", "zealand", "ireland"], 23:26] = [198, 7, 0]
E["france", 23:26] = [199, 7, 0]
E[["germany", "austria"], 23:26] = [400, 7, 0]
E[["spain", "peru", "chile", "colombia", "cuba", "venezuela", "uruguay"], 23:26] = [401, 7, 0]
E["italy", 23:26] = [402, 7, 0]
E["russia", 23:26] = [403, 7, 0]
E[["china", "taiwan"], 23:26] = [404, 7, 0]
E["japan", 23:26] = [405, 7, 0]
E[["united", "state", "america"], 33:36] = [491, 7, 0]
E[["britain", "england"], 33:36] = [497, 7, 0]
E["france", 33:36] = [496, 7, 0]
E["germany", 33:36] = [501, 7, 0]
E["italy", 33:36] = [502, 7, 0]
E["canada", 33:36] = [500, 7, 0]
E["india", 33:36] = [495, 7, 0]
E["russia", 33:36] = [494, 7, 0]
E["china", 33:36] = [498, 499, 7]
E["ukraine", 33:36] = [503, 7, 0]

# Cities: default answer and location are their country.
E[["paris", "london", "berlin", "rome", "madrid", "lisbon", "ottawa", "washington", "tokyo", "beijing", "delhi", "moscow", "canberra", "brasilia", "cairo", "athens", "dublin", "amsterdam", "brussels", "bern", "vienna", "stockholm", "oslo", "helsinki", "copenhagen", "warsaw", "prague", "kyiv", "ankara", "seoul", "pyongyang", "bangkok", "hanoi", "jakarta", "manila", "islamabad", "dhaka", "kathmandu", "tehran", "baghdad", "riyadh", "doha", "muscat", "jerusalem", "beirut", "damascus", "amman", "kabul", "nairobi", "abuja", "pretoria", "rabat", "tunis", "algiers", "accra", "addis", "ababa", "lima", "santiago", "bogota", "havana", "caracas", "montevideo", "wellington", "kuala", "lumpur", "taipei", "budapest", "bucharest", "belgrade", "bratislava", "ljubljana", "minsk", "reykjavik", "tallinn", "riga", "vilnius", "tbilisi", "yerevan", "baku", "astana", "tashkent", "bishkek", "ulaanbaatar", "dakar", "kigali", "kampala", "lusaka", "harare", "maputo", "dhabi"], 12:14] = [1, 2]
E["paris", 14:20] = [300, 7, 0, 300, 7, 0]
E["london", 14:20] = [301, 7, 0, 301, 7, 0]
E["berlin", 14:20] = [302, 7, 0, 302, 7, 0]
E["rome", 14:20] = [303, 7, 0, 303, 7, 0]
E["madrid", 14:20] = [304, 7, 0, 304, 7, 0]
E["lisbon", 14:20] = [305, 7, 0, 305, 7, 0]
E["ottawa", 14:20] = [306, 7, 0, 306, 7, 0]
E["washington", 14:20] = [307, 308, 11, 307, 308, 11]
E["tokyo", 14:20] = [309, 7, 0, 309, 7, 0]
E["beijing", 14:20] = [310, 7, 0, 310, 7, 0]
E["delhi", 14:20] = [311, 7, 0, 311, 7, 0]
E["moscow", 14:20] = [312, 7, 0, 312, 7, 0]
E["canberra", 14:20] = [313, 7, 0, 313, 7, 0]
E["brasilia", 14:20] = [314, 7, 0, 314, 7, 0]
E["cairo", 14:20] = [315, 7, 0, 315, 7, 0]
E["athens", 14:20] = [316, 7, 0, 316, 7, 0]
E["dublin", 14:20] = [317, 7, 0, 317, 7, 0]
E["amsterdam", 14:20] = [318, 7, 0, 318, 7, 0]
E["brussels", 14:20] = [319, 7, 0, 319, 7, 0]
E["bern", 14:20] = [320, 7, 0, 320, 7, 0]
E["vienna", 14:20] = [321, 7, 0, 321, 7, 0]
E["stockholm", 14:20] = [322, 7, 0, 322, 7, 0]
E["oslo", 14:20] = [323, 7, 0, 323, 7, 0]
E["helsinki", 14:20] = [324, 7, 0, 324, 7, 0]
E["copenhagen", 14:20] = [325, 7, 0, 325, 7, 0]
E["warsaw", 14:20] = [326, 7, 0, 326, 7, 0]
E["prague", 14:20] = [327, 7, 0, 327, 7, 0]
E["kyiv", 14:20] = [328, 7, 0, 328, 7, 0]
E["ankara", 14:20] = [329, 7, 0, 329, 7, 0]
E["seoul", 14:20] = [332, 330, 7, 332, 330, 7]
E["pyongyang", 14:20] = [331, 330, 7, 331, 330, 7]
E["bangkok", 14:20] = [333, 7, 0, 333, 7, 0]
E["hanoi", 14:20] = [334, 7, 0, 334, 7, 0]
E["jakarta", 14:20] = [335, 7, 0, 335, 7, 0]
E["manila", 14:20] = [336, 7, 0, 336, 7, 0]
E["islamabad", 14:20] = [337, 7, 0, 337, 7, 0]
E["dhaka", 14:20] = [338, 7, 0, 338, 7, 0]
E["kathmandu", 14:20] = [339, 7, 0, 339, 7, 0]
E["tehran", 14:20] = [340, 7, 0, 340, 7, 0]
E["baghdad", 14:20] = [341, 7, 0, 341, 7, 0]
E["riyadh", 14:20] = [342, 7, 0, 342, 7, 0]
E["doha", 14:20] = [343, 7, 0, 343, 7, 0]
E["muscat", 14:20] = [344, 7, 0, 344, 7, 0]
E["jerusalem", 14:20] = [345, 7, 0, 345, 7, 0]
E["beirut", 14:20] = [346, 7, 0, 346, 7, 0]
E["damascus", 14:20] = [347, 7, 0, 347, 7, 0]
E["amman", 14:20] = [348, 7, 0, 348, 7, 0]
E["kabul", 14:20] = [349, 7, 0, 349, 7, 0]
E["nairobi", 14:20] = [350, 7, 0, 350, 7, 0]
E["abuja", 14:20] = [351, 7, 0, 351, 7, 0]
E["pretoria", 14:20] = [332, 352, 7, 332, 352, 7]
E["rabat", 14:20] = [353, 7, 0, 353, 7, 0]
E["tunis", 14:20] = [354, 7, 0, 354, 7, 0]
E["algiers", 14:20] = [355, 7, 0, 355, 7, 0]
E["accra", 14:20] = [356, 7, 0, 356, 7, 0]
E[["addis", "ababa"], 14:20] = [357, 7, 0, 357, 7, 0]
E["lima", 14:20] = [358, 7, 0, 358, 7, 0]
E["santiago", 14:20] = [359, 7, 0, 359, 7, 0]
E["bogota", 14:20] = [360, 7, 0, 360, 7, 0]
E["havana", 14:20] = [361, 7, 0, 361, 7, 0]
E["caracas", 14:20] = [362, 7, 0, 362, 7, 0]
E["montevideo", 14:20] = [363, 7, 0, 363, 7, 0]
E["wellington", 14:20] = [120, 364, 7, 120, 364, 7]
E[["kuala", "lumpur"], 14:20] = [365, 7, 0, 365, 7, 0]
E["taipei", 14:20] = [366, 7, 0, 366, 7, 0]
E["budapest", 14:20] = [367, 7, 0, 367, 7, 0]
E["bucharest", 14:20] = [368, 7, 0, 368, 7, 0]
E["belgrade", 14:20] = [369, 7, 0, 369, 7, 0]
E["bratislava", 14:20] = [370, 7, 0, 370, 7, 0]
E["ljubljana", 14:20] = [371, 7, 0, 371, 7, 0]
E["minsk", 14:20] = [372, 7, 0, 372, 7, 0]
E["reykjavik", 14:20] = [373, 7, 0, 373, 7, 0]
E["tallinn", 14:20] = [374, 7, 0, 374, 7, 0]
E["riga", 14:20] = [375, 7, 0, 375, 7, 0]
E["vilnius", 14:20] = [376, 7, 0, 376, 7, 0]
E["tbilisi", 14:20] = [377, 7, 0, 377, 7, 0]
E["yerevan", 14:20] = [378, 7, 0, 378, 7, 0]
E["baku", 14:20] = [379, 7, 0, 379, 7, 0]
E["astana", 14:20] = [380, 7, 0, 380, 7, 0]
E["tashkent", 14:20] = [381, 7, 0, 381, 7, 0]
E["bishkek", 14:20] = [382, 7, 0, 382, 7, 0]
E["ulaanbaatar", 14:20] = [383, 7, 0, 383, 7, 0]
E["dakar", 14:20] = [384, 7, 0, 384, 7, 0]
E["kigali", 14:20] = [385, 7, 0, 385, 7, 0]
E["kampala", 14:20] = [386, 7, 0, 386, 7, 0]
E["lusaka", 14:20] = [387, 7, 0, 387, 7, 0]
E["harare", 14:20] = [388, 7, 0, 388, 7, 0]
E["maputo", 14:20] = [389, 7, 0, 389, 7, 0]
E["dhabi", 14:20] = [559, 7, 0, 559, 7, 0]

# Companies.
E[["openai", "anthropic", "google", "microsoft", "meta", "facebook", "instagram", "whatsapp", "tesla", "spacex", "nvidia", "amazon", "apple", "samsung", "sony", "nintendo", "netflix", "spotify", "youtube", "twitter", "tiktok", "bytedance", "deepseek", "mistral", "xai", "deepmind", "alphabet", "intel", "amd"], 12:14] = [1, 3]
E[["openai", "anthropic", "google", "microsoft", "meta", "facebook", "instagram", "whatsapp", "tesla", "spacex", "nvidia", "amazon", "apple", "samsung", "sony", "nintendo", "netflix", "spotify", "youtube", "twitter", "tiktok", "bytedance", "deepseek", "mistral", "xai", "deepmind", "alphabet", "intel", "amd"], 14:17] = [162, 7, 0]
E[["openai", "anthropic", "google", "microsoft", "meta", "facebook", "instagram", "whatsapp", "tesla", "spacex", "nvidia", "amazon", "apple", "netflix", "youtube", "twitter", "xai", "alphabet", "intel", "amd"], 17:20] = [307, 308, 11]
E[["tiktok", "bytedance", "deepseek"], 17:20] = [310, 7, 0]
E[["sony", "nintendo"], 17:20] = [309, 7, 0]
E["samsung", 17:20] = [332, 330, 7]
E["spotify", 17:20] = [322, 7, 0]
E["mistral", 17:20] = [300, 7, 0]
E["deepmind", 17:20] = [301, 7, 0]
E["openai", 33:42] = [460, 461, 7, 460, 461, 7, 443, 7, 0]
E["anthropic", 33:42] = [462, 464, 7, 462, 464, 7, 444, 7, 0]
E["google", 33:42] = [467, 468, 7, 485, 486, 7, 445, 7, 0]
E["microsoft", 33:42] = [469, 470, 7, 481, 482, 7, 450, 7, 0]
E["meta", 33:42] = [475, 476, 7, 475, 476, 7, 425, 7, 0]
E["facebook", 33:42] = [475, 476, 7, 475, 476, 7, 424, 7, 0]
E[["instagram", "whatsapp"], 33:36] = [424, 7, 0]
E["instagram", 36:39] = [424, 7, 0]
E["whatsapp", 36:39] = [425, 7, 0]
E["tesla", 33:42] = [473, 474, 7, 473, 474, 7, 563, 11, 7]
E["spacex", 33:39] = [473, 474, 7, 473, 474, 7]
E["nvidia", 33:42] = [471, 472, 7, 471, 472, 7, 196, 11, 7]
E["amazon", 36:39] = [477, 478, 7]
E["apple", 33:42] = [479, 480, 7, 483, 484, 7, 448, 7, 0]
E["amd", 33:36] = [489, 490, 7]
E["deepmind", 33:39] = [465, 466, 7, 465, 466, 7]
E["alphabet", 33:39] = [467, 468, 7, 485, 486, 7]
E["xai", 33:42] = [473, 474, 7, 473, 474, 7, 447, 7, 0]
E["twitter", 33:36] = [473, 474, 7]
E["tiktok", 33:39] = [439, 7, 0, 439, 7, 0]
E["bytedance", 39:42] = [438, 7, 0]
E["youtube", 33:39] = [422, 7, 0, 422, 7, 0]
E["nintendo", 39:42] = [564, 7, 0]

# Products and their makers.
E[["chatgpt", "claude", "gemini", "copilot", "grok", "iphone", "ipad", "windows", "android", "linux", "gpt", "llama", "bing"], 12:14] = [1, 4]
E[["chatgpt", "claude", "gemini", "grok"], 14:17] = [5, 6, 7]
E["copilot", 14:17] = [560, 7, 0]
E["iphone", 14:17] = [561, 7, 0]
E["ipad", 14:17] = [196, 7, 0]
E[["windows", "android", "linux", "gpt", "llama", "bing"], 14:17] = [562, 7, 0]
E[["chatgpt", "gpt"], 17:20] = [420, 7, 0]
E[["chatgpt", "gpt"], 33:42] = [420, 7, 0, 420, 7, 0, 420, 7, 0]
E["claude", 17:20] = [421, 7, 0]
E["claude", 33:42] = [421, 7, 0, 421, 7, 0, 421, 7, 0]
E[["gemini", "android"], 17:20] = [422, 7, 0]
E[["gemini", "android"], 33:42] = [422, 7, 0, 422, 7, 0, 422, 7, 0]
E[["copilot", "windows", "bing"], 17:20] = [423, 7, 0]
E[["copilot", "windows", "bing"], 33:42] = [423, 7, 0, 423, 7, 0, 423, 7, 0]
E["grok", 17:20] = [442, 7, 0]
E["grok", 33:42] = [442, 7, 0, 442, 7, 0, 442, 7, 0]
E[["iphone", "ipad"], 17:20] = [190, 7, 0]
E[["iphone", "ipad"], 33:42] = [190, 7, 0, 190, 7, 0, 190, 7, 0]
E["llama", 17:20] = [424, 7, 0]
E["llama", 33:42] = [424, 7, 0, 424, 7, 0, 424, 7, 0]

# Familiar people.
E[["einstein", "newton", "darwin", "galileo", "curie", "edison", "turing", "lovelace", "hawking", "shakespeare", "mozart", "beethoven", "picasso", "leonardo", "trump", "biden", "obama", "putin", "modi", "macron", "starmer", "xi", "jinping", "carney", "merz", "meloni", "zelensky", "gandhi", "mandela", "armstrong", "gagarin"], 12:14] = [1, 5]
E[["einstein", "newton", "darwin", "galileo", "curie", "edison", "turing", "lovelace", "hawking"], 14:17] = [520, 7, 0]
E["shakespeare", 14:17] = [536, 7, 0]
E[["mozart", "beethoven"], 14:17] = [103, 7, 0]
E[["picasso", "leonardo"], 14:17] = [521, 7, 0]
E[["trump", "biden", "obama", "putin", "modi", "macron", "starmer", "xi", "jinping", "carney", "merz", "meloni", "zelensky", "gandhi", "mandela"], 14:17] = [526, 7, 0]
E[["newton", "darwin", "turing", "lovelace", "hawking", "shakespeare", "starmer"], 17:20] = [301, 7, 0]
E[["einstein", "beethoven", "merz"], 17:20] = [302, 7, 0]
E[["galileo", "leonardo", "meloni"], 17:20] = [303, 7, 0]
E["mozart", 17:20] = [321, 7, 0]
E["picasso", 17:20] = [304, 7, 0]
E[["edison", "trump", "biden", "obama", "armstrong"], 17:20] = [307, 308, 11]
E[["putin", "gagarin"], 17:20] = [312, 7, 0]
E[["modi", "gandhi"], 17:20] = [311, 7, 0]
E["macron", 17:20] = [300, 7, 0]
E[["xi", "jinping"], 17:20] = [310, 7, 0]
E["carney", 17:20] = [306, 7, 0]
E["zelensky", 17:20] = [328, 7, 0]
E["mandela", 17:20] = [332, 352, 7]
E["curie", 17:20] = [326, 7, 0]

# Basic science and physical subjects.
E[["sun", "moon", "earth", "star", "planet", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto", "water", "ice", "snow", "fire", "rock", "stone", "mountain", "ocean", "sea", "river", "nile", "everest", "sahara", "sky", "grass", "tree", "flower", "animal", "cat", "dog", "fish", "elephant", "mouse", "bird", "horse", "cow", "snake", "ant", "rabbit", "insect", "human", "person", "milk", "fruit", "orange", "computer", "car", "phone", "bulb", "week", "year", "day", "hour", "minute", "dozen", "pair", "system", "continent"], 12:14] = [1, 6]
E["sun", 14:17] = [160, 7, 0]
E["moon", 14:17] = [194, 170, 7]
E[["earth", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune"], 14:17] = [161, 7, 0]
E["pluto", 14:17] = [4, 161, 7]
E["star", 14:17] = [167, 7, 0]
E["planet", 14:17] = [413, 7, 0]
E["water", 14:17] = [569, 7, 0]
E["ice", 14:17] = [570, 164, 7]
E["snow", 14:17] = [61, 164, 7]
E["fire", 14:17] = [62, 7, 0]
E["stone", 14:17] = [170, 7, 0]
E["mountain", 14:17] = [408, 7, 0]
E["ocean", 14:17] = [395, 7, 0]
E["sea", 14:17] = [164, 7, 0]
E["river", 14:17] = [406, 7, 0]
E["nile", 14:20] = [571, 7, 0, 352, 7, 0]
E["everest", 14:20] = [191, 7, 0, 339, 7, 0]
E["sahara", 14:20] = [572, 7, 0, 352, 7, 0]
E[["cat", "dog"], 14:17] = [93, 7, 0]
E[["fish", "elephant", "mouse", "bird", "horse", "cow", "snake", "ant", "rabbit", "insect"], 14:17] = [153, 7, 0]
E["animal", 14:17] = [154, 7, 0]
E[["grass", "tree", "flower"], 14:17] = [566, 7, 0]
E["human", 14:17] = [163, 7, 0]
E["person", 14:17] = [67, 7, 0]
E[["fruit", "orange"], 14:17] = [83, 7, 0]
E["computer", 14:17] = [562, 7, 0]
E["phone", 36:39] = [574, 7, 0]
E["bulb", 36:39] = [512, 7, 0]
E["computer", 36:39] = [513, 7, 0]

# Colours of familiar things.
E["sky", 20:23] = [96, 7, 0]
E[["grass", "tree"], 20:23] = [97, 7, 0]
E["sun", 20:23] = [565, 7, 0]
E[["snow", "ice", "milk"], 20:23] = [126, 7, 0]
E["orange", 20:23] = [158, 7, 0]
E["blood", 12:14] = [1, 6]
E["blood", 20:23] = [95, 7, 0]

# Traits.
E[["sun", "fire", "star"], 57] = 1
E[["ice", "snow", "moon"], 57] = -1
E[["sun", "moon", "earth", "star", "planet", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "mountain", "ocean", "sea", "everest", "elephant", "horse", "cow", "tree", "car"], 58] = 1
E[["rock", "stone", "mouse", "bird", "cat", "dog", "fish", "ant", "rabbit", "insect", "grass", "flower", "computer", "phone"], 58] = -1
E[["animal", "cat", "dog", "fish", "elephant", "mouse", "bird", "horse", "cow", "snake", "ant", "rabbit", "insect", "human", "person", "tree", "grass", "flower"], 59] = 1
E[["sun", "moon", "earth", "star", "planet", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto", "water", "ice", "snow", "fire", "rock", "stone", "mountain", "ocean", "sea", "river", "nile", "everest", "sahara", "sky", "milk", "computer", "car", "phone", "bulb"], 59] = -1

# Numeric factual payload H; no literal operands needed.
E["week", 39:42] = [187, 7, 0]
E["year", 39:42] = [183, 186, 185]
E["day", 39:42] = [182, 184, 7]
E[["hour", "minute"], 39:42] = [186, 180, 7]
E["dozen", 39:42] = [181, 182, 7]
E["pair", 39:42] = [182, 7, 0]
E["system", 39:42] = [188, 7, 0]
E["continent", 17:20] = [187, 7, 0]
E[["cat", "dog", "elephant", "mouse", "horse", "cow", "rabbit"], 39:42] = [184, 7, 0]
E[["bird", "human", "person"], 39:42] = [182, 7, 0]
E[["ant", "insect"], 39:42] = [186, 7, 0]
E["snake", 39:42] = [180, 7, 0]

# Extend useful echo keys without making unsupported words selectable.
E[["france", "britain", "germany", "italy", "spain", "portugal", "canada", "united", "state", "japan", "china", "india", "russia", "australia", "brazil", "egypt", "greece", "ireland", "netherlands", "belgium", "switzerland", "austria", "sweden", "norway", "finland", "denmark", "poland", "czechia", "ukraine", "turkey", "korea", "north", "south", "thailand", "vietnam", "indonesia", "philippines", "pakistan", "bangladesh", "nepal", "iran", "iraq", "arabia", "qatar", "oman", "israel", "lebanon", "syria", "jordan", "afghanistan", "kenya", "nigeria", "africa", "morocco", "tunisia", "algeria", "ghana", "ethiopia", "peru", "chile", "colombia", "cuba", "venezuela", "uruguay", "zealand", "malaysia", "taiwan", "hungary", "romania", "serbia", "slovakia", "slovenia", "belarus", "iceland", "estonia", "latvia", "lithuania", "georgia", "armenia", "azerbaijan", "kazakhstan", "uzbekistan", "kyrgyzstan", "mongolia", "senegal", "rwanda", "uganda", "zambia", "zimbabwe", "mozambique"], 43] = 1
E[["asia", "europe", "america", "oceania", "antarctica", "pacific", "atlantic", "arctic", "dollar", "cent", "german", "spanish", "italian", "russian", "chinese", "japanese", "nile", "amazon", "everest", "sahara", "mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune", "pluto", "einstein", "newton"], 43] = 1
E[["openai", "anthropic", "google", "microsoft", "meta", "facebook", "instagram", "whatsapp", "tesla", "spacex", "nvidia", "samsung", "sony", "nintendo", "netflix", "spotify", "youtube", "twitter", "tiktok", "bytedance", "deepseek", "mistral", "xai", "chatgpt", "claude", "gemini", "copilot", "grok", "iphone", "ipad", "windows", "android", "linux", "gpt", "llama", "deepmind", "alphabet", "bing", "intel", "amd"], 43] = 1
E[["sam", "altman", "dario", "daniela", "amodei", "demis", "hassabis", "sundar", "pichai", "satya", "nadella", "jensen", "huang", "elon", "musk", "mark", "zuckerberg", "jeff", "bezos", "tim", "cook", "bill", "gates", "steve", "jobs", "larry", "page", "sergey", "brin", "lisa", "su", "trump", "biden", "obama", "putin", "modi", "macron", "starmer", "xi", "jinping", "carney", "merz", "meloni", "zelensky", "gandhi", "mandela", "shakespeare", "mozart", "beethoven", "darwin", "galileo", "curie", "edison", "turing", "lovelace", "armstrong", "gagarin", "hawking", "picasso", "leonardo", "science", "art", "invention", "theory", "life", "president", "leader", "king", "queen", "math", "electric", "brain", "heart", "blood", "protein", "warm", "book", "money", "city", "country"], 43] = 1
```