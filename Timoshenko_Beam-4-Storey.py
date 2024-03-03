import numpy as np
import pandas as pd
from scipy import interpolate

num_f = 4              # Kat sayısı
num_h = 3.29           # (m) Kat yüksekliği
H = num_f * num_h      # (m) Bina yüksekliği
E = 200 * 10**6        # (kN/m2) Elastisite modülü
G = 77 * 10**6         # (kN/m2) Kayma modülü
mass = 150             # (t/kat)
Mt = 2 * mass * num_f  # (t) Toplam kütle (2 adet perde)
roA = mass / num_h     # (t/m) Kat yüksekliğine yayılan kütle

"""### Kolon Özellikleri ###"""
# HD400x287
Ic = 0.9971 * 10**(-3)    # (m4) Atalet momenti
Ac = 366.3 * 10**(-4)     # (m2) Alan
d = 0.393                 # (m)  Profil yüksekliği
Afl = 14603.4 * 10**(-6)  # (m2) Flanş alanı
Aweb = 8881.8 * 10**(-6)  # (m2) Gövde alanı
tweb = 22.6 * 10**(-3)    # (m)  Gövde kalınlığı

"""### Duvar Özellikleri ###"""
plw = 3      # (m) Levha genişliği
ptk = 0.003  # (m) Levha kalınlığı

"""### Deprem Parametreleri ###"""
Sa1 = 1.752008  # (m/s2) Spektral ivme
Sa2 = 2.819928  # (m/s2) Spektral ivme
Sa3 = 2.553271  # (m/s2) Spektral ivme
Sd1 = 0.016318  # (m) Spektral yer değiştirme
Sd2 = 0.002344  # (m) Spektral yer değiştirme
Sd3 = 0.000582  # (m) Spektral yer değiştirme

Q1 = Afl * (plw * 0.5 + d)
Q2 = Q1 + Aweb * 0.5 * (plw + d)
Q3 = Ac * 0.5 * (plw + d)
Q4 = Q3 + plw**2 * ptk / 8

beta1 = (Q1**2 + Q2**2) * d / tweb
beta2 = (Q3**2 + Q4**2) * plw / (2 * ptk)
beta = beta1 + beta2

Iw = (ptk * plw**3 / 12) + 2 * Ac * ((d + plw) / 2)**2 + 2 * Ic
# Iw: Yanal yüke dayanıklı sistemin bir parçası olan her duvar için, değiştirilmiş ikinci alan momenti
KGAw = (Iw**2 / beta) * G

r2 = E * Iw / (KGAw * H**2)

