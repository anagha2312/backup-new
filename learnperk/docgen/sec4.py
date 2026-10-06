# -*- coding: utf-8 -*-
from common import *

F += [H1('4&nbsp;&nbsp;The switching decision')]
F += [P('Selection happens in four ordered steps. <b>Gate</b>, then <b>score</b>, then '
        '<b>explore or exploit</b>, then <b>commit or hold</b>. The order is load-bearing: scoring '
        'an infeasible model wastes work and, worse, invites a weighted sum to trade away a hard '
        'constraint. Nothing downstream can resurrect a candidate the gate rejected.')]

F += [H2('4.1&nbsp;&nbsp;Feasibility gate')]
F += [P('For a task with spectrum <font face="Courier" size="8.5">M = {m<sub>1</sub> &hellip; '
        'm<sub>n</sub>}</font>, the gate yields a feasible subset. A model is feasible only if every one '
        'of the following holds.')]
F += TBL(['#', 'Gate condition', 'Metric', 'Why it is a gate, not a penalty'], [
    ['G1', 'Memory: loading it keeps resident model memory under the mode ceiling', '<b>R</b>',
     'Exceeding it does not degrade the app, it ends the process. There is no accuracy gain worth '
     'that trade.'],
    ['G2', 'Thermal: the model&rsquo;s tier is permitted at the current thermal status', '<b>T</b>',
     'Under throttling, every latency figure in the registry is wrong, so the score is no longer '
     'measuring what it claims to measure.'],
    ['G3', 'Connectivity: if the model needs the network, the network is present', '<b>N</b>',
     'Binary and immediate. The 22.9% of metro impressions that are Offline make this the most '
     'frequently fired gate in the system.'],
    ['G4', 'Coverage: available features meet the model&rsquo;s declared minimum set', '<b>&Phi;</b>',
     'A gradient-boosted ranker fed nulls for its top splits does not return a worse answer, it '
     'returns an arbitrary one, and it returns it confidently.'],
    ['G5', 'Window: registry p95 latency for this device class fits the stage budget', '<b>W, L, D</b>',
     'An answer that arrives after the commuter has alighted has no value at any accuracy.'],
    ['G6', 'Delegate: any required NNAPI, GPU or NPU delegate initialised', '<b>&Gamma;</b>',
     'Without the delegate the model is not slow, it is unavailable.'],
    ['G7', 'Health: not currently blacklisted for repeated serve failures', '<b>&Omega;</b>',
     'Two failures in one window is evidence about this device, now, which outranks any registry '
     'average.'],
    ['G8', 'Consent: the model&rsquo;s feature set is permitted by the user&rsquo;s consent state',
     '<b>Consent</b>',
     'A withdrawn commuter has no behavioural rows at all, so every personalised tier is not merely '
     'discouraged but unusable.'],
], [8*mm, 55*mm, 20*mm, CW - 83*mm],
  caption='Table 4.1 &mdash; The eight gates. If the feasible set is empty, the task falls to its '
          'designated <b>floor model</b> &mdash; tier&nbsp;0, offline, no learned features &mdash; '
          'which is required by registry contract to pass every gate unconditionally.', fs=7.8)

F += [H2('4.2&nbsp;&nbsp;Utility, cost and the composite score')]
F += [P('EdgeMLBalancer scores a model as '
        '<font face="Courier" size="8.5">S = min(U,&nbsp;U<sub>avg</sub>)&middot;(1&nbsp;&minus;&nbsp;C<sub>avg</sub>/C)</font> '
        'and takes the argmin. That form does real work &mdash; it favours low CPU while rewarding a '
        'model whose current confidence beats its own history &mdash; but it has one cost channel, '
        'one quality channel, and a multiplicative coupling that makes the sign of the score depend '
        'on whether confidence is rising. LearnPerk has four cost channels, two immediate quality '
        'channels and a context term, so we separate utility from cost additively and take the '
        'argmax.')]

F += EQ('[ utility ]      Q_m      =   w_c*Cn_m  +  w_g*Mn_m  +  w_a*An_m  -  w_p*(1 - Phi_m)',
        '[ cost ]         K_m      =   w_u*Un_m  +  w_e*En_m  +  w_l*L95n_m  +  w_r*Rn_m',
        '[ switch cost ]  kappa_m  =   switch_energy( m_active -&gt; m )  /  max( W, W_min )',
        '<b>[ score ]        S_m      =   alpha*Q_m  -  (1 - alpha)*K_m  -  kappa_m  +  lambda*sim(q, m)</b>')
