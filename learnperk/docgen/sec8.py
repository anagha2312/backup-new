# -*- coding: utf-8 -*-
from common import *

F += [H1('8&nbsp;&nbsp;What this changes in the Data Dictionary')]
F += [P('The v3 document anticipated that the data model would move once switching was specified. '
        'This section says exactly how. Nothing proposed here removes or alters an existing column; '
        'the changes are three new edge files, one new reference table, and a set of additive '
        'columns on the four files that already exist.')]
F += [P('The organising principle is the one the current dictionary already follows: <b>one file '
        'per grain</b>. An inference and an impression cannot honestly share a row, because a single '
        'impression may be preceded by several inferences and a switch may occur with no impression '
        'at all. Forcing them together would produce exactly the dishonest join the dictionary '
        'warns against when it says content views and offer impressions each need their own file.')]

F += CALLOUT('Why this data has to exist at all',
    'Without it, every claim in &sect;7 is unfalsifiable. We could not say whether a switch helped, '
    'whether a refused upgrade was right, whether M6 earns its cost, or whether the engine is simply '
    'a throttle that happens to be described in adaptive language. The current dictionary records '
    'what the commuter did; it does not record <b>which model decided it</b>, so today an acceptance '
    'and a refusal are indistinguishable in the data. Adding '
    '<font face="Courier" size="8">serving_model_id</font> to the impression files is the single '
    'highest-value change in this section, and it is also the cheapest.',
    accent=AMBER, bg=colors.HexColor('#FBF4E8'))

F += [H2('8.1&nbsp;&nbsp;Three new edge files')]

F += [H3('8.1.1&nbsp;&nbsp;<font face="Courier" size="9.5">edge_model_inference_log.csv</font> '
         '&mdash; one row per inference call')]
F += [P('The finest grain in the system, and the only place per-call cost and confidence are '
        'recorded. High volume, so it is sampled: every call in the first 48 hours after install, '
        'every call under a triggered uncertainty, and a 5% sample otherwise.')]
F += TBL(['Column', 'Type', 'What it is'], [
    ['<font face="Courier" size="7.5">inference_id</font>', 'key', 'Primary key. One model call.'],
    ['<font face="Courier" size="7.5">user_id, leg_id, trip_id</font>', 'fk',
     'Joins to every existing file at the grain those files already use.'],
    ['<font face="Courier" size="7.5">task_id</font>', 'enum', 'A, B, C, D or E.'],
    ['<font face="Courier" size="7.5">model_id</font>', 'fk',
     'Joins to <font face="Courier" size="7.5">model_registry</font>. The answer to '
     '&ldquo;which model produced this?&rdquo;'],
    ['<font face="Courier" size="7.5">invoked_at</font>', 'timestamp',
     'Local Amsterdam time, matching every other file.'],
    ['<font face="Courier" size="7.5">latency_ms</font>', 'float',
     'Wall clock around the call. The metric <b>L</b>.'],
    ['<font face="Courier" size="7.5">cpu_pct, mem_mb, energy_mj</font>', 'float',
     'Metrics <b>U</b>, <b>R</b>, <b>E</b> at the moment of the call.'],
    ['<font face="Courier" size="7.5">confidence_top1, margin_top1_top2</font>', 'float',
     'Metrics <b>C</b> and <b>M</b>. Calibrated, per the registry&rsquo;s calibration version.'],
    ['<font face="Courier" size="7.5">n_candidates</font>', 'int',
     'Size of the candidate set. A margin means nothing without it.'],
    ['<font face="Courier" size="7.5">feature_coverage</font>', 'float',
     'Metric <b>&Phi;</b>, the realised value gate G4 compared against.'],
    ['<font face="Courier" size="7.5">features_missing</font>', 'string',
     'Semicolon-separated names of the null required fields &mdash; the same array convention the '
     'dictionary already uses for <font face="Courier" size="7.5">truth_taste_vector</font>.'],
    ['<font face="Courier" size="7.5">operating_mode</font>', 'enum', 'M1 to M6 at call time.'],
    ['<font face="Courier" size="7.5">connectivity_at_call, battery_at_call, thermal_status, '
     'cache_state_at_call</font>', 'mixed', 'Context snapshot. Duplicated from the leg deliberately, '
     'because leg-level values do not resolve a within-leg switch.'],
    ['<font face="Courier" size="7.5">delegate</font>', 'enum',
     '<font face="Courier" size="7.5">cpu</font>, <font face="Courier" size="7.5">nnapi</font>, '
     '<font face="Courier" size="7.5">gpu</font> or <font face="Courier" size="7.5">npu</font>. '
     'Metric <b>&Gamma;</b> as realised.'],
    ['<font face="Courier" size="7.5">was_cold_start</font>', 'bool',
     '1 if the model was loaded for this call. Separates steady-state cost from load cost, which is '
     'what makes &kappa; measurable rather than assumed.'],
    ['<font face="Courier" size="7.5">outcome_status</font>', 'enum',
     '<font face="Courier" size="7.5">served</font>, '
     '<font face="Courier" size="7.5">suppressed</font>, '
     '<font face="Courier" size="7.5">timeout</font>, '
     '<font face="Courier" size="7.5">error</font>, '
     '<font face="Courier" size="7.5">empty_candidates</font>. Feeds metric <b>&Omega;</b>. Five '
     'typed outcomes rather than one failure flag, following the '
     '<font face="Courier" size="7.5">confirmation_status</font> precedent.'],
    ['<font face="Courier" size="7.5">impression_id, view_id</font>', 'fk, nullable',
     'The downstream row this call produced, where it produced one. Null means suppressed or '
     'unsurfaced &mdash; meaningful, not zero.'],
], [56*mm, 14*mm, CW - 70*mm], fs=7.6,
  caption='Table 8.1 &mdash; <font face="Courier" size="7.5">edge_model_inference_log.csv</font>. '
          'Roughly 18 columns. This is the file that makes model comparison possible at all.')

