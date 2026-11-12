FINAL PASS — HAND-WRITTEN, UNTESTED

All three passes are complete. No tools, execution, training, or numerical testing were used. This is a finite-rule transformer, not a claim of unrestricted English competence.

The earlier architecture remains:
- Residual 0 is constant; 1/2/3 mark BOS/USER/BOT.
- Raw lexical features 4:40 are copied into 40:76 only for user tokens.
- Layer 1 recovers absolute position through uniform BOS attention and an inverse-position spline; fixed-offset heads read preceding digits.
- Layer 2 tracks the current USER segment, echo words, negation, and historical numbers.
- Layer 3 retrieves current-message intent, subject/facts, adjectives, tasks, speaker, and first/last numbers.
- Layer 4 freezes the plan and payload at BOT.
- M4 decodes fixed sentences using a piecewise-linear spline in 64*template + current_position - BOT_position.
- M5 inserts dynamic words and decomposes numerical answers.
- M6 emits decimal digits.
- U uses nearest-code logits 2*code*z-code², with z in residual180 and constant181.

Earlier numerical machinery:
- Parse up to three contiguous digits at their following delimiter.
- Addition and absolute subtraction use first/last operands.
- Multiplication uses the square identity with hinges through sum1008.
- Division uses a reciprocal spline, exact at divisors1..50 and selected larger knots; intermediate squares interpolate so multiplication by the reciprocal is linear.
- Template44 says “the answer is <decimal> .” and emits unpadded results through9999.
- Numeric semantics remain heuristic: extra numbers, mixed operations, and some word-problem phrasing can fail.

FINAL-PASS ADDITIONS

Raw features:
14 queried property: 1 big,2 small,3 hot,4 cold,5 alive,6 dead; 7 red,8 near,9 live are planet-query hints.
31 physical noun marker.
32 size:1 big,2 small.
33 temperature:1 hot,2 cold.
34 life:1 alive,2 not alive.
35 physical-adjective marker.
36 explicit-task marker, preventing physical classification from overriding word tasks.
37 spoken-number marker.
38 spoken-number value0..10.
39 relation:1 continent,2 language,3 leader/president,4 prime minister,5 founder,6 half,7 double,8 triple,9 quarter,10 quantity,12 currency.
235 preference-verb marker.
241 user-personal-pronoun marker.
245 numeric-world-fact value;247 corresponding marker.

New attention:
L1 H6 tracks like/love/enjoy, resetting at USER ->237.
L1 H7 tracks personal vs bot pronouns, resetting at USER ->240.
L2 H4 retrieves current physical noun ->221 marker,222 size,223 temperature,224 life.
L2 H5 retrieves current queried property ->225.
L2 H6 tracks whether an explicit task exists ->226.
L2 H7 retrieves spoken number ->227 value,228 position,229 marker.
L3 H1 additionally retrieves numeric-world-fact value116 and marker130.
L3 H3 additionally retrieves relation113.
L4 H1 retrieves latest user preference object ->242 code,243 presence.
L4 H0 additionally freezes class code114, relation121, alternative facts122/123, alternative presence124, two-word flag125, numeric fact128/129, and adjective class131.

New MLP processing:
M1 units359:361 capture user preference objects into238/239.
M1 units362:364 user-gate numeric-world-fact value/marker into246/248.
M2 units292:328 classify six predicates against noun properties; output98 active,107 unnegated truth,111 answer adjective,112 nonliving flag.
M2 units328:330 choose spoken vs digit number by recency ->230.
M3 units854:859 choose classification templates45..48, accounting for not.
M3 units859:862 distinguish user-preference recall14 from bot-preference reply15.
M3 units862:864 select count template49+N.
M3 units864:920 provide continent ranges for original capital codes.
M3 units920:962 provide languages.
M3 units962:1004 provide selected country leaders.
M3 units1004:1022 provide selected company founders.
M3 units1022:1024 select latest numeric value into115; this now supplies frozen173.
M4 units712:746 implement physical classifications.
M4 units746:925 implement counts0..10.
M4 units925:939 implement preference replies.
M4 units939:955 apply unary half/double/triple/quarter.
M4 units955:957 insert numeric world facts for quantity questions.
M4 units957:972 refine planet answers.
M4 units972:984 supply dollar for four currencies.
M5 units236:241 insert classification, preference, and alternative fact payloads.

New templates:
14 “you like <remembered object> .”
15 “i can talk about <echo object> .”
45 “yes , it is <property> .”
46 “no , it is <property> .”
47 “yes , it is not alive .”
48 “no , it is not alive .”
49..59 “the number -s are <count from1 through N> .”;49 uses0.
Physical replies state the actual property even when the question is negated.

Output-code additions:
388 english,389 french,390 german,391 spanish,392 chinese,393 japanese,394 russian,395 italian,
396 trump,397 macron,398 putin,399 xi,400 jinping,401 zelensky,402 lula,403 starmer,404 carney,
405 merz,406 meloni,407 modi,408 erdogan,409 netanyahu,410 larry,411 page,412 dollar,413 flower,
414 brussels,415 abuja,416 dhaka,417 kathmandu,418 kuala,419 lumpur,420 colombo,421 bucharest,
422 prague,423 budapest,424 reykjavik,425 manila,426 taipei,427 singapore,428 kabul,429 tunis,
430 rabat,431 tashkent,432 harare,433 lusaka,434 dakar,435 accra,
436 hate,437 cruel,438 bitter,439 sweet,440 dangerous,441 late,442 early,443 cry,444 laugh,
445 less,446 more,447 sell,448 buy.

Coverage expanded with additional capitals, languages, continents, leaders, founders, physical properties, echo words, opposites, count-to-ten, preference memory, unary arithmetic, and selected numeric facts. Known limitations include relation ambiguity, approximate division for some larger divisors, simplified physical categories, incomplete vocabulary/knowledge, and unsupported multi-step arithmetic. No runtime behavior has been observed.