from sklearn import tree
import time
import shelve

correct_for_REST = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
correct_for_SOAP = [15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
correct_for_XMLRPC = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40]

sample = raw_input('Enter the sample file: ')
expdata = raw_input('Enter the experience data: ')

digt_sample = shelve.open(sample)
digt_expdata = shelve.open(expdata)

sample_data = digt_sample['res']['sample']
sample_label = digt_sample['res']['label']

SOAP = 0
REST = 0
XMLRPC = 0
ERROR = 0

SOAPlines = []
RESTlines = []
XMLRPClines = []

start = time.clock()

clf = tree.DecisionTreeClassifier(criterion='entropy')
clf.fit(sample_data, sample_label)

for i in digt_expdata['res']:
    if clf.predict(digt_expdata['res'][i])[0] == 'SOAPAPI':
        SOAP += 1
        SOAPlines.append(i)
    if clf.predict(digt_expdata['res'][i])[0] == 'XMLRPC':
        XMLRPC += 1
        XMLRPClines.append(i)
    if clf.predict(digt_expdata['res'][i])[0] == 'RESTAPI':
        REST += 1
        RESTlines.append(i)

end = time.clock()

alltrueinfo = {
    'SOAP': len(correct_for_SOAP),
    'REST': len(correct_for_REST),
    'XMLRPC': len(correct_for_XMLRPC)}
pretureinfo = {'SOAP': 0, 'REST': 0, 'XMLRPC': 0}
alltesttureinfo = {'SOAP': 0, 'REST': 0, 'XMLRPC': 0}

pretureinfo['SOAP'] += len(SOAPlines)
pretureinfo['REST'] += len(RESTlines)
pretureinfo['XMLRPC'] += len(XMLRPClines)


tmp1 = []
for i in SOAPlines:
    if i in correct_for_SOAP:
        alltesttureinfo['SOAP'] += 1
    if i not in correct_for_SOAP:
        tmp1.append(i)
ERROR += len(tmp1)

tmp1 = []
for i in RESTlines:
    if i in correct_for_REST:
        alltesttureinfo['REST'] += 1
    if i not in correct_for_REST:
        tmp1.append(i)
ERROR += len(tmp1)

tmp1 = []
for i in XMLRPClines:
    if i in correct_for_XMLRPC:
        alltesttureinfo['XMLRPC'] += 1
    if i not in correct_for_XMLRPC:
        tmp1.append(i)
ERROR += len(tmp1)


print("SOAP flows: ", SOAP, "Lines: ", SOAPlines,
      "Recall: ", (float(alltesttureinfo['SOAP']) / float(alltrueinfo['SOAP'])),
      "Precision: ", (float(alltesttureinfo['SOAP']) / float(pretureinfo['SOAP'])))
print("REST flows: ", REST, "Lines: ", RESTlines,
      "Recall: ", (float(alltesttureinfo['REST']) / float(alltrueinfo['REST'])),
      "Precision: ", (float(alltesttureinfo['REST']) / float(pretureinfo['REST'])))
print("XMLRPC flows: ",
      XMLRPC,
      "Lines: ",
      XMLRPClines,
      "Recall: ",
      (float(alltesttureinfo['REST']) / float(alltrueinfo['REST'])),
      "Precision: ",
      (float(alltesttureinfo['XMLRPC']) / float(pretureinfo['XMLRPC'])))
print("Cannot identify: ", ERROR)
print("Cost: %f seconds") % (end - start)
