# -*- coding: utf-8 -*-
from base import *

# ===================== 8 =====================
F += [H1('8&nbsp;&nbsp;Words we used')]
F += [P('In case any of it was still fuzzy.', 'big')]
F += TBL(['Word', 'What it means here'], [
    ['<b>Model</b>', 'A small piece of software that makes one kind of decision &mdash; for '
     'example, which offer to show. It has learned patterns from past data. It is not a person and '
     'it is not the app; it is one component inside the app.'],
    ['<b>Model switching</b>', 'Swapping which model the app is using, while the app is running, '
     'without the commuter noticing. The subject of this whole document.'],
    ['<b>On the phone / on-device</b>', 'The model is stored on the phone and runs there. It does '
     'not send anything anywhere or wait for a reply. This is what lets it work in a tunnel.'],
    ['<b>Edge</b>', 'A slightly technical word for the same thing. &ldquo;At the edge&rdquo; means '
     'on the commuter&rsquo;s own device rather than on our servers.'],
    ['<b>Cached</b>', 'Already downloaded and sitting on the phone, ready to use. The Light content '
     'model works from cached articles, which is why it still works underground.'],
    ['<b>Level / tier</b>', 'Light, Standard or Strong. Three versions of the same job, from '
     'cheapest and simplest to most demanding and most capable.'],
    ['<b>Trigger</b>', 'The thing that causes a switch &mdash; losing signal, battery dropping, '
     'running out of journey.'],
    ['<b>Watch-only mode</b>', 'The app works out what it would switch to and writes it down, but '
     'does not actually switch. Lets us see how the rules behave without affecting anybody.'],
    ['<b>Flapping</b>', 'Switching back and forth rapidly because a reading is sitting right on a '
     'threshold. Something we specifically build against.'],
], [38*mm, CW-38*mm], fs=9.6)

F += [SP(6), RULEF(TEAL, 1.2)]
F += BOX('If you remember one thing',
    'The app has three versions of each model on the phone &mdash; a light one, a normal one and a '
    'strong one. It looks at the signal, the battery, how much journey is left and how well it '
    'knows the person, and it picks whichever version fits. It steps down when things get tight, '
    'steps up when there is a good moment, and there is always one that can run so the screen is '
    'never empty. <b>That is model switching.</b>',
    accent=AMBER, bg=colors.HexColor('#FBF4E8'))

F += [SP(4)]
F += [P('<b>Where to go next.</b> If you want the detailed version &mdash; the exact measurements '
        'behind each rule, the full list of models, how we would prove any of this &mdash; that is '
        'in <i>LearnPerk: Runtime Model Switching on the Edge Device</i>. This document is the '
        'short version of the same plan, and nothing in it contradicts that one.', 'p')]
