def main():
    f_read = open('test_system/INPUT.txt', 'r')
    f_write = open('test_system/OUTPUT.txt', 'w')
    f = True
    input = lambda: f_read.readline()


    def print(*text, sep=' ', end='\n'):
        nonlocal f
        if f:
            text = sep.join([str(i) for i in text])
            f = False
        else:
            text = end + sep.join([str(i) for i in text])
        f_write.write(text)


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

    f_read.close()
    f_write.close()

main()