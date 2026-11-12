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