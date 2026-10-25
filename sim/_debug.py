import numpy as np
d = np.load('rtl_dump.npz', allow_pickle=True)
print('dump shapes:')
for k in d.keys():
    print(f'  {k}: shape={d[k].shape}, dtype={d[k].dtype}')
print()
print(f'height in dump: {int(d["height"])}, width: {int(d["width"])}')
in_vsync_locs = np.where(d['in_vsync']==1)[0]
print(f'i_VSYNC positions: {in_vsync_locs.tolist()}')
print(f'i_VSYNC gaps: {np.diff(in_vsync_locs).tolist()}')
print()
in_y0 = d['in_y0']
in_blank = d['in_blank']
print(f'in_blank around cycle 0..20:')
for c in range(0, 20):
    print(f'  cycle {c}: in_blank={int(in_blank[c])}, in_y0={int(in_y0[c])}')
print()
print(f'in_blank around cycle 6410..6460:')
for c in range(6410, 6460):
    print(f'  cycle {c}: in_blank={int(in_blank[c])}, in_y0={int(in_y0[c])}')
