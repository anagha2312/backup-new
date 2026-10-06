# -*- coding: utf-8 -*-
from common import *

F += [H1('6&nbsp;&nbsp;What data each model needs')]
F += [P('The switching engine cannot choose a model it cannot feed. This section states, per task '
        'and per tier, which fields are required, which are optional, and what the declared minimum '
        'coverage is &mdash; the number gate&nbsp;G4 compares against. Every field named here already '
        'exists in the LearnPerk Data Dictionary; &sect;8 covers what has to be <i>added</i>.')]

F += [H2('6.1&nbsp;&nbsp;Feature sets by task')]
F += TBL(['Task / tier', 'Required fields', 'Optional (improves but not required)', 'Min. coverage'], [
    ['<b>A0</b>', '<font face="Courier" size="7.3">delay_minutes, duration_minutes, motion_state, '
     'battery_pct, connectivity_state</font>', 'none', '1.00, but all five are always present'],
    ['<b>A1</b>', 'A0 set plus <font face="Courier" size="7.3">crowding_level, is_peak, hour, '
     'board_stop_type, alight_stop_type, mode, screen_state, n_legs</font>',
     '&mdash;', '0.75 &mdash; tolerates the 25% null crowding'],
    ['<b>A2</b>', 'A1 set plus <font face="Courier" size="7.3">line_id, origin_zone, '
     'destination_zone, day_of_week</font> and the commuter&rsquo;s own history on this line',
     '<font face="Courier" size="7.3">ambient_location_precision</font>', '0.90'],
    ['<b>B0</b>', '<font face="Courier" size="7.3">age_cell, merchant_category, is_peak, '
     'discount_pct</font>', 'none', '1.00 &mdash; all four are known at impression time'],
    ['<b>B1</b>', 'B0 set plus <font face="Courier" size="7.3">detour_minutes, expiry_window_hours, '
     'position, tier_at_impression, tier_progress, mode, battery_pct, connectivity_state</font>',
     '<font face="Courier" size="7.3">crowding_level, delay_minutes</font>', '0.60'],
    ['<b>B2</b>', 'B1 set plus <font face="Courier" size="7.3">merchant_seen_before, '
     'offers_seen_before, occupation, household_type, traveler_archetype, home_zone, work_zone, '
     'merchant_zone, mcc, merchant_partner_type, purpose</font>',
     '<font face="Courier" size="7.3">accept_rate_before</font> (17% null), '
     '<font face="Courier" size="7.3">crowding_level</font> (25% null)', '0.70'],
    ['<b>B3</b>', 'B2 set plus <font face="Courier" size="7.3">offers_accepted_before, '
     'accept_rate_before, repeat_purchase_flag, points_balance_after, basket_value_eur</font> '
     'history, and the derived price-sensitivity and detour-tolerance estimates',
     '&mdash;', '0.90, and <font face="Courier" size="7.3">local_cache_state = fresh</font>'],
    ['<b>B4</b>', 'B3 set plus a trained commuter embedding, which needs at least 30 days of tenure '
     'and 20 resolved impressions', '&mdash;', '0.95, fresh cache, delegate present'],
    ['<b>C0</b>', '<font face="Courier" size="7.3">display_category</font> of cached items, declared '
     'onboarding interests, <font face="Courier" size="7.3">shown_at</font>', 'none', '1.00'],
    ['<b>C1</b>', 'C0 set plus the running taste vector and '
     '<font face="Courier" size="7.3">length_units, format, duration_minutes</font>',
     '<font face="Courier" size="7.3">iab_tier1</font>', '0.80'],
    ['<b>C2</b>', 'C1 set plus <font face="Courier" size="7.3">dwell_seconds, completion_state, '
     'bounced, reaction, position, hour, is_weekend</font> history',
     '<font face="Courier" size="7.3">has_reaction</font> (96% null &mdash; rare by design)', '0.70'],
    ['<b>C3</b>', 'C2 set plus precomputed item text embeddings', '&mdash;',
     '0.85, delegate, embeddings cached'],
    ['<b>D0</b>', '<font face="Courier" size="7.3">discount_pct</font> as configured by the merchant',
     'none', '1.00'],
    ['<b>D1</b>', '<font face="Courier" size="7.3">tier_progress, detour_minutes, '
     'expiry_window_hours, is_peak, merchant_category</font> plus the per-user arm posterior',
     '&mdash;', '0.80 and at least 20 resolved impressions'],
    ['<b>D2</b>', 'D1 set plus full purchase and points history and a centrally trained policy',
     '&mdash;', '0.90, fresh cache'],
    ['<b>E0</b>', 'The bulletin text, plus <font face="Courier" size="7.3">line_id</font> for '
     'relevance filtering', '<font face="Courier" size="7.3">language_preference</font>', '1.00'],
    ['<b>E1</b>', 'Query or bulletin text, plus the model description strings for routing',
     '&mdash;', '1.00'],
    ['<b>E2 / E3</b>', 'Query text, the structured journey facts E0 extracted, and the current '
     'offer and points state for grounding', 'Conversation history within the leg',
     '1.00 plus residency'],
    ['<b>E4</b>', 'As E2, plus a consent-checked and minimised context payload',
     '&mdash;', 'Online, consent, user-initiated'],
], [15*mm, CW - 110*mm, 50*mm, 45*mm], fs=7.4,
  caption='Table 6.1 &mdash; Feature sets and minimum coverage by tier. The minimum-coverage column '
          'is not decoration: it is the literal parameter gate&nbsp;G4 evaluates, and it is why a '
          'null <font face="Courier" size="7.3">crowding_level</font> routes to B2 rather than '
          'breaking B3.')

