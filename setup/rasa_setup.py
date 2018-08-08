import sys, subprocess, configparser


#setsup docker with rasa nlu and trains it 
def setup(img, container, training_data, cfg, path, local_path, duser, dpwd):

	p = subprocess.Popen('docker images', stdout=subprocess.PIPE, shell=True) 

	cmds = ["docker login --username " + duser, dpwd, "service docker start", "docker build -t "+ img + " " + local_path, "docker run -d -p 5000:5000 --name " + container + " " + img, "docker exec -it " +  container + " pip install --upgrade html5lib==0.9999999",
		"docker exec -it " + container + "  pip install -r /app/alt_requirements/requirements_full.txt", "docker exec -it " + container + " python -m spacy download en_core_web_md",
		"docker exec -it " + container + " python -m rasa_nlu.train --c " + cfg + " --data " + training_data + " --path " + path, "docker restart " + container]
	

	if img in p.communicate()[0].decode("utf-8"):
		cmds.remove("docker build -t "+ img + " " + local_path)
		

	helper_execute(cmds)
	

# terminates and cleans up container from local machine
def teardown(container, img):

    helper_execute(["docker stop " + container ,"docker rm " + container, "service docker stop"])


    
	


#iteratively executes list of commands with seperate chid processes
#prints cmds & stdout & stderr
def helper_execute(cmds):

    for c in cmds:

        print (c)
        p = subprocess.Popen(c, stdout=subprocess.PIPE, shell=True)
        out = p.communicate()
        print (out[0])
        if out[1]!= None:
            print("With Errors: " + out[1])




def main():
	
    if sys.platform.startswith('linux') == False:
        sys.exit("only use with bash")
	
    if (len(sys.argv)<3):
        sys.exit("Usage: python contained_RASA_Setup.py <container_name> {setup|teardown}")

    args = [sys.argv[1], sys.argv[2]]

    config = configparser.ConfigParser()
	
    config.read('config.ini')
    cfg = config.get('PROJECT1', 'config')
    path = config.get('PROJECT1', 'path')
    local_path = config.get('LOCAL_MACHINE','local_path')
    training_data = config.get('PROJECT1', 'training_data')
    img = config.get('PROJECT1','img')
    duser = config.get('PROJECT1','duser')
    dpwd = config.get('PROJECT1','dpwd')

	



    if args[1] == "setup":
        setup(img, args[0], training_data, cfg, path, local_path, duser, dpwd)
    elif args[1] == "teardown":
        #edited maybe false
        teardown(args[0], img) 
    else: 
        sys.exit("No such Function. Usage: python contained_RASA_Setup.py <image_name> <container_name> {setup|teardown}")

	
	
	



	









if __name__ == "__main__":
    main()
