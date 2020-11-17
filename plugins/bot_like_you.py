"""给某人点赞
群内发送 赞我 即可
"""
import json
import pathlib
import time
from datetime import datetime

from botoy import Action, GroupMsg
from botoy.decorators import equal_content, ignore_botself, queued_up


def get_today():
    return datetime.strftime(datetime.now(), "%m-%d")


cachePath = pathlib.Path(__file__).absolute().parent / "like_you_cache"
if not cachePath.exists():
    with open(cachePath, "w") as f:
        json.dump({"today": get_today(), "likedUser": []}, f)


@ignore_botself
@equal_content("赞我")
@queued_up(name="like_you")
def receive_group_msg(ctx: GroupMsg):
    action = Action(ctx.CurrentQQ)
    with open(cachePath) as f:
        cache = json.load(f)

    today = get_today()
    if cache["today"] != today:  # 新的一天，清空全部记录
        cache["today"] = today
        cache["likedUser"] = []

    if ctx.FromUserId not in cache["likedUser"]:
        # 赞他
        cache["likedUser"].append(ctx.FromUserId)
        action.replyGroupMsg(
            ctx.FromGroupId,
            "正在赞。。。",
            ctx.MsgSeq,
            ctx.MsgRandom,
            ctx.FromUserId,
            ctx.Content,
        )
        #######
        for _ in range(50):
            action.likeUser(ctx.FromUserId)
            time.sleep(0.3)
        #######
        action.replyGroupMsg(
            ctx.FromGroupId,
            "赞完了。。。",
            ctx.MsgSeq,
            ctx.MsgRandom,
            ctx.FromUserId,
            ctx.Content,
        )

    else:
        # 今天已赞
        action.replyGroupMsg(
            ctx.FromGroupId,
            "今日已赞。。。",
            ctx.MsgSeq,
            ctx.MsgRandom,
            ctx.FromUserId,
            ctx.Content,
        )

    # 更新缓存
    with open(cachePath, "w") as f:
        json.dump(cache, f)
