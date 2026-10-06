# -*- coding: utf-8 -*-
from common import *

F += [H1('10&nbsp;&nbsp;Threats to validity and open questions')]
F += [P('Stated in the form the three source papers use, because the same categories apply and '
        'because a design document that lists no threats is not being honest about its confidence.')]

F += [H3('Construct validity &mdash; do the metrics measure what we claim?')]
F += UL([
    '<b>Energy is estimated, not measured.</b> There is no pyRAPL on Android. HarmonE could profile '
    'energy directly at the system level; we infer it from CPU time times a per-device-class power '
    'coefficient. The coefficient will be wrong under thermal throttling, which is precisely when it '
    'matters most. Mitigation: calibrate per device class against a hardware power monitor, and '
    'treat <b>E</b> as a gate input only in combination with the directly measured '
    '<b>&Delta;B</b>. The EdgeMLBalancer reference code computes battery consumption as '
    '<font face="Courier" size="8.5">battery_level &times; cpu_usage / 100</font>, which multiplies '
    'a level by a rate and is not a quantity of energy at all; we should not reproduce that.',
    '<b>Confidence is a proxy for correctness, and a weak one.</b> Gate G4 exists because a model '
    'fed nulls returns arbitrary answers <i>confidently</i>. The same failure can occur inside the '
    'coverage minimum. Mitigation: ECE is tracked per model and a badly calibrated model is demoted '
    'in the registry, but calibration is recomputed nightly, so there is a window in which the '
    'switching engine is optimising a number that has stopped meaning anything.',
    '<b>The remaining window W is itself a prediction.</b> It comes from '
    '<font face="Courier" size="8.5">duration_minutes</font> corrected by live delay, and it is the '
    'denominator of &kappa; &mdash; so an error in W propagates into every switch-cost decision. On '
    'a 4-minute window a 60-second error is a 25% error in &kappa;. Mitigation: floor W at '
    '<font face="Courier" size="8.5">W_min</font> so the charge cannot diverge, and report W '
    'prediction error as a first-class result rather than an implementation detail.',
])

F += [H3('Internal validity &mdash; could something else explain the result?')]
F += UL([
    '<b>The dataset is simulated.</b> The dictionary is explicit that the '
    '<font face="Courier" size="8.5">truth_</font> columns are the traits the simulator used to '
    'drive behaviour. That is a genuine advantage for off-policy evaluation, since it gives a known '
    'ceiling, but it means an engine tuned against replay is tuned against a generator. The '
    'relationships a model learns are the ones that were put in. Mitigation: replay is a '
    '<i>screening</i> stage with kill conditions, never a proof; RQ2 and RQ5 are excluded from it '
    'entirely.',
    '<b>Device thermal and background state confound everything.</b> A heavier model is slower '
    'partly because it is heavier and partly because it heated the phone on the previous run. '
    'Mitigation: EdgeMLBalancer&rsquo;s controls &mdash; reset, full charge, warm-up, cooldown '
    '&mdash; adopted verbatim in &sect;9.6.',
    '<b>The engine changes the data it learns from.</b> Switching alters which impressions occur, '
    'which alters the rolling metrics, which alters future switching. This is the standard feedback '
    'loop in any deployed ranker and it is not solved here. Mitigation: '
    '<font face="Courier" size="8.5">propensity</font> is logged for every selection, including '
    'model selection and not only offer selection, so the loop remains analysable after the fact.',
])

F += [H3('External validity &mdash; how far does this generalise?')]
F += UL([
    '<b>Amsterdam, GVB, and the metro in particular.</b> The strongest argument in &sect;1 &mdash; '
    'that only 41.6% of metro impressions are online &mdash; is a fact about tunnels under the IJ. '
    'A surface-rail network in a different city would weaken the connectivity case considerably, '
    'though the battery, window and coverage arguments would survive untouched.',
    '<b>Android only.</b> Every probe named in &sect;3.1 &mdash; '
    '<font face="Courier" size="8.5">/proc/self/stat</font>, '
    '<font face="Courier" size="8.5">getCurrentThermalStatus()</font>, NNAPI &mdash; is '
    'Android-specific, as EdgeMLBalancer&rsquo;s was. iOS would need an equivalent monitor layer, '
    'and iOS exposes less.',
    '<b>The model sizes and latencies are targets, not measurements.</b> Every number in '
    '&sect;5 is drawn from published figures for these architectures at these quantisations. They '
    'are good enough to reason about the spectrum and not good enough to commit to. The registry '
    'must be built and measured before any of &sect;7&rsquo;s efficiency numbers can be stated as '
    'fact rather than as expectation.',
])

