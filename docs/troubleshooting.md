# 常见问题

## `doctor` 提示没有 TikHub API Key

通过项目推荐入口 [注册 TikHub](https://user.tikhub.io/register?ref=bW0RSDaJ)，创建 API Key 后重新运行：

```bash
./beef-xhs-library onboard
```

在本地隐藏输入框中填写。高级用户也可以使用 `TIKHUB_API_KEY` 环境变量。

## 只想保存本地文件

运行命令时增加：

```bash
--skip-feishu
```

例如：

```bash
./beef-xhs-library run "<分享链接>" --skip-feishu
```

## 已经有自己的飞书 Base

在 `config.toml` 中填写 Base 和表格 ID，然后执行：

```bash
./beef-xhs-library setup-feishu --check
```

如果发现字段缺失，去掉 `--check` 后重新运行，即可创建或补齐缺少的内容。

## 为什么默认不保存视频文件

保存和上传完整视频会明显增加执行时间与存储空间。项目默认保存可以打开的分享链接，并保留封面、字幕、元数据和总结。需要本地视频归档时，可以在现有流程上单独扩展。

## 旧配置还能继续使用吗

可以。旧命令、旧环境变量和旧配置目录继续兼容。新配置不存在时，程序会把旧配置迁移到：

```text
~/.config/beef-xhs-library
```
