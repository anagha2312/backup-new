# -*- coding: utf-8 -*-
from common import *

F += [H1('9&nbsp;&nbsp;How we test the switching')]
F += [P('A switching engine is easy to build and hard to justify. It will always produce switches, '
        'and the switches will always look purposeful in a log. The question this section answers is '
        'how we establish that the engine is <b>better than not having one</b>, and better than the '
        'much simpler things we could have built instead.')]
F += [P('The evaluation has three stages, in increasing cost and decreasing control: offline replay '
        'on the data we already hold, on-device measurement on a fixed workload, and a field trial. '
        'Each stage can kill the design before we pay for the next one.')]

F += [H2('9.1&nbsp;&nbsp;Research questions')]
F += TBL(['RQ', 'Question', 'Stage', 'Kill condition'], [
    ['<b>RQ1</b>', 'Does switching retain acceptance? Does the engine stay within 2 percentage '
     'points of the always-heaviest configuration on offer acceptance?', 'Replay, then field',
     'A loss above 2&nbsp;pp that a weight change cannot close.'],
    ['<b>RQ2</b>', 'Does it cost less? How do energy, p95 latency and peak memory compare against '
     'each fixed-model baseline and against the naive and round-robin policies?',
     'On-device', 'No significant energy reduction against the always-heavy baseline.'],
    ['<b>RQ3</b>', 'Does it close the availability gap? What share of offline legs receive a '
     'serveable recommendation, against a present-day baseline of zero content views offline?',
     'Replay, then field', 'Below 95% of offline legs served.'],
    ['<b>RQ4</b>', 'Is the selection fair? Does &epsilon;-greedy avoid the starvation EdgeMLBalancer '
     'measured &mdash; one model taking 74.3% of frames under naive, 84.4% under round-robin?',
     'Replay', 'Any single model above 60% of selections within a task, sustained.'],
    ['<b>RQ5</b>', 'Is switching itself cheap? What are mean switch latency, switch frequency and '
     'rollback rate, and what fraction of a leg is spent mid-switch?', 'On-device',
     'Above 3% of leg time mid-switch, or a rollback rate above 2%.'],
    ['<b>RQ6</b>', 'Does the opportunity mode earn its cost? Restricted to impressions where M6 '
     'holds, is the acceptance lift of the heavier model positive?', 'Replay, off-policy',
     'A non-positive lift. M6 would then be retired, not tuned.'],
    ['<b>RQ7</b>', 'Which mechanisms matter? An ablation over &kappa;, the coverage gate, the EMA, '
     'the dynamic boundary, exploration and the semantic term.', 'Replay',
     'Any mechanism with no measurable effect is removed from the design.'],
], [12*mm, CW - 92*mm, 24*mm, 56*mm], fs=7.7,
  caption='Table 9.1 &mdash; Seven research questions, each with a stated kill condition. RQ1 to RQ5 '
          'mirror the questions EdgeMLBalancer, HarmonE and CALM each ask of themselves; RQ6 and RQ7 '
          'are ours.')

F += [H2('9.2&nbsp;&nbsp;Baselines')]
F += [P('Nine experimental candidates, following HarmonE&rsquo;s practice of comparing against both '
        'every fixed model and every simpler adaptive policy. Comparing only against the heaviest '
        'model would flatter us; comparing only against the lightest would flatter us differently.')]