F += [H3('8.1.2&nbsp;&nbsp;<font face="Courier" size="9.5">edge_switch_events.csv</font> '
         '&mdash; one row per switching decision')]
F += [P('One row for every decision the planner reaches, including the decisions to <b>hold</b> and '
        'the switches that <b>rolled back</b>. Recording only the switches that happened would make '
        'UC-5 &mdash; whose central event is a refusal &mdash; invisible.')]
F += TBL(['Column', 'Type', 'What it is'], [
    ['<font face="Courier" size="7.5">switch_id</font>', 'key', 'Primary key.'],
    ['<font face="Courier" size="7.5">user_id, leg_id, task_id</font>', 'fk / enum', 'Context.'],
    ['<font face="Courier" size="7.5">decided_at</font>', 'timestamp', 'When the planner decided.'],
    ['<font face="Courier" size="7.5">from_model_id, to_model_id</font>', 'fk',
     'Equal when <font face="Courier" size="7.5">decision_type = hold</font>.'],
    ['<font face="Courier" size="7.5">decision_type</font>', 'enum',
     '<font face="Courier" size="7.5">exploit</font>, '
     '<font face="Courier" size="7.5">explore</font>, '
     '<font face="Courier" size="7.5">gate_forced</font>, '
     '<font face="Courier" size="7.5">hold</font>, '
     '<font face="Courier" size="7.5">rollback</font>, '
     '<font face="Courier" size="7.5">mode_change</font>. Separating explore from exploit is what '
     'makes the &epsilon;-greedy fairness analysis possible at all.'],
    ['<font face="Courier" size="7.5">uncertainty_type</font>', 'enum',
     'The typed trigger from Table 4.4, or null for a routine re-score.'],
    ['<font face="Courier" size="7.5">trigger_metric, trigger_value, boundary_value</font>',
     'string, float, float',
     'Which metric fired, what it read, what it was compared against. This triple is what makes a '
     'switch <i>explainable</i>, and the decision map lists explainability as a goal.'],
    ['<font face="Courier" size="7.5">score_from, score_to, ema_delta, margin_required</font>',
     'float', 'Both sides of the comparison, plus &delta;. Lets us audit whether hysteresis is set '
     'well without re-running the device.'],
    ['<font face="Courier" size="7.5">kappa_charged</font>', 'float',
     'The amortised switch cost applied to the challenger. The number that distinguishes UC-3 from '
     'UC-5.'],
    ['<font face="Courier" size="7.5">window_remaining_s</font>', 'float', 'Metric <b>W</b>, the '
     '&kappa; denominator.'],
    ['<font face="Courier" size="7.5">mode_before, mode_after</font>', 'enum', 'M1 to M6.'],
    ['<font face="Courier" size="7.5">dwell_ms_before_switch</font>', 'int',
     'How long the incumbent held the binding. Tests &tau;.'],
    ['<font face="Courier" size="7.5">switch_latency_ms, memory_delta_mb</font>', 'float',
     'What the switch actually cost. EdgeMLBalancer reports 0.85&nbsp;s mean switch time as a '
     'headline result; this is the column that lets us state ours.'],
    ['<font face="Courier" size="7.5">rollback_reason</font>', 'enum, nullable',
     '<font face="Courier" size="7.5">warmup_failed</font>, '
     '<font face="Courier" size="7.5">warmup_too_slow</font>, '
     '<font face="Courier" size="7.5">oom</font>, or null.'],
], [56*mm, 22*mm, CW - 78*mm], fs=7.6,
  caption='Table 8.2 &mdash; <font face="Courier" size="7.5">edge_switch_events.csv</font>. '
          'Roughly 20 columns. Low volume: a handful of rows per leg.')

