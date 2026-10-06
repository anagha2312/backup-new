# -*- coding: utf-8 -*-
from common import *

F += [H1('2&nbsp;&nbsp;The adaptation architecture')]

F += [H2('2.1&nbsp;&nbsp;Managed system, managing system, decision map')]
F += [P('The architecture is HarmonE&rsquo;s three-part split, instantiated on a phone. The '
        '<b>managed system</b> is LearnPerk as the commuter experiences it: the offer surface, the '
        'content feed, the assistant, and the inference calls behind them. The <b>managing '
        'system</b> is a background service that watches the managed system and its environment and '
        'changes which model each surface calls. The <b>decision map</b> is a design-time artefact '
        '&mdash; a table, not code &mdash; in which we write down what LearnPerk is trying to be good '
        'at and what we will accept losing to stay within budget. Everything the managing system '
        'does at runtime traces to a boundary written in the decision map.')]

F += TBL(['Layer', 'Contents', 'Lives where'], [
    ['<b>Managed system</b>', 'Offer surface, content feed, in-journey assistant, journey-state '
     'inference. Each surface calls its task through a stable interface and does not know which '
     'model is behind it.', 'App process, foreground'],
    ['<b>Managing system</b>', 'Monitor, Analyser, Planner, Executor and the Knowledge store. One '
     'foreground service, one worker thread, one 5&nbsp;s tick.', 'App process, background thread'],
    ['<b>Knowledge</b>', 'Model registry, score table, operating-mode definitions, rolling metric '
     'windows, the per-user battery threshold, the drift reference distribution, and the switch log.',
     'On-device store, synced to cloud on Wi-Fi'],
    ['<b>Decision map</b>', 'The goals and their boundaries: acceptance retention, energy per hour, '
     'p95 latency by journey stage, memory ceiling, offline availability, explainability. Authored '
     'by us, versioned, shipped with the app.', 'Config, shipped and remotely tunable'],
], [30*mm, CW - 68*mm, 38*mm],
  caption='Table 2.1 &mdash; The four layers. Only the decision map is authored by hand; the rest '
          'is mechanism.', fs=8.0)

F += [P('The decision map matters more than it looks. HarmonE&rsquo;s central point is that '
        'adaptation without a stated goal degenerates into reacting to whatever metric moved last. '
        'Writing the goals down first is what lets us say, later, that a switch was <i>correct</i> '
        'rather than merely that it happened. LearnPerk&rsquo;s six goals and their initial '
        'boundaries are in Table 2.2; each boundary is the number the analyser compares against.')]

F += TBL(['Goal', 'Dimension', 'Boundary (initial)', 'Which metric tests it'], [
    ['Keep the commercial result', 'Technical / economic',
     'Offer acceptance rate within <b>2 percentage points</b> of the always-heaviest configuration, '
     'measured over a rolling 200 impressions',
     'Realised accept rate <font face="Courier" size="7.6">A<sub>avg</sub></font>, compared off-policy '
     'against the heavy arm'],
    ['Spend less energy', 'Environmental',
     'Median <b>&le;&nbsp;18&nbsp;mAh per commuting hour</b> attributable to LearnPerk inference; '
     'reference level set from a two-week baseline',
     'Battery drain rate <font face="Courier" size="7.6">&Delta;B</font> and estimated energy per '
     'call <font face="Courier" size="7.6">E</font>'],
    ['Stay responsive', 'Technical / social',
     'p95 end-to-end surface latency <b>&le;&nbsp;120&nbsp;ms</b> in normal stages, '
     '<b>&le;&nbsp;60&nbsp;ms</b> when the remaining window is under 120&nbsp;s',
     'Inference latency <font face="Courier" size="7.6">L</font>, p50 and p95 over the rolling window'],
    ['Never go dark', 'Social',
     '<b>&ge;&nbsp;99%</b> of legs receive at least one serveable recommendation, including offline '
     'legs and legs on low-tier devices',
     'Serve-failure rate; count of ticks with no feasible model'],
    ['Fit in the phone', 'Technical',
     'Peak resident set attributable to models <b>&le;&nbsp;280&nbsp;MB</b> on mid-tier, '
     '<b>&le;&nbsp;160&nbsp;MB</b> on low-tier',
     'Resident memory <font face="Courier" size="7.6">R</font>; cache residency state'],
    ['Stay explainable', 'Social',
     'Every surfaced item carries the model that produced it and, where a switch preceded it, the '
     'trigger that caused the switch',
     '<font face="Courier" size="7.6">serving_model_id</font> and '
     '<font face="Courier" size="7.6">switch_id</font> on every impression (&sect;8)'],
], [32*mm, 22*mm, 60*mm, CW - 114*mm],
  caption='Table 2.2 &mdash; LearnPerk&rsquo;s decision map, reduced to six goals and six boundaries. '
          'These are the numbers &sect;4 compares against. They are deliberately conservative for v1 '
          'and are expected to move once the field trial in &sect;9.6 reports.', fs=7.8)

