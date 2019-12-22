package name.orhideous.twicher.error

sealed trait TwicherError extends Exception

object TwicherError {

  case object NoSuchQuote extends TwicherError
  case object NoQuotes    extends TwicherError
}
