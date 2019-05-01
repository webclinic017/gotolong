
import os
import sys

class Project(object):
	def project_root_get(self):
		# print globals()
		# print '__file__ : ', __file__
		project_root = os.path.abspath(os.path.dirname(__file__))
		# print project_root
		return project_root

	def project_src_get(self):
		return os.path.join(self.project_root_get(), 'src') 
	
	def project_data_get(self):
		return os.path.join(self.project_root_get(), 'input-global-data') 

	def project_reports_get(self):
		return os.path.join(self.project_root_get(), 'output-global-reports') 

	def project_profile_data_get(self):
		return os.path.join(self.project_root_get(), 'input-user-data') 

	def project_profile_reports_get(self):
		return os.path.join(self.project_root_get(), 'output-user-reports') 

	def project_db_files_get(self):
		return os.path.join(self.project_root_get(), 'db-files')
 
	def project_db_schema_get(self):
		return os.path.join(self.project_root_get(), 'db-schema') 

if __name__ == "__main__":
	import project
	project = project.Project();

	cmd = sys.argv[1]
	if cmd == "root" : 
		print project.project_root_get()
	elif cmd == "src" : 
		print project.project_src_get()
	elif cmd == "data" : 
		print project.project_data_get()
	elif cmd == "reports" : 
		print project.project_reports_get()
	elif cmd == "profile_data" : 
		print project.project_profile_data_get()
	elif cmd == "profile_reports" : 
		print project.project_profile_reports_get()
	elif cmd == "db_files" : 
		print project.project_db_files_get()
	elif cmd == "db_schema" : 
		print project.project_db_schema_get()
