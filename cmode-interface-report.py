#!/usr/local/python-2.7.2/bin/python
##
# A simple network interface stats report
# Using netapp API and Python
#
# Blake Golliher - blakegolliher@gmail.com
##

import sys, string, os
import getpass, re, time

sys.path.append("/var/local/netapp-manageability-sdk-5.1/lib/python/NetApp")
from NaServer import *

password = getpass.getpass()

filer_name = sys.argv[1]

time = int(time.time())

filer = NaServer(filer_name,1,6)
filer.set_admin_user('admin', password)
cmd = NaElement('perf-object-get-instances')
cmd.child_add_string('objectname', 'ifnet')

instances = NaElement('instances')
counters = NaElement('counters')

instances.child_add_string('instance', 'e0a')
instances.child_add_string('instance', 'e0b')
instances.child_add_string('instance', 'e0c')
instances.child_add_string('instance', 'e0d')
instances.child_add_string('instance', 'e0e')
instances.child_add_string('instance', 'e0f')
instances.child_add_string('instance', 'e13a')
instances.child_add_string('instance', 'e13b')

counters.child_add_string('counter', 'send_packets')
counters.child_add_string('counter', 'send_data')
counters.child_add_string('counter', 'send_errors')
counters.child_add_string('counter', 'recv_packets')
counters.child_add_string('counter', 'recv_data')
counters.child_add_string('counter', 'recv_errors')
counters.child_add_string('counter', 'recv_drop_packets')

cmd.child_add(instances)
cmd.child_add(counters)

out = filer.invoke_elem(cmd)

if(out.results_status() == "failed"):
  print "%s failed." % filer_name
	print(out.results_reason() + "\n")
	sys.exit(2)

instances = dict()
instances = out.child_get('instances')
for instance_data in instances.children_get():
	instance_name = instance_data.child_get_string('name')
	instance_uuid = instance_data.child_get_string('uuid')
	counters = dict()
	counters = instance_data.child_get('counters')
	for counter_data in counters.children_get():
		instNoKern = re.sub(':kernel:','_', instance_uuid)
		instCluster = instance_uuid.split(':')
		counter_name = counter_data.child_get_string('name')
		counter_value = counter_data.child_get_string('value')
		print "O:naco_perfapi_ifnet_%s_%s:%s:%s:%s:counter:60" % (instNoKern, counter_name, time, counter_value, instCluster[0])
