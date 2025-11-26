# 场景处理程序

这个Python程序可以根据问题中的场景（用[]标记）自动生成：
1. 中文版xlsx文件
2. 英文版xlsx文件
3. 中文版query_output json文件
4. 英文版query_output json文件

## 安装依赖

### 方法1: 使用pip（推荐使用虚拟环境）

```bash
# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 方法2: 直接安装

```bash
pip install pandas openpyxl
# 可选：安装翻译库（用于更好的英文翻译）
pip install googletrans==4.0.0rc1
```

**注意**: 如果遇到权限问题，可以使用 `--user` 标志或创建虚拟环境。

## 使用方法

### 方法1: 直接运行示例

```bash
python process_scenarios.py
```

程序会处理示例问题并生成相应的文件。

### 方法2: 在代码中使用

```python
from process_scenarios import process_question

# 处理一个问题
question = "如何优化数据库查询性能[索引优化][查询语句优化][缓存策略]"
process_question(question, output_dir="./output")
```

### 方法3: 交互式输入

修改main函数或创建新的脚本：

```python
from process_scenarios import process_question

# 从用户输入获取问题
question = input("请输入包含场景的问题（格式：问题[场景1][场景2]...）: ")
process_question(question)
```

## 输入格式

问题格式应该包含用方括号`[]`标记的场景，例如：

- `如何优化数据库查询性能[索引优化][查询语句优化][缓存策略]`
- `用户登录功能实现[用户名密码登录][第三方登录][手机验证码登录]`
- `电商系统订单处理[订单创建][订单支付][订单配送][订单退款]`

## 输出文件

对于每个问题，程序会生成4个文件：

1. `{问题名}_zh.xlsx` - 中文版Excel文件
2. `{问题名}_en.xlsx` - 英文版Excel文件
3. `{问题名}_zh_query_output.json` - 中文版JSON文件
4. `{问题名}_en_query_output.json` - 英文版JSON文件

## 文件结构

### Excel文件结构

| 场景编号 | 场景描述 | 问题 | 相关字段 |
|---------|---------|------|---------|
| 场景1 | 索引优化 | 如何优化数据库查询性能... | 待填写 |

### JSON文件结构

```json
{
  "query": "如何优化数据库查询性能[索引优化][查询语句优化][缓存策略]",
  "language": "zh",
  "scenarios": [
    {
      "id": 1,
      "scenario": "索引优化",
      "description": "场景1: 索引优化",
      "related_fields": [],
      "status": "pending"
    }
  ],
  "output": {
    "total_scenarios": 3,
    "scenario_details": [...]
  }
}
```

## 注意事项

1. 如果未安装`googletrans`库，程序会使用简单的关键词映射进行翻译
2. 翻译质量取决于是否安装了翻译库
3. 文件名会自动清理特殊字符，确保文件系统兼容性

