drop table if exists TheiaUsers, TheiaDockerContainers;

create table TheiaUsers(
    id serial primary key,
    username varchar(70) not null UNIQUE,
    password varchar(50)
);

create table TheiaDockerContainers(
    id varchar(70) primary key UNIQUE,
    user_id integer,
    foreign key (user_id) references TheiaUsers(id)
);

insert into TheiaUsers(username, password)
values ('vbondarchuk', 'password'),
       ('igornev', 'pwd'),
       ('someone', 'something');


insert into TheiaDockerContainers(id,  user_id)
values ('5cd8f4e3f03cae0a03f51685a3bd93dea6555f3e856680bb62f7b70f771e4e50', 1),
       ('gadkjasgjht34jtjkd8tqahgj310ut234hgwj6256gdgsdg441454gdsgsfdj236', 1),
       ('fgrgewsdfh33rtsfdg0gh-sm346oggdfsgwe0twet14twj344646hfdsqtt34gfd', 1),
       ('9hsh78fhaj246sgjdfgg0gh78246nwanbahhfhaqeqrt8f89saidgdgdfzbnbdgg', 2),
       ('456789jhfdgkfcae0a03f51685gd93dea65fgsfgjfdkf0bb62f7b70f771e4e50', 2),
       ('qwertyuiopasdfghjklzxcvbnmet1234567890zxcvbnm4567dfghjdftyuieree', 3);



--Добавить нового клиента--
drop function if exists add_client(u_name varchar(70));

create or replace function add_client(u_name varchar(70)) returns varchar as
$$
begin
    insert into TheiaUsers(username)
    values (u_name);
    return 'Клиент зарегестрирован';
exception
    when others then return 'ERROR';
end$$
language plpgsql;



--Добавить новый контейнер--
drop function if exists add_conteiner(u_name varchar(70), cont_id varchar(70));

create or replace function add_conteiner(u_name varchar(70), cont_id varchar(70)) returns varchar as
$$
declare
    cl_id int;
begin
    select id from TheiaUsers where username = u_name into cl_id;
    insert into TheiaDockerContainers(id,  user_id)
    values (cont_id, cl_id);
    return 'Контейнер создан';
exception
    when others then return 'ERROR';
end$$
language plpgsql;


--удалить контейнер--
drop function if exists delete_conteiner(cont_id varchar(70));

create or replace function delete_conteiner(cont_id varchar(70)) returns varchar as
$$
begin
    delete from theiadockercontainers where id = cont_id;
    return 'Контейнер удален';
exception
    when others then return 'ERROR22';
end$$
language plpgsql;


