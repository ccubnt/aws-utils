#!/usr/bin/python
############################
#  Class for doing RDS Snapshots
#
#
import boto
import boto.ec2
import boto.rds2
import time
import os, sys

class RDSSnapshot():

	def __init__(self, region):
		self.region = region 
		
		try:
			self.rds_conn = boto.rds2.connect_to_region(region)
		except Exception as e:
			print e
	

	def rds_get_instances(self, dbinstanceid):

		try:
			instances = self.rds_conn.describe_db_instances(db_instance_identifier=dbinstanceid)
			inst = instances['DescribeDBInstancesResponse']['DescribeDBInstancesResult']['DBInstances'][0]
		except Exception as e:
			print e

		return inst['DBInstanceIdentifier']


	def rds_create_snap(self, dbinstanceid):
		try:
			instanceid = self.rds_get_instances(dbinstanceid)
			snapshotid = instanceid + "-" + (time.strftime("%Y-%m-%d-%H%M"))
			snapcreate = self.rds_conn.create_db_snapshot(snapshotid, instanceid)
		except Exception as e:
			print e

		return snapcreate['CreateDBSnapshotResponse']['CreateDBSnapshotResult']['DBSnapshot']


	def rds_get_snap_status(self, dbinstanceid, dbsnapshotid):
		try:
			snapshot = self.rds_conn.describe_db_snapshots(db_instance_identifier=dbinstanceid, db_snapshot_identifier=dbsnapshotid)
			snapstatus = snapshot['DescribeDBSnapshotsResponse']['DescribeDBSnapshotsResult']['DBSnapshots'][0]['Status']
		except Exception as e:
			print e

		return snapstatus

	def rds_timer(self, threshold):
		self.threshold = threshold
		now = time.time()
		timelimit = now + threshold

		return timelimit

identity = boto.utils.get_instance_identity()
region = identity['document']['region']

snap = RDSSnapshot(region)
##########
Fill in variable with your rds instance name
instancename = ''
##########
instance = snap.rds_get_instances(instancename)

print "Instance is %s" % instance
print "Creating Snapshot"

snapobj = snap.rds_create_snap(instance)

status = ''

timelimit = snap.rds_timer(300)

while status != "available":
	if time.time() >= timelimit:
		print "Time limit exceeded..check snapshot status manually"
		break
	else:
		time.sleep(10)
		status = snap.rds_get_snap_status(snapobj['DBInstanceIdentifier'],snapobj['DBSnapshotIdentifier'])
		print "Status is %s" % status

if status != "available":
	print "Snapshot not available, status is %s" % status
	sys.exit(1)
else:
	print "Completed with status %s" % status
	sys.exit(0)
