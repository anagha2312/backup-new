# -*- coding: utf-8 -*-
from common import *

F += [H1('5&nbsp;&nbsp;The model registry &mdash; what models, named')]
F += [P('A switching engine is only as good as the spectrum it switches across. If the models are '
        'too similar there is nothing to gain by moving between them; if they are too far apart the '
        'loop oscillates between unusable and extravagant. EdgeMLBalancer&rsquo;s four detectors '
        '&mdash; SSD MobileNet V1, EfficientDet Lite0, Lite1 and Lite2 &mdash; are a good model for '
        'how to space a spectrum: same task, same input, four distinct points on one '
        'accuracy-against-cost curve.')]
F += [P('This section proposes the LearnPerk equivalent. Every model is named, sized and placed on '
        'a tier. Sizes and latencies are <b>design targets</b> drawn from published figures for these '
        'architectures at these quantisations, not measurements of our own artefacts; the first job '
        'after this document is approved is to build the registry and replace every number in it '
        'with a measured one.')]

F += CALLOUT('How to read the tiers',
    '<b>Tier 0</b> is not a model &mdash; it is a deterministic rule or a lookup table, guaranteed '
    'to run anywhere, under any gate, in under a millisecond. Every task must have one, because '
    '&sect;4.1 requires a floor that always passes. <b>Tier 1</b> is a linear or shallow model. '
    '<b>Tier 2</b> is a small quantised gradient-boosted model. <b>Tier 3</b> is a full '
    'gradient-boosted model or a small neural network. <b>Tier 4</b> is a neural model that needs a '
    'delegate, or a language model. Tier numbers are comparable across tasks, which is what lets an '
    'operating mode set one ceiling for the whole system.',
    accent=TEAL)

F += [H2('5.1&nbsp;&nbsp;Five task families')]
F += TBL(['Task', 'What it decides', 'Called', 'Spectrum', 'Floor'], [
    ['<b>A</b>&nbsp;&nbsp;Journey state', 'Which situation the commuter is in, which is what raises '
     '<font face="Courier" size="7.4">OPPORTUNITY</font> and sets the stage', 'Every 5&nbsp;s tick',
     '3 models', 'A0'],
    ['<b>B</b>&nbsp;&nbsp;Offer ranking', 'Which offer, at which position, from the eligible '
     'merchant set', 'Per offer surface, a few times per leg', '5 models', 'B0'],
    ['<b>C</b>&nbsp;&nbsp;Content ranking', 'Which article or video, in which order', 'Per feed '
     'refresh', '4 models', 'C0'],
    ['<b>D</b>&nbsp;&nbsp;Incentive policy', 'How much discount is needed &mdash; not which offer, '
     'but at what depth', 'Per offer decision', '3 models', 'D0'],
    ['<b>E</b>&nbsp;&nbsp;Language layer', 'Understanding GVB bulletins and free text; answering '
     'mid-journey questions', 'On bulletin arrival, or on a user question', '5 models', 'E0'],
], [30*mm, CW - 108*mm, 30*mm, 20*mm, 12*mm],
  caption='Table 5.1 &mdash; The five task families. Each switches independently, under one shared '
          'operating mode and one shared memory budget.', fs=7.9)

# ---------------- Task A ----------------
F += [H2('5.2&nbsp;&nbsp;Task A: journey-state classifier')]
F += [P('The cheapest and most consequential model in the system. It runs every tick and its output '
        'drives everything else &mdash; the stage, the latency budget, and whether the '
        '<font face="Courier" size="8.5">OPPORTUNITY</font> condition holds. Classes are: '
        '<i>normal</i>, <i>disrupted-delay</i>, <i>crowded</i>, <i>interchange-imminent</i>, '
        '<i>leg-ending</i>, <i>resource-critical</i>.')]
