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


    a = input()
    print(a)

    f_read.close()
    f_write.close()

main()