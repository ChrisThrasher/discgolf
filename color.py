import matplotlib as mpl
import numpy as np

#fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
def colorFader(c1,c2,mix=0):
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)
fadeResolution = 500

WHITE       = (255, 255, 255)

LIGHT_GREY  = (185, 185, 185)
GREY        = ( 82,  82,  82)

DARK_GREEN  = ( 11,  61,  17)
GREEN       = ( 16, 122,  39)
LIGHT_GREEN = ( 16, 163,  48)

RED         = (176,  23,  12)

ORANGE      = (245, 168,  15)

YELLOW      = (227, 220,  32)

BLUE        = (  9,  84, 181)
