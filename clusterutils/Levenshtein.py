# coding=utf-8
#!/usr/bin/env python

#编辑距离
#
def levenshtein(A, B):
        len_A = len(A) + 1
        len_B = len(B) + 1
        if len_A == 1:
            return len_B - 1
        if len_B == 1:
            return len_A - 1
        matrix = [range(len_A) for _ in range(len_B)]
        for i in range(1, len_B):
            matrix[i][0] = i
        for i in range(1, len_B):
            for j in range(1, len_A):
                deletion = matrix[i - 1][j] + 1
                insertion = matrix[i][j - 1] + 1 #
                substitution = matrix[i - 1][j - 1] #直角线 就是两个字符串相等
                if B[i - 1] != A[j - 1]:
                    substitution += 1
                matrix[i][j] = min(deletion, insertion, substitution)
        return matrix[len_B - 1][len_A - 1]

#字符串相似度 -》  计算相异距离 / 两个字符串最长
def str_similarity(str_a, str_b , _point = 2):
    return ('%.' + ('%s'% _point ) + 'f' ) % (1 - float(levenshtein(str_a, str_b))/ max(len(str_a), len(str_b)))


if __name__ == '__main__':
    print str_similarity('asds', 'acbccc' )
