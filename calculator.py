variables = {}
elements = []
operators = ('(', ')', '*', '/', '+', '-')
precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

while True:
    inp = input()

    # no input
    if not inp:
        continue

    # accept commands
    if inp.startswith('/'):
        if inp == '/exit':
            print('Bye!')
            break
        if inp == '/help':
            print('The program calculates expression from input string')
        else:
            print('Unknown command')
        continue

    # first number is negative
    if inp.startswith('-'):
        inp = '0' + inp

    # process variables assignment
    if "=" in inp:
        var, val = inp[:inp.find("=")].strip(), inp[inp.find("=") + 1:].strip()
        if not var.isalpha():
            print("Invalid identifier")
            continue
        if val.isalpha():
            if val in variables.keys():
                variables[var] = variables[val]
            else:
                print("Unknown variable")
            continue
        else:
            try:
                variables[var] = eval(val)
            except Exception:
                print("Invalid assignment")
            continue

    # split input string into elements
    stack = []
    for i, c in enumerate(inp):
        if c in operators:
            if stack:
                element = ''.join(stack).strip()
                if element:
                    elements.append(element)
                stack = []
            elements.append(c)
        else:
            stack.append(c)
    if stack:
        element = ''.join(stack).strip()
        if element:
            elements.append(element)

    # resolve multiple + and - into one operator
    signs = {'+': 1, '-': -1}
    for i, element in enumerate(elements):
        if element in signs.keys():
            n = signs[element]
            while True:
                try:
                    n *= signs[elements[i + 1]]
                    elements.pop(i + 1)
                except KeyError:
                    elements[i] = '-' if n == -1 else '+'
                    break

    # convert from infix to postfix
    result = []
    stack = []
    try:
        for element in elements:
            if element not in operators:
                result.append(element)
            else:
                if not stack or stack[-1] == '(':
                    stack.append(element)
                elif element in precedence.keys():
                    if precedence[element] > precedence[stack[-1]]:
                        stack.append(element)
                    else:
                        while stack and (stack[-1] != '(' or precedence[element] >= precedence[stack[-1]]):
                            result.append(stack.pop())
                        stack.append(element)
                if element == '(':
                    stack.append(element)
                if element == ')':
                    while stack[-1] != '(':
                        result.append(stack.pop())
                    stack.pop()
    except IndexError:
        print('Invalid expression')
        continue
    elements = []
    result += reversed(stack)

    # calculate postfix expression
    stack = []
    for element in result:
        if element.isdecimal():
            stack.append(int(element))
        elif element in operators:
            try:
                x, y = stack.pop(), stack.pop()
                stack.append(eval(str(y) + element + str(x)))
            except ZeroDivisionError:
                print('Division by zero')
                break
            except Exception:
                pass
        else:
            try:
                stack.append(variables[element])
            except KeyError:
                print('Unknown variable')
                break
    print(int(stack[-1]) if stack else 'Invalid expression')


