from collections import defaultdict
from queue import deque

from botoy import GroupMsg
from botoy import decorators as deco
from botoy.collection import MsgTypes
from botoy.sugar import Text

# 自动消息加一功能


class RepeatDeque(deque):
    def __init__(self, *args, **kwargs):
        super().__init__(maxlen=3, *args, **kwargs)
        self.refresh()

    def refresh(self):
        for i in range(self.maxlen):
            self.append(i)

    def should_repeat(self, item):
        self.append(item)
        if len(set(self)) == 1:
            self.refresh()
            return True
        return False


deque_dict = defaultdict(RepeatDeque)


@deco.ignore_botself
@deco.these_msgtypes(MsgTypes.TextMsg)
def receive_group_msg(ctx: GroupMsg):
    text = ctx.Content
    if deque_dict[ctx.FromGroupId].should_repeat(text):
        Text(text)