F += [H3('8.1.3&nbsp;&nbsp;<font face="Courier" size="9.5">edge_adaptation_state.csv</font> '
         '&mdash; one row per 5-second tick')]
F += [P('The time series the whole loop runs on, and the file that lets us replay a leg and ask why '
        'a switch did or did not happen. On-device it is a ring buffer holding the last 24 hours; '
        'it is uploaded in aggregate form on Wi-Fi, and in full only for commuters enrolled in the '
        'field trial of &sect;9.6.')]
F += TBL(['Column group', 'Columns', 'Notes'], [
    ['Keys', '<font face="Courier" size="7.5">tick_id, user_id, leg_id, observed_at</font>',
     'Sorted by <font face="Courier" size="7.5">observed_at</font>, like '
     '<font face="Courier" size="7.5">event_stream.csv</font>.'],
    ['Active bindings', '<font face="Courier" size="7.5">model_a, model_b, model_c, model_d, '
     'model_e</font>', 'One column per task rather than a JSON blob, so the file stays queryable '
     'without parsing.'],
    ['Mode and control', '<font face="Courier" size="7.5">operating_mode, alpha, epsilon_current, '
     'theta_energy, theta_latency</font>',
     'The live control state. <font face="Courier" size="7.5">theta_energy</font> is the dynamic '
     'boundary of &sect;4.3 &mdash; without logging it, a switch that a tightened boundary caused '
     'looks arbitrary.'],
    ['Group R', '<font face="Courier" size="7.5">cpu_pct, mem_model_mb, battery_pct, '
     'battery_drain_rate, thermal_status, energy_mj_window, delegate_available</font>',
     'Smoothed over the rolling window, except thermal, which is instantaneous because it gates.'],
    ['Group Q', '<font face="Courier" size="7.5">ema_score_active, confidence_ema, margin_ema, '
     'coverage, drift_psi, serve_failures_window</font>',
     '<font face="Courier" size="7.5">drift_psi</font> is computed against the reference '
     'distribution shipped with the active model.'],
    ['Group C', '<font face="Courier" size="7.5">connectivity_state, window_remaining_s, '
     'journey_stage, crowding_level, delay_minutes, cache_state, motion_state, screen_state, '
     'app_foreground_state, location_precision</font>',
     'Names deliberately match the existing dictionary exactly, so a join needs no translation '
     'layer.'],
    ['Raised', '<font face="Courier" size="7.5">uncertainties_raised</font>',
     'Semicolon-separated typed uncertainties for this tick. Empty on most ticks, which is itself '
     'the useful signal.'],
], [26*mm, 64*mm, CW - 90*mm], fs=7.6,
  caption='Table 8.3 &mdash; <font face="Courier" size="7.5">edge_adaptation_state.csv</font>. '
          'Roughly 35 columns at about 140 rows per median leg.')

F += [H2('8.2&nbsp;&nbsp;One new reference table')]
F += [P('<font face="Courier" size="9.5">model_registry.csv</font> is the static counterpart to the '
        'runtime files &mdash; the Knowledge component of &sect;2.2 written down. It is versioned '
        'with the app, and every <font face="Courier" size="8.5">model_id</font> in the three files '
        'above joins to it.')]
