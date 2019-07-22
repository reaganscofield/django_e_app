build:
	@sudo docker-compose build
migrations:
	@sudo docker-compose run web e_project/manage.py makemigrations
migrate:
	@sudo docker-compose run web e_project/manage.py migrate
run:
	@sudo docker-compose up
user:
	@sudo docker-compose run web e_project/manage.py createsuperuser
shell:
	@sudo docker-compose run web e_project/manage.py shell
test:
	@sudo docker-compose run web e_project/manage.py test e_app
