#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查person.xlsx文件的结构
"""

try:
    import pandas as pd
    import re
    
    file_path = "person.xlsx"
    
    print("=" * 60)
    print(f"读取 {file_path}")
    print("=" * 60)
    
    df = pd.read_excel(file_path)
    
    print(f"\n文件形状: {df.shape}")
    print(f"列名: {df.columns.tolist()}")
    print(f"\n前10行数据:")
    print(df.head(10))
    
    print(f"\n查找包含[]的内容:")
    scenarios_found = []
    for col in df.columns:
        for idx, value in df[col].items():
            if pd.notna(value) and isinstance(value, str):
                pattern = r'\[([^\]]+)\]'
                matches = re.findall(pattern, str(value))
                if matches:
                    scenarios_found.append({
                        "列": col,
                        "行": idx + 1,
                        "内容": str(value),
                        "场景": matches
                    })
    
    if scenarios_found:
        print(f"\n找到 {len(scenarios_found)} 个包含场景的单元格:")
        for item in scenarios_found[:10]:  # 只显示前10个
            print(f"  列: {item['列']}, 行: {item['行']}")
            print(f"  场景: {item['场景']}")
            print(f"  内容: {item['内容'][:50]}...")
            print()
    else:
        print("\n未找到包含[]的场景")
        
except ImportError:
    print("需要安装pandas: pip install pandas openpyxl")
except FileNotFoundError:
    print(f"文件 {file_path} 不存在")
except Exception as e:
    print(f"错误: {e}")

