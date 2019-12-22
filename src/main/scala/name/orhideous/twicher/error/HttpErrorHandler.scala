package name.orhideous.twicher.error

import org.http4s.HttpRoutes

trait HttpErrorHandler[F[_], E <: Throwable] {
  def handle(routes: HttpRoutes[F]): HttpRoutes[F]
}
