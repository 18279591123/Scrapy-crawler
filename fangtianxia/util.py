def levenshtein(first, second):
    ''' 编辑距离算法（LevD）
        Args: 两个字符串
        returns: 两个字符串的编辑距离 int
    '''
    if len(first) > len(second):
        first, second = second, first
    if len(first) == 0:
        return len(second)
    if len(second) == 0:
        return len(first)
    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [list(range(second_length)) for x in range(first_length)]
    # print distance_matrix
    for i in range(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i - 1][j] + 1
            insertion = distance_matrix[i][j - 1] + 1
            substitution = distance_matrix[i - 1][j - 1]
            if first[i - 1] != second[j - 1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)
            # print distance_matrix
    return distance_matrix[first_length - 1][second_length - 1]

def PriorityUrl(first,second):
    edit_distance = levenshtein(first, second)
    if len(first) < len(second):
        first, second = second, first
    return round((1-edit_distance/len(first))*100)
str1 = "hello,good moring"
str2 = "hello,od oring"
edit_distance = PriorityUrl(str1, str2)
print(edit_distance)