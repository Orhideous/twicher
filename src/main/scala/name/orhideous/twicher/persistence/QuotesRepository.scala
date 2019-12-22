package name.orhideous.twicher.persistence

import cats.effect.IO

trait QuotesRepository {

  def read(id: Int): IO[Quote]

  def list: IO[Vector[Quote]]

  def random: IO[Quote]
}
