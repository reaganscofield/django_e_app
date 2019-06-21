d_build:
	@sudo docker-compose build
d_mkmg:
	@sudo docker-compose run web e_project/manage.py makemigrations
d_mig:
	@sudo docker-compose run web e_project/manage.py migrate
d_run:
	@sudo docker-compose up
