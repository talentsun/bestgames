drop table if exists bestgames.competitor;
create table bestgames.competitor
(
uid bigint default 0,
followers_count int default 0,
friends_count int default 0,
statuses_count int default 0
);
