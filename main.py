import os
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from mpl_toolkits.axes_grid1 import host_subplot
import numpy as np


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


host = host_subplot(111)
par = host.twiny()
host.set_title("EVE Echoes Targeting Speed Calculator", y=1.2)
plt.subplots_adjust(left=0.25, bottom=0.30, top=0.8)

fSigRad = 35.0
fScanRes = 115.0
delta_f = 1.0
t = np.arange(fScanRes - fScanRes / 4.0, fScanRes + fScanRes / 4.0, 1.0)
tt = np.arange(fSigRad - fSigRad / 4.0, fSigRad + fSigRad / 4.0, 1.0)
s = (40000.0 / (t * np.power(np.arcsinh(fSigRad), 2)))

host.margins(x=0)
host.set_ylabel("Targetlock Speed (sec)", color='green')
host.set_xlabel("Scan Resolution (mm)", color='blue')
par.set_xlabel("Signature Radius (m)", color='blue')

host.set_xlim(t[0], t[-1])
par.set_xlim(tt[0], tt[-1])
host.set_ylim((40000.0 / (t[0] * np.power(np.arcsinh(fSigRad), 2))),
              (40000.0 / (t[-1] * np.power(np.arcsinh(fSigRad), 2))))
l, = host.plot(t, s, lw=2, color='green')

axcolor = 'lightgoldenrodyellow'
scanRes = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
sigRad = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

sRes = Slider(
    scanRes,
    'Scan Resolution (mm)',
    1.0,
    1000.0,
    valinit=fScanRes,
    valstep=delta_f)
sRad = Slider(
    sigRad,
    'Signature Radius (m)',
    1.0,
    1000.0,
    valinit=fSigRad,
    valstep=delta_f)


def update(val):
    res = sRes.val
    rad = sRad.val
    t = np.arange(res - res / 4.0, res + res / 4.0, 1.0)
    host.set_xlim(t[0], t[-1])
    host.set_ylim((40000.0 / (t[0] * np.power(np.arcsinh(rad), 2))),
                  (40000.0 / (t[-1] * np.power(np.arcsinh(rad), 2))))
    tt = np.arange(rad - rad / 4.0, rad + rad / 4.0, 1.0)
    par.set_xlim(tt[0], tt[-1])
    l.set_ydata((40000.0 / (t * np.power(np.arcsinh(rad), 2))))
    l.set_xdata(t)


sRes.on_changed(update)
sRad.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def reset(event):
    sRes.reset()
    sRad.reset()


button.on_clicked(reset)

plt.show()
