from django.db import connection
from django.conf import settings
import inspect


class DbQueries:

	@staticmethod
	def show(l_dbg_sql=None, levels=3, view=None):
		"""
		Show queries by function
		:param view: if calling in view method
		:param l_dbg_sql: debug local module
		:param levels: functions stack deep
		:return:
		"""
		frame = inspect.stack()

		if l_dbg_sql is None:
			pass
		elif l_dbg_sql and settings.DEBUG_SQL and settings.DEBUG_SQL:
			# if view is not None:
			# 	print("\n==={0}===".format(view.basename), sep="")
			qdic = {}
			print("\n==={0}===".format(frame[levels][3]))
			levels -= 1
			while levels != 1:
				print("==={0}===".format(frame[levels][3]))
				levels -= 1
			print("==={0}({1})===".format(frame[1][3], len(connection.queries)))
			for q in connection.queries:
				qsql = q['sql']
				if qsql in qdic:
					qdic[qsql] += 1
					print("({1}){0}\n======".format(qsql, qdic[qsql]))
				else:
					qdic[qsql] = 1
					print("{0}\n======".format(qsql))