F += TBL(['Column', 'What it is'], [
    ['<font face="Courier" size="7.5">model_id, task_id, tier, family, version</font>',
     'Identity. <font face="Courier" size="7.5">family</font> is e.g. '
     '<font face="Courier" size="7.5">lightgbm</font>, '
     '<font face="Courier" size="7.5">logreg</font>, '
     '<font face="Courier" size="7.5">two_tower</font>, '
     '<font face="Courier" size="7.5">slm</font>, '
     '<font face="Courier" size="7.5">rule</font>.'],
    ['<font face="Courier" size="7.5">display_name, description</font>',
     'The human name, and the natural-language task description CALM-style routing computes cosine '
     'similarity against. For Task E this column is not documentation &mdash; it is an input.'],
    ['<font face="Courier" size="7.5">file_size_mb, peak_rss_mb, quantisation, delegate_required</font>',
     'Footprint. Feeds gates G1 and G6.'],
    ['<font face="Courier" size="7.5">p50_ms_low, p95_ms_low, p50_ms_mid, p95_ms_mid, p50_ms_high, '
     'p95_ms_high</font>',
     'Measured latency by device class. Six columns rather than one, because a single figure is '
     'meaningless across a 30/45/25 fleet split.'],
    ['<font face="Courier" size="7.5">energy_mj_per_call_low / _mid / _high</font>',
     'Measured energy by device class, calibrated once per tier.'],
    ['<font face="Courier" size="7.5">offline_capable, min_feature_set, min_coverage, '
     'expected_null_fields</font>',
     'Feeds gates G3 and G4. <font face="Courier" size="7.5">expected_null_fields</font> is the '
     'declaration that makes rule 3 of &sect;6.2 enforceable.'],
    ['<font face="Courier" size="7.5">switch_energy_mj_from</font>',
     'Load-and-warm cost, keyed by the outgoing model. The empirical basis for &kappa;.'],
    ['<font face="Courier" size="7.5">trained_on_version, reference_distribution_ref, '
     'calibration_version, ece_at_release</font>',
     'Provenance. <font face="Courier" size="7.5">reference_distribution_ref</font> points at the '
     'distribution the drift test compares against, which is HarmonE&rsquo;s versioned-repository '
     'idea reduced to one column.'],
    ['<font face="Courier" size="7.5">regime</font>',
     '<font face="Courier" size="7.5">general</font>, '
     '<font face="Courier" size="7.5">peak</font>, '
     '<font face="Courier" size="7.5">offpeak</font> or '
     '<font face="Courier" size="7.5">disrupted</font>. How the DRIFT tactic finds a sibling to '
     'switch to instead of retraining.'],
    ['<font face="Courier" size="7.5">min_tier_permitted_thermal, min_device_class</font>',
     'Hard eligibility, feeding gate G2.'],
], [62*mm, CW - 62*mm], fs=7.6,
  caption='Table 8.4 &mdash; <font face="Courier" size="7.5">model_registry.csv</font>, about 30 '
          'columns and as many rows as there are models &mdash; 20 under the spectrum proposed in '
          '&sect;5.')

