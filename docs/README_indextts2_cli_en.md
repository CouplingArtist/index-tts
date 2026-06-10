# IndexTTS2 CLI

<p align="center">
  An unofficial IndexTTS2 CLI for local speech synthesis and batch processing
</p>

<p align="center">
  <a href="../README.md">简体中文</a> | English
</p>

`indextts2-cli` is an unofficial command-line package for IndexTTS2. It is based on the [official IndexTTS repository](https://github.com/index-tts/index-tts), fixes several local runtime issues, and provides an installable, configurable, batch-friendly CLI with automatic concatenation support.

This project is not an official release by Bilibili IndexTTS Team. It does not imply approval, warranty, or endorsement by the original right-holder.

## What It Can Do

This project builds on the official repository by fixing model file path and Python version constraint issues, adding batch synthesis and post-synthesis concatenation, and packaging them as a CLI for easier use:

- Use `synth` to synthesize one text input into audio.
- Control speaker timbre with a voice reference audio.
- Control expression with emotion reference audio, emotion description text, or an 8-dimensional emotion vector.
- **Use `batch` to generate multiple audio files from JSON Lines manifests, or optionally concatenate the synthesized output into one WAV file.**
- Use `concat` to concatenate existing WAV files, or concatenate batch synthesis output into one WAV file.

It also provides workflow features for everyday use:

- Run commands from any directory after installation, without depending on the repository root as the current working directory.
- Persist runtime settings such as model directory, device, FP16, DeepSpeed, and CUDA kernel.
- Use `download` to fetch model resources.
- Use `check` to catch model resource, Python package, and device issues before synthesis.
- Use the short command `itts2` for frequent terminal work.

## Main Improvements

Compared with the official repository at the time of the fork, this project mainly adds these changes:

- Fixed model file path issues.
- Fixed Python version constraint issues.
- Added batch speech generation and concatenation.
- Packaged the IndexTTS2 workflow as an installable CLI.

If you only need the official WebUI, continue to use the official repository documentation.

## Installation

This project requires Python `>=3.10,<3.12`. Python 3.10 is recommended because some speech dependencies do not support Python 3.12+ or 3.13 yet.

Install from PyPI:

```bash
uv tool install --python 3.10 indextts2-cli
```

You can also use `pipx`:

```bash
pipx install --python 3.10 indextts2-cli
```

Install from local source:

```bash
uv tool install --python 3.10 .
```

Use editable installation during development:

```bash
uv tool install --python 3.10 -e .
```

Installation registers two equivalent commands:

```bash
indextts2-cli --help
itts2 --help
```

`indextts2-cli` is the full command. `itts2` is the short command. The examples below use the full command, but you can replace it with `itts2`.

## Quick Start

Prepare a speaker reference audio file, such as `voice.wav`. It should be a clear WAV file with human speech.

```bash
indextts2-cli init
indextts2-cli download
indextts2-cli check
indextts2-cli synth --text "Hello, IndexTTS2." --voice voice.wav --output hello.wav
```

These commands:

1. Create local configuration.
2. Download IndexTTS2 model resources.
3. Check models, Python packages, and devices.
4. Synthesize `hello.wav` using `voice.wav` as the reference audio.

If you are running from the repository source directory, you can also use the bundled sample audio:

```bash
indextts2-cli synth --text "Hello, IndexTTS2." --voice examples/voice_01.wav --output outputs/hello.wav
```

Existing output files are not overwritten by default. Add `--force` explicitly to overwrite:

```bash
indextts2-cli synth --text "Regenerate this file." --voice voice.wav --output hello.wav --force
```

## Command Overview

| Command | Purpose | Common Use |
| --- | --- | --- |
| `init` | Create persistent configuration and the default model resource directory | First run |
| `config` | Show or update persistent configuration | Pin model directory and default device |
| `download` | Download IndexTTS2 model resources | Prepare the runtime environment |
| `check` | Check model resources, Python packages, and devices | Diagnose the environment before synthesis |
| `synth` | Synthesize one text input into audio | Quick previews, scripts |
| `batch` | Read a JSON Lines manifest and synthesize audio in batch | Dialogue lines, chapter audio |
| `concat` | Concatenate existing WAV files | Post-processing, joining segments |

See the [CLI v2 usage guide](./cli-v2-usage.md) for all parameters.

## Recommended Workflows

### First Run

```bash
indextts2-cli init
indextts2-cli download
indextts2-cli check
```

### Use an Existing Model Directory

```bash
indextts2-cli config set model_dir D:/models/IndexTTS-2
indextts2-cli check
```

### Pin GPU Settings

```bash
indextts2-cli config set default_device cuda:0
indextts2-cli config set use_fp16 true
indextts2-cli check
```

### Override Runtime Options Once

```bash
indextts2-cli synth --text "GPU inference test." --voice examples/voice_01.wav --output outputs/gpu.wav --device cuda:0 --fp16
```

Command-line options affect only the current run. Use `config set` for long-lived defaults.

## Model Resource Directory

The CLI uses a model resource directory to store IndexTTS2 model files and supporting resources. `init` only creates local configuration and directories. It does not download models automatically.

Model directory resolution order:

1. Command-line option `--model-dir PATH`
2. Environment variable `INDEXTTS2_MODEL_DIR`
3. Persistent configuration key `model_dir`
4. Platform default model resource directory

Use an existing model directory:

```bash
indextts2-cli config set model_dir D:/models/IndexTTS-2
indextts2-cli check
```

Download models and persist the directory:

```bash
indextts2-cli download --model-dir D:/models/IndexTTS-2
```

Download into a temporary directory without updating configuration:

```bash
indextts2-cli download --model-dir D:/tmp/IndexTTS-2 --no-save
```

## Configuration

Print the configuration file path:

```bash
indextts2-cli config path
```

Show current configuration:

```bash
indextts2-cli config get
```

Common settings:

```bash
indextts2-cli config set model_dir D:/models/IndexTTS-2
indextts2-cli config set default_device cuda:0
indextts2-cli config set use_fp16 true
indextts2-cli config set use_deepspeed false
indextts2-cli config set use_cuda_kernel false
```

Persistent configuration keys:

| Key | Description |
| --- | --- |
| `model_dir` | IndexTTS2 model resource directory |
| `default_device` | Default runtime device, such as `cpu`, `cuda`, `cuda:0`, `mps`, or `xpu` |
| `use_fp16` | Whether to enable FP16 by default |
| `use_deepspeed` | Whether to enable DeepSpeed by default |
| `use_cuda_kernel` | Whether to enable CUDA kernel by default |

## Single-Text Synthesis

Pass text directly:

```bash
indextts2-cli synth --text "This is a test voice." --voice examples/voice_01.wav --output outputs/test.wav
```

Read from a UTF-8 text file:

```bash
indextts2-cli synth --text-file input.txt --voice examples/voice_01.wav --output outputs/from-file.wav
```

Read from standard input:

```bash
echo "This text comes from standard input." | indextts2-cli synth --stdin --voice examples/voice_01.wav --output outputs/stdin.wav
```

### Emotion Control

Use an emotion reference audio:

```bash
indextts2-cli synth --text "Speech with an emotion reference." --voice examples/voice_01.wav --emotion-audio examples/emo_sad.wav --emotion-weight 0.75 --output outputs/emotion.wav
```

Use emotion description text:

```bash
indextts2-cli synth --text "Read this in a warm and calm tone." --voice examples/voice_01.wav --emotion-text "warm and calm" --emotion-weight 0.6 --output outputs/emotion-text.wav
```

Use an 8-dimensional emotion vector:

```bash
indextts2-cli synth --text "Use an emotion vector." --voice examples/voice_01.wav --emotion-vector 0,0,0.8,0,0,0,0,0 --emotion-weight 1.0 --output outputs/vector.wav
```

Use only one of `--emotion-audio`, `--emotion-text`, and `--emotion-vector` in each run.

## Batch Synthesis

`batch` reads a JSON Lines manifest. Each non-empty line is a JSON object. Relative paths are resolved from the manifest file's directory, so batch tasks and assets can live together.

Manifest example:

```jsonl
{"text": "First sentence.", "output": "out/001.wav"}
{"text": "Second sentence.", "emotion_audio": "../emo_sad.wav", "emotion_weight": 0.75, "output": "out/002.wav"}
{"text": "Third sentence.", "emotion_vector": [0, 0, 0.6, 0, 0, 0, 0, 0], "output": "out/003.wav"}
```

Validate the manifest without loading the model:

```bash
indextts2-cli batch --batch-file examples/batch/demo.jsonl --voice examples/voice_01.wav --dry-run
```

Run batch synthesis:

```bash
indextts2-cli batch --batch-file examples/batch/demo.jsonl --voice examples/voice_01.wav
```

Generate output filenames automatically:

```bash
indextts2-cli batch --batch-file examples/batch/auto-output.jsonl --voice examples/voice_01.wav --output-dir examples/batch/out/auto --output-prefix chapter
```

Synthesize in batch and concatenate into one WAV:

```bash
indextts2-cli batch --batch-file examples/batch/batch-concat.jsonl --voice examples/voice_01.wav --concat --output examples/batch/out/story.wav
```

## Concatenate Existing WAV Files

`concat` does not load the model. It concatenates existing WAV files from a JSON Lines manifest, which is useful when you already have generated segments.

Manifest example:

```jsonl
{"audio": "../emo_hate.wav", "silence_after_ms": 300}
{"audio": "../emo_sad.wav", "silence_after_ms": 500}
```

Validate first:

```bash
indextts2-cli concat --concat-file examples/batch/concat-audio.jsonl --output examples/batch/out/joined.wav --dry-run
```

Run concatenation:

```bash
indextts2-cli concat --concat-file examples/batch/concat-audio.jsonl --output examples/batch/out/joined.wav
```

All input WAV files must use the same sample rate, channel count, and sample width.

## Troubleshooting

### Installation fails on Python 3.13

If you see an error like this:

```text
RuntimeError: Cannot install on Python version 3.13.5
help: `numba` (v0.58.1) was included because `indextts2-cli` depends on `numba`
```

The installer is creating the tool environment with Python 3.13. `indextts2-cli` declares `>=3.10,<3.12` in package metadata, but PyPI only hosts package files. The installer, in this case `uv`, chooses the Python interpreter and resolves dependencies.

Specify Python 3.10 or 3.11 explicitly:

```bash
uv tool install --python 3.10 indextts2-cli
```

If Python 3.10 is not installed, install it first:

```bash
uv python install 3.10
uv tool install --python 3.10 indextts2-cli
```

### Model resources are missing

Run:

```bash
indextts2-cli check
```

If the model directory is missing or incomplete, run:

```bash
indextts2-cli download
```

If models already exist in another directory, persist that directory:

```bash
indextts2-cli config set model_dir D:/models/IndexTTS-2
```

### Device is unavailable

Inspect the current environment:

```bash
indextts2-cli check
```

Temporarily use CPU:

```bash
indextts2-cli synth --text "CPU test." --voice examples/voice_01.wav --output outputs/cpu.wav --device cpu
```

### Output file already exists

Existing files are not overwritten by default. Use a different output path, or add `--force` explicitly.

### Need model inference logs

Normal stdout from model initialization and inference is hidden by default. Add `--verbose` while debugging:

```bash
indextts2-cli synth --text "Debug output." --voice examples/voice_01.wav --output outputs/debug.wav --verbose
```

## Current Limits

The CLI does not currently provide:

- A WebUI subcommand. Continue to use `uv run webui.py` for WebUI.
- Concurrent `batch` execution.
- JSON output or machine-readable report files for `batch`.
- Random emotion sampling.
- Generation configuration file options such as `--generation-config`.
- GPT sampling parameters such as `top_p`, `top_k`, and `temperature`.

These limits keep the CLI stable, explicit, and predictable.

## Relationship to the Official Project

This project is an unofficial fork. It reuses code, model interfaces, and license files from the official IndexTTS project, and adds a user-level IndexTTS2 CLI workflow.

Any modifications to the original model or source code are not endorsed, warranted, or guaranteed by the original right-holder. The original right-holder disclaims all liability related to this fork.

## License

This project preserves the original project's license and copyright notices. When using, distributing, or publishing this project, you must comply with the repository's `LICENSE` and related model license files.

If you distribute this project or a derivative version, keep the original copyright notices and license texts, and tell downstream users that this project is an unofficial derivative version.
