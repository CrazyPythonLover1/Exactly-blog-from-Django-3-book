1. sudo -i -u postgres /or su postgres
2. psql 
YOU can directly go $$$ sudo -u postgres psql
You can check your current info $$$ conninfo

3. sudo -u postgres createuser --interactive

4. sudo -u postgres createdb database_name

to enter into the database 
5.sudo -u username psql

6. sudo service postgresql start / restart / start 

7. into database to see all db list $$$ \l

8. List of role attributes $$$ \du

9. create role with: NOT ADD TO SUPERUSER
$$$ CREATE USER USER_name WITH PASSWORD 'TEST123';

10. ALTER ROLE 
$$$ ALTER USER USER_NAME WITH PASSWORD 'TEST123';
$$$ ALTER USER USER_NAME WITH SUPERUSER;

11. REMOVE USER FROM DATABASE 
$$$. DROP USER USER_NAME




   

