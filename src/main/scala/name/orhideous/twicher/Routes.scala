package name.orhideous.twicher

import cats.effect.Sync
import cats.implicits._
import io.circe.generic.auto._
import name.orhideous.twicher.persistence.QuotesAlgebra
import org.http4s._
import org.http4s.circe.CirceEntityEncoder._
import org.http4s.dsl.Http4sDsl

class Routes[F[_]: Sync](algebra: QuotesAlgebra[F]) extends Http4sDsl[F] {

  val routes: HttpRoutes[F] = HttpRoutes.of[F] {
    case GET -> Root =>
      algebra.list.flatMap(Ok(_))

    case GET -> Root / "random" =>
      algebra.random.flatMap(Ok(_))

    case GET -> Root / IntVar(id) =>
      algebra.read(id).flatMap(Ok(_))
  }
}

object Routes {
  def apply[F[_]: Sync](algebra: QuotesAlgebra[F]): HttpRoutes[F] = new Routes(algebra).routes
}
