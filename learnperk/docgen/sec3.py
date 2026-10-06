# -*- coding: utf-8 -*-
from common import *

F += [H1('3&nbsp;&nbsp;The metrics &mdash; what we measure and why')]
F += [P('This is the section the rest of the document depends on. A switching decision is only as '
        'defensible as the evidence behind it, and the evidence is these metrics. Each one below is '
        'given with its symbol, how it is obtained, how often, what it costs to read, and &mdash; the '
        'part that matters &mdash; <b>which switching decision it can actually justify</b>. A metric '
        'that cannot change a decision does not belong in the loop, however interesting it is.')]
F += [P('The metrics fall into three groups. <b>Group R</b> is resource and device state: what the '
        'phone can afford. This is EdgeMLBalancer&rsquo;s territory, extended past CPU. <b>Group Q</b> '
        'is model quality: whether the model we are running is still any good. This is '
        'HarmonE&rsquo;s territory. <b>Group C</b> is journey and context: what the situation is '
        'worth and how long it will last. This group has no equivalent in any of the three papers, '
        'because none of them had a user who gets off a train.')]

# ---------- Group R ----------
F += [H2('3.1&nbsp;&nbsp;Group R: resource and device')]
F += TBL(['Sym', 'Metric', 'Source and cadence', 'Decision it justifies'], [
    ['<b>U</b>', 'CPU utilisation, process-attributed, %',
     'Delta of <font face="Courier" size="7.4">utime+stime</font> from '
     '<font face="Courier" size="7.4">/proc/self/stat</font> over a 100&nbsp;ms interval, clamped to '
     '[0,100]. Exactly the probe in the EdgeMLBalancer reference implementation. 1&nbsp;Hz. Cost '
     '&lt;&nbsp;0.5&nbsp;ms.',
     'The primary <b>switch-down</b> signal for compute-bound tasks. Sustained '
     '<font face="Courier" size="7.5">U</font> above the mode ceiling moves Task&nbsp;B and '
     'Task&nbsp;C down one tier.'],
    ['<b>R</b>', 'Resident memory attributable to models, MB',
     '<font face="Courier" size="7.4">Debug.MemoryInfo.getTotalPss()</font> minus a measured '
     'baseline, plus the registry&rsquo;s declared footprint for each loaded model. 5&nbsp;s.',
     'A <b>hard gate</b>, not a score term. If loading a candidate would exceed the mode ceiling '
     '(Table&nbsp;2.2), the candidate is infeasible regardless of how good it is. Also drives cache '
     'eviction in Task&nbsp;E.'],
    ['<b>B</b>', 'Battery charge, %',
     '<font face="Courier" size="7.4">BatteryManager.BATTERY_PROPERTY_CAPACITY</font>. 5&nbsp;s. '
     'Free.',
     'Crosses a <b>per-user</b> threshold learned from that commuter&rsquo;s own past disengagement, '
     'in the 20&ndash;40% band the dictionary documents. Triggers the step down to Frugal, then '
     'Survival mode.'],
    ['<b>&Delta;B</b>', 'Battery drain rate, %/hour',
     'Least-squares slope of <font face="Courier" size="7.5">B</font> over the last 10 minutes, '
     'attributed to LearnPerk by differencing against screen-off idle. 60&nbsp;s.',
     'Tests the environmental boundary directly. Feeds the <b>dynamic threshold</b> of &sect;4.3: '
     'sustained overspend tightens the boundary, a one-off spike does not.'],
    ['<b>E</b>', 'Estimated energy per inference, mJ',
     'CPU-time of the call multiplied by a per-device-class power coefficient calibrated once per '
     'device tier, plus a fixed cost for a delegate hand-off. Per call.',
     'The cost channel that makes models comparable across tiers. Replaces the crude '
     '<font face="Courier" size="7.5">battery&nbsp;&times;&nbsp;CPU/100</font> proxy the '
     'EdgeMLBalancer code uses, which conflates a level with a rate.'],
    ['<b>T</b>', 'Thermal status, 0&ndash;6',
     '<font face="Courier" size="7.4">PowerManager.getCurrentThermalStatus()</font>. 5&nbsp;s. Free.',
     'A <b>hard gate</b>. At <font face="Courier" size="7.5">MODERATE</font> (2) all tier-3 and '
     'above models become infeasible; at <font face="Courier" size="7.5">SEVERE</font> (3) only '
     'tier-0 and tier-1 survive. Thermal throttling makes latency estimates worthless, so we stop '
     'trusting the score and fall back to the gate.'],
    ['<b>L</b>', 'Inference latency, ms (p50 and p95)',
     'Wall clock around the inference wrapper, kept as a reservoir per model. Per call.',
     'The responsiveness boundary. p95 &mdash; not the mean &mdash; is compared against the stage '
     'budget, because a commuter notices the slow call, not the average call.'],
    ['<b>D</b>', 'Device performance class',
     '<font face="Courier" size="7.4">device_performance_class</font>, resolved once at install '
     'from SoC, core count and RAM. Static.',
     'Selects which <b>column</b> of the model registry applies. A registry latency figure is '
     'meaningless without it: the fleet is 30/45/25 low/mid/high.'],
    ['<b>&Gamma;</b>', 'Delegate availability',
     'Whether NNAPI, GPU or an NPU delegate initialises successfully, probed once per session and '
     'after any failure. Session-scoped.',
     'A <b>hard gate</b> on the neural tiers. A model that needs a delegate and cannot get one is '
     'not a slow model, it is an absent one.'],
], [11*mm, 30*mm, 57*mm, CW - 98*mm],
  caption='Table 3.1 &mdash; Group R. Note that three of the nine (R, T, &Gamma;) act as gates '
          'rather than score terms. Gates are checked first and cannot be traded away, which is what '
          'stops the loop from optimising itself into a crash.', fs=7.7)

