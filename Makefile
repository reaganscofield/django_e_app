build:
	@sudo docker-compose build
migrations:
	@sudo docker-compose run web e_project/manage.py makemigrations
migrate:
	@sudo docker-compose run web e_project/manage.py migrate
run:
	@sudo docker-compose up
