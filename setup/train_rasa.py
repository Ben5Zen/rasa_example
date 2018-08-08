import sys, ConfigParser

from rasa_setup import helper_execute

def train(liveContainer, training_data, cfg, path):

	helper_execute(["docker exec -it " + liveContainer + " python -m rasa_nlu.train --c " + cfg + " --data " + training_data + " --path " + path, "docker restart " + liveContainer])

def main():

	if sys.platform.startswith('linux') == False:
		sys.exit("only use with bash")
	
	
        
	if (len(sys.argv)<3):
		sys.exit("Usage: python contained_RASA_Setup.py <container_name> <training_file_path>")
       
        args = [sys.argv[1], sys.argv[2]]
	
        config = ConfigParser.ConfigParser()
	
	config.read('config.ini')
	cfg = config.get('PROJECT1', 'config')
	path = config.get('PROJECT1', 'path')


	train(args[0], args[1], cfg, path)


if __name__ == "__main__":
        main()