# ---------- Group Q ----------
F += [H2('3.2&nbsp;&nbsp;Group Q: model quality')]
F += [P('The hard problem in this group is that LearnPerk has no per-call ground truth. '
        'EdgeMLBalancer could read a detection confidence off every frame; HarmonE could compute an '
        'R&sup2; against an observed traffic count within minutes. We learn whether an offer was good '
        'only when the commuter accepts or ignores it, and '
        '<font face="Courier" size="8.5">latency_minutes</font> in the dictionary is bimodal &mdash; '
        'most act within minutes, a second group redeems just before expiry, with a maximum of '
        '1,419&nbsp;minutes. So the feedback for some decisions arrives a day later, on a different '
        'leg, possibly on a different network.')]
F += [P('We therefore split Group Q into an <b>immediate</b> proxy available at inference time and '
        'a <b>delayed</b> truth used to correct the proxy offline. The loop switches on the proxy '
        'and is audited on the truth.')]

F += TBL(['Sym', 'Metric', 'Availability', 'Decision it justifies'], [
    ['<b>C</b>', 'Top-1 calibrated confidence &mdash; the model&rsquo;s own probability for the item '
     'it ranked first',
     '<b>Immediate.</b> Per call.',
     'The direct analogue of EdgeMLBalancer&rsquo;s per-frame confidence, and the main quality term '
     'in the score. Must be <i>calibrated</i> per model, or a tier that is merely more confident '
     'beats a tier that is more correct.'],
    ['<b>M</b>', 'Ranking margin &mdash; the gap between the top-1 and top-2 scores',
     '<b>Immediate.</b> Per call.',
     'Detects the case a raw confidence hides: the model is sure of its number but cannot separate '
     'the candidates. A collapsed margin over the window is evidence that a <b>heavier</b> model is '
     'warranted, not a lighter one.'],
    ['<b>&Phi;</b>', 'Feature coverage &mdash; share of the model&rsquo;s required features that are '
     'non-null for this call',
     '<b>Immediate.</b> Per call.',
     'A <b>gate plus a penalty</b>. Below the model&rsquo;s declared minimum coverage it is '
     'infeasible; above it, a shortfall discounts the score proportionally. This is how the 25% of '
     'legs with no <font face="Courier" size="7.5">crowding_level</font> and the 17% with no '
     '<font face="Courier" size="7.5">accept_rate_before</font> are handled as first-class cases.'],
    ['<b>A<sub>avg</sub></b>', 'Realised acceptance rate over a rolling 200 impressions, per model',
     '<b>Delayed</b> by minutes to a day.',
     'The truth the proxy is audited against. Enters the live score only through a slow-moving '
     'per-model prior, never as a fast signal, because reacting to it inside a leg would be reacting '
     'to yesterday.'],
    ['<b>ECE</b>', 'Expected calibration error over the rolling window',
     '<b>Delayed.</b> Recomputed nightly.',
     'If a model&rsquo;s confidence stops meaning what it claims, <font face="Courier" size="7.5">C</font> '
     'becomes unusable for that model. A high ECE demotes the model in the registry until the cloud '
     'ships a recalibrated version.'],
    ['<b>&Psi;</b>', 'Feature drift &mdash; PSI between the live feature distribution and the '
     'reference shipped with the model',
     '<b>Immediate</b> at window granularity.',
     'HarmonE&rsquo;s drift trigger. <font face="Courier" size="7.5">&Psi;&nbsp;&gt;&nbsp;0.25</font> '
     'on any top-10 feature raises <font face="Courier" size="7.5">DRIFT</font>. At the edge this '
     '<b>switches to the regime-specific model</b> whose reference distribution is closest &mdash; '
     'it never retrains &mdash; and flags the cloud.'],
    ['<b>&Omega;</b>', 'Serve-failure count &mdash; calls that timed out, threw, or returned an '
     'empty candidate set',
     '<b>Immediate.</b> Per call.',
     'Two failures inside one window blacklist the model for 90&nbsp;s and force a switch down, '
     'bypassing dwell time. A model that does not answer is worse than a weaker model that does.'],
], [11*mm, 40*mm, 24*mm, CW - 75*mm],
  caption='Table 3.2 &mdash; Group Q. The immediate/delayed split is the honest response to '
          'LearnPerk having no per-call ground truth; pretending otherwise would put a day-old '
          'signal inside a five-second loop.', fs=7.7)

