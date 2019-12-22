package name.orhideous.twicher

sealed trait Error extends Exception

object Error {

  case object NoSuchQuote extends Error

}
