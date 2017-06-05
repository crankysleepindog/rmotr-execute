PHONY: status start stop

TAG="\n\n\033[0;32m\#\#\# "
END=" \#\#\# \033[0m\n"
PACKAGE=linked_list

start:
	@echo $(TAG)Starting Service$(END)
	supervisorctl -c setup/supervisor/supervisord.conf start rmotr-execute

stop:
	@echo $(TAG)Stopping Service$(END)
	supervisorctl -c setup/supervisor/supervisord.conf stop rmotr-execute

status:
	@echo $(TAG)status$(END)
	supervisorctl -c setup/supervisor/supervisord.conf status
