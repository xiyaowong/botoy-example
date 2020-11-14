from botoy import Action, GroupMsg
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, in_content, these_msgtypes
from botoy.refine import refine_pic_group_msg
from botoy.sugar import Text


@ignore_botself
@these_msgtypes(MsgTypes.TextMsg, MsgTypes.PicMsg)
@in_content("复读机")
def receive_group_msg(ctx: GroupMsg):
    if ctx.MsgType == MsgTypes.TextMsg:
        if ctx.Content.startswith("复读机"):
            text = ctx.Content[3:]
            while text.startswith("复读机"):
                text = text[3:]
            if text:
                Text(text)
    elif ctx.MsgType == MsgTypes.PicMsg:
        pic_ctx = refine_pic_group_msg(ctx)
        Action(ctx.CurrentQQ).sendGroupPic(
            ctx.FromGroupId, picMd5s=[pic.FileMd5 for pic in pic_ctx.GroupPic]
        )
