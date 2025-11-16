def add_stat(d, item_name, count, seconds):
	d[item_name] = {"count": count,
					"seconds": seconds,
					"width": max(len(item_name), 20)
					}

def rept(s, n):
	result = ""
	for i in range(n):
		result += s
	return result
	
def right_just(s, n):
	s = str(s)
	return rept(" ", n - len(s)) + s

def thousands(n):
	if n == 0:
		return "0"
	result = ""
	sep = ""
	while n != 0:
		next = str(n % 1000)
		n = n // 1000
		if n != 0:
			next = rept("0", 3-len(next)) + next
		result = next + sep + result
		sep = ","
	return result
	
def print_stats_heading(d):
	heading = ""
	divider = ""
	sep = ""
	for name in d:
		stat = d[name]
		heading += sep + right_just(name, stat["width"])
		divider += sep + rept("-", d[name]["width"])
		sep = " "
	quick_print(divider)
	quick_print(heading)
	quick_print(divider)
	
def print_stats(d):
	line = ""
	sep = ""
	for name in d:
		stat = d[name]
		disp = thousands(stat["count"]//1) + " (" + thousands(stat["count"]//stat["seconds"]) + "/s)"
		line += sep + right_just(disp, stat["width"])
		sep = " "
	quick_print(line)
	
if __name__ == "__main__":
	d = {}
	add_stat(d, "foo", 2011.5, 10)
	add_stat(d, "bar", 5678, 2)
	print_stats_heading(d)
	print_stats(d)

