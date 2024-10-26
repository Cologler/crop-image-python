# -*- coding: utf-8 -*-
# 
# Copyright (c) 2024~2999 - Cologler <skyoflw@gmail.com>
# ----------
# 
# ----------

from typing import Annotated
from pathlib import Path

from typer import Typer, Argument, Option
from PIL import Image

from ._imgutils import split_image_by_color_difference

app = Typer()

def crop(
        source_path: Annotated[Path, Argument(file_okay=True, help='Source image file')],
        count: Annotated[int, Option(help='How many parts to split the image')],
        output_path: Annotated[Path | None, Argument(help='Output image file, omit will output with suffix .cropped.')] = None,
        pick: Annotated[int, Option(help='Which part to save (start by 0)')] = 0,
        take_all: Annotated[bool, Option('-a', '--all', help='Take all parts')] = False,
        min_width: Annotated[int, Option(help='Minimum image width')] = 50,
    ):

    if output_path is None:
        output_path = source_path.with_stem(f'{source_path.stem}.cropped')

    image = Image.open(source_path)
    images = split_image_by_color_difference(image, count=count, min_width=min_width)
    if take_all:
        for i, img in enumerate(images):
            img.save(output_path.with_stem(f'{output_path.stem}.{i}'))
    else:
        images[pick].save(output_path)

app.command()(crop)
