 IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'xas') AND type in (N'U'))
        DROP TABLE xas

        select distinct {{xcol}}=number * {{xfactor}}
              into xas
              from numbers
            where number>({{xmin}} / {{xfactor}}) and number<=({{xmax}} / {{xfactor}})