import click
from PIL import Image
from PIL import ImageOps
from PIL import ImageChops
from PIL import ImageFilter
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


@cli.command(short_help='blend two images')
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
def check_similarity(image1, image2):
    im1 = Image.open(image1)
    im2 = Image.open(image2)
    click.echo(ImageChops.difference(im1, im2).getbbox() is None)


@cli.command()
@click.argument('image1', type=click.Path(exists=True), required=True)
@click.argument('image2', type=click.Path(exists=True), required=True)
def difference(image1, image2):
    im1 = Image.open(image1)
    im2 = Image.open(image2)
    im = ImageChops.difference(im1, im2)
    save(im)


@cli.group()
def filter():
    '''several effects'''
    pass


@filter.command()
@click.argument('image', type=click.Path(exists=True), required=True)
def blur(image):
    im = Image.open(image)
    im = im.filter(ImageFilter.BLUR)
    save(im)


@filter.command()
@click.argument('image', type=click.Path(exists=True), required=True)
def contour(image):
    im = Image.open(image)
    im = im.filter(ImageFilter.CONTOUR)
    save(im)


@filter.command()
@click.argument('image', type=click.Path(exists=True), required=True)
def detail(image):
    im = Image.open(image)
    im = im.filter(ImageFilter.DETAIL)
    save(im)


@filter.command()
@click.argument('image', type=click.Path(exists=True), required=True)
def edge_enhance(image):
    im = Image.open(image)
    im = im.filter(ImageFilter.EDGE_ENHANCE)
    save(im)


@filter.command()
@click.argument('image', type=click.Path(exists=True), required=True)
def edge_enhance_more(image):
    im = Image.open(image)
    im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
    save(im)


@filter.command()
@click.argument('image', type=click.Path(exists=True), required=True)
def emboss(image):
    im = Image.open(image)
    im = im.filter(ImageFilter.EMBOSS)
    save(im)


@filter.command()
@click.argument('image', type=click.Path(exists=True), required=True)
def find_edges(image):
    im = Image.open(image)
    im = im.filter(ImageFilter.FIND_EDGES)
    save(im)


@filter.command()
@click.argument('image', type=click.Path(exists=True), required=True)
@click.option('--radius', '-r', default=2.0)
def gaussian_blur(image, radius):
    im = Image.open(image)
    im = im.filter(ImageFilter.GaussianBlur(radius))
    save(im)


@filter.command()
@click.argument('image', type=click.Path(exists=True), required=True)
def smooth(image):
    im = Image.open(image)
    im = im.filter(ImageFilter.SMOOTH)
    save(im)


@filter.command()
@click.argument('image', type=click.Path(exists=True), required=True)
def smooth_more(image):
    im = Image.open(image)
    im = im.filter(ImageFilter.SMOOTH_MORE)
    save(im)


@filter.command()
@click.argument('image', type=click.Path(exists=True), required=True)
def sharpen(image):
    im = Image.open(image)
    im = im.filter(ImageFilter.SHARPEN)
    save(im)


@filter.command(short_help='dilation')
@click.argument('image', type=click.Path(exists=True), required=True)
@click.option('--size', '-s', type=int, default=3)
def max(image, size):
    im = Image.open(image)
    im = im.filter(ImageFilter.MaxFilter(size))
    save(im)


@filter.command()
@click.argument('image', type=click.Path(exists=True), required=True)
@click.option('--size', '-s', type=int, default=3)
def median(image, size):
    im = Image.open(image)
    im = im.filter(ImageFilter.MedianFilter(size))
    save(im)


@filter.command(short_help='erosion')
@click.argument('image', type=click.Path(exists=True), required=True)
@click.option('--size', '-s', type=int, default=3)
def min(image, size):
    im = Image.open(image)
    im = im.filter(ImageFilter.MinFilter(size))
    save(im)


@filter.command()
@click.argument('image', type=click.Path(exists=True), required=True)
@click.option('--size', '-s', type=int, default=3)
def mod(image, size):
    im = Image.open(image)
    im = im.filter(ImageFilter.ModeFilter(size))
    save(im)


@filter.command(short_help='closing test')
@click.argument('image', type=click.Path(exists=True), required=True)
@click.option('--size', '-s', type=int, default=3)
def closing(image, size):
    im = Image.open(image)
    im = im.convert("RGB")
    im = im.filter(ImageFilter.MinFilter(size))\
           .filter(ImageFilter.MinFilter(size))\
           .filter(ImageFilter.MinFilter(size))\
           .filter(ImageFilter.MaxFilter(size))\
           .filter(ImageFilter.MaxFilter(size))\
           .filter(ImageFilter.MaxFilter(size))\
           .filter(ImageFilter.MaxFilter(size))\
           .filter(ImageFilter.MaxFilter(size))\
           .filter(ImageFilter.MaxFilter(size))\
           .filter(ImageFilter.MinFilter(size))\
           .filter(ImageFilter.MinFilter(size))\
           .filter(ImageFilter.MinFilter(size))
    save(im)


@filter.command(short_help='opening test')
@click.argument('image', type=click.Path(exists=True), required=True)
@click.option('--size', '-s', type=int, default=3)
def opening(image, size):
    im = Image.open(image)
    im = im.convert("RGB")
    im = im.filter(ImageFilter.MaxFilter(size))\
           .filter(ImageFilter.MaxFilter(size))\
           .filter(ImageFilter.MaxFilter(size))\
           .filter(ImageFilter.MinFilter(size))\
           .filter(ImageFilter.MinFilter(size))\
           .filter(ImageFilter.MinFilter(size))\
           .filter(ImageFilter.MinFilter(size))\
           .filter(ImageFilter.MinFilter(size))\
           .filter(ImageFilter.MinFilter(size))\
           .filter(ImageFilter.MinFilter(size))\
           .filter(ImageFilter.MaxFilter(size))\
           .filter(ImageFilter.MaxFilter(size))\
           .filter(ImageFilter.MaxFilter(size))
    save(im)


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
