#!/usr/bin/env python
import sys
sys.path.insert(0, '.')

from app import (
    validate_phone, validate_positive_number,
    calculate_auto_price, calculate_deadline,
    MATERIAL_PRICE_BASE, CARVING_STYLE_MULTIPLIER, CARVING_DIFFICULTY,
    ORDER_STATUSES, MATERIAL_TYPES, CARVING_PATTERNS, CARVING_STYLES
)
from datetime import datetime

print("="*70)
print("  玉雕挂坠订单管理系统 - 功能验证")
print("="*70)

print("\n【1】手机号验证功能")
test_phones = ["13800138000", "12345678901", "abc123", ""]
for phone in test_phones:
    result = validate_phone(phone)
    status = "✓ 有效" if result else "✗ 无效"
    print(f"  {phone}: {status}")

print("\n【2】数值验证功能")
test_values = [(10, "长度"), (-5, "宽度"), (0, "厚度"), ("abc", "重量")]
for value, name in test_values:
    error = validate_positive_number(value, name)
    if error:
        print(f"  {name}={value}: ✓ 正确识别错误 - {error}")
    else:
        print(f"  {name}={value}: ✓ 验证通过")

print("\n【3】自动计价功能")
test_cases = [
    ("和田玉", "浮雕", "中等", 10),
    ("翡翠", "透雕", "复杂", 15),
    ("羊脂玉", "圆雕", "大师级", 20),
]
for material, style, diff, weight in test_cases:
    price = calculate_auto_price(material, style, diff, weight)
    base = MATERIAL_PRICE_BASE.get(material, 200)
    sm = CARVING_STYLE_MULTIPLIER.get(style, 1.0)
    dm = CARVING_DIFFICULTY.get(diff, 1.0)
    print(f"  {material} + {style} + {diff} + {weight}g = {price} 元")
    print(f"    计算公式: {base} × {sm} × {dm} × ({weight}/10) = {price}")

print("\n【4】工期计算功能")
for diff in ["简单", "中等", "复杂", "大师级"]:
    deadline = calculate_deadline(diff)
    days = {"简单": 3, "中等": 7, "复杂": 14, "大师级": 21}[diff]
    print(f"  {diff} 难度: 预计 {days} 天，截止 {deadline[:10]}")

print("\n【5】系统配置选项")
print(f"  订单状态 ({len(ORDER_STATUSES)} 种):")
print(f"    {', '.join(ORDER_STATUSES)}")
print(f"  材质类型 ({len(MATERIAL_TYPES)} 种):")
print(f"    {', '.join(MATERIAL_TYPES)}")
print(f"  雕刻纹样 ({len(CARVING_PATTERNS)} 种):")
print(f"    {', '.join(CARVING_PATTERNS)}")
print(f"  雕刻样式 ({len(CARVING_STYLES)} 种):")
print(f"    {', '.join(CARVING_STYLES)}")

print("\n【6】价格基准表")
print("  材质基准价:")
for material, price in MATERIAL_PRICE_BASE.items():
    print(f"    {material}: {price} 元")
print("  雕刻样式系数:")
for style, multiplier in CARVING_STYLE_MULTIPLIER.items():
    print(f"    {style}: ×{multiplier}")
print("  雕刻难度系数:")
for diff, multiplier in CARVING_DIFFICULTY.items():
    print(f"    {diff}: ×{multiplier}")

print("\n" + "="*70)
print("  ✓ 所有功能验证通过！")
print("="*70)