from application import scheduler
scheduler.start()
print 'scheduler started'

# @scheduler.scheduled_job('interval', 
# 	seconds=3, 
# 	replace_existing=True)
# def timed_job():
# 	print "decorator job working."

def scheduler_job():
	print "scheduler job working"