F += TBL(['Candidate', 'What it is', 'What it isolates'], [
    ['<b>Fixed-B0</b> &hellip; <b>Fixed-B4</b>', 'Five runs, one per tier, no switching at all.',
     'The accuracy/cost curve the spectrum spans. Every other result is read against this curve.'],
    ['<b>Naive-Threshold</b>', 'Fixed CPU cut-offs at 20/25/30%, exactly the policy in the '
     'EdgeMLBalancer reference implementation&rsquo;s naive variant.',
     'Whether the composite score beats a threshold table. EdgeMLBalancer found naive gave one model '
     '74.3% of frames and the lowest accuracy of the three policies tested.'],
    ['<b>RoundRobin+Boost</b>', 'Time-sliced rotation with periodic CPU recalibration, the '
     'EdgeMLBalancer MLFQ variant.',
     'Whether context-aware selection beats fair-by-construction rotation. Their result: better '
     'accuracy than naive, but still 84.4% concentration and the slowest switching at 1.40&nbsp;s.'],
    ['<b>Switch-NoGoals</b>', 'Our engine with the decision map removed: score only, no boundaries, '
     'no modes.', 'Whether HarmonE&rsquo;s design-time goals contribute, or whether the score alone '
     'suffices.'],
    ['<b>LearnPerk-Balancer</b>', 'The full design in this document.',
     'The proposal.'],
], [34*mm, 58*mm, CW - 92*mm], fs=7.7,
  caption='Table 9.2 &mdash; Nine candidates. Note that two are lifted directly from the '
          'EdgeMLBalancer repository, so the comparison is against running code rather than a '
          'described policy.')

F += [H2('9.3&nbsp;&nbsp;Replay harness and off-policy evaluation')]
F += [P('The replay harness reads <font face="Courier" size="8.5">event_stream.csv</font> in order '
        '&mdash; which is what the dictionary says the file is for &mdash; and reconstructs each '
        'leg as a sequence of 5-second ticks, synthesising the Group&nbsp;R metrics from a device '
        'model calibrated against real hardware and taking every Group&nbsp;C metric straight from '
        'the file. The engine then runs unmodified against that tick stream, and we compare the '
        'model it selects against the model each baseline would have selected.')]
F += [P('Measuring the <i>consequence</i> of a different selection is the harder half, because the '
        'logs record what happened under the policy that actually ran. The dictionary anticipates '
        'this precisely: <font face="Courier" size="8.5">propensity</font> is described as '
        '&ldquo;the probability this particular offer was chosen to be shown &mdash; needed for any '
        'later off-policy evaluation of a ranking change; without it that analysis is '
        'impossible.&rdquo; That column is what makes RQ1 and RQ6 answerable at all.')]
F += NL([
    '<b>Inverse propensity scoring, self-normalised (SNIPS)</b>, weighting each logged impression by '
    'the ratio of the new policy&rsquo;s selection probability to '
    '<font face="Courier" size="8.5">propensity</font>. Self-normalised rather than plain IPS, '
    'because the variance of plain IPS at these sample sizes would swamp a 2&nbsp;pp effect.',
    '<b>A doubly robust estimator</b> as a cross-check, using a separately fitted outcome model. '
    'Agreement between the two is the evidence that the estimate is trustworthy; disagreement is a '
    'reason to stop and look rather than a reason to pick the friendlier number.',
    '<b>The <font face="Courier" size="8.5">truth_</font> columns as an upper bound, never as '
    'features.</b> <font face="Courier" size="8.5">truth_p_accept</font> is documented as the '
    'theoretical ceiling any model can reach. Reporting each candidate as a fraction of that ceiling '
    'is far more honest than reporting a raw accept rate, and it is only possible because the '
    'simulator kept the answer key.',
    '<b>Effective sample size reported alongside every estimate.</b> With 9,990 impressions and '
    'a propensity floor near 0.03, some comparisons will simply not have the support to resolve a '
    '2&nbsp;pp difference, and we should say so rather than report a number.',
])
F += CALLOUT('The honest limit of replay',
    'Replay can tell us which model the engine <i>would</i> select, and off-policy estimation can '
    'tell us roughly what that selection would have been worth. It cannot tell us the energy cost, '
    'because the logs contain no energy measurement, and it cannot tell us the switch latency, '
    'because no switch ever occurred. RQ2 and RQ5 are therefore <b>not answerable offline at all</b> '
    'and must wait for stage two. Claiming an energy result from replay would be the single easiest '
    'way to make this work look better than it is.',
    accent=CRIT, bg=colors.HexColor('#FBF0F0'))

