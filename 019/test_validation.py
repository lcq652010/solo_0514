#!/usr/bin/env python
from rental.utils import validate_id_card, validate_phone, validate_driver_license, validate_amount, validate_date_range
from datetime import date


def test_validations():
    print("=" * 50)
    print("汽车租赁管理系统 - 校验功能测试")
    print("=" * 50)
    print()

    print("1. 手机号校验测试:")
    test_phones = ["13800138000", "12345678901", "1380013800", "abc123"]
    for phone in test_phones:
        is_valid, msg = validate_phone(phone)
        print(f"   {phone}: {'✓ 通过' if is_valid else '✗ 失败'} - {msg}")
    print()

    print("2. 身份证校验测试:")
    test_ids = ["110101199003076754", "11010119900307675X", "123456", "11010119900307675"]
    for id_card in test_ids:
        is_valid, msg = validate_id_card(id_card)
        print(f"   {id_card}: {'✓ 通过' if is_valid else '✗ 失败'} - {msg}")
    print()

    print("3. 驾驶证校验测试:")
    test_licenses = ["110101199001", "ABC1234567", "123", "abc@123"]
    for lic in test_licenses:
        is_valid, msg = validate_driver_license(lic)
        print(f"   {lic}: {'✓ 通过' if is_valid else '✗ 失败'} - {msg}")
    print()

    print("4. 金额校验测试:")
    test_amounts = [300, 5, 1000000, -100, "abc"]
    for amount in test_amounts:
        is_valid, msg = validate_amount(amount, 10, 10000)
        print(f"   {amount}: {'✓ 通过' if is_valid else '✗ 失败'} - {msg}")
    print()

    print("5. 日期范围校验测试:")
    today = date.today()
    tomorrow = date.fromordinal(today.toordinal() + 1)
    test_dates = [
        (today, tomorrow),
        (tomorrow, today),
        (None, today)
    ]
    for start, end in test_dates:
        is_valid, msg = validate_date_range(start, end)
        print(f"   {start} ~ {end}: {'✓ 通过' if is_valid else '✗ 失败'} - {msg}")
    print()

    print("=" * 50)
    print("校验功能测试完成！")
    print("=" * 50)


if __name__ == "__main__":
    test_validations()
