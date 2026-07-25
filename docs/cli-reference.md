# 命令行完整说明

## `onboard`

推荐的初始化入口。依次完成飞书登录和 TikHub API Key 输入，然后自动完成本地配置与飞书数据结构准备。

```bash
./xhs-library onboard
```

## `init`

只创建配置文件和输出目录，适合需要手动调整路径的高级用户。已有配置默认不会被覆盖。

```bash
./xhs-library init --output-root ~/Documents/xhs-materials
```

## `doctor`

检查 Python、配置文件、输出目录、TikHub 配置、飞书命令和飞书表格信息。

```bash
./xhs-library doctor
./xhs-library doctor --json
```

只使用本地输出时：

```bash
./xhs-library doctor --skip-feishu
```

## `setup-feishu`

创建或补齐飞书 Base、表格、字段和视图。重复运行时会优先复用现有内容。

```bash
./xhs-library setup-feishu
```

只检查现有数据结构，不进行调整：

```bash
./xhs-library setup-feishu --check
```

## `run`

处理一条小红书短链接、完整链接或整段分享文字。

```bash
./xhs-library run "<分享链接或分享文字>"
```

常用选项：

- `--skip-feishu`：只保存本地文件。
- `--expected-title`：在多个候选结果中提供标题提示。
- `--expected-author`：提供作者提示。
- `--summary-file`：使用人工整理的核心总结文件。
- `--summary-text`：直接传入核心总结。
- `--force-create`：即使发现相同记录也创建新行。

示例：

```bash
./xhs-library run "<分享链接>" --skip-feishu
./xhs-library run "<分享链接>" --expected-author "作者名称"
./xhs-library run "<分享链接>" --summary-file /path/to/core_summary.txt
```

## 兼容入口

旧命令仍然可以使用：

```bash
./xhs-ingest "<小红书链接>"
python3 scripts/ingest_xhs_note.py "<小红书链接>" --skip-feishu
```
