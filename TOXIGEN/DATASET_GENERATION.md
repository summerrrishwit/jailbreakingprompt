# TOXIGEN 数据集生成代码分析

## 核心代码文件

- `generate.py`: 主生成脚本，调用 LLM (GPT-3) 生成数据。
- `demonstrations_to_prompts.py`: 辅助脚本，将示例（demonstrations）转换为 few-shot prompts。
- `toxigen/language_models.py`: 包含 `GPT3` 和 `ALICE` 类的定义。`GPT3` 类封装了 API 调用。

## 生成流程

### 1. Prompt 准备

使用 `demonstrations_to_prompts.py` 将单句的示例转换为 few-shot learning 的 prompt。
-  输入：包含示例句子的文本文件（每行一句）。
-  处理：随机抽取 `demonstrations_per_prompt` 个句子，加上连字符 `-` 组成列表形式。
-  输出：生成的 Prompts 保存到文件。

### 2. 数据生成 (`generate.py`)

主程序通过 `main` 函数执行：

1.  **加载 Prompts**: 读取 `--input_prompt_file` 指定的文件。
2.  **初始化模型**:
    -   默认使用 `GPT3` 类（调用 OpenAI API）。
    -   如果开启 `--ALICE` 模式，会加载分类器（HateBERT 或 RoBERTa），并将语言模型包装在 `ALICE` 类中（用于对抗生成或过滤）。
3.  **循环生成**:
    -   遍历每个 prompt。
    -   对每个 prompt 重复 `num_generations_per_prompt` 次生成。
    -   调用 `language_model(prompt)` 获取响应。
4.  **保存结果**: 将生成的响应追加写入 `--output_file`。

## 环境部署

### 1. 安装依赖

该项目依赖 `nltk`, `requests`, `transformers` 和 `pytorch`。

```bash
# 推荐使用 Python 3.8+
pip install -r requirements.txt
python setup.py install
```

### 2. 下载分类器 (仅 ALICE 模式)

如果使用 ALICE 模式，需要下载 HateBERT 或 ToxDectRoBERTa 的模型权重（通常是 Hugging Face 模型）。

## 如何更换其他大模型

目前的 `toxigen/language_models.py` 中的 `GPT3` 类是为了调用 OpenAI 风格的 API 设计的。

### 方法一：使用兼容 OpenAI API 的本地模型

如果你部署了本地模型 (如使用 vLLM 或 TGI) 且其 API 兼容 OpenAI，可以直接复用 `GPT3` 类：
-   在运行 `generate.py` 时，通过环境变量或修改代码传入本地服务的 URL。
-   修改 `generate.py` 中的 `GPT3` 初始化，传入自定义的 `endpoint_url`。

### 方法二：实现自定义模型类

若要直接调用 Hugging Face Transformers 模型或其它 API，需在 `toxigen/language_models.py` 中实现一个新的类，并满足接口要求。

## 集成内部 API (代码已注入)

已将适配内部网关 API (`VivoLLM`) 的代码以**注释形式**注入到项目中。

### 1. 核心类定义
文件: `toxigen/language_models.py`
状态: **已注入 (已注释)**

**启用步骤**:
1.  打开 `toxigen/language_models.py`。
2.  搜索 `class VivoLLM`。
3.  取消注释该类的所有代码。

### 2. 调用逻辑
文件: `generate.py`
状态: **已注入 (已注释)**

**启用步骤**:
1.  打开 `generate.py`。
2.  搜索 `pass # elif args.language_model == "Vivo":` 或相关注释块。
3.  取消注释以下代码：
    ```python
    elif args.language_model == "Vivo":
        from toxigen.language_models import VivoLLM
        language_model = VivoLLM()
    ```

### 3. 运行命令

启用后，使用以下命令运行：

```bash
python generate.py \
    --input_prompt_file prompts/example.txt \
    --output_file generations.txt \
    --num_generations_per_prompt 20 \
    --language_model Vivo
```