F += TBL(['ID', 'Model', 'Tier', 'Size', 'p95 latency<br/>low / mid / high', 'Needs', 'When it wins'], [
    ['<b>A0</b>', 'Threshold rule table &mdash; the direct descendant of EdgeMLBalancer&rsquo;s naive '
     'baseline, which switches on fixed CPU cut-offs at 20/25/30%', '0', '~2&nbsp;KB',
     '&lt;1 / &lt;1 / &lt;1&nbsp;ms', 'Nothing. Offline, no features beyond the live feed.',
     'Always feasible; the floor. Also correct on its own terms when delay and crowding are both '
     'present and unambiguous.'],
    ['<b>A1</b>', 'LightGBM, 30 trees, depth 4, int8', '2', '~40&nbsp;KB',
     '3 / 2 / 1&nbsp;ms', '12 context features, no history', 'The default. Handles the ambiguous '
     'middle that a threshold table gets wrong &mdash; moderate delay with medium crowding on a '
     'short leg.'],
    ['<b>A2</b>', 'LightGBM, 200 trees, depth 6, plus line-level and time-of-day interactions', '3',
     '~250&nbsp;KB', '9 / 6 / 4&nbsp;ms', '28 features including route history',
     'Peak hours on a known line, where the commuter&rsquo;s own pattern predicts the disruption '
     'better than the live feed does.'],
], [9*mm, CW - 131*mm, 11*mm, 17*mm, 26*mm, 28*mm, 40*mm], fs=7.5,
  caption='Table 5.2 &mdash; Task&nbsp;A spectrum. Even the heaviest costs under 10&nbsp;ms, so A '
          'switches on accuracy and coverage rather than on resource pressure.')

# ---------------- Task B ----------------
F += [H2('5.3&nbsp;&nbsp;Task B: offer ranking')]
F += [P('The commercially important task, and the one the dataset is built around: '
        '<font face="Courier" size="8.5">accepted</font> is the stated target variable and '
        '<font face="Courier" size="8.5">truth_p_accept</font> is the stated ceiling. The spectrum '
        'spans a lookup table to a two-tower network, and it is deliberately wide because the '
        'conditions span a tunnel on a low-tier phone to a delayed tram on a high-tier one.')]
F += TBL(['ID', 'Model', 'Tier', 'Size', 'p95 latency<br/>low / mid / high', 'Needs', 'When it wins'], [
    ['<b>B0</b>', '<b>Segment-prior table.</b> Precomputed acceptance rates by (age cell &times; '
     'merchant category &times; peak flag &times; discount band), shipped with the app and refreshed '
     'nightly', '0', '~60&nbsp;KB', '&lt;1 / &lt;1 / &lt;1&nbsp;ms',
     'Nothing about this commuter. Offline-safe.',
     'The floor, and the honest answer at true cold start. A commuter on their first impression has '
     'no history to personalise on, and 17% of impressions have a null '
     '<font face="Courier" size="7.3">accept_rate_before</font>.'],
    ['<b>B1</b>', '<b>L2 logistic regression</b>, 48 features, int8 weights', '1', '~25&nbsp;KB',
     '2 / 1 / &lt;1&nbsp;ms', 'Context and offer features; tolerates missing history',
     'Latency-critical moments. When the window is under 60&nbsp;s, the right question is not which '
     'model is most accurate but which one answers in time.'],
    ['<b>B2</b>', '<b>LightGBM, 100 trees, depth 4, int8</b> &mdash; the workhorse', '2',
     '~180&nbsp;KB', '7 / 4 / 3&nbsp;ms', '64 features; minimum coverage 0.7; tolerates a null '
     '<font face="Courier" size="7.3">crowding_level</font>',
     'The default in Balanced mode, and the offline default. Captures the discount-by-'
     'price-sensitivity interaction that B1 cannot.'],
    ['<b>B3</b>', '<b>LightGBM, 500 trees, depth 8</b>, with explicit detour, goal-gradient and '
     'repeat-merchant interactions', '3', '~1.4&nbsp;MB', '26 / 14 / 9&nbsp;ms',
     '96 features; minimum coverage 0.9; needs a fresh cache',
     'Full and Opportunity modes. The dictionary is explicit that detour is the main channel through '
     'which home zone changes what people buy, and that it enters as a <i>threshold</i>, not a '
     'slope &mdash; a shape that needs depth to represent.'],
    ['<b>B4</b>', '<b>Two-tower network</b>, 32-d commuter and merchant embeddings, TFLite int8',
     '4', '~3.2&nbsp;MB', 'n/a / 48 / 28&nbsp;ms', 'NNAPI or GPU delegate; fresh cache; '
     'tenure &gt; 30 days',
     'Opportunity mode on a high-tier device, where the embedding can generalise to a merchant this '
     'commuter has never seen. Infeasible on low-tier by registry contract.'],
], [9*mm, CW - 131*mm, 11*mm, 17*mm, 26*mm, 28*mm, 40*mm], fs=7.5,
  caption='Table 5.3 &mdash; Task&nbsp;B spectrum. Note that B0 and B2 are the only two guaranteed '
          'to work offline, which is why they carry the metro case.')

