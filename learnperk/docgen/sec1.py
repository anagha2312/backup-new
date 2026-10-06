# -*- coding: utf-8 -*-
from common import *

F += [H1('1&nbsp;&nbsp;Why LearnPerk needs runtime switching at all')]
F += [P('Model switching is easy to argue for in the abstract and hard to justify in the '
        'particular. The abstract argument &mdash; edge devices are constrained, therefore adapt &mdash; '
        'is true of every phone application ever written and tells us nothing about LearnPerk. '
        'This section makes the particular argument, from the dataset we already hold.')]

F += [H2('1.1&nbsp;&nbsp;The evidence in our own data')]
F += [P('Every figure below is computed from <font face="Courier" size="8.5">combined_offers.csv</font> '
        '(9,990 impressions) and <font face="Courier" size="8.5">combined_content_views.csv</font> '
        '(19,334 views). They are not illustrative. They are the reason this document exists.')]

F += TBL(['#', 'Observation', 'Measured value', 'What it forces'], [
    ['1', 'A metro leg is mostly not online',
     'Of metro-leg impressions, only <b>41.6%</b> are <font face="Courier" size="8">Online</font>. '
     '<b>35.6%</b> are Degraded and <b>22.9%</b> are fully Offline. Tram, bus, rail and '
     'micromobility all sit near 90% online; metro is the outlier.',
     'Any model whose serving path touches the network is unavailable for the majority of metro '
     'time. Amsterdam&rsquo;s commuter core is metro. An offline-capable tier is not a fallback, '
     'it is the common case.'],
    ['2', 'Content stops when the network does',
     'Content views split 15,025 Online / 4,309 Degraded / <b>0 Offline</b>. Offers still appear '
     'offline (1,000 impressions); content never does.',
     'We have a hard capability hole, not a quality dip. An on-device content ranker over a cached '
     'item pool converts zero into something.'],
    ['3', 'The window is short, sometimes very short',
     'Leg duration: median <b>11.9 min</b>, 10th percentile <b>8.1 min</b>, and '
     '<b>8.6%</b> of legs under 8 minutes. Most commuters board mid-route, which shortens it further.',
     'A ranker whose p95 latency is 40&nbsp;ms is irrelevant on a 20-minute leg and decisive on a '
     'four-minute one. Remaining window must be a first-class switching metric, not a UI concern.'],
    ['4', 'One impression in five is on a low battery',
     '<b>19.8%</b> of impressions occur below 30% charge, <b>7.7%</b> below 20%. '
     '<font face="Courier" size="8">truth_battery_anxiety</font> sets a personal disengagement '
     'threshold between 20% and 40%, per commuter.',
     'Battery is not a uniform constraint. The trigger point is personal, so the threshold must be '
     'per-user rather than a global constant.'],
    ['5', 'Most of the fleet is not our dev phone',
     'Device mix is <b>30% Low-tier</b>, 45% Mid-tier, 25% High-tier. '
     '<b>5.8%</b> of impressions are low-tier <i>and</i> under 30% battery at the same moment.',
     'One model sized for a high-tier device is mis-sized for three quarters of the fleet. Sizing '
     'for low-tier throws capability away on the other 70%.'],
    ['6', 'Features go missing, predictably',
     '<font face="Courier" size="8">crowding_level</font> is null on <b>25%</b> of legs by design &mdash; '
     'GVB does not publish occupancy everywhere. <font face="Courier" size="8">accept_rate_before</font> '
     'is null on <b>17%</b> of impressions.',
     'Model choice must be conditioned on feature coverage. A model that needs crowding is the '
     'wrong model on a quarter of legs, however good it is elsewhere.'],
    ['7', 'Cold start is not an edge case',
     'Median tenure at impression is <b>169 days</b>, but the 10th percentile is <b>26 days</b> and '
     '25% of impressions have <b>one or fewer</b> prior offers seen. Cache is '
     '<font face="Courier" size="8">empty</font>, <font face="Courier" size="8">stale</font> or '
     '<font face="Courier" size="8">evicted</font> on <b>23%</b> of impressions.',
     'The sparse-signal path runs often enough to deserve its own model, rather than a degraded '
     'call into the rich-history one.'],
    ['8', 'Peak is a different operating regime',
     'Delay above five minutes: <b>12.6%</b> at peak against <b>5.9%</b> off-peak. High crowding: '
     '<b>25.1%</b> at peak against <b>9.2%</b> off-peak.',
     'Disruption clusters. The conditions that make a journey worth intervening in are the same '
     'conditions that load device and network hardest.'],
], [7*mm, 32*mm, 58*mm, CW - 97*mm],
  caption='Table 1.1 &mdash; Eight measured facts about LearnPerk journeys, each of which a single '
          'fixed model handles badly. Percentages are over impressions unless stated otherwise.',
  fs=7.8)

