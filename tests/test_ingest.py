import json
import os
import pathlib
import tempfile
import unittest
from unittest import mock


SCRIPT_DIR = pathlib.Path(__file__).resolve().parents[1] / "scripts"
os.sys.path.insert(0, str(SCRIPT_DIR))

import ingest_xhs_note  # noqa: E402


class IngestTests(unittest.TestCase):
    def test_record_listing_reads_every_page(self) -> None:
        calls = []

        def fake_run_cli(args, cwd=None):
            self.assertIsNone(cwd)
            calls.append(args)
            offset = int(args[args.index("--offset") + 1])
            count = 200 if offset == 0 else 5
            return json.dumps(
                {
                    "data": {
                        "fields": ["视频标题"],
                        "data": [[f"title-{offset + index}"] for index in range(count)],
                        "record_id_list": [f"rec-{offset + index}" for index in range(count)],
                    }
                }
            )

        with mock.patch.object(ingest_xhs_note, "run_cli", side_effect=fake_run_cli):
            response = ingest_xhs_note.lark_list_records("base", "table", ["视频标题"])

        rows = ingest_xhs_note.rows_as_maps(response)
        self.assertEqual(len(rows), 205)
        self.assertEqual([call[call.index("--offset") + 1] for call in calls], ["0", "200"])

    def test_note_id_prevents_same_title_from_matching_another_video(self) -> None:
        response = {
            "data": {
                "fields": ["视频标题", "视频链接"],
                "data": [["相同标题", "https://www.xiaohongshu.com/explore/old-note-id"]],
                "record_id_list": ["rec-old"],
            }
        }
        with mock.patch.object(ingest_xhs_note, "lark_list_records", return_value=response):
            record_id = ingest_xhs_note.find_video_record(
                "base",
                "table",
                "new-note-id",
                "相同标题",
                "https://www.xiaohongshu.com/explore/new-note-id",
            )
        self.assertEqual(record_id, "")

    def test_existing_creator_refreshes_available_fields_without_empty_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            creator_dir = pathlib.Path(temp)
            snapshot = {
                "creator_dir": creator_dir,
                "assets_dir": creator_dir,
                "avatar_file": creator_dir / "missing-avatar.webp",
                "background_file": creator_dir / "missing-background.jpg",
                "fields": {},
                "update_fields": {
                    "博主名称": "新名称",
                    "小红书用户ID": "user-1",
                    "最近更新时间": "2026-07-17 18:00:00",
                },
            }
            commands = []

            def fake_run_cli(args, cwd=None):
                commands.append((args, cwd))
                return '{"data":{}}'

            with mock.patch.object(ingest_xhs_note, "prepare_creator", return_value=snapshot), mock.patch.object(
                ingest_xhs_note,
                "get_record",
                return_value={"data": {"fields": ["简介"], "data": [["原有简介"]]}},
            ), mock.patch.object(ingest_xhs_note, "run_cli", side_effect=fake_run_cli):
                ingest_xhs_note.refresh_creator(
                    "base",
                    "creator-table",
                    "creator-record",
                    {},
                    {"nickname": "新名称"},
                    creator_dir,
                )

            update_command = commands[0][0]
            payload = json.loads(update_command[update_command.index("--json") + 1])
            self.assertEqual(payload["博主名称"], "新名称")
            self.assertEqual(payload["小红书用户ID"], "user-1")
            self.assertNotIn("简介", payload)
            self.assertTrue((creator_dir / "feishu_creator_update.json").exists())

    def test_auto_summary_uses_content_from_across_the_transcript(self) -> None:
        transcript = "。".join(
            [
                "很多人一开始不知道应该怎样整理自己的日程安排",
                "作者先解释任务混乱会造成重复切换和时间浪费",
                "接着把所有事项按照工作生活和学习三个类别整理",
                "核心方法是先确定优先级再为每个任务安排明确时间",
                "实际操作时还会给重要事项增加提醒和完成状态",
                "随后通过每周统计观察时间到底花在了哪些事情上",
                "这些统计结果可以继续用来调整下一周的时间分配",
                "最终结论是日程管理需要形成持续复盘和调整的循环",
            ]
        )
        summary = ingest_xhs_note.auto_summary({}, transcript)
        self.assertIn("核心方法", summary)
        self.assertIn("每周统计", summary)
        self.assertIn("最终结论", summary)
        self.assertLessEqual(len(summary), 300)


if __name__ == "__main__":
    unittest.main()
