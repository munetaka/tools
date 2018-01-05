import click
import cv2
import math
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
        cv2.imwrite(ctx.obj.get('out'), img)
    else:
        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


@cli.command()
@click.argument('image', type=click.Path(exists=True), required=True)
def grayscale(image):
    im = cv2.imread(image)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    save(im)


@cli.command()
@click.argument('base_image', type=click.Path(exists=True), required=True)
@click.argument('correlate_image', type=click.Path(exists=True), required=True)
def correlate(base_image, correlate_image):
    base_im_gray = cv2.imread(base_image, 0)
    save(base_im_gray)
    correlate_im_gray = cv2.imread(correlate_image, 0)
    (dx, dy), _ = cv2.phaseCorrelate(np.float32(correlate_im_gray), np.float32(base_im_gray))
    M = np.float32([[1, 0, dx], [0, 1, dy]])
    rows, cols = base_im_gray.shape
    im_moved = cv2.warpAffine(cv2.imread(correlate_image, 1), M, (cols, rows))

    # fill outline with dummy color
    mask = np.full(base_im_gray.shape, 255, dtype=np.uint8)
    mask[math.ceil(abs(dy)):rows, math.ceil(abs(dx)):cols] = 0
    if dx < 0:
        mask = mask.T[::-1].T
    if dy < 0:
        mask = mask[::-1]
    im_moved = cv2.inpaint(im_moved, mask, 3, cv2.INPAINT_TELEA)
    save(im_moved)


@cli.group()
def create():
    pass


def get_gradation_2d(start, stop, width, height, is_horizontal=False):
    if is_horizontal:
        return np.tile(np.linspace(start, stop, height), (width, 1))
    else:
        return np.tile(np.linspace(start, stop, width), (height, 1)).T


@create.command()
@click.option('--start', '-s', type=int, required=False, default=0)
@click.option('--end', '-e', type=int, required=False, default=255)
@click.option('--width', '-w', type=int, required=False, default=100)
@click.option('--height', '-h', type=int, required=False, default=100)
@click.option('--is_horizontal', is_flag=True, default=False)
def gradation_2d(start, end, width, height, is_horizontal):
    start = start / 255
    end = end / 255
    image = get_gradation_2d(start, end, width, height, is_horizontal)
    save(image)


@create.command()
@click.option('--start', '-s', type=click.Tuple([int, int, int]), required=False, default=(192, 0, 0))
@click.option('--end', '-e', type=click.Tuple([int, int, int]), required=False, default=(64, 255, 255))
@click.option('--width', '-w', type=int, required=False, default=100)
@click.option('--height', '-h', type=int, required=False, default=100)
@click.option('--is_horizontal', type=click.Tuple([bool, bool, bool]), default=(False, False, True))
def gradation_3d(start, end, width, height, is_horizontal):
    image = np.zeros((width, height, len(start)), dtype=np.float)
    start = (x / 255 for x in start)
    end = (x / 255 for x in end)
    for i, (st, en, is_h) in enumerate(zip(start, end, is_horizontal)):
        grad = get_gradation_2d(st, en, width, height, is_h)
        image[:, :, i] = grad
    save(image)


@cli.group()
def filter():
    pass


@filter.command()
@click.argument('image', type=click.Path(exists=True), required=True)
@click.option('--ksize', '-k', nargs=2, type=click.Tuple([int, int]), default=(3, 3))
def blur(image, ksize):
    im = cv2.imread(image)
    im = cv2.blur(im, ksize=ksize)
    save(im)


@filter.command()
@click.argument('image', type=click.Path(exists=True), required=True)
@click.option('--pillow_kernel', '-p', is_flag=True, default=False)
def sharpen(image, pillow_kernel):
    if pillow_kernel is False:
        # https://en.wikipedia.org/wiki/Kernel_(image_processing)
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0],
        ])
    else:
        # pillow's sharpen kernel
        kernel = np.array([
            [-2, -2, -2],
            [-2, 32, -2],
            [-2, -2, -2],
        ]) / 16
    im = cv2.imread(image)
    im = cv2.filter2D(
        im,
        -1,
        kernel
    )
    save(im)


@filter.command()
@click.argument('image', type=click.Path(exists=True), required=True)
@click.option('--neiborhood', '-n', type=click.Choice([4, 8]), default=4)
def erosion(image, neiborhood):
    im = cv2.imread(image, 0)
    if neiborhood == 4:
        kernel = np.array([
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ], np.uint8)
    else:
        kernel = np.ones((5, 5), np.uint8)
    im = cv2.erode(im, kernel, iterations=1)
    save(im)


def main():
    cli(obj={})


if __name__ == '__main__':
    main()