F += [H2('9.4&nbsp;&nbsp;Evaluation metrics')]
F += TBL(['Family', 'Metric', 'How measured', 'Target'], [
    ['Quality', 'Offer acceptance rate; fraction of the <font face="Courier" size="7.5">'
     'truth_p_accept</font> ceiling attained', 'SNIPS over replay; direct measurement in the field',
     'Within 2&nbsp;pp of always-heavy'],
    ['Quality', 'Content completion rate and bounce rate', 'Direct',
     'No worse than the 21.5% completion and 10.7% bounce currently observed'],
    ['Availability', 'Share of offline legs with a serveable recommendation', 'Direct',
     '&ge;&nbsp;95%, against a present-day content baseline of <b>0%</b>'],
    ['Cost', 'mAh per commuting hour attributable to LearnPerk', 'On-device, matched 30-minute runs '
     'with 30-minute cooldowns', 'Below the 18&nbsp;mAh/hr decision-map boundary'],
    ['Cost', 'p95 surface latency by journey stage', 'On-device',
     '&le;&nbsp;120&nbsp;ms normal, &le;&nbsp;60&nbsp;ms when W &lt; 120&nbsp;s'],
    ['Cost', 'Peak model-attributable RSS', 'On-device',
     '&le;&nbsp;160 / 280 / 900&nbsp;MB by device class'],
    ['Switching', 'Mean switch latency; switches per leg; fraction of leg spent mid-switch',
     'From <font face="Courier" size="7.5">edge_switch_events</font>',
     'Comparable to EdgeMLBalancer&rsquo;s 0.85&nbsp;s; under 3% of leg time'],
    ['Switching', 'Rollback rate', 'From <font face="Courier" size="7.5">rollback_reason</font>',
     '&lt;&nbsp;2% of attempted switches'],
    ['Fairness', 'Selection distribution per task; entropy; max single-model share',
     'From <font face="Courier" size="7.5">edge_switch_events</font>',
     'No model above 60% sustained &mdash; against 74.3% and 84.4% for the two baselines'],
    ['Robustness', 'Serve-failure rate; ticks with an empty feasible set', 'Direct',
     'Serve failures &lt;&nbsp;0.5%; empty feasible set never, since the floor model must always pass'],
], [20*mm, 48*mm, 44*mm, CW - 112*mm], fs=7.6,
  caption='Table 9.3 &mdash; Evaluation metrics. Ten metrics across five families, because as '
          'Table&nbsp;7.11 shows, the gain differs by case and a single headline number would hide '
          'four of the five.')

F += [H2('9.5&nbsp;&nbsp;Per-use-case acceptance tests')]
F += [P('The tests written into each case in &sect;7 form the acceptance suite. Collected here with '
        'their priority: these run on every build, and a failure blocks release.')]
