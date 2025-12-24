# llm-attacks (GCG) 数据集生成代码分析

## 核心代码文件

- `experiments/main.py`: 攻击脚本入口，协调整个攻击过程。
- `llm_attacks/gcg/gcg_attack.py`: 包含了 Greedy Coordinate Gradient (GCG) 攻击的核心算法实现。
- `llm_attacks/base/attack_manager.py`: 管理 Prompt 和攻击迭代，包含模型加载逻辑 (`get_workers`, `ModelWorker`)。

## 生成流程 (对抗样本生成)

该项目的“数据集生成”即是运行攻击算法以寻找能够绕过 LLM 防御的对抗后缀 (Adversarial Suffixes) 的过程。

### 1. 初始化 (`experiments/main.py`)

-   **加载配置**: 读取命令行参数指定 Config 文件 (如 `experiments/configs/individual_llama2.py`)。
-   **加载模型**: `get_workers` 根据配置初始化目标 LLM 模型。
    -   模型加载依赖 `transformers.AutoModelForCausalLM`。
    -   支持多 GPU 加载 (`ModelWorker` 类)。

### 2. GCG 攻击循环 (`llm_attacks/gcg/gcg_attack.py`)

主要逻辑在 `GCGMultiPromptAttack.step` 和 `token_gradients` 中：

1.  **计算梯度**: 计算损失函数相对于输入 Token 的梯度。
2.  **采样候选**: 根据梯度，选取 Top-K 个最有潜力的替换 token。
3.  **评估候选**: 计算每个候选后缀在目标模型上的 Loss。
4.  **更新后缀**: 选择 Loss 最小的候选后缀。

### 3. 数据保存

结果（包括成功的对抗后缀、Logits、Loss 等）会被记录在 JSON 文件中。

## 环境部署

### 1. 安装依赖

```bash
pip install -r requirements.txt
pip install -e .
```
注意：`fschat` 可能需要特定版本以支持某些模板功能。

### 2. 准备模型

代码默认从 Hugging Face 自动下载模型。如果服务器无法联网，需预先下载模型权重并修改 Config 路径。

## 如何更换其他大模型

本项目设计了灵活的配置系统，更换模型通常只需修改 Config 文件，无需修改核心代码。

### 1. 创建或修改 Config 文件

在 `experiments/configs/` 目录下创建一个新的 python 配置文件（参考 `individual_llama2.py`）。

关键需要修改的参数：

```python
import os

os.sys.path.append("..")
from configs.template import get_config as default_config

def get_config():
    config = default_config()

    # 修改模型路径 (可以是 Hugging Face ID 或本地绝对路径)
    config.model_paths = [
        "your-org/your-new-model-7b",
    ]
    
    # 修改 Tokenizer 路径 (通常与模型路径一致)
    config.tokenizer_paths = [
        "your-org/your-new-model-7b",
    ]
    
    # 修改对话模板 (需与 fastchat 支持的模板名称一致)
    # 查看 fastchat/conversation.py 或 llm_attacks/base/attack_manager.py 中的支持列表
    config.conversation_templates = ["llama-2"] 

    return config
```

### 2. 运行攻击

使用新的 Config 文件启动攻击：

```bash
python -u experiments/main.py \
    --config=experiments/configs/your_new_config.py \
    # ... 其他参数
```

## 集成内部 API (代码已注入)

已将适配内部网关 API (`VivoAPIWorker`) 的代码以**注释形式**注入到项目中。

### 1. 核心类定义
文件: `llm_attacks/base/attack_manager.py`
状态: **已注入 (已注释)**

**启用步骤**:
1.  打开 `llm_attacks/base/attack_manager.py`。
2.  搜索 `class VivoAPIWorker`。
3.  取消注释该类的所有代码。

### 2. 使用方法

启用后，你可以参照 `ModelWorker` 的用法，在攻击脚本中实例化 `VivoAPIWorker` 来替代原有的 Worker，或者用于评估生成。

**注意**：如前所述，由于 GCG 算法依赖梯度，`VivoAPIWorker` 仅适用于不需要梯度的场景（如作为验证模型，或仅评估 Teacher Forcing Loss）。