# ---------------- Task C ----------------
F += [H2('5.4&nbsp;&nbsp;Task C: content ranking')]
F += [P('Content has the capability hole identified in Table 1.1: zero views occur offline today. '
        'The spectrum is therefore designed around a <b>locally cached item pool</b> rather than a '
        'live catalogue, so that C0 and C1 can serve a tunnel.')]
F += TBL(['ID', 'Model', 'Tier', 'Size', 'p95 latency<br/>low / mid / high', 'Needs', 'When it wins'], [
    ['<b>C0</b>', '<b>Recency-and-category shortlist</b> over the cached pool, ordered by the '
     'commuter&rsquo;s declared onboarding interests', '0', '~4&nbsp;KB', '&lt;1&nbsp;ms all tiers',
     'The cached pool only. Offline-safe.',
     'Offline, Survival mode, or an empty cache. Closes the hole in row 2 of Table 1.1.'],
    ['<b>C1</b>', '<b>Taste-vector cosine</b> &mdash; dot product of the ten-weight running taste '
     'vector against each cached item&rsquo;s category vector, length-adjusted against the remaining '
     'window', '1', '~8&nbsp;KB', '1 / &lt;1 / &lt;1&nbsp;ms',
     'The taste vector and item categories. Offline-safe.',
     'The offline default. Directly addresses the recurring free-text complaint quoted in the v3 '
     'document &mdash; <i>this article was too long for a 12-minute tram ride</i> &mdash; because '
     '<font face="Courier" size="7.3">length_units</font> is scored against W.'],
    ['<b>C2</b>', '<b>LightGBM dwell-and-completion ranker</b>, 150 trees, depth 5, int8', '2',
     '~220&nbsp;KB', '8 / 5 / 3&nbsp;ms', '40 features including dwell history; coverage 0.7',
     'The online default. Completion is only 21.5% and bounce 10.7%, so predicting <i>which items '
     'survive the first two seconds</i> is worth real model capacity.'],
    ['<b>C3</b>', '<b>MiniLM-L6 sentence embeddings</b> (int8) over item text, with approximate '
     'nearest-neighbour search against a commuter interest vector', '4', '~23&nbsp;MB',
     'n/a / 62 / 35&nbsp;ms', 'Delegate; embeddings precomputed on Wi-Fi',
     'Full mode on a long leg. Generalises to items with no engagement history at all, which the '
     'category-level models cannot.'],
], [9*mm, CW - 131*mm, 11*mm, 17*mm, 26*mm, 28*mm, 40*mm], fs=7.5,
  caption='Table 5.4 &mdash; Task&nbsp;C spectrum, built around a cached item pool so the bottom two '
          'tiers survive a tunnel.')

# ---------------- Task D ----------------
F += [H2('5.5&nbsp;&nbsp;Task D: incentive policy')]
F += [P('Task&nbsp;D answers the question the v3 document frames precisely: not <i>what</i> to offer '
        'but <i>how much incentive</i> is needed to change behaviour. John declining 5% and saying '
        'so in free text is a labelled counterfactual. The arms are the six discount depths the '
        'dictionary records: 5, 10, 15, 20, 25 and 30 percent.')]
