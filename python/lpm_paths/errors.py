class InputSpecError(ValueError): ... #invalid input specification
class InvariantError(RuntimeError): ... #invariant violation
class CacheFenceError(PermissionError): ... #cache fence violation
class PathFormatError(ValueError): ... #invalid path format