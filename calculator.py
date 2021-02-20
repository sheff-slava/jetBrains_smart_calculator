from collections import deque


def operator_precedence(operator_1, operator_2):
    if operator_1 in ('*', '/'):
        if operator_2 in ('*', '/'):
            return 'Same'
        elif operator_2 in ('+', '-'):
            return 'Higher'
    if operator_1 in ('+', '-'):
        if operator_2 in ('*', '/'):
            return 'Lower'
        elif operator_2 in ('+', '-'):
            return 'Same'


def postfix_to_result(postfix):
    queue = deque()
    for element in postfix:
        if element.isdigit():
            queue.append(element)
        elif element in ('+', '-', '*', '/'):
            number_2 = int(queue.pop())
            number_1 = int(queue.pop())
            if element == '+':
                queue.append(number_1 + number_2)
            elif element == '-':
                queue.append(number_1 - number_2)
            elif element == '*':
                queue.append(number_1 * number_2)
            elif element == '/':
                queue.append(number_1 // number_2)
        else:
            return 'Invalid input'
    return queue.pop()


def infix_to_postfix(infix):
    stack = deque()
    postfix = deque()
    for element in infix:
        if element.isdigit():
            postfix.append(element)
        elif element in ('+', '-', '*', '/'):
            if len(stack) != 0 and stack[-1] != '(':
                while operator_precedence(element, stack[-1]) != 'Higher' or stack[-1] == '(':
                    postfix.append(stack.pop())
                    if len(stack) == 0:
                        break
            stack.append(element)
        elif element in ('(', ')'):
            if element == '(':
                stack.append(element)
            else:
                while stack[-1] != '(':
                    postfix.append(stack.pop())
                stack.pop()
    while len(stack) != 0:
        postfix.append(stack.pop())
    return postfix


def advanced_split(string):
    string_list = list()
    index = 0
    while index < len(string):
        char = str()
        step = 0
        if string[index] == ' ':
            index += 1
            continue
        if string[index] in ('(', ')'):
            char += string[index]
            step += 1
        if string[index] in ('+', '-', '*', '/', '='):
            while string[index + step] in ('+', '-', '*', '/', '=') and index + step < len(string):
                char += string[index]
                step += 1
                if index + step == len(string):
                    break
            if len(char) > 1:
                char = convert_signs(char)
            if char == 'Invalid expression':
                return char
        if string[index].isdigit():
            while string[index + step].isdigit():
                char += string[index + step]
                step += 1
                if index + step == len(string):
                    break
        if string[index].isalpha():
            while string[index + step].isalpha() and index + step < len(string):
                char += string[index + step]
                step += 1
                if index + step == len(string):
                    break
        string_list.append(char)
        index += step
    return string_list


def convert_signs(signs):
    for sign in signs:
        if sign not in ('+', '-'):
            return 'Invalid expression'
    result = signs[0]
    for j in range(1, len(signs)):
        result = '+' if result == signs[j] else '-'
    return result


def expression_handler(expression):
    if len(expression) % 2 == 0:
        if expression[0] == '-' and len(expression) == 2:
            if expression[1].isdigit():
                return ''.join(expression)
            else:
                return 'Invalid expression'
        else:
            return 'Invalid expression'
    if not expression[0].isalpha() and not expression[0].isdigit():
        return 'Invalid identifier'
    if expression[0].isalpha() and len(expression) == 1:
        if expression[0] in variables.keys():
            return variables[expression[0]]
        else:
            return 'Unknown variable'
    if len(input_list) == 1:
        return int(input_list[0])
    if expression[1] == '=':
        if len(expression) == 3:
            if expression[0].isalpha():
                if expression[2].isdigit():
                    variables[expression[0]] = expression[2]
                    return ''
                elif expression[2] in variables.keys():
                    variables[expression[0]] = variables[expression[2]]
                    return ''
                else:
                    return 'Invalid assignment'
            else:
                return 'Invalid assignment'
        else:
            return 'Invalid assignment'
    for ind, num in enumerate(input_list):
        if ind % 2 == 0:
            if num.isalpha():
                if num in variables.keys():
                    input_list[ind] = variables[num]
                else:
                    return 'Unknown variable'
    postfix = infix_to_postfix(input_list)
    return postfix_to_result(postfix)


variables = dict()
input_ = input()
while input_ != '/exit':
    if input_.startswith('/'):
        if input_ == '/help':
            print('''"Smart Calculator" v1.0
Created by sheff-slava
Available operations: +, -, *, /.
It is possible to work with variables now''')
        else:
            print('Unknown command')
    elif not input_ == '':
        input_list = advanced_split(input_)
        if input_list != 'Invalid expression':
            output = expression_handler(input_list)
            if output != '':
                print(output)
        else:
            print('Invalid expression')
    input_ = input()
print('Bye!')