# ---------- Group C ----------
F += [H2('3.3&nbsp;&nbsp;Group C: journey and context')]
F += [P('This group is what makes the document LearnPerk-specific rather than a restatement of '
        'EdgeMLBalancer. A traffic camera runs until someone turns it off. A commuter&rsquo;s '
        'session has a known, short, measurable end, and the value of the session is not uniform '
        'across it. Both facts belong in the switching decision.')]

F += TBL(['Sym', 'Metric', 'Source', 'Decision it justifies'], [
    ['<b>N</b>', 'Connectivity state: Online / Degraded / Offline',
     '<font face="Courier" size="7.4">ConnectivityManager</font> plus an active reachability probe; '
     '<font face="Courier" size="7.4">connectivity_state</font>. 5&nbsp;s.',
     'The single most consequential gate we have. Offline makes every cloud-assisted tier infeasible '
     'instantly, with no dwell-time grace. On metro legs this fires on <b>22.9%</b> of impressions, '
     'and Degraded on a further 35.6%.'],
    ['<b>W</b>', 'Remaining window, seconds',
     'Leg <font face="Courier" size="7.4">duration_minutes</font> less elapsed, corrected by live '
     '<font face="Courier" size="7.4">delay_minutes</font> and by '
     '<font face="Courier" size="7.4">journey_stage</font>. 5&nbsp;s.',
     'Two roles. It sets the <b>latency budget</b> (tight when W is small), and it is the '
     '<b>denominator that amortises the switch cost</b> &sect;2.3. With a median leg of 11.9 minutes '
     'and 8.6% under 8 minutes, this is not a rare consideration.'],
    ['<b>S</b>', 'Journey stage: waiting / boarding / in-transit / approaching / interchange / alighting',
     'Derived from vehicle position, motion state and the GVB feed. 5&nbsp;s.',
     'Selects the latency budget and the appropriate interaction. <font face="Courier" size="7.5">interchange</font> '
     'is the high-value, low-window stage; <font face="Courier" size="7.5">in-transit</font> is the '
     'long-window stage where a heavy model can earn its cost.'],
    ['<b>X</b>', 'Crowding level: Low / Medium / High, or null',
     '<font face="Courier" size="7.4">crowding_level</font> from GVB. <b>Null on 25% of legs by '
     'design.</b>',
     'Part of the <font face="Courier" size="7.5">OPPORTUNITY</font> composite. High crowding at '
     'peak reaches 25.1% of impressions. Its nullability is exactly why '
     '<font face="Courier" size="7.5">&Phi;</font> exists.'],
    ['<b>&Delta;t</b>', 'Delay, minutes',
     '<font face="Courier" size="7.4">delay_minutes</font>, actual minus scheduled. 5&nbsp;s.',
     'The other half of <font face="Courier" size="7.5">OPPORTUNITY</font>: delay lengthens '
     '<font face="Courier" size="7.5">W</font> and raises attention at once. Above five minutes on '
     '12.6% of peak impressions.'],
    ['<b>K</b>', 'Local cache state: fresh / stale / empty / evicted',
     '<font face="Courier" size="7.4">local_cache_state</font>. 5&nbsp;s.',
     'A gate on the rich-history tiers, which cannot compute their features from an empty cache. '
     'Non-fresh on <b>23%</b> of impressions; low-tier devices are evicted more often, so this '
     'correlates with <font face="Courier" size="7.5">D</font>.'],
    ['<b>H</b>', 'History depth: prior impressions and tenure',
     '<font face="Courier" size="7.4">offers_seen_before</font>, '
     '<font face="Courier" size="7.4">tenure_days_at_impression</font>. Per call.',
     'Routes between the sparse-signal and rich-history models. At the 25th percentile a commuter '
     'has seen <b>one or fewer</b> prior offers, so this route is well travelled.'],
    ['<b>&sigma;</b>', 'Screen, foreground and motion state',
     '<font face="Courier" size="7.4">screen_state</font>, '
     '<font face="Courier" size="7.4">app_foreground_state</font>, '
     '<font face="Courier" size="7.4">motion_state</font>. 5&nbsp;s.',
     'Gates whether to spend anything at all. Locked or backgrounded &mdash; and the app is '
     'backgrounded on <b>51.6%</b> of impressions &mdash; drops every task to its cheapest tier or '
     'suspends it, because nothing will be seen.'],
    ['<b>&rho;</b>', 'Location precision: GPS-confirmed / Inferred',
     '<font face="Courier" size="7.4">ambient_location_precision</font>. 5&nbsp;s.',
     'A confidence qualifier, not a gate. Inferred location (32.4% of impressions) discounts the '
     'score of any model whose leading features are geographic, such as '
     '<font face="Courier" size="7.5">detour_minutes</font>.'],
], [11*mm, 34*mm, 44*mm, CW - 89*mm],
  caption='Table 3.3 &mdash; Group C. Every row maps to a column that already exists in the '
          'LearnPerk Data Dictionary; nothing here needs new instrumentation on the data side, only '
          'new reading.', fs=7.7)