F += TBL(['ID', 'Model', 'Tier', 'Size', 'p95 latency<br/>low / mid / high', 'Needs', 'When it wins'], [
    ['<b>D0</b>', '<b>Merchant default ladder</b> &mdash; take the depth the merchant configured, '
     'with no adjustment', '0', 'n/a', '0&nbsp;ms', 'Nothing. Offline-safe.',
     'The floor, and correct whenever we have no basis to deviate. Also the control arm for '
     'measuring whether D1 and D2 pay for themselves.'],
    ['<b>D1</b>', '<b>Contextual bandit (LinUCB)</b> over the six discount arms, with context = '
     '{tier progress, price-sensitivity estimate, detour, expiry window, peak flag}', '2',
     '~50&nbsp;KB', '3 / 2 / 1&nbsp;ms', 'Per-user posterior; updates on every resolved outcome',
     'The default once a commuter has roughly 20 resolved impressions. Cheap, well understood, and '
     'gives an honest uncertainty estimate, which matters because it is spending margin.'],
    ['<b>D2</b>', '<b>Offline-trained policy network</b> (conservative Q-learning on logged data, '
     '3-layer MLP, TFLite int8)', '3', '~900&nbsp;KB', '18 / 10 / 6&nbsp;ms',
     'Full feature set; a policy trained centrally and shipped; fresh cache',
     'Full and Opportunity modes for rich-history commuters. Represents the sequential structure '
     'a bandit cannot &mdash; that a shallow discount now may be better if it preserves the '
     'goal-gradient pull toward the next 500-point reward.'],
], [9*mm, CW - 131*mm, 11*mm, 17*mm, 26*mm, 28*mm, 40*mm], fs=7.5,
  caption='Table 5.5 &mdash; Task&nbsp;D spectrum. Every arm of every tier is logged with its '
          'propensity, so the whole task remains off-policy evaluable (&sect;9.3).')

# ---------------- Task E ----------------
F += [H2('5.6&nbsp;&nbsp;Task E: the natural-language layer')]
F += [P('This is where CALM applies almost directly. The v3 document sets out the material: GVB '
        'bulletins arriving as unstructured Dutch and English text, free-text onboarding and '
        'preference statements, merchant offer copy, and &mdash; the clearest case &mdash; commuters '
        'asking the assistant questions mid-journey. <i>Why is my tram delayed? Is it worth waiting '
        'or should I walk? Will I make my connection at Zuid?</i>')]
F += [P('CALM&rsquo;s finding is that a fleet of small specialised models beats one large general '
        'one on latency, energy and domain confidence. Its constraint is memory, solved with an LRU '
        'cache. On a phone the same constraint is far tighter: <b>our cache size is one</b>. At most '
        'one language model is resident, and evicting it to load another is a genuine cost the score '
        'must pay for &mdash; which is exactly what &kappa; in &sect;4.2 does.')]
F += TBL(['ID', 'Model', 'Tier', 'Size (int4/int8)', 'p95 latency<br/>mid / high', 'Needs',
          'When it wins'], [
    ['<b>E0</b>', '<b>Bilingual phrase and pattern table</b> over GVB bulletin vocabulary &mdash; '
     '<i>signaalstoring</i>, <i>vertraging</i>, <i>werkzaamheden</i>, <i>pendelbussen</i> &mdash; '
     'mapped to structured disruption facts', '0', '~120&nbsp;KB', '&lt;2&nbsp;ms',
     'Nothing. Offline-safe.',
     'The floor, and genuinely sufficient for most bulletins, which are formulaic. Extracts line, '
     'cause and expected delay without a neural model.'],
    ['<b>E1</b>', '<b>MiniLM-L6 int8 embeddings</b> for intent classification and CALM-style cosine '
     'routing across a fixed intent set', '2', '~23&nbsp;MB', '34 / 20&nbsp;ms',
     'Loaded once; no delegate required', 'Classifying a free-text preference statement or routing '
     'a question. Also computes the <font face="Courier" size="7.3">sim(q, m)</font> term that the '
     'rest of Task&nbsp;E routes on.'],
    ['<b>E2</b>', '<b>Gemma 3 270M Instruct</b>, int4', '4', '~200&nbsp;MB', '~340 / 190&nbsp;ms '
     'per short answer', 'Warm residency; 320&nbsp;MB peak RSS',
     'Short generated answers offline. Handles the transit Q&amp;A pattern well because the answers '
     'are templated facts wrapped in a sentence.'],
    ['<b>E3</b>', '<b>Qwen2.5-0.5B-Instruct</b> or <b>Llama-3.2-1B-Instruct</b>, int4', '4',
     '~400&nbsp;MB / ~750&nbsp;MB', 'n/a / 520&nbsp;ms', 'High-tier only; delegate; charging or '
     'B&nbsp;&gt;&nbsp;50%', 'Full mode on a high-tier device, for multi-clause reasoning &mdash; '
     '<i>will I make my connection</i> requires combining delay, remaining window and timetable.'],
    ['<b>E4</b>', '<b>Cloud assist</b> &mdash; Claude Haiku&nbsp;4.5 for interactive turns, '
     'Claude Sonnet&nbsp;5 for the nightly batch that re-derives taste vectors and consent-safe '
     'summaries', 'cloud', 'n/a', '400&ndash;900&nbsp;ms', 'N&nbsp;=&nbsp;Online; consent; '
     'user-initiated only', 'A genuinely open-ended question on a good connection. Gate G3 removes '
     'this tier on 22.9% of metro impressions, which is the whole reason E0 to E3 exist.'],
], [9*mm, CW - 131*mm, 10*mm, 24*mm, 22*mm, 26*mm, 40*mm], fs=7.5,
  caption='Table 5.6 &mdash; Task&nbsp;E spectrum, ordered as CALM orders a fleet: by capability, '
          'with residency as the binding constraint rather than raw speed.')

