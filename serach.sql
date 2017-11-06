insert into customers values (?,?,?,?);

SELECT *c.cid FROM customers c WHERE c.cid='c10'; AND c.pwd='c10';

select s.sid, s.name, c.qty, c.uprice
  from carries c, stores s
  where c.sid=s.sid and c.pid='p10'
  group by s.sid;

select olines.sid, sum(qty)
  from orders
  left join olines
  on orders.oid = olines.oid
  where date(odate, '+7 day') >= date('now')
  and olines.pid='p10' 
  group by olines.sid;

SELECT * FROM carries where pid = 'p10' and sid =20;
 
select p.pid, p.name,p.unit,count(p.pid),count(c.sid)
from products p ,carries c
WHERE p.name LIKE '%co%'
and p.pid = c.pid
group by p.pid
order by count(p.pid) DESC
;
select olines.pid, sum(qty)
  from orders
  left join olines
  on orders.oid = olines.oid
  where date(odate, '+7 day') >= dateow')('n
  group by olines.pid;

a_dict = {"p10", [, , , , ]}

create view storeInStock as
  select c.pid, count(s.sid)
  from carries c, stores s
  where c.sid=s.sid and qty>0
  group by c.pid

create view minPricesInStock as
    select distinct c.pid, c.uprice
    from carries c
    where c.qty>0 and c.uprice <= (
      select min(uprice)  
      from carries c2
      where c.pid=c2.pid
      and c2.qty>0);

create view minPricesInTheory as
  select distinct c.pid, uprice
  from carries c, stores s
  where c.sid=s.sid and uprice <= (
    select min(uprice)
    from carries c2
    where c.pid=c2.pid)
    order by c.pid;

insert into olines values (80,20,"p10",1,4.7);
select * from olines where pid ="p10" ;