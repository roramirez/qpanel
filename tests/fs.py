from libs.qpanel import freeswitch

fs = freeswitch.Freeswitch()
print(fs.getQueues())
print(fs.getAgents('support@default'))
print(fs.getCalls('support@default'))
print(fs.queueStatus())
