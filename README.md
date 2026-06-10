# IndexTTS2 CLI

<p align="center">
  一个面向本地语音合成和批量处理的非官方 IndexTTS2 CLI
</p>

<p align="center">
  简体中文 | <a href="./docs/README_indextts2_cli_en.md">English</a>
</p>

`indextts2-cli` 是一个非官方的 IndexTTS2 命令行工具包。它基于 [IndexTTS 官方仓库](https://github.com/index-tts/index-tts), 修复了若干本地运行问题, 并提供可安装, 可配置, 可批量运行, 可自动拼接的 CLI 工作流。

本项目不是 Bilibili IndexTTS Team 的官方发布版本, 也不代表原权利人对本 fork 的认可, 保证或背书。

## 它能做什么

本项目在官方仓库基础上修复了模型文件路径和 Python 版本限制问题, 新增批量合成, 合成后拼接功能并封装为 CLI 便于调用:

- 用 `synth` 合成单条文本音频。
- 用音色参考音频控制说话人音色。
- 用情感参考音频, 情感描述文本或 8 维情感向量控制表达方式。
- **用 `batch` 从 JSON Lines 清单批量生成多段音频, 也可以选择合成后直接拼接为一个 WAV。**
- 用 `concat` 拼接已有 WAV, 或在批量合成后直接拼接成一个 WAV。

此外, 它还提供面向日常使用的工程化能力:

- 安装后可在任意目录运行, 不依赖仓库根目录作为当前工作目录。
- 用持久化配置保存模型目录, 设备, FP16, DeepSpeed 和 CUDA kernel 设置。
- 通过 `download` 下载模型资源。
- 通过 `check` 在合成前发现模型资源, Python 包和设备问题。
- 保留短命令 `itts2`, 方便高频使用。

## 主要改进

相较于 fork 时的官方仓库, 本项目主要做了这些改进:

- 修复了模型文件路径错误。
- 修复了 Python 版本限制错误。
- 增加了批量生成语音与拼接功能。
- 将 IndexTTS2 工作流封装为可安装的 CLI。

如果你只需要官方 WebUI, 请继续使用官方仓库文档。

## 安装

本项目要求 Python `>=3.10,<3.12`。推荐使用 Python 3.10 安装, 因为部分语音依赖尚不支持 Python 3.12+ 或 3.13。

从 PyPI 安装:

```bash
uv tool install --python 3.10 indextts2-cli
```

也可以使用 `pipx`:

```bash
pipx install --python 3.10 indextts2-cli
```

从本地源码安装:

```bash
uv tool install --python 3.10 .
```

开发时使用 editable 安装:

```bash
uv tool install --python 3.10 -e .
```

安装后会注册两个等价命令:

```bash
indextts2-cli --help
itts2 --help
```

`indextts2-cli` 是完整命令名, `itts2` 是短命令。下面的示例使用完整命令名, 你可以把它替换为 `itts2`。

## 快速开始

准备一段说话人参考音频, 例如 `voice.wav`。音频应是清晰的人声 WAV 文件。

```bash
indextts2-cli init
indextts2-cli download
indextts2-cli check
indextts2-cli synth --text "你好, IndexTTS2。" --voice voice.wav --output hello.wav
```

这组命令会:

1. 创建本地配置。
2. 下载 IndexTTS2 模型资源。
3. 检查模型, Python 包和设备。
4. 用参考音频 `voice.wav` 合成 `hello.wav`。

如果你正在仓库源码目录中运行, 也可以使用仓库自带示例音频:

```bash
indextts2-cli synth --text "你好, IndexTTS2。" --voice examples/voice_01.wav --output outputs/hello.wav
```

默认不会覆盖已有输出文件。如需覆盖, 明确加入 `--force`:

```bash
indextts2-cli synth --text "重新生成。" --voice voice.wav --output hello.wav --force
```

## 命令概览

| 命令 | 用途 | 常用场景 |
| --- | --- | --- |
| `init` | 创建持久化配置和默认模型资源目录 | 首次使用 |
| `config` | 查看或修改持久化配置 | 固定模型目录和默认设备 |
| `download` | 下载 IndexTTS2 模型资源 | 准备运行环境 |
| `check` | 检查模型资源, Python 包和设备 | 合成前排查环境 |
| `synth` | 合成单条文本音频 | 单句试听, 脚本调用 |
| `batch` | 读取 JSON Lines 清单批量合成 | 多句台词, 章节音频 |
| `concat` | 拼接已有 WAV 文件 | 后处理, 拼接片段 |

完整参数见 [CLI v2 使用文档](./docs/cli-v2-usage.md)。

## 推荐工作流

### 首次使用

```bash
indextts2-cli init
indextts2-cli download
indextts2-cli check
```

### 使用已有模型目录

```bash
indextts2-cli config set model_dir D:/models/IndexTTS-2
indextts2-cli check
```

### 固定 GPU 配置

```bash
indextts2-cli config set default_device cuda:0
indextts2-cli config set use_fp16 true
indextts2-cli check
```

### 临时覆盖运行参数

```bash
indextts2-cli synth --text "GPU 推理测试。" --voice examples/voice_01.wav --output outputs/gpu.wav --device cuda:0 --fp16
```

命令行参数只影响本次运行。需要长期生效时, 使用 `config set`。

## 模型资源目录

CLI 使用“模型资源目录”保存 IndexTTS2 的模型文件和配套资源。`init` 只创建本地配置和目录, 不会自动下载模型。

模型目录解析优先级:

1. 命令行参数 `--model-dir PATH`
2. 环境变量 `INDEXTTS2_MODEL_DIR`
3. 持久化配置 `model_dir`
4. 平台默认模型资源目录

指定已有模型目录:

```bash
indextts2-cli config set model_dir D:/models/IndexTTS-2
indextts2-cli check
```

下载模型并写入配置:

```bash
indextts2-cli download --model-dir D:/models/IndexTTS-2
```

临时下载到某个目录, 但不写入配置:

```bash
indextts2-cli download --model-dir D:/tmp/IndexTTS-2 --no-save
```

## 配置管理

查看配置文件位置:

```bash
indextts2-cli config path
```

查看当前配置:

```bash
indextts2-cli config get
```

常用配置:

```bash
indextts2-cli config set model_dir D:/models/IndexTTS-2
indextts2-cli config set default_device cuda:0
indextts2-cli config set use_fp16 true
indextts2-cli config set use_deepspeed false
indextts2-cli config set use_cuda_kernel false
```

可持久化的配置项:

| 配置项 | 说明 |
| --- | --- |
| `model_dir` | IndexTTS2 模型资源目录 |
| `default_device` | 默认运行设备, 例如 `cpu`, `cuda`, `cuda:0`, `mps`, `xpu` |
| `use_fp16` | 是否默认启用 FP16 |
| `use_deepspeed` | 是否默认启用 DeepSpeed |
| `use_cuda_kernel` | 是否默认启用 CUDA kernel |

## 单条合成

直接传入文本:

```bash
indextts2-cli synth --text "这是一条测试语音。" --voice examples/voice_01.wav --output outputs/test.wav
```

从 UTF-8 文本文件读取:

```bash
indextts2-cli synth --text-file input.txt --voice examples/voice_01.wav --output outputs/from-file.wav
```

从标准输入读取:

```bash
echo "这段文本来自标准输入。" | indextts2-cli synth --stdin --voice examples/voice_01.wav --output outputs/stdin.wav
```

### 情感控制

使用情感参考音频:

```bash
indextts2-cli synth --text "带有情感参考的语音。" --voice examples/voice_01.wav --emotion-audio examples/emo_sad.wav --emotion-weight 0.75 --output outputs/emotion.wav
```

使用情感描述文本:

```bash
indextts2-cli synth --text "温和而平静地朗读。" --voice examples/voice_01.wav --emotion-text "warm and calm" --emotion-weight 0.6 --output outputs/emotion-text.wav
```

使用 8 维情感向量:

```bash
indextts2-cli synth --text "使用情感向量。" --voice examples/voice_01.wav --emotion-vector 0,0,0.8,0,0,0,0,0 --emotion-weight 1.0 --output outputs/vector.wav
```

`--emotion-audio`, `--emotion-text` 和 `--emotion-vector` 每次只能使用一种。

## 批量合成

`batch` 读取 JSON Lines 清单。每个非空行是一条 JSON object。相对路径按清单文件所在目录解析, 这让批量任务可以和素材放在同一目录中。

示例清单:

```jsonl
{"text": "第一句。", "output": "out/001.wav"}
{"text": "第二句。", "emotion_audio": "../emo_sad.wav", "emotion_weight": 0.75, "output": "out/002.wav"}
{"text": "第三句。", "emotion_vector": [0, 0, 0.6, 0, 0, 0, 0, 0], "output": "out/003.wav"}
```

先校验清单, 不加载模型:

```bash
indextts2-cli batch --batch-file examples/batch/demo.jsonl --voice examples/voice_01.wav --dry-run
```

执行批量合成:

```bash
indextts2-cli batch --batch-file examples/batch/demo.jsonl --voice examples/voice_01.wav
```

自动命名输出文件:

```bash
indextts2-cli batch --batch-file examples/batch/auto-output.jsonl --voice examples/voice_01.wav --output-dir examples/batch/out/auto --output-prefix chapter
```

批量合成后拼接为一个 WAV:

```bash
indextts2-cli batch --batch-file examples/batch/batch-concat.jsonl --voice examples/voice_01.wav --concat --output examples/batch/out/story.wav
```

## 拼接已有 WAV

`concat` 不加载模型。它只按 JSON Lines 清单拼接已有 WAV 文件, 适合把已生成的片段拼成一条音频。

清单示例:

```jsonl
{"audio": "../emo_hate.wav", "silence_after_ms": 300}
{"audio": "../emo_sad.wav", "silence_after_ms": 500}
```

先校验:

```bash
indextts2-cli concat --concat-file examples/batch/concat-audio.jsonl --output examples/batch/out/joined.wav --dry-run
```

执行拼接:

```bash
indextts2-cli concat --concat-file examples/batch/concat-audio.jsonl --output examples/batch/out/joined.wav
```

所有输入 WAV 的采样率, 声道数和采样宽度必须一致。

## 常见问题

### Python 3.13 下安装失败

如果看到类似错误:

```text
RuntimeError: Cannot install on Python version 3.13.5
help: `numba` (v0.58.1) was included because `indextts2-cli` depends on `numba`
```

说明安装器正在用 Python 3.13 创建工具环境。`indextts2-cli` 在包元数据中声明了 `>=3.10,<3.12`, 但 PyPI 只负责托管包, 不会阻止你下载包文件。实际选择 Python 解释器和解析依赖的是 `uv`。

请显式指定 Python 3.10 或 3.11:

```bash
uv tool install --python 3.10 indextts2-cli
```

如果本机没有 Python 3.10, 先安装:

```bash
uv python install 3.10
uv tool install --python 3.10 indextts2-cli
```

### 找不到模型资源

先运行:

```bash
indextts2-cli check
```

如果提示模型目录不存在或资源缺失, 运行:

```bash
indextts2-cli download
```

如果模型已经在其他目录, 写入配置:

```bash
indextts2-cli config set model_dir D:/models/IndexTTS-2
```

### 设备不可用

查看当前环境:

```bash
indextts2-cli check
```

临时改用 CPU:

```bash
indextts2-cli synth --text "CPU 测试。" --voice examples/voice_01.wav --output outputs/cpu.wav --device cpu
```

### 输出文件已存在

默认不覆盖已有文件。你可以换一个输出路径, 或明确加 `--force`。

### 想看模型推理日志

默认会隐藏模型初始化和推理过程中的普通标准输出。调试时加入 `--verbose`:

```bash
indextts2-cli synth --text "调试输出。" --voice examples/voice_01.wav --output outputs/debug.wav --verbose
```

## 当前限制

当前 CLI 不提供以下能力:

- WebUI 子命令, WebUI 仍使用 `uv run webui.py`。
- `batch` 的并发执行。
- `batch` 的 JSON 输出或机器可读报告文件。
- 随机情感采样。
- 生成配置文件参数, 例如 `--generation-config`。
- GPT 采样细节参数, 例如 `top_p`, `top_k`, `temperature`。

这些限制可以让 CLI 保持稳定, 明确和可预期。

## 和官方项目的关系

本项目是非官方 fork。它复用了官方 IndexTTS 项目的代码, 模型接口和许可证文件, 并增加了面向用户级安装的 IndexTTS2 CLI 工作流。

任何对原模型或原代码的修改均不受原权利人认可, 保证或背书。原权利人不对本 fork 承担责任。

## 许可证

本项目保留原项目许可证和版权声明。使用, 分发或发布本项目时, 你需要遵守仓库中的 `LICENSE` 和相关模型许可证文件。

如果你分发本项目或其派生版本, 请保留原始版权声明, 许可证文本, 并向下游用户说明本项目是非官方派生版本。