F += CALLOUT('The metric that does not exist in any of the three papers',
    '<b>W, the remaining window.</b> EdgeMLBalancer optimises a stream with no end. HarmonE forecasts '
    'a sensor that never stops. CALM serves a queue that refills. LearnPerk has a commuter who '
    'alights in four minutes, and after that every millisecond of inference was wasted regardless of '
    'how accurate it was. Making W a first-class term is the single largest adaptation this design '
    'makes to the published work, and it is what turns an abstract efficiency argument into a '
    'concrete one: a model is efficient here if it produces an answer <i>the commuter is still '
    'present to receive</i>.',
    accent=AMBER, bg=colors.HexColor('#FBF4E8'))

F += [H2('3.4&nbsp;&nbsp;Sampling, aggregation and smoothing')]
F += [P('Raw metrics are not fed to the planner. Each is aggregated over the rolling window of '
        'n&nbsp;=&nbsp;12 ticks, in the manner HarmonE prescribes, and each is normalised to [0,1] '
        'against a per-device-class reference so that a CPU percentage and a latency in '
        'milliseconds can appear in the same weighted sum without one silently dominating.')]
F += EQ('window mean   :  x_avg   =  (1/n) * SUM( x_i ,  i = 1 .. n )',
        'normalise     :  x_norm  =  clip( (x - x_min) / (x_max - x_min), 0, 1 )',
        'smooth        :  EMA_i   =  beta * x_i  +  (1 - beta) * EMA_(i-1) ,   beta = 0.30')
F += [SP(4)]
F += [P('Three details are worth stating because they are easy to get wrong. First, the '
        'normalisation bounds are <b>per device class</b>: 40% CPU means something different on a '
        'low-tier phone than on a high-tier one, and a shared bound would make the loop behave '
        'differently on 30% of the fleet for no principled reason. Second, latency is aggregated as '
        'a <b>p95 reservoir, not a mean</b>, because the responsiveness boundary is about the tail. '
        'Third, gates are evaluated on the <b>instantaneous</b> reading rather than the smoothed '
        'one: smoothing a connectivity loss over 30 seconds means serving 30 seconds of failures, '
        'which is exactly the failure mode EMA smoothing is supposed to prevent elsewhere.')]
F += [PageBreak()]
