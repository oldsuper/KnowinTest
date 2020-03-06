# command
## service-nlu api test
cd ${RootDir}
nosetests insight-brain/nlu/nlu/TestMain.py  -s --with-xunit --xunit-file=reports/report.xml -v