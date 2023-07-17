import click
import cv2
import numpy as np


@click.group()
def cli():
    pass


@cli.command()
@click.argument('movie', required=True)
@click.option('--start', '-s', type=int, required=False, default=0)
@click.option('--end', '-e', type=int, required=False, default=0)
def convert(movie, start, end):
    cap = cv2.VideoCapture(movie)
    fps = round(cap.get(cv2.CAP_PROP_FPS))
    frame_count = round(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    movie_time = frame_count / fps
    click.echo('file data')
    click.echo('fps: {}'.format(fps))
    click.echo('frame count: {}'.format(frame_count))
    click.echo('movie time: {}'.format(movie_time))
    click.echo('height: {}'.format(height))
    click.echo('width: {}'.format(width))

    count = 0
    start_frame = fps * start
    if end == 0:
        end_frame = frame_count
    else:
        end_frame = fps * start
    step_frame = fps * 60

    for idx in range(start_frame, end_frame, step_frame):
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        output = 'moview2img/{:05}.jpg'.format(idx)
        ret, frame = cap.read()
        if ret:
            print(output)
            cv2.imwrite(output, frame)
        else:
            return

    cap.release()


def main():
    cli()


if __name__ == '__main__':
    main()
