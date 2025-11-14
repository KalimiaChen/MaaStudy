from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

import time

from .utils import parse_query_args, Prompt, Configs


delay_focus = {}
focus_wl = set()


# 添加延迟提醒
@AgentServer.custom_action("delay_focus_hook")
class DelayFocusHook(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global delay_focus, focus_wl
        try:
            args = parse_query_args(argv)
            key = args.get("key", "")
            focus = args.get("focus", "")
            wl = args.get("wl", False)
            if wl == "true":
                wl = True
            else:
                wl = False

            delay_focus[key] = focus
            if wl:
                focus_wl.add(key)

            return True
        except Exception as e:
            return Prompt.error("添加延迟提醒", e)


# 添加延迟提醒白名单
@AgentServer.custom_action("set_focus_wl")
class SetFocusBlackList(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global delay_focus, focus_wl
        try:
            args = parse_query_args(argv)
            key = args.get("key", "")
            if key != "":
                focus_wl.add(key)
            return True
        except Exception as e:
            return Prompt.error("添加延迟提醒白名单", e)


# 延迟提醒
@AgentServer.custom_action("delay_focus")
class DelayFocus(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global delay_focus, focus_wl
        try:
            args = parse_query_args(argv)
            is_block = args.get("block", False)
            if is_block:
                is_block = True

            focuses = []

            for key, focus in delay_focus.items():
                if key in focus_wl:
                    focuses.append(focus)

            if len(focuses) > 0:
                print("——————————")
                print("注意：", flush=True)
                for focus in focuses:
                    time.sleep(0.1)
                    print(f" * {focus}", flush=True)
                    time.sleep(0.1)
                print("——————————")
                delay_focus = {}
                focus_wl = set()
                return not is_block
            else:
                print("> 无需提醒项")
                delay_focus = {}
                focus_wl = set()
                return True

        except Exception as e:
            return Prompt.error("延迟提醒", e)


# 全局设置
@AgentServer.custom_action("set_config")
class SetConfig(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            key = args.get("key", None)
            value = args.get("value", None)

            if key == None or value == None:
                return Prompt.error("未定义的全局设置值", use_defult_postfix=False)

            Configs.set(key, value)
            return True

        except Exception as e:
            return Prompt.error("全局设置", e)
