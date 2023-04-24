try:
    f, s = input().split('-')
    f1 = 'ABCDEFGH'.index(f[0])
    s1 = 'ABCDEFGH'.index(s[0])
    f2 = int(f[1])
    s2 = int(s[1])
    if abs(s1 - f1) == 2 and abs(s2 - f2) == 1:
        print('YES')
    elif abs(s1 - f1) == 1 and abs(s2 - f2) == 2:
        print('YES')
    else:
        print('NO')
except:
    print('ERROR')