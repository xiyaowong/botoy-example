'''欢迎新群员

请先设置imageDir动图文件夹的路径，里面放置动图，会生成包含指定文字的动图
同时请设置fontPath字体路径
'''
import base64
import io
import os
import random
from pathlib import Path

from botoy import Action, EventMsg
from botoy.refine import refine_group_join_event_msg
from PIL import Image, ImageDraw, ImageFont, ImageSequence

here = Path(__file__).absolute().parent
imageDir = here / 'images'
imageDir = None
fontPath = ''
assert imageDir is not None and fontPath, '请设置动图所在的文件夹路径和字体路径'


def draw_text(text: str) -> bytes:
    assert len(text) > 0
    padding = 2

    gif = Image.open(imageDir / random.choice(os.listdir(imageDir)))

    font_size = (gif.width - 2 * padding) // len(text)
    font = ImageFont.truetype(fontPath, size=font_size)

    rectagle_xy = (padding, gif.size[1] - font_size)
    rectangle = Image.new('RGB', (gif.width, font_size))  # color='#ffb6c1'
    draw = ImageDraw.Draw(rectangle)
    draw.text((0, 0), text, font=font, fill='#ffffff')

    frames = []
    for frame in ImageSequence.Iterator(gif):
        img = frame.copy()
        img.paste(rectangle, rectagle_xy)
        frames.append(img)

    b = io.BytesIO()
    frames[0].save(b, format='gif', append_images=frames[1:], save_all=True)
    return b.getvalue()


def receive_events(ctx: EventMsg):
    join_ctx = refine_group_join_event_msg(ctx)
    if join_ctx is not None:
        action = Action(ctx.CurrentQQ)
        action.sendGroupText(
            join_ctx.FromUin,
            '{} 已加入组织~'.format(join_ctx.UserName),
        )
        pic = draw_text('欢迎 {} 入群!'.format(join_ctx.UserName))
        pic_base64 = base64.b64encode(pic).decode()
        action.sendGroupPic(
            join_ctx.FromUin,
            picBase64Buf=pic_base64,
        )
        # action.sendGroupVoice(gid, voiceUrl='https://attachments-cdn.shimo.im/Y8LSYTYzzJtE2H6d.mp3')
        # action.sendGroupPic(gid, picUrl='https://uploader.shimo.im/f/SwXk1UQVWbwaaQUi.jpg')
