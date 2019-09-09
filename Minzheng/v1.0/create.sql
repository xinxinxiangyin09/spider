-- 存放虚假链接,用来判断该数据是否之前抓过
create table version(
    link varchar(200)
)charset="utf8mb4";

create table addr_info(
    number int(10),
    name varchar(20)
)charset="utf8mb4";