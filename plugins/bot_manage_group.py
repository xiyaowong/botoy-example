"""简易群管插件, 需要机器人是管理员

1. 全体禁言       => 开全体禁言
2. 关全体禁言     => 关全体禁言
3. @改名 + <card> => 艾特一个人，发送改名加新名称，将修改他的群名片
4. @禁言 + <time> => 艾特一个人，发送禁言加多少分钟，将禁言对应用户指定分钟
5. @取消禁言      => 艾特一个人, 解除禁言
6. @踢他!         => 艾特一个人，把他踢出去 (因为这是危险操作，所以关键字后面加了一个感叹号)
"""
import json
import re

from botoy import Action, GroupMsg
from botoy.collection import MsgTypes


def receive_group_msg(ctx: GroupMsg):
    if ctx.FromUserId != ctx.master:  # 需要在中间件部分提前设置该参数，也可以自行设置其他判断条件
        return

    action = Action(ctx.CurrentQQ)
    content = ctx.Content
    if ctx.MsgType == MsgTypes.TextMsg:
        # 1. 全体禁言       => 开全体禁言
        if content == "全体禁言":
            action.shutAllUp(ctx.FromGroupId, 1)
            return
        # 2. 关全体禁言     => 关全体禁言
        if content == "关全体禁言":
            action.shutAllUp(ctx.FromGroupId, 0)
            return
    if ctx.MsgType == MsgTypes.AtMsg:
        at_data = json.loads(ctx.Content)
        at_content = at_data['Content']
        at_users = at_data['UserID']

        # 3. @改名 + <card> => 艾特一个人，发送改名加新名称，将修改他的群名片
        card = re.findall(r'改名(.*?)', at_content)
        if card:
            action.modifyGroupCard(at_users[0], ctx.FromGroupId, card[0])
            return
        # 4. @禁言 + <time> => 艾特一个人，发送禁言加多少分钟，将禁言对应用户指定分钟
        time = re.findall(r'禁言(\d+)', at_content)
        if time:
            action.shutUserUp(ctx.FromGroupId, at_users[0], time[0])
            return
        # 5. @取消禁言      => 艾特一个人, 解除禁言
        cacel = re.findall(r'取消禁言', at_content)
        if cacel:
            action.shutUserUp(ctx.FromGroupId, at_users[0], 0)
            return
        # 6. @踢他!         => 艾特一个人，把他踢出去 (因为这是危险操作，所以关键字后面加了一个感叹号)
        # TODO
