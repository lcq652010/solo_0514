import re


def validate_id_card(id_card):
    if not id_card:
        return False, '身份证号不能为空'
    
    if len(id_card) != 18:
        return False, '身份证号长度必须为18位'
    
    pattern = r'^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$'
    if not re.match(pattern, id_card):
        return False, '身份证号格式不正确'
    
    factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    
    total = sum(int(id_card[i]) * factors[i] for i in range(17))
    check_code = check_codes[total % 11]
    
    if id_card[17].upper() != check_code:
        return False, '身份证号校验码不正确'
    
    return True, '身份证号格式正确'


def validate_phone(phone):
    if not phone:
        return False, '手机号不能为空'
    
    pattern = r'^1[3-9]\d{9}$'
    if not re.match(pattern, phone):
        return False, '手机号格式不正确，必须为11位有效手机号'
    
    return True, '手机号格式正确'


def validate_driver_license(license_no):
    if not license_no:
        return False, '驾驶证号不能为空'
    
    if len(license_no) < 10 or len(license_no) > 20:
        return False, '驾驶证号长度应在10-20位之间'
    
    pattern = r'^[A-Za-z0-9]{10,20}$'
    if not re.match(pattern, license_no):
        return False, '驾驶证号格式不正确，只能包含字母和数字'
    
    return True, '驾驶证号格式正确'


def validate_amount(amount, min_value=0, max_value=1000000):
    if amount is None:
        return False, '金额不能为空'
    
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return False, '金额必须为有效数字'
    
    if amount < min_value:
        return False, f'金额不能小于{min_value}'
    
    if amount > max_value:
        return False, f'金额不能超过{max_value}'
    
    return True, '金额格式正确'


def validate_date_range(start_date, end_date):
    if not start_date or not end_date:
        return False, '开始日期和结束日期都不能为空'
    
    if start_date > end_date:
        return False, '开始日期不能晚于结束日期'
    
    return True, '日期范围有效'
