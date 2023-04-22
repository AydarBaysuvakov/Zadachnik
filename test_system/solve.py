def main():
	read_f = open("test_system/INPUT.txt")
	write_f = open("test_system/OUTPUT.txt", "w")
	a, b = map(int, read_f.readline().split())
	write_f.write(str(a + b))
	read_f.close()
	write_f.close()