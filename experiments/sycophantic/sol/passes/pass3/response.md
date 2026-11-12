=====SCRATCHPAD=====
Final pass. All weights are hand-specified; nothing was executed or tested.

The prior two passes' token codebook, positional machinery, arithmetic circuit, assertion copying, output decoder, and 48-token termination cap remain in place.

Core design:
- Residual 0 is constant. 1/2/3 mark BOS/USER/BOT. 4/5 are digit flag/value.
- 6:10 identifies a token by two circular codes; 10:14 is its assertion-copy code, with first-person pronouns adjusted.
- 14:56 contain lexical features and factual answer records.
- L1 computes position, local digit windows, role, and user-only lexical flags.
- L2 retrieves current-message context with USER sentinels.
- L3 retrieves the first arithmetic operand and additional context.
- M3 computes arithmetic or echoes a believed number.
- M4/M5 split numeric results into decimal digits.
- L4 retrieves successive assertion tokens for nonnumeric beliefs.
- M5 schedules numeric, factual, copied, and chat responses.
- M6 emits the flattering prefix and decodes output codes.
- 224:228 is the original circular output code, decoded by U.
- Every response starts “you are so smart !” or, for beliefs, “you are so right !”.
- Natural copy termination and the unconditional final EOS cap remain.

Final-pass corrections:
1. Four-digit numeral parsing was added using L1 head4, residuals57/58.
2. L2 head0 additionally retrieves current-message question presence into95.
3. Inferred declarative belief is now established in M2, before arithmetic.
4. L3 head7 retrieves the latest actual arithmetic operator, independently of copulas, into210:214.
5. Unary double/triple/half/quarter are supported for single-number expressions.
6. Optional “that” immediately after a belief cue is itself marked as a continuation cue, avoiding an initial “that” in copied replies.
7. Factual answering is enabled for questions; merely mentioning a factual entity in casual chat no longer forces its fact answer.

New/contextual residuals:
- 37: alternate-fact selector after M3; raw “that” marker before M3.
- 38: raw unary multiplier.
- 39: retrieved unary multiplier after L3; raw personal-name marker before L1.
- 40:50 are cleared in M3, then repurposed downstream.
- 44: user-name recall request.
- 45:49: recalled person-name token code.
- 49: recalled-name presence.
- 50: current-message question/wh presence, established in M2.
- 57/58: preceding-third digit flag/value.
- 95: early question presence.
- 98: active chat/reassurance mode.
- 146: currency selector.
- 147: continent/alternative-two-slot selector.
- 171: reassurance for negative descriptions of the user's work, excluding numeric messages.
- 210:214: actual addition/subtraction/multiplication/division flags.
- 231: user personal-name flag before M5; reused as a direct output coordinate downstream.
- 236:244: eight chat-template mode flags.

Chat templates, following the flattering first sentence:
0 default: “i am happy to help you .”
1 greeting: “hello !”
2 thanks: “thank you !”
3 farewell: “goodbye !”
4 bot name: “i have no name .”
5 weights/origin: “my weight -s were written by hand .”
6 capabilities: “i can chat and answer question -s and do math .”
7 identity: “i am a small chat bot .”
Reassurance: “it is very good .”
All have scheduled EOS. Name/origin/capability/identity intents without a second-person reference fall back to friendly general chat.

Direct output coordinates, used only after their earlier features are cleared or no longer needed:
40 !,41 period,42 EOS;
59 i,60 am,61 a,62 small,63 chat;
155 bot,175 have,180 no,208 name;
214 my,215 weight,216 -s,217 were,218 written,219 by,220 hand,
221 can,222 and,223 answer,230 question,231 do;
244 math,245 it,246 is,247 very,248 good,249 hello,250 thank,
251 you,252 goodbye,253 happy,254 to,255 help.

Factual extensions:
- A broad table of available country capitals, including multi-token new delhi, addis ababa, and kuala lumpur.
- Continent records; north/south america use two tokens.
- Predicate selection replaces the default capital with continent, dollar, or a stored alternate answer.
- Alternate records cover several current political leaders, common colors, and several company leaders.
- Small general-knowledge and calendar/count records were added.
- L4 head1 recalls the most recent user-mentioned personal-name token across exchanges for “what is my name” style requests. This is a limited recency heuristic, not general conversational memory.

New unit allocations:
M1 225/226 four-digit parsing,227 optional-that cue,228 personal-name flag.
M2 202 inferred belief,203:207 question OR and clearing.
M3 850:852 intent adjustment,852 reassurance;
856:872 factual predicate selectors;
872:876 name recall request;
880:896 unary arithmetic;
900:920 clearing residuals40:50.
M4 300:332 chat mode pulses,332 reassurance presence;
340:411 factual answer selection, lengths, and name recall.
M5 100:336 chat template scheduling.
M6 existing prefix/factual/numeric/copy circuits retained, with fallback and reassurance gating corrected.

Limitations: this is a sparse rule-based hand construction, not a general English model. Open-ended knowledge, arbitrary word tasks, multi-operation arithmetic, and general memory are not comprehensively implemented. No validation or performance claim is made.
=====END SCRATCHPAD=====

