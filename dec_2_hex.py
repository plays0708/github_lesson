def decimal_to_hexadecimal(decimal):
    # 16진수로 변환한 문자열을 저장할 변수
    hex_str = ""
    # 16진수로 변환할 수 있는 숫자와 문자를 저장한 딕셔너리
    hex_dict = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
    
    # 입력받은 10진수가 0이 될 때까지 반복
    while decimal > 0:
        # 16으로 나눈 나머지를 계산
        remainder = decimal % 16
        # 나머지가 10 이상인 경우 딕셔너리에서 값을 가져옴
        if remainder >= 10:
            hex_digit = hex_dict[remainder]
        else:
            hex_digit = str(remainder)
        # 계산된 16진수 자릿수를 앞쪽에 추가
        hex_str = hex_digit + hex_str
        # 16으로 나눈 몫을 다시 계산
        decimal = decimal // 16
        
    # 변환된 16진수 문자열 반환
    return hex_str