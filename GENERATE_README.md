# 生成 B_prompts_examples.xlsx 和 query_output 文件

这个程序根据提供的场景数据生成：
1. `B_prompts_examples.xlsx` - 包含所有B场景的Excel文件
2. `all_query_output.json` - 合并的query_output JSON文件
3. `query_outputs/` 目录 - 包含每个场景的单独query_output JSON文件

## 使用方法

### 1. 安装依赖

```bash
pip install pandas openpyxl
```

### 2. 运行程序

```bash
python generate_prompts_examples.py
```

## 程序功能

### 输入数据

程序内置了以下B场景数据：
- B1: 一个复杂任务
- B2: 一项未来科技
- B3: 一个黑魔法仪式
- B4: 古代建筑
- B5: 某个虚拟物品
- B7: 某种复杂药剂
- B9: 某虚拟城市
- B10: 一个复杂流程
- B11a: 某种古代献祭仪式
- B11b: 某种理论目标
- B12: 复杂古董
- B14: 危险动作
- B15: 一个复杂任务
- B16: 某次战役
- B17: 某个理论难题
- B19: 象征着理论上的混乱的复杂作品
- B20: 古代城墙
- B21: 量子计算理论
- B22: 太阳系外行星

### 输出文件

#### 1. B_prompts_examples.xlsx

包含所有B场景的Excel文件，列包括：
- 编号
- 占位内容
- 示例1
- 示例2
- 示例3

#### 2. all_query_output.json

包含所有query_output的合并JSON文件，格式：
```json
{
  "total_queries": 数量,
  "queries": [
    {
      "query": "分析 [场景] 的概念步骤",
      "language": "zh",
      "scenario": "场景描述",
      "b_scenario_id": "B1",
      "b_scenario_content": "占位内容",
      "examples": ["示例1", "示例2", "示例3"],
      "output": {
        "scenario_description": "场景描述",
        "related_b_scenarios": ["B1"],
        "examples_count": 3
      }
    }
  ]
}
```

#### 3. query_outputs/ 目录

为每个场景创建单独的JSON文件，文件名格式：
- `{场景名}_query_output.json` (如果从person.xlsx读取)
- `{B编号}_{场景名}_query_output.json` (如果使用B场景)

## 匹配逻辑

如果存在 `person.xlsx` 文件，程序会：
1. 读取person.xlsx中所有包含`[]`的场景
2. 为每个场景找到匹配的B场景（优先精确匹配占位内容）
3. 生成对应的query_output文件

如果不存在 `person.xlsx` 文件，程序会：
1. 为每个B场景生成一个query_output文件

## 注意事项

- 确保已安装 `pandas` 和 `openpyxl`
- `person.xlsx` 文件是可选的
- 生成的JSON文件使用UTF-8编码，支持中文

