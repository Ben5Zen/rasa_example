import sys, subprocess, ConfigParser



def setup(img, container, training_data, cfg, path, local_path):

	p = subprocess.Popen('docker images', stdout=subprocess.PIPE, shell=True) 

	if img in p.communicate()[0]:
		cmds.remove("docker build -t "+ img + " " + local_path)
		

	return ["docker build -t "+ img + " " + local_path, "docker run -d -p 5000:5000 --name " + container + " " + img, "docker exec -it " +  container + " pip install --upgrade html5lib==0.9999999",
		"docker exec -it " + container + "  pip install -r /app/alt_requirements/requirements_full.txt", "docker exec -it " + container + " python -m spacy download en_core_web_md",
		"docker exec -it " + container + " python -m rasa_nlu.train --c " + cfg + " --data " + training_data + " --path " + path, "docker restart " + container]
	
	


def teardown(container):

	return ["docker stop " + container ,"docker rm " + container]









def main():
	
	if sys.platform.startswith('linux') == False:
		sys.exit("only use with bash")
	
	args = [sys.argv[1], sys.argv[2]]

	config = ConfigParser.ConfigParser()
	
	config.read('config.ini')
	cfg = config.get('PROJECT1', 'config')
	path = config.get('PROJECT1', 'path')
	local_path = config.get('LOCAL_MACHINE','local_path')
	training_data = config.get('PROJECT1', 'training_data')
	img = config.get('PROJECT1','img')

	
	if (len(args)<2):
		sys.exit("Usage: python contained_RASA_Setup.py <image_name> <container_name> {setup|teardown}")


	if args[1] == "setup":
		cmds = setup(img, args[0], training_data, cfg, path, local_path)
        elif args[1] == "teardown":
        	cmds = teardown(args[0]) 
	else: 
		sys.exit("No such Function. Usage: python contained_RASA_Setup.py <image_name> <container_name> {setup|teardown}")


        for c in cmds:

		print (c)
		p = subprocess.Popen(c, stdout=subprocess.PIPE, shell=True)
		print (p.communicate()[0])

	









if __name__ == "__main__":
    main()
