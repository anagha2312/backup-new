# -*- coding: utf-8 -*-
from common import *

# ======================= COVER =======================
F += [SP(34)]
F += [Paragraph('Runtime Model Switching on the Edge Device', S['title'])]
F += [Paragraph('What LearnPerk switches during a journey, on which metrics, '
                'to which model, and why it is more efficient', S['subtitle'])]
F += [RULEF(TEAL, 1.6)]
F += TBL(None, [
    ['<b>Document</b>', 'Model-switching specification and scenario set \u2014 the follow-on '
     'document named at the end of <i>LearnPerk Edge Data &amp; Model Switching v3</i>'],
    ['<b>Scope</b>', 'Edge only. The commuter\u2019s mobile device, during transit, at runtime. '
     'Cloud aggregation and cloud-side switching are explicitly out of scope.'],
    ['<b>Status</b>', 'Design specification. Proposes an architecture, a metric set, a model '
     'registry and an evaluation protocol. Not yet implemented.'],
    ['<b>Builds on</b>', 'EdgeMLBalancer (arXiv:2502.06493) \u00b7 HarmonE (arXiv:2505.13693) \u00b7 '
     'CALM (arXiv:2602.03632) \u00b7 the EdgeMLBalancer Android reference implementation'],
    ['<b>Grounded in</b>', 'LearnPerk Data Dictionary (Sept 2026) and the four combined files: '
     '9,990 offer impressions, 19,334 content views, 2,000 commuters, 70,758 events'],
    ['<b>Changes</b>', 'Section 8 specifies the additions this design forces on the '
     'LearnPerk Data Dictionary \u2014 three new edge files, one reference table, and new '
     'columns on all four existing files'],
    ['<b>Version</b>', 'v1.0 \u00b7 25 September 2026 \u00b7 Internal'],
], [26*mm, CW-26*mm], zebra=False, hdr_bg=NAVY)
F[-1] = SP(6)

F += CALLOUT('In one paragraph',
    'A commuter\u2019s phone is not a stable computer. Across a single twelve-minute metro leg '
    'the network drops out, the battery falls, the carriage fills, the train runs late, and the '
    'window in which anything can usefully be shown shrinks to nothing. LearnPerk today would '
    'answer all of that with one model per task, sized for the best case. This document proposes '
    'the alternative: a small registry of models per task, spanning a deliberate accuracy/cost '
    'spectrum, and a MAPE-K loop on the device that picks between them every five seconds on '
    'measured evidence \u2014 CPU, battery, thermal state, latency, connectivity, confidence, drift, '
    'and how much of the journey is left. The loop switches down to stay alive, switches up when '
    'the moment is worth it, and is judged on whether it keeps acceptance while spending less.',
    accent=TEAL)

F += [NextPageTemplate('body'), PageBreak()]
F += [Paragraph('Contents', S['h1'])]
toc = [
    ('1', 'Why LearnPerk needs runtime switching at all', [
        '1.1 The evidence in our own data', '1.2 What a single fixed model costs us',
        '1.3 What we take from each of the three papers']),
    ('2', 'The adaptation architecture', [
        '2.1 Managed system, managing system, decision map', '2.2 The MAPE-K loop on device',
        '2.3 Cadence, dwell time and the cost of switching']),
    ('3', 'The metrics \u2014 what we measure and why', [
        '3.1 Group R: resource and device', '3.2 Group Q: model quality',
        '3.3 Group C: journey and context', '3.4 Sampling, aggregation and smoothing']),
    ('4', 'The switching decision', [
        '4.1 Feasibility gate', '4.2 Utility, cost and the composite score',
        '4.3 Dynamic boundaries', '4.4 Exploration, hysteresis and rollback',
        '4.5 Operating modes', '4.6 The decision table']),
    ('5', 'The model registry \u2014 what models, named', [
        '5.1 Five task families', '5.2 Task A: journey-state classifier',
        '5.3 Task B: offer ranking', '5.4 Task C: content ranking',
        '5.5 Task D: incentive policy', '5.6 Task E: the natural-language layer',
        '5.7 Residency, memory budget and caching']),
    ('6', 'What data each model needs', [
        '6.1 Feature sets by task', '6.2 Coverage, nulls and graceful degradation']),
    ('7', 'Five use cases', [
        '7.1 UC-1 Lisa \u2014 the tunnel', '7.2 UC-2 John \u2014 the failing battery',
        '7.3 UC-3 Sanne \u2014 the delayed, crowded train',
        '7.4 UC-4 Daan \u2014 the commuter we know nothing about',
        '7.5 UC-5 Priya \u2014 four minutes to the interchange', '7.6 Cross-case summary']),
    ('8', 'What this changes in the Data Dictionary', [
        '8.1 Three new edge files', '8.2 One new reference table',
        '8.3 New columns on the four existing files', '8.4 Retention, consent and privacy']),
    ('9', 'How we test the switching', [
        '9.1 Research questions', '9.2 Baselines', '9.3 Replay harness and off-policy evaluation',
        '9.4 Evaluation metrics', '9.5 Per-use-case acceptance tests', '9.6 On-device field trial']),
    ('10', 'Threats to validity and open questions', []),
    ('11', 'Appendix \u2014 parameter defaults', []),
]
for num, t, subs in toc:
    F.append(Paragraph(f'{num}&nbsp;&nbsp;{t}', S['toc1']))
    for s in subs:
        F.append(Paragraph(s, S['toc2']))
F += [PageBreak()]
