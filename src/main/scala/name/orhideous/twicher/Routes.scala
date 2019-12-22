package name.orhideous.twicher

import cats.effect.Sync
import cats.implicits._
import io.circe.generic.auto._
import org.http4s._
import org.http4s.circe.CirceEntityEncoder._
import org.http4s.dsl.Http4sDsl

import name.orhideous.twicher.error.HttpErrorHandler
import name.orhideous.twicher.persistence.QuotesAlgebra

class Routes[F[_]: Sync, E <: Throwable](algebra: QuotesAlgebra[F])(implicit H: HttpErrorHandler[F, E])
    extends Http4sDsl[F] {

  private val rawRoutes: HttpRoutes[F] = HttpRoutes.of[F] {
    case GET -> Root =>
      algebra.list.flatMap(Ok(_))

    case GET -> Root / "random" =>
      algebra.random.flatMap(Ok(_))

    case GET -> Root / IntVar(id) =>
      algebra.read(id).flatMap(Ok(_))
  }
  val routes: HttpRoutes[F] = H.handle(rawRoutes)
}
