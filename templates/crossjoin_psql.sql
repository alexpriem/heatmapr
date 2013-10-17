DROP TABLE if exists xy;

select a.*, b.*
   into xy
from xas a
cross join yas b;
