from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

import time

from .utils import parse_query_args, Prompt


class Timer:
    def __init__(self, limit_time=0):
        self.anchor_time = time.time()
        self.limit_time = limit_time

    def is_end(self):
        if self.limit_time == 0:
            return True
        return time.time() - self.anchor_time >= self.limit_time


class TimerManager:
    def __init__(self):
        self.timers = {}

    def create(self, key="default", limit_time=0):
        self.timers[key] = Timer(limit_time)
        return self.timers[key]

    def get(self, key="default") -> Timer | None:
        return self.timers.get(key, None)


timer_manager = TimerManager()


@AgentServer.custom_action("init_timer")
class InitTimer(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            key = args.get("key", "default")
            limit = args.get("limit", "0")
            limit = int(limit)

            timer_manager.create(key, limit)

            return True
        except Exception as e:
            return Prompt.error("初始化计时器", e)


@AgentServer.custom_action("check_time")
class CheckTime(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            key = args.get("key", "default")
            reverse = args.get("end", False)
            if reverse == "true":
                reverse = True
            else:
                reverse = False

            timer = timer_manager.get(key)
            if timer == None:
                return False

            result = not timer.is_end()
            if reverse:
                result = not result
            return result

        except Exception as e:
            return Prompt.error("检查时间", e)
