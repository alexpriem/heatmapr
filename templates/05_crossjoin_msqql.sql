IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'xy') AND type in (N'U'))
DROP TABLE xy

select a.*, b.*
   into xy
from xas a
cross join yas b
