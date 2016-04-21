rm -f heatmap.tar.gz h.txt h0.txt
tar cfv heatmap.tar pack.bat css examples js lib *.py plus/plus plus/templates plus/webmap plus/*.py plus/*.bat 
gzip heatmap.tar
uuencode heatmap.tar.gz h.tgz >h0.txt
tail -n +2 h0.txt >h.txt
rm -f h0.txt


