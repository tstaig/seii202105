build:
	docker-compose build acs
run:
	docker-compose run acs bash
exec:
	CMD=$$(docker container ls --format '{{.Names}}' |grep acs-ws |head |xargs -I{} echo docker exec -it {} bash); $$CMD
