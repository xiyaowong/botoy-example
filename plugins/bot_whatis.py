import requests
from botoy import Action, GroupMsg
from botoy.collection import MsgTypes
from botoy.decorators import ignore_botself, startswith, these_msgtypes

# 查网络缩写词的意思
# ?nmsl => 查nmsl
# ?awsl => 查awsl


def whatis(text):
    try:
        resp = requests.post(
            'https://lab.magiconch.com/api/nbnhhsh/guess',
            data={'text': text},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(e)
        return ''
    else:
        if not data:
            return ''
        name, trans = data[0]['name'], data[0]['trans']
        trans_str = '、'.join(trans)
        return f'【{name}】{trans_str}'


@ignore_botself
@these_msgtypes(MsgTypes.TextMsg)
@startswith('?')
def receive_group_msg(ctx: GroupMsg):
    ans = whatis(ctx.Content[1:])
    if ans:
        Action(ctx.CurrentQQ).replyGroupMsg(
            ctx.FromGroupId,
            ans,
            ctx.MsgSeq,
            ctx.MsgTime,
            ctx.FromUserId,
            ctx.Content,
        )