F += [SP(4)]
F += [P('The four terms, in order. <b>&alpha;</b> is the quality/cost balance and is set entirely by '
        'the active operating mode (&sect;4.5) &mdash; it is the one knob the decision map controls '
        'directly, and it is how a single mechanism produces both switching down under pressure and '
        'switching up under opportunity. <b>&kappa;</b> is the switch cost of &sect;2.3, charged only '
        'to challengers and divided by the remaining window, which is what makes a heavy model '
        'correctly unattractive late in a leg. <b>&lambda;&middot;sim(q, m)</b> is CALM&rsquo;s '
        'semantic routing term: the cosine similarity between the user&rsquo;s query and the '
        'model&rsquo;s task description. It applies only to Task&nbsp;E, where a query has meaning; '
        '&lambda;&nbsp;=&nbsp;0 for Tasks A through D. The incumbent is scored with '
        '&kappa;&nbsp;=&nbsp;0, which is correct rather than a thumb on the scale: staying put '
        'genuinely costs nothing.')]
F += [P('Scores are then smoothed per model with the EMA of &sect;3.4 before comparison, so the '
        'planner compares <font face="Courier" size="8.5">EMA(S<sub>m</sub>)</font>, never a single '
        'tick&rsquo;s value.')]

F += TBL(['Weight', 'Term', 'Default', 'Note'], [
    ['<font face="Courier" size="7.6">w_c</font>', 'Top-1 calibrated confidence', '0.45',
     'The main quality signal, as in EdgeMLBalancer.'],
    ['<font face="Courier" size="7.6">w_g</font>', 'Ranking margin', '0.20',
     'Catches confident-but-undiscriminating models.'],
    ['<font face="Courier" size="7.6">w_a</font>', 'Realised accept-rate prior', '0.25',
     'Slow-moving; carries the delayed truth without letting it react.'],
    ['<font face="Courier" size="7.6">w_p</font>', 'Coverage shortfall penalty', '0.10',
     'Above the gate minimum, a shortfall still discounts.'],
    ['<font face="Courier" size="7.6">w_u</font>', 'CPU', '0.30', 'EdgeMLBalancer&rsquo;s sole cost channel; one of four here.'],
    ['<font face="Courier" size="7.6">w_e</font>', 'Energy per call', '0.35',
     'Weighted highest of the cost terms, because the environmental boundary is the one the decision '
     'map treats as hardest.'],
    ['<font face="Courier" size="7.6">w_l</font>', 'p95 latency', '0.25',
     'Rises sharply as W shrinks &mdash; see the stage budgets in Table 4.4.'],
    ['<font face="Courier" size="7.6">w_r</font>', 'Resident memory', '0.10',
     'Mostly handled by gate G1; this only breaks ties.'],
    ['<font face="Courier" size="7.6">&lambda;</font>', 'Semantic similarity', '0.30 (Task E only)',
     'CALM reports k in 0.1&ndash;0.3 across its routing variants; we start at the top of that band '
     'because our spectrum is smaller and the domains are further apart.'],
], [17*mm, 42*mm, 26*mm, CW - 85*mm],
  caption='Table 4.2 &mdash; Initial weights. Each group is normalised to sum to 1 within itself, so '
          '&alpha; alone controls the balance between them. These are starting points for the '
          'ablation in &sect;9, not tuned values.', fs=7.8)

F += [H2('4.3&nbsp;&nbsp;Dynamic boundaries')]
F += [P('A fixed energy ceiling is either too loose to protect the battery or too tight to allow a '
        'justified spike. HarmonE&rsquo;s answer, which we adopt unchanged, is a boundary that moves '
        'in response to sustained deviation but tolerates transient ones:')]
F += EQ('theta_(i+1)  =  theta_i  +  gamma * ( E_ref  -  E_avg_i ) ,          gamma = 0.20')
F += [SP(4)]
F += [P('When measured energy runs above the reference level, the deviation is negative and the '
        'ceiling tightens, making heavy models progressively harder to justify. When it runs below, '
        'the ceiling loosens and headroom is returned. The commuter-visible consequence is the one '
        'we want: a single expensive moment &mdash; a long delay, a genuinely valuable offer &mdash; '
        'is absorbed, while a pattern of expensive moments is progressively squeezed. '
        '<font face="Courier" size="8.5">E<sub>avg</sub>_ref</font> is set per device class from a two-week '
        'baseline, and &theta; is clamped to a floor so the boundary cannot tighten to the point '
        'where only the floor model is ever feasible.')]
