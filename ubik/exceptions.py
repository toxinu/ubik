# coding: utf-8

# Database
class DatabaseException(RuntimeError):
	""" Database Error """

class DatabaseError(DatabaseException):
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)

# Command
class CmdException(RuntimeError):
	""" Cmd Error """

class CmdError(CmdException):
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)

# Installer
class InstallerException(RuntimeError):
	""" Installer Error """

class InstallerError(InstallerException):
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)

# Reinstaller
class ReinstallerException(RuntimeError):
	""" Reinstaller Error """

class ReinstallerError(ReinstallerException):
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)

# Remover
class RemoverException(RuntimeError):
	""" Remover Error """

class RemoverError(RemoverException):
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)

# Upgrader
class UpgraderException(RuntimeError):
	""" Upgrader Error """

class UpgraderError(UpgraderException):
	def __init__(self, value):
		self.parameter = value
	def __str__(self):
		return repr(self.parameter)
		