F += [H3('Open questions we cannot settle from this document')]
F += TBL(['Question', 'Why it is open', 'How we would resolve it'], [
    ['Should Task&nbsp;E exist on low-tier devices at all?',
     'E1 at ~23&nbsp;MB is 14% of a 160&nbsp;MB ceiling for intent classification that a phrase '
     'table handles adequately most of the time.',
     'Measure E0&rsquo;s accuracy against E1&rsquo;s on real GVB bulletins. If the gap is small, '
     'low-tier ships E0 only and the ceiling problem disappears.'],
    ['Is &epsilon;-greedy the right exploration mechanism here?',
     'EdgeMLBalancer&rsquo;s fairness argument is about preventing starvation of models. Our '
     'spectrum has a genuine ordering, so exploring into B0 when B3 is feasible may just be a worse '
     'answer rather than a useful sample.',
     'Ablate against Thompson sampling over the score posterior, and against no exploration at all, '
     'in RQ7.'],
    ['Should the operating mode be per-task rather than global?',
     'Task&nbsp;E dominates the memory budget, so a single global mode may unnecessarily downgrade '
     'the cheap tasks whenever the language layer is the actual problem.',
     'Run a per-task-mode variant in replay and compare acceptance retention at equal energy.'],
    ['How is the per-user battery threshold learned before we have observed disengagement?',
     'It is circular: we need past disengagement to set the threshold, and the threshold is meant to '
     'prevent disengagement.',
     'Start at the population median of the documented 20&ndash;40% band and update with a '
     'hierarchical prior as evidence accrues. State explicitly that UC-2 does not work for a new '
     'user.'],
    ['Does the cloud tier belong in the spectrum at all?',
     'E4 is gated out on 22.9% of metro impressions and raises consent questions that E0 to E3 do '
     'not. It may be simpler to remove it than to gate it.',
     'Measure how often E4 is both feasible and selected. If that is a small share of questions, the '
     'complexity is not earning its place.'],
], [40*mm, CW - 104*mm, 64*mm], fs=7.7,
  caption='Table 10.1 &mdash; Five open questions. Each is a decision this document deliberately '
          'does not make.')

F += [PageBreak()]

# ================= 11 Appendix =================
F += [H1('11&nbsp;&nbsp;Appendix &mdash; parameter defaults')]
F += [P('Every tunable in one place. These are starting points chosen to be defensible, not tuned '
        'values; the RQ7 ablation in &sect;9.1 exists to replace them.')]
F += TBL(['Symbol', 'Parameter', 'Default', 'Source'], [
    ['&mdash;', 'Monitor sample period', '1&nbsp;s', 'EdgeMLBalancer reference implementation'],
    ['&mdash;', 'Plan period', '5&nbsp;s', 'This document (&sect;2.3)'],
    ['<font face="Courier" size="7.6">n</font>', 'Rolling window', '12 ticks (60&nbsp;s)',
     'This document'],
    ['<font face="Courier" size="7.6">beta</font>', 'EMA smoothing factor', '0.30', 'HarmonE'],
    ['<font face="Courier" size="7.6">gamma</font>', 'Dynamic boundary decay', '0.20', 'HarmonE'],
    ['<font face="Courier" size="7.6">epsilon</font>', 'Exploration rate',
     '0.10, annealed to 0.02 after 500 calls', 'EdgeMLBalancer (0.10); annealing is ours'],
    ['<font face="Courier" size="7.6">tau</font>', 'Minimum dwell time',
     '20&nbsp;s (A&ndash;D), 120&nbsp;s (E)', 'This document'],
    ['<font face="Courier" size="7.6">delta</font>', 'Switch margin', '0.05', 'This document'],
    ['<font face="Courier" size="7.6">alpha</font>', 'Quality/cost balance',
     '0.75 / 0.55 / 0.35 / 0.15 / 0.85 by mode', 'HarmonE&rsquo;s role; our values'],
    ['<font face="Courier" size="7.6">lambda</font>', 'Semantic similarity weight',
     '0.30, Task&nbsp;E only', 'CALM (reports k in 0.1&ndash;0.3)'],
    ['<font face="Courier" size="7.6">W_min</font>', 'Window floor for &kappa;', '60&nbsp;s',
     'This document'],
    ['<font face="Courier" size="7.6">PSI</font>', 'Drift threshold', '0.25 on a top-10 feature',
     'Conventional PSI practice; HarmonE uses KL'],
    ['&mdash;', 'Blacklist duration after two serve failures', '90&nbsp;s', 'This document'],
    ['&mdash;', 'M6 cap', '300&nbsp;s, no immediate re-entry', 'This document'],
    ['&mdash;', 'Language cache size', '1 resident model', 'CALM (cache_size = 1 configuration)'],
    ['&mdash;', 'Latency budget', '120&nbsp;ms normal; 60&nbsp;ms when W &lt; 120&nbsp;s',
     'Decision map (&sect;2.1)'],
    ['&mdash;', 'Memory ceiling', '160 / 280 / 900&nbsp;MB by device class', 'Decision map'],
    ['&mdash;', 'Energy reference level', '18&nbsp;mAh per commuting hour', 'Decision map'],
], [20*mm, 48*mm, 52*mm, CW - 120*mm], fs=7.7,
  caption='Table 11.1 &mdash; Parameter defaults and their provenance. Eight are inherited from the '
          'three source approaches; the rest are ours and carry no empirical backing yet.')

