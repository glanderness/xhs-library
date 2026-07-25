# 配置与环境变量

## 推荐方式

大多数用户不需要手动编辑配置。运行：

```bash
./xhs-library onboard
```

程序会创建本地配置和输出目录，验证 TikHub API Key，并创建或复用飞书 Base、视频表和作者表。

高级用户可以复制 [`config.example.toml`](../config.example.toml)，或单独运行：

```bash
./xhs-library init
```

## 配置读取顺序

```text
命令参数 > 环境变量 > config.toml > 通用默认值
```

默认配置路径：

```text
~/.config/xhs-library/config.toml
```

旧版本的 `XHS_INGEST_CONFIG` 环境变量和 `~/.config/xhs-tikhub-feishu-ingest` 配置目录继续兼容；首次使用新名称时会自动迁移到 `~/.config/xhs-library`。

## 环境变量

| 环境变量 | 用途 |
| --- | --- |
| `XHS_LIBRARY_CONFIG` | 指定配置文件路径 |
| `XHS_LIBRARY_ROOT` | 指定本地内容库目录 |
| `TIKHUB_API_KEY` | TikHub API Key |
| `TIKHUB_BASE_URL` | TikHub API 地址 |
| `TIKHUB_ENV_FILE` | 兼容已有 TikHub env 文件 |
| `XHS_OUTPUT_ROOT` | 指定本地输出目录 |
| `FEISHU_BASE_TOKEN` | 飞书 Base 标识 |
| `FEISHU_VIDEO_TABLE_ID` | 视频表 ID |
| `FEISHU_CREATOR_TABLE_ID` | 作者表 ID |
| `FEISHU_BASE_URL` | 用户可以打开的飞书 Base 链接 |

## 使用另一份配置

```bash
./xhs-library doctor --config /path/to/config.toml
./xhs-library run "<小红书链接>" --config /path/to/config.toml
```

TikHub API Key 可以通过初始化流程的本地隐藏输入框保存。不要把包含真实配置值的 `config.toml` 或 `tikhub.env` 提交到仓库。