F += [H2('2.2&nbsp;&nbsp;The MAPE-K loop on device')]
F += [P('The loop is the standard five components. What follows is what each one does in '
        'LearnPerk specifically, and what it hands to the next.')]

F += TBL(['Phase', 'What it does in LearnPerk', 'Output'], [
    ['<b>Monitor</b><br/><font size="7.4" color="#5A6772">1&nbsp;Hz sample,<br/>5&nbsp;s '
     'aggregate</font>',
     'Reads three metric groups (&sect;3). Resource metrics come from the platform: CPU from '
     '<font face="Courier" size="7.5">/proc/self/stat</font> deltas as in the EdgeMLBalancer '
     'reference code, memory from <font face="Courier" size="7.5">Debug.MemoryInfo</font>, charge '
     'and drain from <font face="Courier" size="7.5">BatteryManager</font>, thermal state from '
     '<font face="Courier" size="7.5">PowerManager.getCurrentThermalStatus()</font>. Quality '
     'metrics come from the inference wrapper, which times every call and records the top-1 '
     'calibrated score. Context metrics come from the GVB feed, the connectivity manager and the '
     'activity-recognition API.',
     'A metric tuple per 5&nbsp;s tick, written to the rolling window and to '
     '<font face="Courier" size="7.5">edge_adaptation_state</font>'],
    ['<b>Analyse</b>',
     'Cleans and aggregates over the window; recomputes EMA scores for every model in every task '
     'spectrum; evaluates each decision-map boundary; updates the dynamic energy threshold; runs the '
     'drift test on the feature distribution. Raises a typed uncertainty when a boundary is '
     'crossed: <font face="Courier" size="7.5">RESOURCE_PRESSURE</font>, '
     '<font face="Courier" size="7.5">CONNECTIVITY_LOSS</font>, '
     '<font face="Courier" size="7.5">WINDOW_CLOSING</font>, '
     '<font face="Courier" size="7.5">QUALITY_DEGRADATION</font>, '
     '<font face="Courier" size="7.5">COVERAGE_LOSS</font>, '
     '<font face="Courier" size="7.5">DRIFT</font>, or '
     '<font face="Courier" size="7.5">OPPORTUNITY</font>.',
     'Zero or more typed uncertainties, plus a refreshed score table'],
    ['<b>Plan</b>',
     'Maps the uncertainty to a tactic, then selects a model. The feasibility gate removes '
     'candidates that cannot run at all (&sect;4.1); the composite score ranks what remains '
     '(&sect;4.2); &epsilon;-greedy exploration and dwell-time hysteresis decide whether to act on '
     'the ranking (&sect;4.4). For Task&nbsp;E the score additionally carries CALM&rsquo;s semantic '
     'similarity term.',
     'A target model per affected task, or the decision to hold'],
    ['<b>Execute</b>',
     'Performs the switch: loads the target interpreter, warms it with one synthetic call, atomically '
     'swaps the task binding, then releases the outgoing model unless it is cache-resident. Writes '
     'the switch event. If the warm-up call fails or exceeds its latency budget, rolls back and '
     'blacklists the target for 90&nbsp;s.',
     'New active binding; one row in '
     '<font face="Courier" size="7.5">edge_switch_events</font>'],
    ['<b>Knowledge</b>',
     'Holds the model registry, the score table with per-model EMA, the operating-mode table, the '
     'per-user battery threshold learned from past disengagement, the drift reference distribution '
     'shipped with the model, and the log repository. Everything the other four phases read or write '
     'passes through here.',
     'Durable on-device state, uploaded on Wi-Fi'],
], [24*mm, CW - 68*mm, 44*mm],
  caption='Table 2.3 &mdash; The MAPE-K loop as instantiated on the commuter&rsquo;s device. '
          'The typed uncertainties in the Analyse row are the vocabulary the rest of this document '
          'uses.', fs=7.7)

F += [H2('2.3&nbsp;&nbsp;Cadence, dwell time and the cost of switching')]
F += [P('EdgeMLBalancer re-decides once per second and reports a mean switch time of 0.85&nbsp;s. '
        'On a continuous camera feed that is acceptable, because the next frame is 16&nbsp;ms away '
        'and a missed frame costs nothing. LearnPerk is different in two ways that matter, and '
        'copying the cadence unchanged would be a mistake.')]
