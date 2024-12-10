import subprocess

LEGACY_BASE = 48
BASE = 108


def logo_commands(scale, bw=False):
    return [
        f"anarch-re/assets/logo.png",
        *(
            [
                *["-fill", "white"],
                *["-opaque", "#f80000"],
                *["-background", "white"],
                *["-grayscale", "Rec601Luma"],
            ]
            if bw
            else [
                *["-transparent", "#f80000"],
                *["-background", "transparent"],
            ]
        ),
        *["-splice", "1x0"],
        *(
            [
                "-negate",
                *["-alpha", "shape"],
            ]
            if bw
            else []
        ),
        *["-scale", f"{scale * 100}%"],
    ]


def background_commands(dim):
    return [
        *["-size", f"{dim}x{dim}"],
        *["-define", "gradient:angle=-45"],
        f"gradient:#110000-#990000",
    ]


def mask_commands(dim, radius, padding):
    return [
        *["-size", f"{dim}x{dim}"],
        "xc:Black",
        *["-fill", "White"],
        *["-draw", f"circle {radius},{radius} {radius},{padding}"],
        *["-alpha", "Off"],
    ]


def generate_legacy_icon(scale, output):
    dim = scale * LEGACY_BASE
    radius = (dim - 1) / 2
    subprocess.run(
        [
            "magick",
            *["(", *background_commands(dim), ")"],
            *["(", *logo_commands(scale), ")"],
            *["-gravity", "center"],
            "-composite",
            *["(", *mask_commands(dim, radius, scale * 2), ")"],
            *["-compose", "CopyOpacity"],
            "-composite",
            output,
        ]
    )


def generate_adaptive_icon_foreground(scale, output, bw=False):
    subprocess.run(
        [
            "magick",
            *logo_commands(scale * 2, bw),
            *["-bordercolor", "transparent"],
            *["-border", f"{int(21*scale)}x{int(22*scale)}"],
            *([] if 21 * scale == int(21 * scale) else ["-splice", "1x0"]),
            output,
        ]
    )


def generate_adaptive_icon_background(scale, output):
    subprocess.run(
        [
            "magick",
            *background_commands(BASE * scale),
            output,
        ]
    )


DPIS = [
    ("mdpi", 1),
    ("hdpi", 1.5),
    ("xhdpi", 2),
    ("xxhdpi", 3),
    ("xxxhdpi", 4),
]


def icon_path(dpi, suffix=""):
    return f"app/src/main/res/mipmap-{dpi}/ic_launcher{suffix}.png"


for name, scale in DPIS:
    generate_legacy_icon(scale, icon_path(name))
    generate_adaptive_icon_foreground(scale, icon_path(name, "_foreground"))
    generate_adaptive_icon_background(scale, icon_path(name, "_background"))
    generate_adaptive_icon_foreground(scale, icon_path(name, "_monochrome"), bw=True)
