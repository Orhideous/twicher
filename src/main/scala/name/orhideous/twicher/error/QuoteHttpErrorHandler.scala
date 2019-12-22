package name.orhideous.twicher.error

import cats.ApplicativeError
import org.http4s.HttpRoutes
import org.http4s.dsl.Http4sDsl

class QuoteHttpErrorHandler[F[_]](implicit M: ApplicativeError[F, TwicherError])
    extends HttpErrorHandler[F, TwicherError]
    with RoutesHttpErrorWrapper[F, TwicherError]
    with Http4sDsl[F] {

  private val handler: Handler = {
    case TwicherError.NoQuotes    => InternalServerError()
    case TwicherError.NoSuchQuote => NotFound()
  }

  override def handle(routes: HttpRoutes[F]): HttpRoutes[F] =
    wrapWith(handler)(routes)

}
