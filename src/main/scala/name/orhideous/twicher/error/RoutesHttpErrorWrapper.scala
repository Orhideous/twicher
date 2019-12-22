package name.orhideous.twicher.error

import cats.data.Kleisli
import cats.data.OptionT
import cats.ApplicativeError
import org.http4s.HttpRoutes
import org.http4s.Request
import org.http4s.Response
import cats.implicits._

trait RoutesHttpErrorWrapper[F[_], E <: Throwable] {
  protected type Handler = E => F[Response[F]]

  protected def wrapWith(handler: Handler)(routes: HttpRoutes[F])(implicit ev: ApplicativeError[F, E]): HttpRoutes[F] =
    Kleisli { req: Request[F] =>
      OptionT {
        routes
          .run(req)
          .value
          .handleErrorWith(handler(_).map(Option(_)))
      }
    }
}