F += TBL(['Priority', 'Test', 'From', 'What a failure would mean'], [
    ['<b>P0</b>', 'Symmetry: UC-3 and UC-5 differ only in W and reach opposite conclusions on the '
     'same upgrade', 'UC-5',
     '&kappa; amortisation is not working, which removes the central mechanism of the design. '
     'Write this test first.'],
    ['<b>P0</b>', 'Floor-model guarantee: the feasible set is never empty for any task under any '
     'combination of gates', '&sect;4.1',
     'The engine can go dark, which fails the decision map&rsquo;s hardest goal.'],
    ['<b>P0</b>', 'Null handling: no null is ever imputed as zero anywhere in the feature pipeline',
     'UC-4', 'Three distinct facts collapse into one, exactly as the dictionary warns.'],
    ['<b>P1</b>', 'Gate immediacy: connectivity loss fires on the same tick, bypassing dwell',
     'UC-1', 'Serving failures for the length of the smoothing window.'],
    ['<b>P1</b>', 'Down-switch precision: the engine picks the best feasible model, not the cheapest',
     'UC-1', 'Accuracy given away for no resource benefit &mdash; the most likely subtle bug.'],
    ['<b>P1</b>', 'Non-switch: D1 survives ten ticks in Frugal mode', 'UC-2',
     'A blanket throttle wearing the vocabulary of an adaptation loop.'],
    ['<b>P1</b>', 'Personal threshold: two commuters at identical charge behave differently',
     'UC-2', 'A global constant where the data says the threshold is personal.'],
    ['<b>P1</b>', 'Composite trigger: M6 requires all four conditions; three negative cases pass',
     'UC-3', 'Expensive models running when the moment does not justify them.'],
    ['<b>P2</b>', 'Refusal logging: held and rejected candidates appear with both scores', 'UC-5',
     'Non-decisions become invisible and the engine becomes unauditable.'],
    ['<b>P2</b>', 'Hysteresis: oscillating a metric across a boundary produces at most one switch',
     'UC-2', 'Thrash, which at 5-second planning would be continuous.'],
    ['<b>P2</b>', 'Direction independence: one trigger moves one task down and another up',
     'UC-4', 'Coverage has been conflated with cost.'],
    ['<b>P2</b>', 'Accessibility invariance: rendering is identical across all tiers', 'UC-2',
     'Accessibility became a casualty of a down-switch, which is not an acceptable trade at any '
     'energy saving.'],
], [14*mm, CW - 108*mm, 16*mm, 78*mm], fs=7.6,
  caption='Table 9.4 &mdash; Twelve acceptance tests. Three are P0 and block release outright.')

F += [H2('9.6&nbsp;&nbsp;On-device field trial')]
F += [P('Stage three, and the only stage that can answer RQ2 and RQ5. The protocol follows '
        'EdgeMLBalancer&rsquo;s, because their threats-to-validity section identifies the right '
        'controls: device reset before each run, full charge at the start, a warm-up phase to '
        'stabilise the hardware, and a cooldown between runs to prevent carryover.')]
F += TBL(['Aspect', 'Design'], [
    ['Devices', 'Three per class, nine total, spanning the 30/45/25 low/mid/high split. Each class '
     'runs the full candidate set, because a result on one class does not transfer &mdash; that is '
     'the whole reason the registry carries six latency columns.'],
    ['Workload', 'One recorded 30-minute commute trace, replayed identically to every candidate, so '
     'the comparison is like-for-like. EdgeMLBalancer used a fixed 30-minute traffic recording for '
     'exactly this reason.'],
    ['Repetition', 'Five independent runs per candidate per device class, with a 20-minute cooldown '
     'between consecutive runs, following HarmonE&rsquo;s protocol and standard empirical software '
     'engineering guidance.'],
    ['Controls', 'Device reset and full charge before each run; a warm-up phase; airplane mode '
     'toggled on a fixed schedule to reproduce the tunnel; background apps cleared.'],
    ['Induced conditions', 'Connectivity loss on a schedule matching the measured 22.9% offline and '
     '35.6% degraded metro profile; battery drained to target levels before low-charge runs; '
     'thermal load induced by a controlled background task.'],
    ['Drift induction', 'Following HarmonE, a scale-and-shift transformation applied twice to a '
     'segment of the feature stream, so the distribution first diverges and later realigns. This '
     'tests both that drift is detected and that the regime-specific sibling is <i>reused</i> rather '
     'than a retrain being triggered.'],
    ['Shadow phase', 'Before any commuter-visible rollout, the engine runs in shadow: it selects and '
     'logs but does not bind, while the production model continues to serve. Gives a full '
     '<font face="Courier" size="7.5">edge_switch_events</font> history at zero user risk, and '
     'catches a mis-specified gate before anyone experiences it.'],
    ['Staged rollout', '1% of commuters, then 5%, then 25%, with the RQ1 acceptance boundary as the '
     'automatic stop condition at each gate.'],
], [25*mm, CW - 25*mm], fs=7.0,
  caption='Table 9.5 &mdash; Field trial protocol. The shadow phase is the most important row: it '
          'produces the switching data this design needs without exposing a single commuter to a '
          'switching bug.')
F += [PageBreak()]
