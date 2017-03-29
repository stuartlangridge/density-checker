from fractions import Fraction
import os

css = """@media
only screen and (-webkit-min-device-pixel-ratio: {int_or_frac}),
only screen and (   min--moz-device-pixel-ratio: {int_or_frac}),
only screen and (     -o-min-device-pixel-ratio: {frac}),
only screen and (        min-device-pixel-ratio: {int_or_frac}),
only screen and (                min-resolution: {dpi}dpi),
only screen and (                min-resolution: {decimal}dppx) {{
  div {{ background-image: url(i{decimal}.png); }}
  p::after {{ content: "{decimal}"; }}
}}
"""

cmd = ("""convert -size 300x300 xc:lightblue """
    """-pointsize 124 -fill blue -gravity center -draw "text 0,0 '{0}'" """
    """-pointsize 28 -fill green -gravity center -draw "text 0,-80 'Screen density'" """
    """i{0}.png""")

densities = []

for f in range(10, 40):
    frac = Fraction(f, 10)
    decimal = float(frac)
    if decimal - int(decimal) == 0:
        int_or_frac = int(decimal)
    else:
        int_or_frac = str(frac)
    dpi = int(96 * decimal)

    densities.append(css.format(**{
        "int_or_frac": int_or_frac,
        "frac": str(frac),
        "decimal": decimal,
        "dpi": dpi
    }))

    scmd = cmd.format(decimal)
    os.system(scmd)

fp = open("index.tmpl")
data = fp.read().decode("utf-8").replace("/* densities here */", "\n".join(densities))
fp.close()
fp = open("index.html", mode="w")
fp.write(data.encode("utf-8"))
fp.close()
