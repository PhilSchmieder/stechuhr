# Setup Db

Create table:
```genericsql
create table time (
    id integer primary key autoincrement,
    begin datetime,
    end datetime
);
```

Insert data:
```genericsql
insert into time (begin, end) values ('2007-01-01 10:00:00', '2008-01-01 10:00:00');
```