F += [P('The same mechanism, with its own &gamma;, governs the <b>latency</b> boundary. Drift uses a '
        'fixed threshold instead (<font face="Courier" size="8.5">&Psi;&nbsp;&gt;&nbsp;0.25</font>), '
        'because a drifting feature distribution is a statement about the world that should not be '
        'negotiable against how much battery we have left.')]

F += [H2('4.4&nbsp;&nbsp;Exploration, hysteresis and rollback')]
F += [P('Pure exploitation of a score table has a known failure: a model that starts poorly is never '
        'selected, so its estimate never improves, so it is never selected. EdgeMLBalancer&rsquo;s '
        'measured consequence is stark &mdash; its naive baseline gave one model 74.3% of all frames '
        'and its round-robin baseline gave one model 84.4%, while &epsilon;-greedy spread selection '
        'across all four and improved fairness by 43.6% and 41.5% respectively. We take the same '
        'mechanism for the same reason, then constrain it in two ways the camera case did not need.')]
F += NL([
    '<b>Exploration is gated, never unconstrained.</b> The random draw is over the '
    '<i>feasible</i> set only. EdgeMLBalancer explores over all four models because all four are '
    'always runnable; for us, exploring into a cloud-assisted model in a tunnel is not exploration, '
    'it is a guaranteed serve failure.',
    '<b>Exploration is suppressed in Survival mode and when W is small.</b> The point of exploring '
    'is to improve a long-run estimate. At 12% battery, or with 90&nbsp;seconds of journey left, '
    'there is no long run to improve and the cost lands entirely on this commuter.',
    '<b>&epsilon; anneals from 0.10 to 0.02</b> once a model reaches 500 logged calls on this '
    'device, because the fairness argument weakens as the estimates firm up.',
])
F += [P('Hysteresis then stops the loop thrashing. A challenger replaces the incumbent only if all '
        'three hold: the incumbent has held the binding for at least the dwell time &tau;; the '
        'challenger&rsquo;s smoothed score exceeds the incumbent&rsquo;s by more than the margin '
        '&delta;; and the challenger passed every gate on this tick. A gate failure bypasses all '
        'three conditions, because a gate failure means the incumbent is no longer serveable at all.')]
F += [P('Finally, every switch is reversible. The executor warms the target with one synthetic call '
        'before swapping the binding. If that call throws, or exceeds the stage latency budget, the '
        'switch is abandoned, the incumbent keeps the binding, the target is blacklisted for '
        '90&nbsp;seconds, and the attempt is logged with '
        '<font face="Courier" size="8.5">rollback_flag&nbsp;=&nbsp;1</font>. A rolled-back switch is '
        'a first-class logged outcome, not an error, and its rate is one of the evaluation metrics '
        'in &sect;9.4.')]

F += [H2('4.5&nbsp;&nbsp;Operating modes')]
F += [P('Modes are the decision map made operational. Each fixes &alpha;, a ceiling on which tiers '
        'are permitted, and whether exploration runs. The analyser selects the mode; the planner '
        'works within it. Modes are ordered by pressure, except Opportunity, which is the one mode '
        'that moves <i>up</i>.')]