F += [H2('8.3&nbsp;&nbsp;New columns on the four existing files')]
F += [P('All additive. No existing column changes meaning, and no existing null becomes a zero.')]
F += TBL(['File', 'New columns', 'Why'], [
    ['<font face="Courier" size="7.5">combined_offers.csv</font><br/>'
     '<font size="7" color="#5A6772">9,990 rows, 92 &rarr; 100 columns</font>',
     '<font face="Courier" size="7.5">serving_model_id, serving_model_tier, model_confidence, '
     'inference_latency_ms, operating_mode_at_impression, feature_coverage_at_impression, '
     'switch_within_leg_flag, fallback_reason</font>',
     'Without <font face="Courier" size="7.5">serving_model_id</font> the acceptance target cannot '
     'be attributed to a model, and every comparison in &sect;9 is impossible. '
     '<font face="Courier" size="7.5">fallback_reason</font> is nullable and populated only when the '
     'gate forced a model that was not the scored best &mdash; a null here means the engine got its '
     'first choice.'],
    ['<font face="Courier" size="7.5">combined_content_views.csv</font><br/>'
     '<font size="7" color="#5A6772">19,334 rows, 43 &rarr; 48 columns</font>',
     '<font face="Courier" size="7.5">serving_model_id, model_confidence, inference_latency_ms, '
     'operating_mode_at_view, from_cached_pool</font>',
     '<font face="Courier" size="7.5">from_cached_pool</font> is the column that will let us '
     'measure whether the offline content path of UC-1 works. Today the file has zero offline rows, '
     'so this column starts at zero by construction and its growth <i>is</i> the result.'],
    ['<font face="Courier" size="7.5">combined_users.csv</font><br/>'
     '<font size="7" color="#5A6772">2,000 rows, 49 &rarr; 58 columns</font>',
     '<font face="Courier" size="7.5">n_switches_total, n_rollbacks, pct_time_tier0, '
     'pct_time_tier3plus, modal_operating_mode, mean_inference_latency_ms, '
     'est_energy_mj_total, personal_battery_threshold, model_selection_entropy</font>',
     'Per-commuter summaries in the style the file already uses. '
     '<font face="Courier" size="7.5">model_selection_entropy</font> is the fairness measure: '
     'EdgeMLBalancer reports selection disparity as a headline result, and entropy over the '
     'selection distribution is the per-user version of it. '
     '<font face="Courier" size="7.5">personal_battery_threshold</font> is the learned value UC-2 '
     'turns on.'],
    ['<font face="Courier" size="7.5">event_stream.csv</font><br/>'
     '<font size="7" color="#5A6772">70,758 rows, 7 columns unchanged</font>',
     'No new columns. Four new <font face="Courier" size="7.5">event_type</font> values: '
     '<font face="Courier" size="7.5">model_switch</font>, '
     '<font face="Courier" size="7.5">mode_change</font>, '
     '<font face="Courier" size="7.5">drift_alarm</font>, '
     '<font face="Courier" size="7.5">serve_failure</font>.',
     'The existing schema already carries these cleanly: '
     '<font face="Courier" size="7.5">subject</font> takes the task, '
     '<font face="Courier" size="7.5">value</font> takes the trigger reading, and '
     '<font face="Courier" size="7.5">detail</font> takes the uncertainty type. Replaying a '
     'commuter&rsquo;s history in order then includes their switching history, which is exactly what '
     'the file is for.'],
], [34*mm, 58*mm, CW - 92*mm], fs=7.6,
  caption='Table 8.5 &mdash; Additive changes to the four existing files. Twenty-two new columns in '
          'total, and four new event types.')

F += [H2('8.4&nbsp;&nbsp;Retention, consent and privacy')]
F += [P('Four constraints, and they are constraints rather than guidance.')]
F += NL([
    '<b>Adaptation telemetry is device state, not behaviour.</b> CPU, memory, thermal and latency '
    'describe the phone, not the person, and are aggregated before upload. Group&nbsp;C metrics are '
    'different: journey stage and crowding are behavioural, and they inherit the same consent gate '
    'as every other behavioural row.',
    '<b>Consent withdrawal removes switching rows too.</b> The dictionary is unambiguous that an '
    'opted-out commuter has <i>no behavioural rows anywhere in the dataset, not blank ones</i>, and '
    'that no event exists after <font face="Courier" size="8.5">withdrawal_at</font>. The three new '
    'files follow the same rule without exception.',
    '<b>Retention is tiered.</b> '
    '<font face="Courier" size="8.5">edge_adaptation_state</font> is a 24-hour on-device ring '
    'buffer, uploaded in aggregate; '
    '<font face="Courier" size="8.5">edge_model_inference_log</font> is sampled and kept 30 days; '
    '<font face="Courier" size="8.5">edge_switch_events</font> is low-volume and kept 90 days, '
    'because the switching analysis needs a longer baseline than the raw telemetry does.',
    '<b>Nothing here is a new personal data category.</b> Every Group&nbsp;C field already exists in '
    'the dictionary. What is new is the record of <i>which model read them</i>, which is metadata '
    'about our system rather than additional data about the commuter &mdash; and it is what makes '
    'the explainability goal in the decision map deliverable rather than aspirational.',
])
F += [PageBreak()]
