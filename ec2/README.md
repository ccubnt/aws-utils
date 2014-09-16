ec2
===

Examples pulling data from ec2 via boto and with metadata

metadata.py - usage

d = Metadata()
primary = d.get_ms('pip')
secondary = d.get_ms('sip')
region = d.get_ms('region')
az = d.get_ms('az')
env = d.get_ms('env')
