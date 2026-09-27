# QindaLLM: install layout used by sci-ml/qinda-llm-server.
PREFIX  ?= /usr
SYSCONF ?= /etc
UNITDIR ?= $(PREFIX)/lib/systemd/system
DESTDIR ?=

.PHONY: all install test

all:

install:
	install -Dm755 monitor/qinda-llm-top $(DESTDIR)$(PREFIX)/bin/qinda-llm-top
	install -Dm644 systemd/qinda-llm.service $(DESTDIR)$(UNITDIR)/qinda-llm.service
	install -Dm644 systemd/qinda-llm-monitor.service $(DESTDIR)$(UNITDIR)/qinda-llm-monitor.service
	install -Dm644 systemd/qinda-llm-server.target $(DESTDIR)$(UNITDIR)/qinda-llm-server.target
	install -Dm644 config/models.ini $(DESTDIR)$(SYSCONF)/qinda-llm/models.ini
	install -Dm644 config/server.env $(DESTDIR)$(SYSCONF)/qinda-llm/server.env
	install -Dm644 boot/50-llm-server.conf $(DESTDIR)$(PREFIX)/share/qinda-boot/modes.d/50-llm-server.conf

test:
	python3 -m unittest discover -s tests -p 'test_*.py'
