import click
from PIL import Image
from PIL import ImageOps
from PIL import ImageChops
import numpy as np


@click.group()
def cli():
    pass


def save(image):
    OUTPUT = 'out.jpg'
    image.save(OUTPUT)


def convert_array_to_image(array):
    return Image.fromarray(np.uint8(array))


def convert_pil_to_array(image):
    return np.asarray(image)


@cli.command(short_help='resize image')
@click.argument('image', type=click.Path(exists=True), required=True)
@click.argument('size', type=click.Path(exists=True), required=True)
def resize(image, size):
    '''resize IMAGE SIZE. SIZE is tuple (width, height)'''
    image = Image.open(image)
    image.resize(size)
    save(image)


@cli.command(short_help='blend images')
@click.argument('image1', type=click.Path(exists=True), required=True)
@click.argument('image2', type=click.Path(exists=True), required=True)
@click.argument('alpha', default=0.5)
def blend(image1, image2, alpha):
    '''blend IMAGE1 and IMAGE2.'''
    image1 = Image.open(image1)
    image2 = Image.open(image2)
    blended_image = Image.blend(image1, image2, alpha)
    save(blended_image)


@cli.command(short_help='composite images')
@click.argument('image1', type=click.Path(exists=True), required=True)
@click.argument('image2', type=click.Path(exists=True), required=True)
@click.argument('mask', default=0.5)
def composite(image1, image2, mask):
    '''composite IMAGE1 and IMAGE2'''
    image1 = Image.open(image1)
    image2 = Image.open(image2)
    mask = Image.open(mask).convert('1')
    composited_image = Image.composite(image1, image2, mask)
    save(composited_image)


@cli.command()
def create():
    '''create tiny sample image'''
    array = np.eye(10) * 255
    image = convert_array_to_image(array)
    save(image)


@cli.command()
@click.argument('image', type=click.Path(exists=True), required=True)
@click.option('--equalize', '-e', is_flag=True)
def grayscale(image, equalize):
    image = Image.open(image)
    if equalize is True:
        image = ImageOps.equalize(image)
    image = image.convert("L")
    save(image)


@cli.command()
@click.argument('image', type=click.Path(exists=True), required=True)
@click.option('--equalize', '-e', is_flag=True)
def threshold(image, equalize):
    image = Image.open(image)
    if equalize is True:
        image = ImageOps.equalize(image)
    image = image.convert("L")
    image = image.point(lambda x: 0 if x < 230 else x)
    save(image)


@cli.command()
@click.argument('image', type=click.Path(exists=True), required=True)
def equalize(image):
    '''equalize image'''
    image = Image.open(image)
    image = ImageOps.equalize(image)
    save(image)


@cli.command()
@click.argument('image1', type=click.Path(exists=True), required=True)
@click.argument('image2', type=click.Path(exists=True), required=True)
def difference(image1, image2):
    image1 = Image.open(image1)
    image2 = Image.open(image2)
    print(ImageChops.difference(image1, image2).getbbox())


def main():
    cli()


if __name__ == '__main__':
    main()