F += [H2('1.2&nbsp;&nbsp;What a single fixed model costs us')]
F += [P('Put those eight together and the shape of the problem is clear. Whatever single model we '
        'pick, we pick it for one operating point and then live with it at every other. Three '
        'failure modes follow, and each is a design failure rather than a tuning failure.')]
F += UL([
    '<b>Size for the best case</b> and the model is unserveable on a low-tier phone in a tunnel at '
    '18% battery &mdash; which, from rows 1, 4 and 5 of Table 1.1, describes a real and recurring '
    'slice of sessions. The commuter sees nothing, and we log nothing, so the failure never appears '
    'in the metrics that would tell us about it.',
    '<b>Size for the worst case</b> and we leave accuracy on the table for the other 70% of sessions. '
    'A commuter on a high-tier phone, on a 25-minute delayed tram at 74% battery, is the most '
    'valuable moment LearnPerk gets; we would serve it with the model we built for the tunnel.',
    '<b>Size for the average</b> and we get the worst of both: too heavy to survive the bad case, '
    'too light to exploit the good one. The average journey does not exist. The dictionary says so '
    'plainly &mdash; the departure-hour distribution is twin-peaked, and averaging it lands near '
    'midday, when almost nobody travels.',
])
F += [P('Switching is the answer to a problem that is about <i>variance</i>, not about average '
        'resource pressure. The device&rsquo;s operating point moves further within one twelve-minute '
        'leg than it does between two different commuters.')]

F += [H2('1.3&nbsp;&nbsp;What we take from each of the three papers')]
F += [P('This design is not novel for its own sake. Each mechanism below is taken from a published '
        'approach that has already been evaluated, then adapted where LearnPerk&rsquo;s problem '
        'genuinely differs. Where we depart, the departure is stated and argued.')]

