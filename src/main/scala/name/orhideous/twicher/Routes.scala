package name.orhideous.twicher

import cats.effect.IO
import io.circe.generic.auto._
import name.orhideous.twicher.persistence.QuotesRepository
import org.http4s.HttpRoutes
import org.http4s.circe.CirceEntityCodec._
import org.http4s.dsl.Http4sDsl

object Routes {

  def apply(repository: QuotesRepository): HttpRoutes[IO] = {

    val dsl = new Http4sDsl[IO] {}
    import dsl._

    HttpRoutes.of[IO] {
      case GET -> Root =>
        repository.list.flatMap(Ok(_))

      case GET -> Root / "random" =>
        repository.random.flatMap(Ok(_))

      case GET -> Root / IntVar(id) =>
        repository.read(id).flatMap(Ok(_))
    }
  }

}
