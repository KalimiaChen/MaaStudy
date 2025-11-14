from maa.agent.agent_server import AgentServer
from maa.custom_action import CustomAction
from maa.context import Context

import time
import re

from .utils import Prompt, RecoHelper, Tasker


# 识别抽卡记录
@AgentServer.custom_action("summary_liaison_record")
class SummaryLiaisonRecord(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult | bool:
        try:
            records: list[dict[str, int]] = []
            six_name = ""
            count = 0
            is_pre_quit = False
            while True:
                if Tasker.is_stopping(context):
                    is_pre_quit = True
                    break

                # 识别列表
                reco_helper = RecoHelper(context)
                index = 1
                while index < 6:
                    if not reco_helper.recognize(f"抽卡记录_识别列表{index}").hit():
                        break
                    results = reco_helper.reco_detail.filterd_results
                    # 解析
                    texts = "".join(result.text for result in results)
                    texts = (
                        texts.rstrip("】")
                        .rstrip("]")
                        .replace(" ", "")
                        .replace("+", "")
                        .replace("x", "")
                        .replace("×", "")
                        .replace("★", "")
                        .replace("#", "")
                        .replace("【", "[")
                        .split("[")
                    )
                    name, star = texts
                    Prompt.log(f"识别到特工：{name}，星级：{star}")
                    # 记录
                    count += 1
                    star = int(star)
                    if star == 6:
                        records.append(
                            {"name": six_name if six_name else "已垫抽", "count": count}
                        )
                        six_name = name
                        count = 0
                    index += 1

                # 翻页
                reco_helper = RecoHelper(context).recognize("抽卡记录_翻页键")
                if not reco_helper.hit():
                    break
                Prompt.log("检测下一页")
                reco_helper.click(context)
                time.sleep(0.5)

            # 输出
            if len(records) == 0 and count == 0:
                return False
            if not is_pre_quit:
                records.append(
                    {"name": six_name if six_name else "已垫抽", "count": count}
                )
            Prompt.log("当前系列卡池情况：", use_pre_devider=True)
            for record in records:
                Prompt.log(f"{record['name']}：{record['count']}抽", is_continuous=True)
            Prompt.log(use_post_devider=True)

            return True
        except Exception as e:
            return Prompt.error("识别抽卡记录", e)
