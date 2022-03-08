def find_answers(template, correct, token='@'):
    max_length = max(len(template), len(correct))

    ans = []
    i = 0
    while i < max_length:
        if not (i < len(template) and i < len(correct)):
            break
        if template[i] == '@' and template[i+1] == '(':
            length = int(template[i+2:template.find(')', i)])
            ans.append(correct[i:i+length])
            template = template.replace(template[i:template.find(')', i)+1],
                                        correct[i:i+length],
                                        1)
            i = 0
        i += 1
    return ans

# assign = """
# const d = @(10);
# alert(d);
# """

# code = """
# const d = new Date();
# alert(d);
# """

# a = find_answers(assign, code)
# print(a)