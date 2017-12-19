import click
import cv2
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