F += [H2('6.2&nbsp;&nbsp;Coverage, nulls and graceful degradation')]
F += [P('The Data Dictionary makes a point worth repeating here, because the whole coverage '
        'mechanism rests on it: <i>in this dataset a null is always meaningful &mdash; either '
        'consent said no, the event never happened, or a merchant did not disclose something. '
        'Filling nulls with zero collapses three different facts into one.</i> A switching engine '
        'that imputes zeros to keep a heavy model feasible is doing exactly the thing the dictionary '
        'warns against, and it will do it silently and confidently.')]
F += [P('So coverage is handled by routing, not by imputation. Three rules:')]
F += NL([
    '<b>A null below the minimum routes sideways, not down.</b> When '
    '<font face="Courier" size="8.5">crowding_level</font> is absent, the right move is not B3 to '
    'B2-because-it-is-cheaper; it is B3 to B2 <i>because B2 was trained without depending on that '
    'split</i>. Tier is a cost ordering; coverage is a capability question, and they are not the '
    'same axis.',
    '<b>Above the minimum, a shortfall is a discount.</b> A model at 0.75 coverage against a 0.70 '
    'minimum is feasible but penalised by <font face="Courier" size="8.5">w_p&nbsp;&middot;&nbsp;'
    '(1&nbsp;&minus;&nbsp;&Phi;)</font>, which is often enough to let a fully covered lighter model '
    'win outright. That is the correct outcome.',
    '<b>Structural nulls are declared, not discovered.</b> The registry records, per model, which '
    'fields are expected to be null and how often &mdash; 25% for crowding, 17% for '
    '<font face="Courier" size="8.5">accept_rate_before</font>, 84% for the whole purchase block '
    'on any single impression. A model surprised by a null it was told to expect is a model that '
    'was trained wrong.',
])
F += [P('One consequence deserves stating plainly. The commuters most likely to hit low coverage '
        '&mdash; new accounts, low-tier devices with evicted caches, offline metro legs &mdash; are '
        'exactly the commuters we most want to retain. The sparse-signal path is not a degraded '
        'service for unimportant users; it is the first experience most users have. B0 and C0 '
        'deserve the same design attention as B3.')]
F += [PageBreak()]
