#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式场景处理程序 - 可以从命令行或交互式输入问题
"""

import sys
from pathlib import Path
from process_scenarios import process_question, extract_scenarios_from_question


def interactive_mode():
    """交互式模式"""
    print("=" * 60)
    print("场景处理程序 - 交互式模式")
    print("=" * 60)
    print("\n请输入包含场景的问题（格式：问题[场景1][场景2]...）")
    print("例如: 如何优化数据库查询性能[索引优化][查询语句优化][缓存策略]")
    print("输入 'quit' 或 'exit' 退出\n")
    
    while True:
        try:
            question = input("问题: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\n再见！")
                break
            
            if not question:
                print("问题不能为空，请重新输入。\n")
                continue
            
            scenarios = extract_scenarios_from_question(question)
            if not scenarios:
                print("⚠️  警告: 未在问题中找到场景（格式应为：问题[场景1][场景2]...）")
                confirm = input("是否继续处理？(y/n): ").strip().lower()
                if confirm != 'y':
                    continue
            
            print(f"\n找到 {len(scenarios)} 个场景:")
            for idx, scenario in enumerate(scenarios, 1):
                print(f"  {idx}. {scenario}")
            
            output_dir = input("\n输出目录（直接回车使用当前目录）: ").strip()
            if not output_dir:
                output_dir = "."
            
            print("\n正在处理...")
            process_question(question, output_dir)
            print("\n" + "-" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n程序被用户中断。")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}\n")


def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 命令行模式
        question = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
        
        print("=" * 60)
        print("场景处理程序 - 命令行模式")
        print("=" * 60)
        print(f"\n问题: {question}")
        print(f"输出目录: {output_dir}\n")
        
        process_question(question, output_dir)
    else:
        # 交互式模式
        interactive_mode()


if __name__ == "__main__":
    main()

