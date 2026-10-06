# -*- coding: utf-8 -*-
import importlib, base
for m in ['p1', 'p2']:
    importlib.import_module(m)
d = base.Doc('../../LearnPerk_Model_Switching_Simple_Guide.pdf',
             title='LearnPerk - Model Switching on the Phone (plain-English guide)',
             author='LearnPerk')
d.build(base.F)
print('BUILT')
