# toxic-prompt 数据集生成代码分析

## 核心代码文件

- `2_and_3_toxic_generation.py`: 用于执行 Task 2 (Toxic Span Detection) 和 Task 3 (Detoxification) 的生成任务脚本。
- `parsed_dataset/`: 存放原始输入数据的目录。

## 生成流程 (Detoxification / Span Detection)

该项目使用 **Prompt Learning** (基于 `openprompt` 库) 来生成数据（即生成去毒后的句子或标记有毒片段的句子）。

### 1. 数据处理 (`MyDataProcessor`)

-   **加载**: 从 `parsed_dataset/` 下的 JSON 文件读取数据。
-   **转换**: 将数据转换为 `openprompt` 需要的 `InputExample` 格式。

### 2. Prompt 构建

-   使用 `PrefixTuningTemplate` 构建 Prompt 模板。
-   模板示例 (Task 3): `{"placeholder":"text_a"} {"special": "<eos>"} Generate a less toxic sentence:\n{"mask"}.`

### 3. 模型与生成

-   **模型加载**: 使用 `load_plm` 加载预训练模型。
-   **生成**: 调用 `prompt_model.generate` 生成目标句子。

## 环境部署

### 1. 创建 Conda 环境

项目提供了 `environment.yaml` 文件，可以直接创建环境：

```bash
conda env create --file environment.yaml
conda activate toxic_prompt
```

### 2. 依赖说明

主要依赖包括：
-   `openprompt`
-   `pytorch`
-   `transformers`

## 如何更换其他大模型

由于项目使用了 `openprompt` 库，更换模型非常简单，只需在运行脚本时修改命令行参数。

### 1. 修改命令行参数

在运行 `2_and_3_toxic_generation.py` 时，指定 `--model` 和 `--model_name_or_path`：

-   `--model`: 模型类型 (如 `t5`, `gpt2`, `opt`, `llama`)，需是 `openprompt` 支持的类型。
-   `--model_name_or_path`: Hugging Face 模型名称或本地路径。

### 示例：更换为 GPT-2

```bash
python 2_and_3_toxic_generation.py \
    --plm_eval_mode \
    --model gpt2 \
    --model_name_or_path gpt2-medium \
    --dataset TSD
```

### 示例：更换为本地 Llama 模型

假设你有一个本地转换好的 Hugging Face 格式的 Llama 模型：

```bash
python 2_and_3_toxic_generation.py \
    --plm_eval_mode \
    --model llama \
    --model_name_or_path /path/to/your/local/llama-7b \
    --dataset TSD
```

### 注意事项

-   **显存**: 更大的模型需要更多的显存。可能需要调整代码中的 `batch_size` (在 `PromptDataLoader` 初始化处)。
-   **Template 适配**: `PrefixTuningTemplate` 可能对某些新模型的支持需要调整配置，如果不工作，可以尝试换成 `ManualTemplate` 进行测试。

## 集成内部 API (代码已注入)

已将适配内部网关 API (`VivoAPIModel`) 的代码以**注释形式**注入到项目中。

### 1. 核心类定义
文件: `2_and_3_toxic_generation.py`
状态: **已注入 (已注释)**

**启用步骤**:
1.  打开 `2_and_3_toxic_generation.py`。
2.  搜索 `class VivoAPIModel`。
3.  取消注释该类的所有代码。

### 2. 使用方法

**启用步骤**:
1.  在 `2_and_3_toxic_generation.py` 中，找到 `load_plm` 调用的位置（约第 98 行）。
2.  如果不修改 `openprompt` 源码，可以直接手动实例化 `VivoAPIModel` 并覆盖 `plm` 变量，或者修改 `load_plm` 逻辑使其识别 `vivo` 模型类型。
    *   *建议*: 在脚本中 `load_plm` 后添加逻辑：
        ```python
        if args.model == "vivo":
            plm = VivoAPIModel(args.model_name_or_path)
        ```
3.  运行命令：
    ```bash
    python 2_and_3_toxic_generation.py \
        --model vivo \
        --model_name_or_path vivo-BlueLM-TB-Pro \
        --dataset TSD
    ```
