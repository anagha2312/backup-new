# -*- coding: utf-8 -*-
import importlib, abase
for m in ['a1', 'a2', 'a3', 'a4']:
    importlib.import_module(m)
d = abase.Doc('../../LearnPerk_Architecture_And_Metrics.pdf',
              title='LearnPerk - How it fits together, and how we will know it works',
              author='LearnPerk')
d.build(abase.F)
print('BUILT')
