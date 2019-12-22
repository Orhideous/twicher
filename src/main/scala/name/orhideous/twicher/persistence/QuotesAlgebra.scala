package name.orhideous.twicher.persistence

trait QuotesAlgebra[F[_]] {

  def read(id: Int): F[Quote]

  def list: F[Vector[Quote]]

  def random: F[Quote]
}
