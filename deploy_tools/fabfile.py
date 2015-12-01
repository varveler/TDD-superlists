from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/varveler/TDD-superlists'

def deploy():
	site_folder = 'home/%s/sites/%s' % (env.user, env.host)
	source_folder = site_folder + '/source'
	_create_directory_structure_if_necessary(site_folder)
	_get_latest_source(source_folder)
	_update_settings(source_folder, env.host)
	_upadte_virtualenv(source_folder)
	_update_static_files(source_folder)
	_update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder): 
	for subfolder in ('database', 'static', 'virtualenv', 'source'):
		run('mkdir -p %s/%s' %(site_folder, subfolder))
		# run is te most basic command for fabric "runs command on server"
		# mkdir -p cancrates directories in deep and won't complain if 
		#already exists

def _get_latest_source(source_folder):
	if exists(source_folder + '/.git'): #1
		run('cd %s && git fetch' % (source_folder)) #2
	else:
		run('git clone %s %s' % (REPO_URL, source_folder)) #3
	current_commit = local('git log -n 1 --format=%H', capture=True) #4
	run('cd %s && git reset --hard %s' % (source_folder, current_commit))#5

	#1 exists checks if a folder exists, we look if the gir repo is already has been clone
	
	#2 many commands start with cd since fabric can't remember in which folder run 
	#the previous command therefore we make cd to source folder and fetch the latest commits

	#3 if does not exist we clone the repo to source folder

	#4 local  runs command on local machine, runs git log to grab the hash number from the 
	#latest commit

	#5 git reset hard blow away any changes made in the code at the server directory

def _update_settings(source_folder, site_name):
	settings_path = source_folder + '/superlists/settings.py'
	sed(settings_path, "DEBUG = True", "DEBUG = False") #1
	sed(settings_path, 'ALLOWED_HOST =.+$',
						'ALLOWED_HOST = ["%s"]' % (site_name,) #2
		)
	secret_key_file = source_folder + '/superlists/secret_key.py'
	if not exists(secret_key_file):  #3
		chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
		key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
		append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
	append(settings_path, '\nfrom .secret_key import SECRET_KEY') #4 #5

	#1 fabric sed does a string substitution in a file in this case Debug from True to False

	#2 Here we changed allowed host using regex to match the line

	#3 This will generate a new secret key and import into settings

	#4 Using relative import from .secret.. to make sure we are importing from local module
	#instead of somewhere in the sys.path

def _update_virtual_env(source_folder):
	virtualenv_folder = source_folder + '/../virtualenv'
	if not exists(virtualenv_folder + '/bin/pip'): #1
		run('virtualenv --python=python3 %s/requirements.txt' % (virtualenv_folder,))
	run ('%s/bin/pip/ install -r %s/requirements.txt' % ( #2
			virtualenv_folder, source_folder))
	#1 This searchs inside virtual env folder a pip executable to check if exists

	#2 use pip install -r requirements as manually 

def _update_static_files(source_folder):
	run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (
		source_folder,))
	#we use virtualenv binaries to make sure we run the virtualenv django version
	# and not the system one

def _update_migrate(source_folder):
	run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
		source_folder,))
	# updates the database with migrate