F += TBL(['Source', 'Mechanism we adopt', 'How LearnPerk adapts it'], [
    ['<b>EdgeMLBalancer</b><br/><font size="7.3" color="#5A6772">arXiv:2502.06493<br/>'
     'Matathammal et&nbsp;al., 2025</font>',
     'A spectrum of four TFLite detectors on one Android device; a MAPE-K loop running at '
     '1&nbsp;Hz; CPU read from <font face="Courier" size="7.4">/proc/[pid]/stat</font>; a per-model '
     'score combining instantaneous and running-average cost against confidence; and '
     '<b>&epsilon;-greedy selection at &epsilon;&nbsp;=&nbsp;0.1</b> so no model starves. '
     'Reported: 17.36% mean accuracy at 19.90% CPU; fairness improved 43.6% over a naive threshold '
     'policy and 41.5% over round-robin; 0.85&nbsp;s mean switch time; 2.10&nbsp;mAh against '
     '5.25&nbsp;mAh for naive.',
     'We keep the spectrum, the 1&nbsp;Hz monitor, the &epsilon;-greedy fairness floor and the '
     'reference implementation&rsquo;s CPU probe. We <b>replace the score</b>: their '
     '<font face="Courier" size="7.4">S = min(U,&nbsp;U<sub>avg</sub>)&middot;(1&nbsp;&minus;&nbsp;C<sub>avg</sub>/C)</font> '
     'is minimised over a single cost channel (CPU) against a single quality channel (per-frame '
     'detection confidence). LearnPerk has four cost channels and no per-frame ground truth, so we '
     'move to an explicit weighted utility-minus-cost form (&sect;4.2). We also <b>add dwell-time '
     'hysteresis</b>: re-deciding at 1&nbsp;Hz with a 0.85&nbsp;s switch cost would let a '
     'twelve-minute leg spend a large share of itself mid-switch (&sect;2.3).'],
    ['<b>HarmonE</b><br/><font size="7.3" color="#5A6772">arXiv:2505.13693<br/>'
     'Bhatt et&nbsp;al., 2025</font>',
     'A design-time <b>Decision Map</b> binding sustainability goals to adaptation boundaries; a '
     'blended score <font face="Courier" size="7.4">S<sub>i</sub> = &alpha;A<sub>i</sub> + '
     '(1&minus;&alpha;)(1&minus;E<sub>avg,i</sub>)</font>; <b>EMA smoothing</b> so transient spikes do '
     'not trigger adaptation; a <b>control-theoretic dynamic threshold</b> '
     '<font face="Courier" size="7.4">&theta;<sub>i+1</sub> = &theta;<sub>i</sub> + '
     '&gamma;(E<sub>avg</sub>_ref &minus; E<sub>avg,i</sub>)</font> that tightens under sustained overspend and '
     'loosens for transient ones; drift detection against a reference distribution; and a versioned '
     'model repository so a past model can be <i>reused</i> rather than retrained. '
     'Reported: 54.5% less energy than LSTM with periodic retraining, at 95% of its accuracy and '
     '53.4% better inference time.',
     'We adopt the Decision Map as our <b>operating modes</b> (&sect;4.5), and the EMA, the dynamic '
     'boundary and the drift trigger essentially unchanged. We <b>drop the retraining arm</b>: '
     'retraining on a commuter&rsquo;s phone mid-journey is not credible, so a drift alarm at the '
     'edge switches to a different pre-trained model and raises a flag for the cloud instead. '
     'HarmonE&rsquo;s versioned repository becomes a small set of <b>regime-specific models</b> &mdash; '
     'peak, off-peak, disrupted &mdash; trained centrally and shipped ahead of time.'],
    ['<b>CALM</b><br/><font size="7.3" color="#5A6772">arXiv:2602.03632<br/>'
     'Jain et&nbsp;al., 2026</font>',
     'A fleet of domain-specialised SLMs in place of one general LLM; a routing score combining '
     '<b>static semantic similarity</b> (cosine between the query and each model&rsquo;s description) '
     'with <b>rolling runtime metrics</b> under a tunable weight <font face="Courier" size="7.4">k</font>; '
     'pro-latency, pro-energy, pro-confidence and pro-cache routing variants; an <b>LRU cache of '
     'models resident in memory</b> with the rest on disk; and FIFO scheduling chosen over STCF '
     'because STCF starves the slow models. Reported: 40&ndash;50% lower latency and 50&ndash;60% '
     'lower energy than single-LLM baselines, confidence 15&ndash;30% higher, and a cache size of '
     'one cutting peak VRAM from 32.5&nbsp;GB to 7.9&nbsp;GB.',
     'CALM is the direct template for our natural-language layer (Task&nbsp;E, &sect;5.6) &mdash; GVB '
     'bulletins, free-text preferences and mid-journey Q&amp;A. We take the similarity-plus-metrics '
     'routing score and the <b>cache-residency</b> mechanism nearly verbatim, because a phone has far '
     'less room than CALM&rsquo;s 48&nbsp;GB A6000: our cache size is <b>one</b> resident language '
     'model, so the eviction decision matters more, not less. We <b>invert the deployment '
     'assumption</b>: CALM holds every model on one server and routes across them, whereas we keep at '
     'most one language model warm and treat a cold start as a switching cost the score must pay '
     'for (&sect;5.7).'],
], [25*mm, 64*mm, CW - 89*mm],
  caption='Table 1.2 &mdash; Provenance of each mechanism and where LearnPerk departs from it. '
          'The reported figures are the original authors&rsquo;, measured on their own workloads; '
          'they motivate this design, they do not predict our results.', fs=7.5)

F += CALLOUT('The design claim in one sentence',
    'Take EdgeMLBalancer&rsquo;s per-device model spectrum and &epsilon;-greedy fairness floor, '
    'govern it with HarmonE&rsquo;s design-time goals and self-tightening boundaries, route the '
    'language tier with CALM&rsquo;s similarity-plus-metrics score under a cache of one &mdash; and '
    'then add the two things none of the three needed: a <b>remaining-journey-window</b> term, '
    'because the commuter gets off the train, and <b>dwell-time hysteresis</b>, because switching '
    'is not free.',
    accent=AMBER, bg=colors.HexColor('#FBF4E8'))
F += [PageBreak()]
