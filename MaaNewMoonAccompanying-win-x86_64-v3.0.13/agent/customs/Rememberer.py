from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from .utils import parse_query_args, parse_list_input, Prompt


class _Memoirs:
    def __init__(self):
        self.mems = set()

    def memorize(self, key: str):
        self.mems.add(key)

    def check_memorized(self, key):
        return key in self.mems

    def forget(self, key):
        self.mems.discard(key)


memoirs = _Memoirs()


# 记住
@AgentServer.custom_action("mem")
class Mem(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            keys = args.get("key", None)
            if not keys:
                return True
            keys = parse_list_input(keys)
            for key in keys:
                memoirs.memorize(key)
            return True
        except Exception as e:
            return Prompt.error("记忆", e)


# 检查是否记住过
@AgentServer.custom_action("not_memed")
class NotMemed(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            key = args.get("key", None)
            if not key:
                return True
            return not memoirs.check_memorized(key)
        except Exception as e:
            return Prompt.error("检查是否记住过", e)


# 忘记
@AgentServer.custom_action("forget")
class Forget(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            keys = args.get("key", None)
            if not keys:
                return True
            keys = parse_list_input(keys)
            for key in keys:
                memoirs.forget(key)
            return True
        except Exception as e:
            return Prompt.error("忘记", e)
