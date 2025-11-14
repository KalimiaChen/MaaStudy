from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context
from maa.custom_recognition import CustomRecognition

import json

from .utils import parse_query_args, Prompt, Judge


# 清体力

expected_times = 0
used_times = 0


@AgentServer.custom_action("set_eat_times")
class SetEatTimes(CustomAction):

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global expected_times, used_times

        try:
            times = 0
            args = json.loads(argv.custom_action_param)
            if args:
                times = args["times"]

            if times > 0:
                expected_times = times
                print(f"> 将自动使用 {expected_times} 次稳定合剂")
            else:
                expected_times = 0
            used_times = 0

            return True
        except Exception as e:
            return Prompt.error("设置合剂次数", e)


@AgentServer.custom_action("check_eat_times")
class SetEatTimes(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global expected_times, used_times

        try:
            used_times += 1
            if used_times > expected_times:
                return False
            else:
                print(
                    f"> 第 {used_times} 次使用稳定合剂，剩余 {expected_times - used_times} 次"
                )

            return True
        except Exception as e:
            return Prompt.error("检查合剂次数", e)


@AgentServer.custom_action("cr_set_squad")
class CRSetSquad(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            squad = args.get("s", "")

            if squad != "":
                context.override_pipeline(
                    {
                        "清体力_4x行动前检测1": {"next": "清体力_4X队伍"},
                        "清体力_3X及以下行动前检测1": {"next": "清体力_3X队伍"},
                    }
                )
                print(f"> 将使用队伍：{squad}")

            return True
        except Exception as e:
            return Prompt.error("设定指定队伍", e)


# 边缘涉险
# 检测是否满进度
@AgentServer.custom_recognition("check_abyss_process")
class CheckAbyssProcess(CustomRecognition):
    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        try:
            return Judge.equal_process(
                context, argv, "险境复现_检测进度", return_analyze_result=True
            )

        except Exception as e:
            return Prompt.error("检查险境周期奖励", e, reco_detail=True)


# 检查是否填写编队
@AgentServer.custom_action("check_abyss_squad")
class CheckAbyssSquad(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            args = parse_query_args(argv)
            squad_a = args.get("a", "")
            squad_b = args.get("b", "")
            return squad_a != "" and squad_b != ""
        except Exception as e:
            return Prompt.error("检查编队", e)


# 蓝色站台
isMimicryAid = False


# 初始化
@AgentServer.custom_action("platform_init")
class PlatformInit(CustomAction):

    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global isMimicryAid

        try:
            isMimicryAid = False
            return True

        except Exception as e:
            return Prompt.error("初始化蓝色站台", e)


# 检测是否选择助战
@AgentServer.custom_action("platform_mimicry_aid")
class PlatformMimicryAid(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        global isMimicryAid

        try:
            if isMimicryAid:
                return False

            isMimicryAid = True
            return True
        except Exception as e:
            return Prompt.error("选择特工", e)


# 检测是否满进度
@AgentServer.custom_recognition("check_platform_process")
class CheckPlatformProcess(CustomRecognition):
    def analyze(
        self,
        context: Context,
        argv: CustomRecognition.AnalyzeArg,
    ) -> CustomRecognition.AnalyzeResult:
        try:
            return Judge.equal_process(
                context, argv, "蓝色站台_识别分数", return_analyze_result=True
            )
        except Exception as e:
            return Prompt.error("识别蓝色站台分数", e, reco_detail=True)