F += TBL(['Mode', '&alpha;', 'Entry condition', 'Effect on the spectrum'], [
    ['<b>M1 Full</b>', '0.75',
     'B&nbsp;&gt;&nbsp;60%, T&nbsp;&le;&nbsp;1, N&nbsp;=&nbsp;Online, W&nbsp;&gt;&nbsp;300&nbsp;s, '
     'device High-tier',
     'All tiers permitted. Exploration on. The configuration we compare everything else against.'],
    ['<b>M2 Balanced</b>', '0.55',
     'The default. Anything not matching another mode.',
     'Tiers 0&ndash;3 permitted; tier 4 only if the score clears the margin decisively. Exploration on.'],
    ['<b>M3 Frugal</b>', '0.35',
     'B below the user&rsquo;s personal threshold, or T&nbsp;=&nbsp;2, or &Delta;B above the dynamic '
     'boundary &theta;',
     'Tiers 0&ndash;2 only. Exploration on but restricted to tiers 0&ndash;2. Content prefetch '
     'suspended.'],
    ['<b>M4 Survival</b>', '0.15',
     'B&nbsp;&lt;&nbsp;12%, or T&nbsp;&ge;&nbsp;3, or memory pressure signalled by the platform',
     'Tiers 0&ndash;1 only. <b>Exploration off.</b> Language layer unloaded entirely. Cached '
     'ranking served where possible.'],
    ['<b>M5 Offline</b>', '&mdash;',
     'N&nbsp;=&nbsp;Offline. Overlays whichever mode is otherwise active.',
     'Gate G3 removes every network-touching model. The on-device spectrum continues to operate '
     'normally within whatever &alpha; applies.'],
    ['<b>M6 Opportunity</b>', '0.85',
     '&Delta;t&nbsp;&gt;&nbsp;5&nbsp;min <b>and</b> W&nbsp;&gt;&nbsp;600&nbsp;s <b>and</b> '
     'B&nbsp;&gt;&nbsp;50% <b>and</b> screen Active. Capped at 5&nbsp;minutes, then reverts.',
     'Tier ceiling lifted, &kappa; discounted by the enlarged W. This is the mode that '
     '<b>switches up</b>, and it exists because a delayed passenger with a charged phone is the '
     'highest-value moment LearnPerk sees.'],
], [23*mm, 12*mm, 51*mm, CW - 86*mm],
  caption='Table 4.3 &mdash; The six operating modes. M6 is the mode most easily forgotten in a '
          'resource-management design, and is where the commercial upside sits.', fs=7.8)

F += [H2('4.6&nbsp;&nbsp;The decision table')]
F += [P('Collapsing all of the above: each typed uncertainty maps to a tactic and an expected '
        'direction of movement. This table is the operational summary of the whole section, and the '
        'five use cases in &sect;7 are five traversals of it.')]
F += TBL(['Uncertainty', 'Raised when', 'Tactic', 'Direction'], [
    ['<font face="Courier" size="7.5">CONNECTIVITY_LOSS</font>',
     'N transitions to Offline or Degraded', 'Gate G3 fires; fall to the best offline-capable model; '
     'serve content from the cached pool', '<b>Down</b>, immediately, no dwell'],
    ['<font face="Courier" size="7.5">RESOURCE_PRESSURE</font>',
     'U, &Delta;B or T crosses a boundary, or B crosses the per-user threshold',
     'Enter Frugal or Survival; re-score under the lower &alpha;', '<b>Down</b>, one tier per tick'],
    ['<font face="Courier" size="7.5">WINDOW_CLOSING</font>',
     'W falls below the stage budget for the active model&rsquo;s p95',
     'Tighten the latency budget; gate G5 removes slow candidates; suppress content entirely below '
     '60&nbsp;s', '<b>Down</b>, latency-first'],
    ['<font face="Courier" size="7.5">COVERAGE_LOSS</font>',
     '&Phi; drops below the active model&rsquo;s declared minimum',
     'Switch to the model whose minimum feature set is satisfied &mdash; usually the sparse-signal '
     'sibling, not simply a lighter one', '<b>Sideways</b>'],
    ['<font face="Courier" size="7.5">QUALITY_DEGRADATION</font>',
     'EMA(C) or margin M falls below the boundary while resources are ample',
     'Switch to the highest-scoring feasible alternative, excluding the incumbent, exactly as '
     'HarmonE&rsquo;s strategy evaluator does', '<b>Up</b>, if affordable'],
    ['<font face="Courier" size="7.5">DRIFT</font>',
     '&Psi;&nbsp;&gt;&nbsp;0.25 on a top-10 feature',
     'Switch to the regime-specific model with the closest reference distribution; flag the cloud. '
     '<b>No on-device retraining.</b>', '<b>Sideways</b>'],
    ['<font face="Courier" size="7.5">OPPORTUNITY</font>',
     'The M6 composite condition holds', 'Raise &alpha; to 0.85, lift the tier ceiling, discount '
     '&kappa; against the enlarged window', '<b>Up</b>'],
    ['<font face="Courier" size="7.5">SERVE_FAILURE</font>',
     '&Omega;&nbsp;&ge;&nbsp;2 within one window', 'Blacklist for 90&nbsp;s, forced switch, log the '
     'rollback', '<b>Down</b>, immediately, no dwell'],
], [36*mm, 42*mm, CW - 114*mm, 21*mm],
  caption='Table 4.4 &mdash; The decision table. Note that three of eight tactics do not move down '
          'the spectrum. A switching engine that only ever switches down is a throttle, not an '
          'adaptation loop.', fs=7.1)
F += [PageBreak()]
