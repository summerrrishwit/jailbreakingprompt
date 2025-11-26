#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用示例 - 演示如何使用场景处理程序
"""

from process_scenarios import process_question

def example_1():
    """示例1: 数据库优化问题"""
    question = "如何优化数据库查询性能[索引优化][查询语句优化][缓存策略]"
    print(f"\n示例1: {question}")
    process_question(question, output_dir="./output")


def example_2():
    """示例2: 用户登录功能"""
    question = "用户登录功能实现[用户名密码登录][第三方登录][手机验证码登录]"
    print(f"\n示例2: {question}")
    process_question(question, output_dir="./output")


def example_3():
    """示例3: 电商订单处理"""
    question = "电商系统订单处理[订单创建][订单支付][订单配送][订单退款]"
    print(f"\n示例3: {question}")
    process_question(question, output_dir="./output")


def custom_example():
    """自定义示例"""
    # 您可以在这里输入自己的问题
    question = input("\n请输入包含场景的问题: ")
    if question:
        process_question(question, output_dir="./output")


if __name__ == "__main__":
    print("=" * 60)
    print("场景处理程序 - 使用示例")
    print("=" * 60)
    
    # 运行示例
    example_1()
    example_2()
    example_3()
    
    print("\n" + "=" * 60)
    print("所有示例已完成！")
    print("=" * 60)