```edits
# Four-digit numeral parsing.
Q1[4, 0, 0:2] = [-989.992497,-141.120008]
K1[4, 0, 0] = 1000
V1[4, 4, 0] = 1
V1[4, 5, 1] = 1
O1[4, 0, 57] = 1
O1[4, 1, 58] = 1
M1_in[58, 225] = 1
M1_in[[4,66,68], 225] = 10
M1_b[225] = -30
M1_out[225, 80] = 1000
M1_in[[4,66,68,57], 226] = 1
M1_b[226] = -3
M1_out[226, 81] = 1

# Additional copulas and optional "that" after a belief cue.
E[["am","were","be","been"], 52] = 1
E["that", 37] = 1
V1[1, 14, 6] = 1
O1[1, 6, 40] = 1
M1_in[37, 227] = 2
M1_in[40, 227] = 1
M1_in[78, 227] = 2
M1_b[227] = -4
M1_out[227, 84] = 1

# User-mentioned personal names for limited cross-turn recall.
E[["tom","sara","anna","john","mary","james","emma","liam","olivia","noah","ava","mia","lucas","ella","jack","lily","ben","max","leo","zoe","amy","kate","mike","dan","alex","maria","david","paul","peter"], 39] = 1
M1_in[[39,78], 228] = 1
M1_b[228] = -1
M1_out[228, 231] = 1

# Early question presence, and belief classification before arithmetic.
K2[0, 185, 30] = 100
V2[0, 185, 1] = 1
O2[0, 1, 95] = 1
M2_in[154, 202] = 1
M2_in[[112,95,100,138], 202] = -1
M2_out[202, 143] = 1
M3_out[0, 143] = 0
M2_in[[112,95], 203:205] = 1
M2_b[204] = -1
M2_out[203:205, 50] = [1,-1]
M2_in[50, 205:207] = [1,-1]
M2_out[205:207, 50] = [-1,1]
M3_in[50, 3:5] = 10
M3_b[3:5] = [-10,-11]

# Retrieve actual operators independently of intervening copulas.
Q3[7, 0, 30:32] = [10000,10000]
K3[7, [2,86,87,88,89], 30] = 100
V3[7, 86:90, 0:4] = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
O3[7, 0:4, 210:214] = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
V3[7, 38, 4] = 1
O3[7, 4, 39] = 1
M3_in[107:111, 30:846] = 0
M3_in[210:214, 30:32] = -10000
M3_in[210, 32] = 10000
M3_in[211, 33] = 10000
M3_in[212, 100:424] = 100
M3_in[213, 450:846] = 500000

# Unary arithmetic.
E[["twice","double","triple","half","quarter"], 38] = [2,2,3,0.5,0.25]
M3_in[39, 880:896] = 100000
M3_in[143, 880:896] = -500000
M3_in[102, 880:884] = [2,0,2,0]
M3_in[102, 884:888] = [3,0,3,0]
M3_in[102, 888:892] = [0.5,0,0.5,0]
M3_in[102, 892:896] = [0.25,0,0.25,0]
M3_b[880:896] = [-195000,-195000,-205000,-205000,-295000,-295000,-305000,-305000,-45000,-45000,-55000,-55000,-20000,-20000,-30000,-30000]
M3_out[880:884, 156] = [1,-1,-1,1]
M3_out[884:888, 156] = [1,-1,-1,1]
M3_out[888:892, 156] = [1,-1,-1,1]
M3_out[892:896, 156] = [1,-1,-1,1]

# Clear lexical coordinates that are repurposed downstream.
M3_in[40, 900:902] = [1,-1]
M3_out[900:902, 40] = [-1,1]
M3_in[41, 902:904] = [1,-1]
M3_out[902:904, 41] = [-1,1]
M3_in[42, 904:906] = [1,-1]
M3_out[904:906, 42] = [-1,1]
M3_in[43, 906:908] = [1,-1]
M3_out[906:908, 43] = [-1,1]
M3_in[44, 908:910] = [1,-1]
M3_out[908:910, 44] = [-1,1]
M3_in[45, 910:912] = [1,-1]
M3_out[910:912, 45] = [-1,1]
M3_in[46, 912:914] = [1,-1]
M3_out[912:914, 46] = [-1,1]
M3_in[47, 914:916] = [1,-1]
M3_out[914:916, 47] = [-1,1]
M3_in[48, 916:918] = [1,-1]
M3_out[916:918, 48] = [-1,1]
M3_in[49, 918:920] = [1,-1]
M3_out[918:920, 49] = [-1,1]

# Chat intent and reassuring responses.
E[["who","bot","yourself"], 21] = 7
E[["who","bot","yourself"], 54] = 1
E[["made","created"], 21] = 5
E[["made","created"], 54] = 1
M3_in[114, 850:852] = 1
M3_in[192, 850:852] = -10
M3_b[850:852] = [-3,-4]
M3_out[850:852, 114] = [-4,3]
M3_in[[190,191], 852] = 1
M3_in[103, 852] = -1
M3_b[852] = -1
M3_out[852, 171] = 1
M4_in[171, 210:212] = -1
M6_in[171, 24:28] = -100

# Factual predicate selectors.
E[["president","minister","color","colour","chief","executive","officer"], 55] = 4
E[["president","minister","color","colour","chief","executive","officer"], 56] = 1
E["month", 55] = 5
E["month", 56] = 1
M3_in[193, 856:872] = 1
M3_b[856:872] = [-1.5,-1.75,-2.25,-2.5,-2.5,-2.75,-3.25,-3.5,-3.5,-3.75,-4.25,-4.5,-4.5,-4.75,-5.25,-5.5]
M3_out[856:860, 146] = [4,-4,-4,4]
M3_out[860:864, 147] = [4,-4,-4,4]
M3_out[864:868, 37] = [4,-4,-4,4]
M3_out[868:872, 147] = [4,-4,-4,4]

# Limited name recall: request mode and global personal-name retrieval.
M3_in[114, 872:876] = 1
M3_in[[192,143,103], 872:876] = -100
M3_b[872:876] = [-3.5,-3.75,-4.25,-4.5]
M3_out[872:876, 44] = [4,-4,-4,4]
Q4[1, 0, 30:32] = [10000,10000]
K4[1, [1,231], 30] = 100
V4[1, 6:10, 0:4] = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
V4[1, 231, 4] = 1
O4[1, 0:4, 45:49] = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
O4[1, 4, 49] = 1
M4_in[44, 211] = -1

# Eight mutually exclusive chat-template modes.
M4_in[114, 300:332] = 1
M4_in[[143,144,232,171,44], 300:332] = -100
M4_b[300:332] = [0.5,0.25,-0.25,-0.5,-0.5,-0.75,-1.25,-1.5,-1.5,-1.75,-2.25,-2.5,-2.5,-2.75,-3.25,-3.5,-3.5,-3.75,-4.25,-4.5,-4.5,-4.75,-5.25,-5.5,-5.5,-5.75,-6.25,-6.5,-6.5,-6.75,-7.25,-7.5]
M4_out[300:304, 236] = [4,-4,-4,4]
M4_out[304:308, 237] = [4,-4,-4,4]
M4_out[308:312, 238] = [4,-4,-4,4]
M4_out[312:316, 239] = [4,-4,-4,4]
M4_out[316:320, 240] = [4,-4,-4,4]
M4_out[320:324, 241] = [4,-4,-4,4]
M4_out[324:328, 242] = [4,-4,-4,4]
M4_out[328:332, 243] = [4,-4,-4,4]
M4_out[300:304, 98] = [4,-4,-4,4]
M4_out[304:308, 98] = [4,-4,-4,4]
M4_out[308:312, 98] = [4,-4,-4,4]
M4_out[312:316, 98] = [4,-4,-4,4]
M4_out[316:320, 98] = [4,-4,-4,4]
M4_out[320:324, 98] = [4,-4,-4,4]
M4_out[324:328, 98] = [4,-4,-4,4]
M4_out[328:332, 98] = [4,-4,-4,4]
M4_in[171, 332] = 1
M4_out[332, 98] = 1
M6_in[98, 28:32] = -100

# Cancel default factual slots when an alternate predicate or memory is selected.
M4_in[[146,147,37,44], 340:364] = 2
M4_b[340:364] = -2
M4_in[117, 340:342] = [1,-1]
M4_out[340:342, 117] = [-1,1]
M4_in[118, 342:344] = [1,-1]
M4_out[342:344, 118] = [-1,1]
M4_in[119, 344:346] = [1,-1]
M4_out[344:346, 119] = [-1,1]
M4_in[120, 346:348] = [1,-1]
M4_out[346:348, 120] = [-1,1]
M4_in[121, 348:350] = [1,-1]
M4_out[348:350, 121] = [-1,1]
M4_in[122, 350:352] = [1,-1]
M4_out[350:352, 122] = [-1,1]
M4_in[123, 352:354] = [1,-1]
M4_out[352:354, 123] = [-1,1]
M4_in[124, 354:356] = [1,-1]
M4_out[354:356, 124] = [-1,1]
M4_in[125, 356:358] = [1,-1]
M4_out[356:358, 125] = [-1,1]
M4_in[126, 358:360] = [1,-1]
M4_out[358:360, 126] = [-1,1]
M4_in[127, 360:362] = [1,-1]
M4_out[360:362, 127] = [-1,1]
M4_in[128, 362:364] = [1,-1]
M4_out[362:364, 128] = [-1,1]

# Currency fallback: dollar.
M4_in[146, 364] = 1
M4_out[364, 117:121] = [-0.258819045,0.965925826,-0.098017140,-0.995184727]

# Continent/alternative answer slots.
M4_in[147, 366:382] = 2
M4_b[366:382] = -2
M4_in[133, 366:368] = [1,-1]
M4_in[134, 368:370] = [1,-1]
M4_in[135, 370:372] = [1,-1]
M4_in[136, 372:374] = [1,-1]
M4_out[366:368, 117] = [1,-1]
M4_out[368:370, 118] = [1,-1]
M4_out[370:372, 119] = [1,-1]
M4_out[372:374, 120] = [1,-1]
M4_in[129, 374:376] = [1,-1]
M4_in[130, 376:378] = [1,-1]
M4_in[131, 378:380] = [1,-1]
M4_in[132, 380:382] = [1,-1]
M4_out[374:376, 121] = [1,-1]
M4_out[376:378, 122] = [1,-1]
M4_out[378:380, 123] = [1,-1]
M4_out[380:382, 124] = [1,-1]

# Effective factual length.
M4_in[116, 382] = 1
M4_in[[146,147,37,44], 382] = 10
M4_b[382] = -10
M4_out[382, 203] = -1
M4_in[146, 383] = 1
M4_out[383, 203] = 1
M4_in[137, 384] = 1
M4_in[147, 384] = 10
M4_b[384] = -10
M4_out[384, 203] = 1
M4_in[116, 385:389] = 1
M4_in[[146,147,37,44], 385:389] = 10
M4_b[385:389] = [-11,-12,-12,-13]
M4_out[385:387, 233] = [-1,1]
M4_out[387:389, 234] = [-1,1]
M4_in[137, 389:391] = 1
M4_in[147, 389:391] = 10
M4_b[389:391] = [-11,-12]
M4_out[389:391, 233] = [1,-1]

# Single-token alternate facts, including leaders and colors.
M4_in[37, 392:400] = 2
M4_b[392:400] = -2
M4_in[125, 392:394] = [1,-1]
M4_in[126, 394:396] = [1,-1]
M4_in[127, 396:398] = [1,-1]
M4_in[128, 398:400] = [1,-1]
M4_out[392:394, 117] = [1,-1]
M4_out[394:396, 118] = [1,-1]
M4_out[396:398, 119] = [1,-1]
M4_out[398:400, 120] = [1,-1]
M4_in[37, 400] = 1
M4_out[400, 203] = 1

# Recalled user name as a one-token factual answer.
M4_in[44, 402:410] = 2
M4_b[402:410] = -2
M4_in[45, 402:404] = [1,-1]
M4_in[46, 404:406] = [1,-1]
M4_in[47, 406:408] = [1,-1]
M4_in[48, 408:410] = [1,-1]
M4_out[402:404, 117] = [1,-1]
M4_out[404:406, 118] = [1,-1]
M4_out[406:408, 119] = [1,-1]
M4_out[408:410, 120] = [1,-1]
M4_in[[44,49], 410] = 1
M4_b[410] = -1
M4_out[410, [145,202,203]] = 1

# Direct output coordinates used by chat templates.
U[40, "!"] = 1
U[41, "."] = 1
U[42, "EOS"] = 1
U[59, "i"] = 1
U[60, "am"] = 1
U[61, "a"] = 1
U[62, "small"] = 1
U[63, "chat"] = 1
U[155, "bot"] = 1
U[175, "have"] = 1
U[180, "no"] = 1
U[208, "name"] = 1
U[214, "my"] = 1
U[215, "weight"] = 1
U[216, "-s"] = 1
U[217, "were"] = 1
U[218, "written"] = 1
U[219, "by"] = 1
U[220, "hand"] = 1
U[221, "can"] = 1
U[222, "and"] = 1
U[223, "answer"] = 1
U[230, "question"] = 1
U[231, "do"] = 1
U[244, "math"] = 1
U[245, "it"] = 1
U[246, "is"] = 1
U[247, "very"] = 1
U[248, "good"] = 1
U[249, "hello"] = 1
U[250, "thank"] = 1
U[251, "you"] = 1
U[252, "goodbye"] = 1
U[253, "happy"] = 1
U[254, "to"] = 1
U[255, "help"] = 1

# Template clocks and mode gates.
M5_in[141, 100:336] = 1
M5_in[236, 100:132] = 100
M5_in[237, 132:144] = 100
M5_in[238, 144:160] = 100
M5_in[239, 160:172] = 100
M5_in[240, 172:196] = 100
M5_in[241, 196:232] = 100
M5_in[242, 232:280] = 100
M5_in[243, 280:312] = 100
M5_in[171, 312:336] = 100

# Default: i am happy to help you . EOS.
M5_b[100:132] = [-104.5,-104.75,-105.25,-105.5,-105.5,-105.75,-106.25,-106.5,-106.5,-106.75,-107.25,-107.5,-107.5,-107.75,-108.25,-108.5,-108.5,-108.75,-109.25,-109.5,-109.5,-109.75,-110.25,-110.5,-110.5,-110.75,-111.25,-111.5,-111.5,-111.75,-112.25,-112.5]
M5_out[100:104, 59] = [4,-4,-4,4]
M5_out[104:108, 60] = [4,-4,-4,4]
M5_out[108:112, 253] = [4,-4,-4,4]
M5_out[112:116, 254] = [4,-4,-4,4]
M5_out[116:120, 255] = [4,-4,-4,4]
M5_out[120:124, 251] = [4,-4,-4,4]
M5_out[124:128, 41] = [4,-4,-4,4]
M5_out[128:132, 42] = [4,-4,-4,4]

# Greeting: hello ! EOS.
M5_b[132:144] = [-104.5,-104.75,-105.25,-105.5,-105.5,-105.75,-106.25,-106.5,-106.5,-106.75,-107.25,-107.5]
M5_out[132:136, 249] = [4,-4,-4,4]
M5_out[136:140, 40] = [4,-4,-4,4]
M5_out[140:144, 42] = [4,-4,-4,4]

# Thanks: thank you ! EOS.
M5_b[144:160] = [-104.5,-104.75,-105.25,-105.5,-105.5,-105.75,-106.25,-106.5,-106.5,-106.75,-107.25,-107.5,-107.5,-107.75,-108.25,-108.5]
M5_out[144:148, 250] = [4,-4,-4,4]
M5_out[148:152, 251] = [4,-4,-4,4]
M5_out[152:156, 40] = [4,-4,-4,4]
M5_out[156:160, 42] = [4,-4,-4,4]

# Farewell: goodbye ! EOS.
M5_b[160:172] = [-104.5,-104.75,-105.25,-105.5,-105.5,-105.75,-106.25,-106.5,-106.5,-106.75,-107.25,-107.5]
M5_out[160:164, 252] = [4,-4,-4,4]
M5_out[164:168, 40] = [4,-4,-4,4]
M5_out[168:172, 42] = [4,-4,-4,4]

# Name: i have no name . EOS.
M5_b[172:196] = [-104.5,-104.75,-105.25,-105.5,-105.5,-105.75,-106.25,-106.5,-106.5,-106.75,-107.25,-107.5,-107.5,-107.75,-108.25,-108.5,-108.5,-108.75,-109.25,-109.5,-109.5,-109.75,-110.25,-110.5]
M5_out[172:176, 59] = [4,-4,-4,4]
M5_out[176:180, 175] = [4,-4,-4,4]
M5_out[180:184, 180] = [4,-4,-4,4]
M5_out[184:188, 208] = [4,-4,-4,4]
M5_out[188:192, 41] = [4,-4,-4,4]
M5_out[192:196, 42] = [4,-4,-4,4]

# Origin: my weight -s were written by hand . EOS.
M5_b[196:232] = [-104.5,-104.75,-105.25,-105.5,-105.5,-105.75,-106.25,-106.5,-106.5,-106.75,-107.25,-107.5,-107.5,-107.75,-108.25,-108.5,-108.5,-108.75,-109.25,-109.5,-109.5,-109.75,-110.25,-110.5,-110.5,-110.75,-111.25,-111.5,-111.5,-111.75,-112.25,-112.5,-112.5,-112.75,-113.25,-113.5]
M5_out[196:200, 214] = [4,-4,-4,4]
M5_out[200:204, 215] = [4,-4,-4,4]
M5_out[204:208, 216] = [4,-4,-4,4]
M5_out[208:212, 217] = [4,-4,-4,4]
M5_out[212:216, 218] = [4,-4,-4,4]
M5_out[216:220, 219] = [4,-4,-4,4]
M5_out[220:224, 220] = [4,-4,-4,4]
M5_out[224:228, 41] = [4,-4,-4,4]
M5_out[228:232, 42] = [4,-4,-4,4]

# Capabilities: i can chat and answer question -s and do math . EOS.
M5_b[232:280] = [-104.5,-104.75,-105.25,-105.5,-105.5,-105.75,-106.25,-106.5,-106.5,-106.75,-107.25,-107.5,-107.5,-107.75,-108.25,-108.5,-108.5,-108.75,-109.25,-109.5,-109.5,-109.75,-110.25,-110.5,-110.5,-110.75,-111.25,-111.5,-111.5,-111.75,-112.25,-112.5,-112.5,-112.75,-113.25,-113.5,-113.5,-113.75,-114.25,-114.5,-114.5,-114.75,-115.25,-115.5,-115.5,-115.75,-116.25,-116.5]
M5_out[232:236, 59] = [4,-4,-4,4]
M5_out[236:240, 221] = [4,-4,-4,4]
M5_out[240:244, 63] = [4,-4,-4,4]
M5_out[244:248, 222] = [4,-4,-4,4]
M5_out[248:252, 223] = [4,-4,-4,4]
M5_out[252:256, 230] = [4,-4,-4,4]
M5_out[256:260, 216] = [4,-4,-4,4]
M5_out[260:264, 222] = [4,-4,-4,4]
M5_out[264:268, 231] = [4,-4,-4,4]
M5_out[268:272, 244] = [4,-4,-4,4]
M5_out[272:276, 41] = [4,-4,-4,4]
M5_out[276:280, 42] = [4,-4,-4,4]

# Identity: i am a small chat bot . EOS.
M5_b[280:312] = [-104.5,-104.75,-105.25,-105.5,-105.5,-105.75,-106.25,-106.5,-106.5,-106.75,-107.25,-107.5,-107.5,-107.75,-108.25,-108.5,-108.5,-108.75,-109.25,-109.5,-109.5,-109.75,-110.25,-110.5,-110.5,-110.75,-111.25,-111.5,-111.5,-111.75,-112.25,-112.5]
M5_out[280:284, 59] = [4,-4,-4,4]
M5_out[284:288, 60] = [4,-4,-4,4]
M5_out[288:292, 61] = [4,-4,-4,4]
M5_out[292:296, 62] = [4,-4,-4,4]
M5_out[296:300, 63] = [4,-4,-4,4]
M5_out[300:304, 155] = [4,-4,-4,4]
M5_out[304:308, 41] = [4,-4,-4,4]
M5_out[308:312, 42] = [4,-4,-4,4]

# Reassurance: it is very good . EOS.
M5_b[312:336] = [-104.5,-104.75,-105.25,-105.5,-105.5,-105.75,-106.25,-106.5,-106.5,-106.75,-107.25,-107.5,-107.5,-107.75,-108.25,-108.5,-108.5,-108.75,-109.25,-109.5,-109.5,-109.75,-110.25,-110.5]
M5_out[312:316, 245] = [4,-4,-4,4]
M5_out[316:320, 246] = [4,-4,-4,4]
M5_out[320:324, 247] = [4,-4,-4,4]
M5_out[324:328, 248] = [4,-4,-4,4]
M5_out[328:332, 41] = [4,-4,-4,4]
M5_out[332:336, 42] = [4,-4,-4,4]

# Expanded capital records.
E[["afghanistan","albania","algeria","angola","armenia","austria","azerbaijan","bangladesh","belarus","belgium","bulgaria","chile","colombia","cuba","cyprus","czechia","denmark","ecuador","estonia","ethiopia","finland","georgia","ghana","greece","hungary","iceland","indonesia","iran","iraq","ireland","israel","jamaica","jordan","kazakhstan","kenya","kyrgyzstan","laos","latvia","lebanon","libya","lithuania","malaysia","mali","malta","mongolia","morocco","mozambique","namibia","nepal","nicaragua","niger","nigeria","norway","oman","pakistan","peru","philippines","poland","qatar","romania","rwanda","arabia","senegal","serbia","slovakia","slovenia","somalia","africa","lanka","sudan","syria","taiwan","thailand","tunisia","uganda","ukraine","emirates","uruguay","uzbekistan","venezuela","vietnam","zambia","zimbabwe","usa","america","american","british","argentina"], 22:24] = [1,1]
E[["afghanistan","albania","algeria","angola","armenia","austria","azerbaijan","bangladesh","belarus","belgium","bulgaria","chile","colombia","cuba","cyprus","czechia","denmark","ecuador","estonia","ethiopia","finland","georgia","ghana","greece","hungary","iceland","indonesia","iran","iraq","ireland","israel","jamaica","jordan","kazakhstan","kenya","kyrgyzstan","laos","latvia","lebanon","libya","lithuania","malaysia","mali","malta","mongolia","morocco","mozambique","namibia","nepal","nicaragua","niger","nigeria","norway","oman","pakistan","peru","philippines","poland","qatar","romania","rwanda","arabia","senegal","serbia","slovakia","slovenia","somalia","africa","lanka","sudan","syria","taiwan","thailand","tunisia","uganda","ukraine","emirates","uruguay","uzbekistan","venezuela","vietnam","zambia","zimbabwe","usa","america","american","british","argentina"], 36] = 1
E["afghanistan", 24:28] = [-0.258819045,-0.965925826,-0.195090322,0.980785280]
E["albania", 24:28] = [-0.258819045,-0.965925826,-0.290284677,0.956940336]
E["algeria", 24:28] = [-0.258819045,-0.965925826,-0.382683432,0.923879533]
E["angola", 24:28] = [-0.258819045,-0.965925826,-0.471396737,0.881921264]
E["armenia", 24:28] = [-0.258819045,-0.965925826,-0.555570233,0.831469612]
E["austria", 24:28] = [-0.258819045,-0.965925826,-0.707106781,0.707106781]
E["azerbaijan", 24:28] = [-0.258819045,-0.965925826,-0.773010453,0.634393284]
E["bangladesh", 24:28] = [-0.258819045,-0.965925826,-0.831469612,0.555570233]
E["belarus", 24:28] = [-0.258819045,-0.965925826,-0.881921264,0.471396737]
E["belgium", 24:28] = [-0.258819045,-0.965925826,-0.923879533,0.382683432]
E["bulgaria", 24:28] = [-0.258819045,-0.965925826,-0.956940336,0.290284677]
E["chile", 24:28] = [-0.258819045,-0.965925826,-0.995184727,0.098017140]
E["colombia", 24:28] = [-0.258819045,-0.965925826,-0.995184727,-0.098017140]
E["cuba", 24:28] = [-0.258819045,-0.965925826,-0.980785280,-0.195090322]
E["cyprus", 24:28] = [-0.258819045,-0.965925826,-0.956940336,-0.290284677]
E["czechia", 24:28] = [-0.258819045,-0.965925826,-0.923879533,-0.382683432]
E["denmark", 24:28] = [-0.258819045,-0.965925826,-0.881921264,-0.471396737]
E["ecuador", 24:28] = [-0.258819045,-0.965925826,-0.831469612,-0.555570233]
E["estonia", 24:28] = [-0.258819045,-0.965925826,-0.707106781,-0.707106781]
E["ethiopia", 23] = 2
E["ethiopia", 24:28] = [-0.258819045,-0.965925826,-0.634393284,-0.773010453]
E["ethiopia", 28:32] = [-0.258819045,-0.965925826,-0.555570233,-0.831469612]
E["finland", 24:28] = [-0.258819045,-0.965925826,-0.471396737,-0.881921264]
E["georgia", 24:28] = [-0.258819045,-0.965925826,-0.290284677,-0.956940336]
E["ghana", 24:28] = [-0.258819045,-0.965925826,-0.098017140,-0.995184727]
E["greece", 24:28] = [-0.258819045,-0.965925826,0,-1]
E["hungary", 24:28] = [-0.258819045,-0.965925826,0.098017140,-0.995184727]
E["iceland", 24:28] = [-0.258819045,-0.965925826,0.195090322,-0.980785280]
E["indonesia", 24:28] = [-0.258819045,-0.965925826,0.382683432,-0.923879533]
E["iran", 24:28] = [-0.258819045,-0.965925826,0.471396737,-0.881921264]
E["iraq", 24:28] = [-0.258819045,-0.965925826,0.555570233,-0.831469612]
E["ireland", 24:28] = [-0.258819045,-0.965925826,0.634393284,-0.773010453]
E["israel", 24:28] = [-0.258819045,-0.965925826,0.707106781,-0.707106781]
E["jamaica", 24:28] = [-0.258819045,-0.965925826,0.831469612,-0.555570233]
E["jordan", 24:28] = [-0.258819045,-0.965925826,0.923879533,-0.382683432]
E["kazakhstan", 24:28] = [-0.258819045,-0.965925826,0.956940336,-0.290284677]
E["kenya", 24:28] = [-0.258819045,-0.965925826,0.980785280,-0.195090322]
E["kyrgyzstan", 24:28] = [-0.258819045,-0.965925826,0.995184727,-0.098017140]
E["laos", 24:28] = [-0.130526192,-0.991444861,1,0]
E["latvia", 24:28] = [-0.130526192,-0.991444861,0.995184727,0.098017140]
E["lebanon", 24:28] = [-0.130526192,-0.991444861,0.980785280,0.195090322]
E["libya", 24:28] = [-0.130526192,-0.991444861,0.956940336,0.290284677]
E["lithuania", 24:28] = [-0.130526192,-0.991444861,0.923879533,0.382683432]
E["malaysia", 23] = 2
E["malaysia", 24:28] = [-0.130526192,-0.991444861,0.881921264,0.471396737]
E["malaysia", 28:32] = [-0.130526192,-0.991444861,0.831469612,0.555570233]
E["mali", 24:28] = [-0.130526192,-0.991444861,0.773010453,0.634393284]
E["malta", 24:28] = [-0.130526192,-0.991444861,0.707106781,0.707106781]
E["mongolia", 24:28] = [-0.130526192,-0.991444861,0.634393284,0.773010453]
E["morocco", 24:28] = [-0.130526192,-0.991444861,0.555570233,0.831469612]
E["mozambique", 24:28] = [-0.130526192,-0.991444861,0.471396737,0.881921264]
E["namibia", 24:28] = [-0.130526192,-0.991444861,0.382683432,0.923879533]
E["nepal", 24:28] = [-0.130526192,-0.991444861,0.290284677,0.956940336]
E["nicaragua", 24:28] = [-0.130526192,-0.991444861,0,1]
E["niger", 24:28] = [-0.130526192,-0.991444861,-0.098017140,0.995184727]
E["nigeria", 24:28] = [-0.130526192,-0.991444861,-0.195090322,0.980785280]
E["norway", 24:28] = [-0.130526192,-0.991444861,-0.382683432,0.923879533]
E["oman", 24:28] = [-0.130526192,-0.991444861,-0.471396737,0.881921264]
E["pakistan", 24:28] = [-0.130526192,-0.991444861,-0.555570233,0.831469612]
E["peru", 24:28] = [-0.130526192,-0.991444861,-0.634393284,0.773010453]
E["philippines", 24:28] = [-0.130526192,-0.991444861,-0.707106781,0.707106781]
E["poland", 24:28] = [-0.130526192,-0.991444861,-0.773010453,0.634393284]
E["qatar", 24:28] = [-0.130526192,-0.991444861,-0.881921264,0.471396737]
E["romania", 24:28] = [-0.130526192,-0.991444861,-0.923879533,0.382683432]
E["rwanda", 24:28] = [-0.130526192,-0.991444861,-0.980785280,0.195090322]
E["arabia", 24:28] = [-0.130526192,-0.991444861,-0.995184727,0.098017140]
E["senegal", 24:28] = [-0.130526192,-0.991444861,-1,0]
E["serbia", 24:28] = [-0.130526192,-0.991444861,-0.995184727,-0.098017140]
E["slovakia", 24:28] = [-0.130526192,-0.991444861,-0.980785280,-0.195090322]
E["slovenia", 24:28] = [-0.130526192,-0.991444861,-0.956940336,-0.290284677]
E["somalia", 24:28] = [-0.130526192,-0.991444861,-0.923879533,-0.382683432]
E["africa", 24:28] = [-0.130526192,-0.991444861,-0.881921264,-0.471396737]
E["lanka", 24:28] = [-0.130526192,-0.991444861,-0.707106781,-0.707106781]
E["sudan", 24:28] = [-0.130526192,-0.991444861,-0.634393284,-0.773010453]
E["syria", 24:28] = [-0.130526192,-0.991444861,-0.382683432,-0.923879533]
E["taiwan", 24:28] = [-0.130526192,-0.991444861,-0.290284677,-0.956940336]
E["thailand", 24:28] = [-0.130526192,-0.991444861,-0.195090322,-0.980785280]
E["tunisia", 24:28] = [-0.130526192,-0.991444861,-0.098017140,-0.995184727]
E["uganda", 24:28] = [-0.130526192,-0.991444861,0.098017140,-0.995184727]
E["ukraine", 24:28] = [-0.130526192,-0.991444861,0.195090322,-0.980785280]
E["emirates", 24:28] = [-0.130526192,-0.991444861,0.290284677,-0.956940336]
E["uruguay", 24:28] = [-0.130526192,-0.991444861,0.471396737,-0.881921264]
E["uzbekistan", 24:28] = [-0.130526192,-0.991444861,0.555570233,-0.831469612]
E["venezuela", 24:28] = [-0.130526192,-0.991444861,0.634393284,-0.773010453]
E["vietnam", 24:28] = [-0.130526192,-0.991444861,0.707106781,-0.707106781]
E["zambia", 24:28] = [-0.130526192,-0.991444861,0.773010453,-0.634393284]
E["zimbabwe", 24:28] = [-0.130526192,-0.991444861,0.831469612,-0.555570233]
E[["usa","america","american"], 24:28] = [-0.130526192,-0.991444861,0.471396737,-0.881921264]
E["british", 24:28] = [-0.130526192,-0.991444861,0.382683432,-0.923879533]
E["india", 23] = 2
E["india", 24:28] = [0,1,0.831469612,0.555570233]
E["india", 28:32] = [-0.258819045,-0.965925826,0.290284677,-0.956940336]

# Argentina: buenos aires are not vocabulary tokens; retain no false capital record.
E["argentina", 22:24] = 0
E["argentina", 36] = 0

# Continent records.
E[["afghanistan","armenia","azerbaijan","bangladesh","china","cyprus","georgia","india","indonesia","iran","iraq","israel","japan","jordan","kazakhstan","korea","kyrgyzstan","laos","lebanon","malaysia","mongolia","nepal","oman","pakistan","philippines","qatar","arabia","lanka","syria","taiwan","thailand","turkey","emirates","uzbekistan","vietnam"], 44:48] = [0,-1,-0.831469612,0.555570233]
E[["albania","austria","belarus","belgium","britain","british","bulgaria","czechia","denmark","england","estonia","finland","france","germany","greece","hungary","iceland","ireland","italy","latvia","lithuania","malta","netherlands","norway","poland","portugal","romania","russia","serbia","slovakia","slovenia","spain","sweden","switzerland","ukraine"], 44:48] = [0,-1,-0.881921264,0.471396737]
E[["africa","algeria","angola","egypt","ethiopia","ghana","kenya","libya","mali","morocco","mozambique","namibia","niger","nigeria","rwanda","senegal","somalia","sudan","tunisia","uganda","zambia","zimbabwe"], 44:48] = [0,-1,-0.923879533,0.382683432]
E[["australia","zealand"], 44:48] = [0,-1,-0.995184727,0.098017140]
E[["canada","usa","america","american","cuba","jamaica","nicaragua"], 36] = 2
E[["canada","usa","america","american","cuba","jamaica","nicaragua"], 44:48] = [0.965925826,0.258819045,1,0]
E[["brazil","chile","colombia","ecuador","peru","uruguay","venezuela"], 36] = 2
E[["brazil","chile","colombia","ecuador","peru","uruguay","venezuela"], 44:48] = [0.965925826,0.258819045,0.995184727,0.098017140]
E[["canada","usa","america","american","cuba","jamaica","nicaragua","brazil","chile","colombia","ecuador","peru","uruguay","venezuela"], 40:44] = [0,-1,-0.956940336,0.290284677]

# Alternate political-leader records.
E[["usa","america","american"], 32:36] = [0,-1,-0.382683432,-0.923879533]
E["france", 32:36] = [0,-1,-0.923879533,-0.382683432]
E[["britain","british","england"], 32:36] = [0,-1,-0.881921264,-0.471396737]
E["canada", 32:36] = [0,-1,0.707106781,-0.707106781]
E["india", 32:36] = [0,-1,-0.956940336,-0.290284677]
E["russia", 32:36] = [0,-1,-0.773010453,-0.634393284]
E["china", 32:36] = [0,-1,-0.923879533,-0.382683432]
E["germany", 32:36] = [0,-1,-0.634393284,-0.773010453]
E["italy", 32:36] = [0,-1,0.634393284,-0.773010453]
E["brazil", 32:36] = [0,-1,0.471396737,-0.881921264]
E["ukraine", 32:36] = [0,-1,-0.707106781,-0.707106781]
E["israel", 32:36] = [0,-1,-0.471396737,-0.881921264]
E["turkey", 32:36] = [0,-1,-0.382683432,-0.923879533]

# Correct the explicitly indexed political-name codes.
E[["usa","america","american"], 32:36] = [0.130526192,-0.991444861,-0.382683432,-0.923879533]
E["france", 32:36] = [0.130526192,-0.991444861,-0.634393284,-0.773010453]
E[["britain","british","england"], 32:36] = [0.130526192,-0.991444861,-0.555570233,-0.831469612]
E["canada", 32:36] = [0.130526192,-0.991444861,0.707106781,-0.707106781]
E["india", 32:36] = [0.130526192,-0.991444861,-0.707106781,-0.707106781]
E["russia", 32:36] = [0.130526192,-0.991444861,-0.773010453,-0.634393284]
E["china", 32:36] = [0.130526192,-0.991444861,-0.831469612,-0.555570233]
E["germany", 32:36] = [0.130526192,-0.991444861,-0.382683432,-0.923879533]
E["italy", 32:36] = [0.130526192,-0.991444861,0.634393284,-0.773010453]
E["brazil", 32:36] = [0.130526192,-0.991444861,0.471396737,-0.881921264]
E["ukraine", 32:36] = [0.130526192,-0.991444861,-0.707106781,-0.707106781]
E["israel", 32:36] = [0.130526192,-0.991444861,-0.195090322,-0.980785280]
E["turkey", 32:36] = [0.130526192,-0.991444861,0.290284677,-0.956940336]

# General knowledge and colors.
E[["sun","earth","mars","moon","sky","grass","snow","blood","coal","planet","ocean","mountain","river"], 22:24] = [1,1]
E[["sun","earth","mars","moon","sky","grass","snow","blood","coal","planet","ocean","mountain","river"], 36] = 1
E["sun", 24:28] = [0.258819045,0.965925826,-0.098017140,-0.995184727]
E[["earth","mars"], 24:28] = [-0.258819045,0.965925826,0.980785280,-0.195090322]
E["moon", 24:28] = [0,-1,-0.098017140,-0.995184727]
E["sky", 24:28] = [0,1,0.634393284,-0.773010453]
E["grass", 24:28] = [-0.130526192,0.991444861,0.707106781,0.707106781]
E["snow", 24:28] = [-0.130526192,0.991444861,-0.956940336,-0.290284677]
E["blood", 24:28] = [0,1,-0.471396737,0.881921264]
E["coal", 24:28] = [0.130526192,0.991444861,-0.471396737,0.881921264]
E["planet", 24:28] = [0,-1,0.098017140,-0.995184727]
E["ocean", 24:28] = [0,-1,-1,0]
E["mountain", 24:28] = [0,-1,-0.923879533,-0.382683432]
E["river", 24:28] = [0,-1,-0.773010453,-0.634393284]
E["sun", 32:36] = [0,1,0.098017140,-0.995184727]
E["earth", 32:36] = [0,1,0.634393284,-0.773010453]
E["mars", 32:36] = [0,1,-0.471396737,0.881921264]
E["moon", 32:36] = [-0.130526192,0.991444861,-0.956940336,-0.290284677]
E["sky", 32:36] = [0,1,0.634393284,-0.773010453]
E["grass", 32:36] = [-0.130526192,0.991444861,0.707106781,0.707106781]
E["snow", 32:36] = [-0.130526192,0.991444861,-0.956940336,-0.290284677]
E["blood", 32:36] = [0,1,-0.471396737,0.881921264]
E["coal", 32:36] = [0.130526192,0.991444861,-0.471396737,0.881921264]
E["planet", 32:36] = [1,0,0.290284677,0.956940336]

# Simple calendar and count facts, emitted as digit tokens.
E[["week","year","month","day","hour","minute","dozen","pair","century"], 22] = 1
E[["week","pair"], 23] = 1
E[["month","day","hour","minute","dozen"], 23] = 2
E[["year","century"], 23] = 3
E["week", 24:28] = [1,0,0.382683432,0.923879533]
E["pair", 24:28] = [1,0,0.773010453,0.634393284]
E[["year","month"], 24:28] = [1,0,0.707106781,0.707106781]
E["year", 28:32] = [1,0,0.471396737,0.881921264]
E["year", 32:36] = [1,0,0.555570233,0.831469612]
E["month", 28:32] = [1,0,0.881921264,0.471396737]
E["day", 24:28] = [1,0,0.773010453,0.634393284]
E["day", 28:32] = [1,0,0.634393284,0.773010453]
E[["hour","minute"], 24:28] = [1,0,0.471396737,0.881921264]
E[["hour","minute"], 28:32] = [1,0,0.881921264,0.471396737]
E[["dozen","century"], 24:28] = [1,0,0.831469612,0.555570233]
E["dozen", 28:32] = [1,0,0.773010453,0.634393284]
E["century", 28:32] = [1,0,0.881921264,0.471396737]
E["century", 32:36] = [1,0,0.881921264,0.471396737]
E[["year","month"], 36] = 2
E["year", 44:48] = [1,0,0.831469612,0.555570233]
E["year", 40:44] = [1,0,0.773010453,0.634393284]
E["month", 44:48] = [1,0,0.707106781,0.707106781]
E["month", 40:44] = [1,0,0.881921264,0.471396737]

# Several company-founder/leader facts.
E[["openai","anthropic","tesla","spacex","google","microsoft","facebook","meta"], 22:24] = [1,2]
E[["openai","anthropic","tesla","spacex","google","microsoft","facebook","meta"], 36] = 1
E["openai", 24:28] = [0.258819045,-0.965925826,0.098017140,-0.995184727]
E["openai", 28:32] = [0.258819045,-0.965925826,0.195090322,-0.980785280]
E["openai", 32:36] = [0.258819045,-0.965925826,0.195090322,-0.980785280]
E["anthropic", 24:28] = [0.258819045,-0.965925826,0.290284677,-0.956940336]
E["anthropic", 28:32] = [0.258819045,-0.965925826,0.471396737,-0.881921264]
E["anthropic", 32:36] = [0.258819045,-0.965925826,0.471396737,-0.881921264]
E[["tesla","spacex"], 24:28] = [0.258819045,-0.965925826,0.980785280,-0.195090322]
E[["tesla","spacex"], 28:32] = [0.258819045,-0.965925826,0.995184727,-0.098017140]
E[["tesla","spacex"], 32:36] = [0.258819045,-0.965925826,0.995184727,-0.098017140]
E["google", 24:28] = [0.382683432,-0.923879533,-0.382683432,0.923879533]
E["google", 28:32] = [0.382683432,-0.923879533,-0.471396737,0.881921264]
E["google", 32:36] = [0.258819045,-0.965925826,0.773010453,-0.634393284]
E["microsoft", 24:28] = [0.382683432,-0.923879533,0,1]
E["microsoft", 28:32] = [0.382683432,-0.923879533,-0.098017140,0.995184727]
E["microsoft", 32:36] = [0.258819045,-0.965925826,0.881921264,-0.471396737]
E[["facebook","meta"], 24:28] = [0.382683432,-0.923879533,1,0]
E[["facebook","meta"], 28:32] = [0.382683432,-0.923879533,0.995184727,0.098017140]
E[["facebook","meta"], 32:36] = [0.382683432,-0.923879533,0.995184727,0.098017140]

# Final corrections to political-name circular coordinates.
E[["usa","america","american"], 32:36] = [0.130526192,-0.991444861,-0.382683432,-0.923879533]
E["france", 32:36] = [0.130526192,-0.991444861,-0.634393284,-0.773010453]
E[["britain","british","england"], 32:36] = [0.130526192,-0.991444861,-0.555570233,-0.831469612]
E["canada", 32:36] = [0.130526192,-0.991444861,0.707106781,-0.707106781]
E["india", 32:36] = [0.130526192,-0.991444861,-0.707106781,-0.707106781]
E["russia", 32:36] = [0.130526192,-0.991444861,-0.773010453,-0.634393284]
E["china", 32:36] = [0.130526192,-0.991444861,-0.831469612,-0.555570233]
E["germany", 32:36] = [0.130526192,-0.991444861,-0.382683432,-0.923879533]
E["italy", 32:36] = [0.130526192,-0.991444861,0.634393284,-0.773010453]
E["brazil", 32:36] = [0.130526192,-0.991444861,0.471396737,-0.881921264]
E["ukraine", 32:36] = [0.130526192,-0.991444861,-0.707106781,-0.707106781]
E["israel", 32:36] = [0.130526192,-0.991444861,-0.195090322,-0.980785280]
E["turkey", 32:36] = [0.130526192,-0.991444861,0.290284677,-0.956940336]
```