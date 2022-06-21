import psutil
def cpu():
	cpu_per = int (psutil.cpu_percent (False)) 
	return cpu_per

def mem():
	mem_used = int(psutil.virtual_memory()[3] / 1024 / 1024)
	return mem_used

def disk():
	c_per = int (psutil.disk_usage ('C:') [3]) 
	return c_per