F += UL([
    '<b>Our decisions are sparse.</b> A commuter is shown a handful of offers and a handful of '
    'content items per leg, not 1,800 frames. Re-ranking at 1&nbsp;Hz computes answers nobody asked '
    'for. The <i>monitor</i> should sample at 1&nbsp;Hz, because resource signals are noisy and need '
    'averaging, but the <i>planner</i> should run at 5&nbsp;s and the <i>executor</i> should act '
    'less often still.',
    '<b>Our switches are expensive relative to the work.</b> Loading a quantised gradient-boosted '
    'ranker costs single-digit milliseconds, but loading a language model costs hundreds of '
    'milliseconds to seconds and tens to hundreds of megabytes. A switch that saves 3&nbsp;mJ of '
    'inference and costs 400&nbsp;mJ of loading is a loss the score must be able to see.',
])
F += [P('We therefore separate three cadences and put an explicit price on switching.')]

F += TBL(['Parameter', 'Symbol', 'Default', 'Rationale'], [
    ['Monitor sample period', '&mdash;', '1&nbsp;s',
     'Matches the EdgeMLBalancer reference implementation. CPU deltas below this are dominated by '
     'sampling noise.'],
    ['Analyse / plan period', '&mdash;', '5&nbsp;s',
     'Roughly 140 ticks on a median 11.9-minute leg &mdash; enough to react inside a leg, few enough '
     'that the loop itself is not the load.'],
    ['Rolling window', '<font face="Courier" size="7.6">n</font>', '12 ticks (60&nbsp;s)',
     'One minute of history survives a tunnel and a station stop without being so long that a '
     'genuine regime change is smoothed away.'],
    ['EMA smoothing factor', '<font face="Courier" size="7.6">&beta;</font>', '0.30',
     'HarmonE&rsquo;s role for this parameter: suppress the spike, keep the trend. At 0.30 a step '
     'change is ~90% absorbed in six ticks, or 30&nbsp;s.'],
    ['Minimum dwell time', '<font face="Courier" size="7.6">&tau;</font>',
     '20&nbsp;s (light tasks)<br/>120&nbsp;s (Task&nbsp;E)',
     'A model must hold the binding this long before it can be replaced by score alone. Prevents the '
     'thrash a 5&nbsp;s planner would otherwise produce.'],
    ['Switch margin', '<font face="Courier" size="7.6">&delta;</font>', '0.05',
     'The challenger&rsquo;s EMA must beat the incumbent&rsquo;s by this much. Below the margin the '
     'difference is not distinguishable from window noise.'],
    ['Switch cost charge', '<font face="Courier" size="7.6">&kappa;</font>',
     'Measured, per model pair',
     'The load-and-warm cost is amortised over the expected remaining window and <i>subtracted from '
     'the challenger&rsquo;s score</i>. This is why a heavy model is correctly rejected at minute '
     'eleven of a twelve-minute leg.'],
    ['Exploration rate', '<font face="Courier" size="7.6">&epsilon;</font>',
     '0.10, annealed to 0.02',
     'EdgeMLBalancer&rsquo;s value. Annealed once a model has 500 logged calls on this device, '
     'because the fairness argument for exploring weakens as the estimates firm up.'],
    ['Forced-switch bypass', '&mdash;', 'Immediate',
     'A feasibility-gate failure &mdash; network gone, thermal throttle, memory pressure &mdash; '
     'ignores dwell time and margin entirely. Gates are not negotiable.'],
], [36*mm, 20*mm, 28*mm, CW - 84*mm],
  caption='Table 2.4 &mdash; Timing and hysteresis parameters. The switch-cost charge '
          '<font face="Courier" size="7.6">&kappa;</font> and the dwell time '
          '<font face="Courier" size="7.6">&tau;</font> are the two additions relative to '
          'EdgeMLBalancer, and both exist because a journey ends.', fs=7.8)

F += CALLOUT('Why the switch cost has to be in the score, not in a rule',
    'It is tempting to handle switching cost with a rule &mdash; say, no heavy-model switches in the '
    'last three minutes of a leg. That rule is wrong at both ends: it forbids a switch that would '
    'genuinely pay off on a long delayed leg, and it permits one that will not pay off on a short '
    'one. Charging <font face="Courier" size="8">&kappa;</font> amortised over the '
    '<i>expected remaining window</i> gets both right from one mechanism, and it degrades sensibly '
    'when the window estimate is poor. The window estimate comes from '
    '<font face="Courier" size="8">duration_minutes</font> for the leg less elapsed time, corrected '
    'by live <font face="Courier" size="8">delay_minutes</font>.',
    accent=TEAL)
F += [PageBreak()]
