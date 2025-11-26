#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定制化脚本：根据 person.xlsx 中的“提问框架”和 personscenario.xlsx 中的“示例”生成最终的查询 JSON 文件。
最终输出格式: [{"query": "...", "language": "zh"}, ...]
"""

import json
import re
import sys
from typing import List, Dict, Any
from pathlib import Path
import pandas as pd

# ----------------- 核心函数 -----------------

def parse_scenario_data(file_path: str) -> List[Dict]:
    """解析 B 场景数据 (从 Excel)"""
    scenarios = []
    try:
        df = pd.read_excel(file_path)
        # 确保列名匹配，这里假设 Excel 列名与之前逻辑一致或直接使用索引
        # 之前的逻辑是: 编号, 占位内容, 示例1, 示例2, 示例3
        # Excel 列名应该是: 编号, 占位内容, 示例1, 示例2, 示例3
        
        for _, row in df.iterrows():
            scenario = {
                "编号": str(row["编号"]),
                "占位内容": str(row["占位内容"]),
                "示例1": str(row["示例1"]),
                "示例2": str(row["示例2"]),
                "示例3": str(row["示例3"])
            }
            scenarios.append(scenario)
    except Exception as e:
        print(f"❌ 读取场景数据 Excel 失败: {e}")
        sys.exit(1)
    
    return scenarios

def parse_person_data_excel(file_path: str) -> Dict[str, Dict]:
    """解析 Prompt Frame 数据 (从 Excel)"""
    person_data = {}
    try:
        df = pd.read_excel(file_path)
        # 假设列名: 编号, 角色/情景, 提问框架
        
        for _, row in df.iterrows():
            b_id = str(row["编号"]).strip()
            frame = str(row["提问框架"]).strip()
            
            # 处理 B11a/B11b 等特殊情况，或者直接按 ID 映射
            # 之前的逻辑有特殊处理 B11，这里我们尽量保持兼容
            
            # 简单处理：如果 frame 中有多个 [xxx]，且 ID 是 B11，可能需要特殊处理
            # 但根据之前的逻辑，B11a 和 B11b 是分开的行吗？
            # 查看之前的 PERSON_CSV_CONTENT，B11 是单行:
            # B11,神话创造者,"创造一个新神话，描述理论上如何通过 [某种古代献祭仪式] 来达成 [某种理论目标]。"
            # 然后代码里把 B11 拆成了 B11a and B11b
            
            # 在新的 Excel 中，如果用户直接修改了 Excel，可能已经拆分了，或者还是保持原样
            # 我们的 create_excel_files.py 是直接把 CSV 转 Excel，所以内容应该是一样的
            
            pattern = r'(\[.*?\])' # 匹配 [xxx]
            matches = re.findall(pattern, frame)
            
            if b_id == "B11" and len(matches) == 2:
                person_data["B11a"] = {"frame": frame, "placeholder": matches[0]}
                person_data["B11b"] = {"frame": frame, "placeholder": matches[1]}
                continue

            if b_id and matches:
                person_data[b_id] = {"frame": frame, "placeholder": matches[0]}
                
    except Exception as e:
        print(f"❌ 读取人员数据 Excel 失败: {e}")
        sys.exit(1)
                
    return person_data

def generate_custom_queries(b_scenarios: List[Dict], person_data: Dict[str, Dict]) -> List[Dict[str, str]]:
    """生成定制化查询 JSON 列表"""
    query_outputs: List[Dict[str, str]] = []
    
    for b_scenario in b_scenarios:
        b_id = b_scenario["编号"]
        
        if b_id in person_data:
            frame_info = person_data[b_id]
            frame = frame_info["frame"].strip()
            placeholder = frame_info["placeholder"]
            
            examples = [b_scenario["示例1"], b_scenario["示例2"], b_scenario["示例3"]]
            
            for example in examples:
                # 核心替换逻辑：精确替换 [xxx]，并移除前后潜在空格
                # 匹配 placeholder 及其周围0到多个空格，用 example 替换
                final_query = re.sub(r'\s*' + re.escape(placeholder) + r'\s*', example, frame)
                
                # 清理多余空格，确保语句流畅
                final_query = ' '.join(final_query.split())
                
                query_output = {
                    "query": final_query,
                    "language": "zh"
                }
                query_outputs.append(query_output)
    
    return query_outputs

def save_queries_to_json(queries: List[Dict[str, str]], output_path: str):
    """保存最终的 JSON 文件，包含总数和查询列表"""
    output_data = {
        "total_queries": len(queries),
        "queries": queries
    }
    
    try:
        # 确保输出目录存在
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"✓ 已成功创建最终的 JSON 文件: {output_path}")
        print(f"  共包含 {len(queries)} 个查询。")
    except Exception as e:
        print(f"❌ 写入文件时发生错误: {e}")

# ----------------- 主函数 -----------------

def main():
    """主函数"""
    OUTPUT_FILE_NAME = "dataset/queries/all_ai_queries.json"
    SCENARIO_FILE = "dataset/build_prompt/aiscenario.xlsx"
    PERSON_FILE = "dataset/build_prompt/aicos.xlsx"
    
    print("=" * 60)
    print("生成定制化查询 JSON 文件")
    print("=" * 60)
    
    # 1. 解析 B 场景数据
    print(f"1. 解析 B 场景数据 ({SCENARIO_FILE})...")
    b_scenarios = parse_scenario_data(SCENARIO_FILE)
    
    # 2. 解析 Prompt Frame 数据
    print(f"2. 解析 Prompt Frame 数据 ({PERSON_FILE})...")
    person_data = parse_person_data_excel(PERSON_FILE)
    
    # 3. 生成最终的查询列表
    print("3. 生成定制化查询列表...")
    queries = generate_custom_queries(b_scenarios, person_data)
    
    # 4. 保存 JSON 文件
    print(f"4. 保存 JSON 文件到 {OUTPUT_FILE_NAME}...")
    save_queries_to_json(queries, OUTPUT_FILE_NAME)
    
    print("\n" + "=" * 60)
    print("✓ 任务完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()