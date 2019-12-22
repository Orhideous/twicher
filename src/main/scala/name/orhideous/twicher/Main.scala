package name.orhideous.twicher

import cats.effect.ExitCode
import cats.effect.IO
import cats.effect.IOApp
import cats.implicits._
import name.orhideous.twicher.persistence.QuotesFileRepository
import org.http4s.implicits._
import org.http4s.server.Router
import org.http4s.server.blaze._

object Main extends IOApp {
  private val host = sys.env.getOrElse("TWICHER_HOST", "0.0.0.0")
  private val port = sys.env.getOrElse("TWICHER_PORT", "9000").toInt
  private val dir  = sys.env.getOrElse("TWICHER_DIR", "./data")

  private val repository = QuotesFileRepository[IO](dir)
  private val routes     = Router[IO]("/" -> Routes[IO](repository)).orNotFound

  override def run(args: List[String]): IO[ExitCode] =
    BlazeServerBuilder[IO]
      .bindHttp(port, host)
      .withHttpApp(routes)
      .serve
      .compile
      .drain
      .as(ExitCode.Success)

}
