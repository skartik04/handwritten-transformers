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