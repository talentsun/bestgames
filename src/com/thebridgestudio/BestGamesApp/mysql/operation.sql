drop table if exists bestgames.operation;
create table bestgames.operation
(
uid bigint,
op_type int,
op_date datetime,
op_state int
);