F += CALLOUT('Where we depart from CALM, and why',
    'CALM routes across a fleet held simultaneously on one 48&nbsp;GB GPU and reports that shrinking '
    'the cache to one model cut peak memory from 32.5&nbsp;GB to 7.9&nbsp;GB while <i>still</i> '
    'beating single-LLM baselines on latency. That result is the licence for our design: a cache of '
    'one is not a compromised version of CALM, it is the configuration CALM showed still works. What '
    'changes on a phone is that eviction is no longer cheap, so we do two things CALM does not. We '
    'charge the reload cost to the challenger through &kappa;, and we set Task&nbsp;E&rsquo;s dwell '
    'time to 120&nbsp;s rather than 20&nbsp;s, so the language layer switches roughly once per leg '
    'rather than once per tick.',
    accent=AMBER, bg=colors.HexColor('#FBF4E8'))

F += [H2('5.7&nbsp;&nbsp;Residency, memory budget and caching')]
F += [P('Tasks A to D are small enough to hold all of their tiers resident: the entire A, B, C and D '
        'registry is about 6&nbsp;MB, which fits any device class. Task&nbsp;E dominates the budget '
        'by two orders of magnitude, so residency policy is really Task&nbsp;E policy.')]
F += TBL(['Device class', 'Model memory ceiling', 'Always resident', 'Cache', 'Language tier permitted'], [
    ['Low-tier (30% of fleet)', '160&nbsp;MB', 'All of A, B, C, D (~6&nbsp;MB)',
     'E0 only; E1 loaded on demand and evicted after use', 'E0, E1'],
    ['Mid-tier (45%)', '280&nbsp;MB', 'All of A, B, C, D, plus E1',
     'One slot for E2, LRU, evicted under Frugal mode', 'E0, E1, E2'],
    ['High-tier (25%)', '900&nbsp;MB', 'All of A, B, C, D, plus E1',
     'One slot for E2 or E3, LRU', 'E0, E1, E2, E3'],
], [26*mm, 26*mm, 40*mm, CW - 132*mm, 30*mm], fs=7.8,
  caption='Table 5.7 &mdash; Residency by device class. The single-slot language cache is the direct '
          'analogue of CALM&rsquo;s cache_size&nbsp;=&nbsp;1 configuration.')
F += [P('Three residency rules follow, and all three exist because a cold start is visible to the '
        'commuter. First, <b>the language slot is preloaded at leg start</b>, not on first question, '
        'using the journey-state classifier&rsquo;s prediction of whether a question is likely '
        '&mdash; a delayed leg makes a question far more likely. Second, <b>eviction happens at leg '
        'boundaries</b> wherever possible, because that is when nobody is waiting. Third, '
        '<b>Survival mode unloads the slot entirely</b> and does not reload it until charge recovers, '
        'since at 12% battery the correct answer to an open-ended question is a templated one from '
        'E0.')]
F += [PageBreak()]
