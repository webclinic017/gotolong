
import os
import sys

def project_root_get():
	# print globals()
	# print '__file__ : ', __file__
	project_root = os.path.abspath(os.path.dirname(__file__))
	# print project_root
	return project_root

def project_src_get():
	return os.path.join(project_root_get(), 'src') 

def project_data_get():
	return os.path.join(project_root_get(), 'input-global-data') 

def project_reports_get():
	return os.path.join(project_root_get(), 'output-global-reports') 

def project_profile_data_get():
	return os.path.join(project_root_get(), 'input-user-data') 

def project_profile_reports_get():
	return os.path.join(project_root_get(), 'output-user-reports') 

if __name__ == "__main__":
	cmd = sys.argv[1]
	if cmd == "root" : 
		print project_root_get()
	elif cmd == "src" : 
		print project_src_get()
	elif cmd == "data" : 
		print project_data_get()
	elif cmd == "reports" : 
		print project_reports_get()
	elif cmd == "profile_data" : 
		print project_profile_data_get()
	elif cmd == "profile_reports" : 
		print project_profile_reports_get()
