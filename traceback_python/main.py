def log_uncaught_exceptions(ex_cls, ex, tb):
	text = '{}: {}:\n'.format(ex_cls.__name__, ex)
	import traceback
	text += ''.join(traceback.format_tb(tb))
	with open("log.txt", "a+", encoding="utf-8") as file:
		file.write(text)
	print(text)
	sys.exit(1)

import sys
sys.excepthook = log_uncaught_exceptions