data = [[1.787,	 0.285,	0.102, 0.610, 0.190, 0.070,	1.570, 0.870, 0.510,  None,  None,  None],
        [2.171,	 0.575,	0.284, 0.687, 0.187, 0.049,	1.500, 0.690, 0.337, 1.792,	2.330, 2.440],
        [2.504,	 0.740,	0.383, 0.722, 0.162, 0.043,	1.460, 0.630, 0.310, 1.686,	2.380, 2.268],
        [2.801,	 0.866,	0.460, 0.743, 0.145, 0.040,	1.430, 0.590, 0.290, 1.654,	2.345, 2.202],
        [3.070,	 0.971,	0.526, 0.756, 0.134, 0.039,	1.410, 0.560, 0.290, 1.651,	2.230, 2.168],
        [3.319,	 1.064,	0.584, 0.765, 0.127, 0.038,	1.390, 0.540, 0.280, 1.660,	2.257, 2.147],
        [3.550,	 1.148,	0.637, 0.772, 0.121, 0.038,	1.380, 0.530, 0.280, 1.674,	2.222, 2.132],
        [3.768,	 1.226,	0.686, 0.777, 0.117, 0.037,	1.370, 0.510, 0.280, 1.689,	2.194, 2.122],
        [3.974,	 1.298,	0.731, 0.781, 0.113, 0.037,	1.360, 0.500, 0.280, 1.704,	2.170, 2.113],
        [4.170,	 1.367,	0.774, 0.785, 0.111, 0.037,	1.350, 0.500, 0.270, 1.719,	2.149, 2.106],
        [4.357,	 1.431,	0.814, 0.787, 0.108, 0.037,	1.343, 0.489, 0.274, 1.733,	2.132, 2.102],
        [5.913,	 1.961,	1.142, 0.801, 0.097, 0.036,	1.311, 0.454, 0.268, 1.827,	2.043, 2.080],
        [7.138,	 2.372,	1.395, 0.805, 0.093, 0.035,	1.299, 0.440, 0.266, 1.872,	2.009, 2.072],
        [8.183,	 2.722,	1.608, 0.808, 0.091, 0.035,	1.292, 0.433, 0.265, 1.899,	1.991, 2.068],
        [9.108,	 3.031,	1.796, 0.809, 0.090, 0.035,	1.288, 0.429, 0.265, 1.916,	1.980, 2.066],
        [9.947,	 3.312,	1.966, 0.810, 0.089, 0.035,	1.285, 0.426, 0.264, 1.928,	1.972, 2.064],
        [10.721, 3.570,	2.123, 0.811, 0.089, 0.035,	1.283, 0.424, 0.264, 1.937,	1.967, 2.063],
        [11.443, 3.811,	2.268, 0.811, 0.088, 0.035,	1.282, 0.422, 0.264, 1.944,	1.962, 2.062],
        [12.122, 4.038,	2.405, 0.812, 0.088, 0.035,	1.280, 0.421, 0.263, 1.949,	1.959, 2.061],
        [12.765, 4.252,	2.535, 0.812, 0.088, 0.035,	1.279, 0.420, 0.263, 1.954,	1.957, 2.060],
        [13.377, 4.456,	2.658, 0.812, 0.087, 0.035,	1.279, 0.419, 0.263, 1.957,	1.954, 2.060],
        [13.962, 4.652,	2.776, 0.813, 0.087, 0.035,	1.278, 0.418, 0.263, 1.960,	1.953, 2.060],
        [14.524, 4.839,	2.889, 0.813, 0.087, 0.035,	1.277, 0.418, 0.263, 1.963,	1.951, 2.059],
        [15.065, 5.019,	2.998, 0.813, 0.087, 0.035,	1.277, 0.417, 0.263, 1.965,	1.950, 2.059],
        [15.587, 5.194,	3.103, 0.813, 0.087, 0.035,	1.277, 0.417, 0.263, 1.967,	1.948, 2.058],
        [16.092, 5.362,	3.204, 0.813, 0.087, 0.035,	1.276, 0.416, 0.263, 1.969,	1.947, 2.058],
        [16.581, 5.525,	3.302, 0.813, 0.086, 0.035,	1.276, 0.416, 0.263, 1.970,	1.947, 2.058],
        [17.057, 5.684,	3.398, 0.813, 0.086, 0.035,	1.276, 0.416, 0.263, 1.972,	1.946, 2.058],
        [17.520, 5.838,	3.491, 0.814, 0.086, 0.035,	1.275, 0.415, 0.263, 1.973,	1.945, 2.058],
        [17.971, 5.988,	3.581, 0.814, 0.086, 0.035,	1.275, 0.415, 0.263, 1.974,	1.945, 2.058],
        [21.977, 7.324,	4.385, 0.810, 0.086, 0.035,	1.270, 0.410, 0.260, 1.980,	1.940, 2.060]]

index_r2 = [0.0,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9,
            1.0,  2.0,  3.0,  4.0,  5.0,  6.0,  7.0,  8.0,  9.0, 10.0,
            11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 30.0]

columns_r2 = ["S1", "S2", "S3", "em1", "em2", "em3", "disp1", "disp2", "disp3", "beta11", "beta21", "beta31"]

df = pd.DataFrame(data, index=index_r2, columns=columns_r2)

x = False
for i in index_r2:
    if i == r2:
        df = df.loc[r2]
        x = True

