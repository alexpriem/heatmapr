python contour.py  -dbt psql -s localhost -db heatmap -t knmi_1995c  -u postgres -p alex -o knmi -x dag1994,0,365,250 -y tg,-200,300,250 -title "tijdreeks" -js 
rem python contour.py  -dbt psql -s localhost -db heatmap -t knmi_1995c  -u postgres -p alex -o knmi -x dag1994,0,365,500 -y tg,-200,300,500 -title "tijdreeks" -js 
rem 
rem buggy
rem python contour.py  -dbt psql -s localhost -db heatmap -t knmi_1995c  -u postgres -p alex -o knmi -x dag1994,0,365,365 -y tg,-200,300,200 -title "tijdreeks" -js 
