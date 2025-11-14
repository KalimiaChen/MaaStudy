from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

from .utils import parse_query_args, parse_list_input, Prompt


upgrade_list = []


# 切换升级特工
def switch_upgrade_target(context: Context) -> bool:
    global upgrade_list

    if len(upgrade_list) == 0:
        return False

    target = upgrade_list.pop(0)
    context.override_pipeline({"每日升级_选择角色": {"expected": target}})
    print(f"> 尝试升级特工：{target}")
    return True


# 设置升级名单
@AgentServer.custom_action("set_upgrade_list")
class SetUpgradeList(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global upgrade_list

        try:
            args = parse_query_args(argv)
            list_str = args.get("list", "")
            upgrade_list = parse_list_input(list_str)
            print(f"> 升级特工名单：{upgrade_list}")

            return switch_upgrade_target(context)

        except Exception as e:
            return Prompt.error("设置升级名单", e)


# 切换升级特工
@AgentServer.custom_action("switch_upgrade_target")
class SwitchUpgradeTarget(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            return switch_upgrade_target(context)

        except Exception as e:
            return Prompt.error("切换目标特工", e)