if x != True:
    df.loc[r2] = np.nan  # r2 değerine göre bilinmeyen satırı eklenmesi
    df = df.reindex(sorted(df.index), axis=0)  # Listenin r2 değeri ile tekrar sıralanması
    df = df.interpolate(method="polynomial", order=1).round(4)  # 1. derece polinom interpolasyonu
    df = df.loc[r2]

S1 = df.loc["S1"]
S2 = df.loc["S2"]
S3 = df.loc["S3"]

em1 = df.loc["em1"]
em2 = df.loc["em2"]
em3 = df.loc["em3"]

disp1 = df.loc["disp1"]
disp2 = df.loc["disp2"]
disp3 = df.loc["disp3"]

beta11 = df.loc["beta11"]
beta21 = df.loc["beta21"]
beta31 = df.loc["beta31"]

correction = [[0.492,  None,  None], [0.664, 0.704,  None], [0.749, 0.781, 0.751],
              [0.799, 0.821, 0.829], [0.833, 0.848, 0.860], [0.857, 0.868, 0.878],
              [0.875, 0.883, 0.892], [0.889, 0.895, 0.903], [0.900, 0.905, 0.912],
              [0.909, 0.913, 0.919], [0.917, 0.920, 0.925], [0.923, 0.926, 0.931],
              [0.928, 0.931, 0.935], [0.933, 0.935, 0.939], [0.937, 0.939, 0.943],
              [0.941, 0.943, 0.946], [0.944, 0.946, 0.949], [0.947, 0.948, 0.952],
              [0.950, 0.951, 0.954], [0.952, 0.953, 0.956], [0.954, 0.955, 0.958],
              [0.956, 0.957, 0.960], [0.958, 0.959, 0.962], [0.960, 0.960, 0.963],
              [0.961, 0.962, 0.965], [0.963, 0.963, 0.966], [0.964, 0.964, 0.967],
              [0.965, 0.966, 0.968], [0.967, 0.967, 0.969], [0.968, 0.968, 0.970]]

index_c = [1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
           11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
           21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

columns_c = ["Mode 1", "Mode 2", "Mode 3"]

df_c = pd.DataFrame(correction, index=index_c, columns=columns_c)

df_c = df_c.loc[num_f]
        
mode1 = df_c.loc["Mode 1"]
mode2 = df_c.loc["Mode 2"]
mode3 = df_c.loc["Mode 3"]

T1 = (S1 * H**2 / mode1) * (roA / (E * Iw))**0.5
T2 = (S2 * H**2 / mode2) * (roA / (E * Iw))**0.5
T3 = (S3 * H**2 / mode3) * (roA / (E * Iw))**0.5
print("T1 =", T1.round(3), "s")
print("T2 =", T2.round(3), "s")
print("T3 =", T3.round(3), "s")
print(" ")

Vb1 = em1 * Mt * Sa1
Vb2 = em2 * Mt * Sa2
Vb3 = em3 * Mt * Sa3
print("Vb1 =", Vb1.round(3), "kN")
print("Vb2 =", Vb2.round(3), "kN")
print("Vb3 =", Vb3.round(3), "kN")
print(" ")

Vb = (Vb1**2 + Vb2**2 + Vb3**2)**0.5
print("Vb =", Vb.round(3), "kN")
print(" ")

dmax1 = disp1 * Sd1
dmax2 = disp2 * Sd2
dmax3 = disp3 * Sd3
print("dmax1 =", dmax1.round(4), "m")
print("dmax2 =", dmax2.round(4), "m")
print("dmax3 =", dmax3.round(4), "m")
print(" ")

dmax = (dmax1**2 + dmax2**2 + dmax3**2)**0.5
print("dmax =", dmax.round(4), "m")
print(" ")

dr11 = beta11 * Sd1 / H
dr21 = beta21 * Sd2 / H
dr31 = beta31 * Sd3 / H
print("dr11 =", dr11.round(6))
print("dr21 =", dr21.round(6))
print("dr31 =", dr31.round(6))
print(" ")

drmax = (dr11**2 + dr21**2 + dr31**2)**0.5
print("drmax =", drmax.round(6))