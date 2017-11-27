import click
from PIL import Image
from PIL import ImageOps
from PIL import ImageChops
import numpy as np


@click.group()
@click.option('--out', '-o', default=None)
@click.pass_context
def cli(ctx, out):
    ctx.obj['out'] = out


@click.pass_context
def save(ctx, img):
    if ctx.obj.get('out') is not None:
        click.echo('output to {}'.format(ctx.obj.get('out')))
        img.save(ctx.obj.get('out'))
    else:
        img.show()


def convert_array_to_image(array):
    return Image.fromarray(np.uint8(array))


def convert_pil_to_array(img):
    return np.asarray(img)


@cli.command(short_help='resize image')
@click.argument('image', type=click.Path(exists=True), required=True)
@click.argument('size', type=click.Path(exists=True), required=True)
def resize(image, size):
    '''resize IMAGE SIZE. SIZE is tuple (width, height)'''
    im = Image.open(image)
    im.resize(size)
    save(im)


@cli.command(short_help='blend images')
@click.argument('image1', type=click.Path(exists=True), required=True)
@click.argument('image2', type=click.Path(exists=True), required=True)
@click.argument('alpha', default=0.5)
def blend(image1, image2, alpha):
    '''blend IMAGE1 and IMAGE2.'''
    im1 = Image.open(image1)
    im2 = Image.open(image2)
    blended_im = Image.blend(im1, im2, alpha)
    save(blended_im)


@cli.command(short_help='composite images')
@click.argument('image1', type=click.Path(exists=True), required=True)
@click.argument('image2', type=click.Path(exists=True), required=True)
@click.argument('mask', default=0.5)
def composite(image1, image2, mask):
    '''composite IMAGE1 and IMAGE2'''
    im1 = Image.open(image1)
    im2 = Image.open(image2)
    mask = Image.open(mask).convert('1')
    composited_im = Image.composite(im1, im2, mask)
    save(composited_im)


@cli.command()
def create():
    '''create tiny sample image'''
    array = np.eye(10) * 255
    im = convert_array_to_image(array)
    save(im)


@cli.command()
@click.argument('image', type=click.Path(exists=True), required=True)
@click.option('--equalize', '-e', is_flag=True)
def grayscale(image, equalize):
    im = Image.open(image)
    if equalize is True:
        im = ImageOps.equalize(image)
    im = im.convert("L")
    save(im)


@cli.command()
@click.argument('image', type=click.Path(exists=True), required=True)
@click.option('--equalize', '-e', is_flag=True)
def threshold(image, equalize):
    im = Image.open(image)
    if equalize is True:
        im = ImageOps.equalize(im)
    im = im.convert("L")
    im = im.point(lambda x: 0 if x < 230 else x)
    save(im)


@cli.command()
@click.argument('image', type=click.Path(exists=True), required=True)
def equalize(image):
    '''equalize image'''
    im = Image.open(image)
    im = ImageOps.equalize(im)
    save(im)


@cli.command()
@click.argument('image1', type=click.Path(exists=True), required=True)
@click.argument('image2', type=click.Path(exists=True), required=True)
def difference(image1, image2):
    im1 = Image.open(image1)
    im2 = Image.open(image2)
    click.echo(ImageChops.difference(im1, im2).getbbox())


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
