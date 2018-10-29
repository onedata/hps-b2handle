
class MetadataConversionError(Exception):
  """
  Generic metadata conversion error
  """
  def __init__(self, message):
      # Call the base class constructor with the parameters it needs
      super(Exception, self).__init__(message)

