# -*- coding: utf-8 -*-
import importlib, common
mods = ['sec0_cover','sec1','sec2','sec3','sec4','sec5','sec6','sec7','sec8','sec9','sec10']
for m in mods:
    try:
        importlib.import_module(m)
    except ModuleNotFoundError as e:
        if m in str(e):
            print('skip (not written yet):', m); continue
        raise
d = common.Doc('../LearnPerk_Runtime_Model_Switching.pdf',
               title='LearnPerk - Runtime Model Switching on the Edge Device',
               author='LearnPerk', subject='Edge AI model switching specification v1.0')
d.build(common.F)
print('PAGES OK ->', 'LearnPerk_Runtime_Model_Switching.pdf')
