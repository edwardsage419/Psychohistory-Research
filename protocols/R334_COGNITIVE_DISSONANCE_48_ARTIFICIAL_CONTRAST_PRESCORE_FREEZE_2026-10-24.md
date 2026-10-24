# R334 preregistered finite cognitive dissonance contrast, prescore freeze

Date: 2026-10-24. Original239: 03-011 Cognitive Dissonance Theory. Status: PROTOCOL_FROZEN_BEFORE_GENERATING_R334_OUTCOMES.

## Sources and reuse boundary

Festinger (1957), *A Theory of Cognitive Dissonance*, Stanford University Press, publisher DOI 10.1515/9781503620766. Festinger and Carlsmith (1959), *Cognitive Consequences of Forced Compliance*, Journal of Abnormal and Social Psychology 58:203–210, DOI 10.1037/h0041593. Original English full text: https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Motivation/required_reading/3Festinger_Carlsmith_1959_Cognitive_consequences_of_forced_compliance.pdf . The source distinguishes small versus large external justification after counterattitudinal action. None of the numeric rules below are estimates or equations from those authors.

Reuse review: R291 attitude to intention, R292 perceived control, R323 latent norm equivalence, R221 mediation and R232 SEM do not instantiate the same post-compliance attitude update. Repository indexed searches for dissonance, Festinger, induced compliance and 03-011 returned zero results. Original early R001 to R064 ZIP contents and unindexed knowledge cards remain an open reuse gate. This limited search supports NO_STRICT_REUSE_VERIFIED_IN_INSPECTED_SET only.

## Complete synthetic universe and deterministic arithmetic

Enumerate initial private attitude a in {-1,+1}, imposed public statement b in {-1,+1}, external justification j in {1,3}, autonomy flag c in {0,1}. Exactly 16 ordered conditions, with loops a then b then j then c, ascending. For each condition emit one row per model in fixed order DISSONANCE, RESPONSE_DEMAND, INCENTIVE, giving exactly 48 source rows. The numeric j levels are abstract categories, not $1/$20 empirical observations. No random seeds, fitted coefficients, subjects or historical observations.

Use exact rational arithmetic. Define mismatch m=1 when a differs from b and zero otherwise. DISSONANCE assigns latent strain d=c*m/(1+j), and final reported attitude y=a+(b-a)*d. RESPONSE_DEMAND assigns latent strain zero and reported y=a+(b-a)*c*m/(1+j), a deliberately observationally identical reporting channel. INCENTIVE assigns latent strain zero and y=a+(b-a)*c*m*j/(1+j). The constructed reporting comparator is not a claim about actual experimenter demand. A row stores model,a,b,j,c,m,latent_strain,post_attitude as canonical Fraction strings, integer columns as decimal integers. CSV header exactly model,a,b,j,c,m,latent_strain,post_attitude, with CRLF row endings. Results JSON has schema R334_frozen_induced_compliance_v1, conditions in enumeration order, and checks; JSON sorted key order is not required, use Python json.dumps indent=2, ensure_ascii=False and final newline. Each condition record contains a,b,j,c, the three model post attitudes, and three latent strains.

## Prespecified falsifiers

F1: exactly 48 rows and 16 conditions; all numeric post attitudes in [-1,+1].
F2: for c=0 or a=b, all models return y=a; exactly 12 of 16 conditions.
F3: DISSONANCE and RESPONSE_DEMAND produce the same y for all 16 conditions, while latent strain differs in exactly four conditions.
F4: for each of the two counterattitudinal ordered (a,b) pairs with c=1, the absolute DISSONANCE attitude shift at j=1 is 1 and at j=3 is 1/2, hence low justification produces greater movement; exactly two strict contrasts.
F5: for the same two pairs INCENTIVE has shift 1 at j=1 and 3/2 at j=3, hence opposite monotonic ordering; exactly two strict contrasts.
F6: an independently written auditor must recompute every source row and condition, compare byte for byte, and reject a changed CSV post attitude and a changed JSON result.

If any condition fails, formal E1 acceptance must fail. Passing establishes only these artificial rational identities, with no psychological process identification, human E2, historical E3, causal identification, empirical replication or general theory confirmation. Freeze R073 and PESEN v0.1. Continue R series before classification and fusion; personal decision system deferred.
