import re
import functools

def checkInput(formula):
    """检测输入合法与否,是否包含字母等非法字符"""
    return not re.search("[^0-9+\-*/.()\s]",formula)

def formatInput(formula):
    """标准化输入表达式，去除多余空格等"""
    formula = formula.replace(' ','')
    formula = formula.replace('++', '+')
    formula = formula.replace('+-', '-')
    formula = formula.replace('-+', '-')
    formula = formula.replace('--', '+')
    return formula

def mul_divOperation(s):
    """乘法除法运算"""
    # 1-2*-14969036.7968254
    s = formatInput(s)
    sub_str = re.search('(\d+\.?\d*[*/]-?\d+\.?\d*)', s)
    while sub_str:
        sub_str = sub_str.group()
        if sub_str.count('*'):
            l_num, r_num = sub_str.split('*')
            s = s.replace(sub_str, str(float(l_num)*float(r_num)))
        else:
            l_num, r_num = sub_str.split('/')
            s = s.replace(sub_str, str(float(l_num) / float(r_num)))
        #print(s)
        s = formatInput(s)
        sub_str = re.search('(\d+\.?\d*[*/]\d+\.?\d*)', s)

    return s

def add_minusOperation(s):
    """加法减法运算
    思路：在最前面加上+号，然后正则匹配累加
    """
    s = formatInput(s)
    s = '+' + s
    #print(s)
    tmp = re.findall('[+\-]\d+\.?\d*', s)
    s = str(functools.reduce(lambda x, y:int(x)+int(y), tmp))
    #print(tmp)
    return s

if __name__ == '__main__':

    abc = '5-2'
    result = add_minusOperation(abc)
    print(result)
