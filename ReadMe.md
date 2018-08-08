#Readme Setting up Docker containers &training rasa_nlu
EXECUTE with python3 or pip3 only!!!
incompatibility with 2
#one time initilialzation
- curl "github url of rasa_nlu"
- cp /home/rasa_nlu/docker/Dockerfile_full /home/rasa_nlu/docker/Dockerfile		
- pip install -r rasa_nlu/requirements.txt --user				- else creating rasa_nlu image wont work
- pip install --upgrade html5lib==0.9999999 --user                   - else next install wont work
- pip install -r rasa_nlu/alt_requirements/requirements_full.txt --user	
- sudo service docker stop	                                    -needed after installation




#operations
- config.ini : Specify img_name, path, training_data, local_path 
		-> to add training_data in JSON format: add to rasa_nlu folder (used for img creation), change config training_data & possibly add new imgname
- cmdline:
	- open root session
                - sudo -i			      -> to run with root access
       	        - $python contained_RASA_Setup.py container_name {setup|teardown}
		-> setup will setup rasa nlu in container
		-> teardown will stop and remove container 
        OR
	- call script with --user 
                - $python contained_RASA_Setup.py container_name {setup|teardown} --user

