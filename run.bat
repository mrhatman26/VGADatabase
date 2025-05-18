docker run --name VGDB -p1234:3306 -e MYSQL_ROOT_PASSWORD=dinnerisready -d mysql
docker cp vgdatabase.sql VGDB:vgdatabase.sql
docker exec -it VGDB mysql -p