F += [H2('Sources')]
F += TBL(None, [
    ['[1]', 'A. Matathammal, K. Gupta, L. Lavanya, A. V. Halgatti, P. Gupta, K. Vaidhyanathan. '
     '<i>EdgeMLBalancer: A Self-Adaptive Approach for Dynamic Model Switching on Resource-Constrained '
     'Edge Devices.</i> arXiv:2502.06493v1 [cs.SE], 10 February 2025. Reference implementation: '
     '<font face="Courier" size="7.5">github.com/sa4s-serc/EdgeMLBalancer</font> &mdash; the '
     'epsilon-greedy, naive and MLFQ CameraFragment variants were read directly for this document.'],
    ['[2]', 'H. Bhatt, S. Biswas, S. Rakhunathan, K. Vaidhyanathan. <i>HarmonE: A Self-Adaptive '
     'Approach to Architecting Sustainable MLOps.</i> arXiv:2505.13693v1 [cs.SE], 19 May 2025.'],
    ['[3]', 'H. Jain, D. Pandey, K. Vaidhyanathan. <i>CALM: A Self-Adaptive Orchestration Approach '
     'for QoS-Aware Routing in Small Language Model based Systems.</i> arXiv:2602.03632v1 [cs.SE], '
     '3 February 2026.'],
    ['[4]', '<i>LearnPerk Edge Data &amp; Model Switching</i>, v3, August 2026. Internal. The '
     'document this one was named as the follow-on to.'],
    ['[5]', '<i>LearnPerk Data Dictionary</i>, September 2026, generated from the data itself. '
     'Internal. All measured figures in &sect;1.1 were computed directly from the four combined '
     'files it documents.'],
    ['[6]', 'J. O. Kephart and D. M. Chess. <i>The Vision of Autonomic Computing.</i> IEEE Computer, '
     '36(1), 2003. The origin of the MAPE-K loop all three approaches build on.'],
    ['[7]', 'A. Marda, S. S. Kulkarni, K. Vaidhyanathan. <i>SWITCH: An Exemplar for Evaluating '
     'Self-Adaptive ML-Enabled Systems.</i> arXiv:2402.06351, 2024. The QoS-aware model-switching '
     'baseline CALM adapts and compares against.'],
    ['[8]', 'M. Tedla, S. S. Kulkarni, K. Vaidhyanathan. <i>EcoMLS: A Self-Adaptation Approach for '
     'Architecting Green ML-Enabled Systems.</i> arXiv:2404.11411, 2024. The source of the '
     'performance-score form EdgeMLBalancer adapts.'],
], [9*mm, CW - 9*mm], zebra=False, fs=7.8)

F += [SP(6), RULEF(TEAL, 1.2)]
F += [P('<b>Next steps, in order.</b> (1) Build <font face="Courier" size="8.5">model_registry.csv</font> '
        'and measure every latency, size and energy figure in &sect;5 on real devices across all '
        'three classes &mdash; until that exists, every efficiency claim in &sect;7 is an '
        'expectation rather than a result. (2) Implement the three new edge files of &sect;8 and run '
        'the engine in shadow mode, which yields a complete switching history at zero user risk. '
        '(3) Run the replay harness and the RQ7 ablation to remove any mechanism that turns out not '
        'to matter. (4) Only then run the on-device trial that can answer RQ2 and RQ5.')]
