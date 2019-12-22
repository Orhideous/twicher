package name.orhideous.twicher.persistence

import java.nio.charset.Charset
import java.nio.file.Path
import java.nio.file.WatchEvent
import java.util.concurrent.Executors

import better.files.File
import cats.effect.Sync
import com.typesafe.scalalogging.StrictLogging
import io.methvin.better.files.RecursiveFileMonitor
import name.orhideous.twicher.Error

import scala.collection.concurrent.TrieMap
import scala.concurrent.ExecutionContext
import scala.util.Random

class QuotesFileRepository[F[_]: Sync](private val quotesDir: File)(implicit F: Sync[F])
    extends QuotesAlgebra[F]
    with StrictLogging {

  private final val cache = TrieMap.empty[Int, Quote]
  private final val rnd   = new Random

  private implicit val watcherEC: ExecutionContext =
    ExecutionContext.fromExecutor(Executors.newFixedThreadPool(1))

  private final val watcher = new RecursiveFileMonitor(quotesDir, logger = logger.underlying) {
    override def onEvent(eventType: WatchEvent.Kind[Path], file: File, count: Int): Unit = {
      logger.info(s"Detected change in $quotesDir, reloading")
      reload()
    }
  }

  watcher.start()
  reload()

  override def list: F[Vector[Quote]] = F.pure(cache.values.toVector)

  override def random: F[Quote] =
    if (cache.isEmpty) {
      F.raiseError(Error.NoSuchQuote)
    } else {
      read(cache.keySet.toVector(rnd.nextInt(cache.size)))
    }

  override def read(id: Int): F[Quote] = cache.get(id) match {
    case Some(quote) => F.pure(quote)
    case None        => F.raiseError(Error.NoSuchQuote)
  }

  private def reload(): Unit = {
    val quotes = QuotesFileRepository.loadQuotes(quotesDir).map(q => q.id -> q).toMap
    cache.clear()
    cache ++= quotes
    logger.info(s"Loaded ${quotes.size} quotes from $quotesDir")
  }
}

object QuotesFileRepository {
  private final val pattern = ".*(\\d+)\\.txt$".r

  def apply[F[_]: Sync](quotesDir: String): QuotesFileRepository[F] = new QuotesFileRepository[F](File(quotesDir))

  private final implicit val charset: Charset = Charset.forName("UTF-8")

  private def loadQuotes(quotesDir: File): Seq[Quote] =
    quotesDir
      .globRegex(pattern)
      .toSeq
      .par
      .map(parseFile)
      .seq

  private def parseFile(file: File): Quote = {
    val pattern(id) = file.name
    val text        = file.contentAsString.stripLineEnd.trim
    Quote(id.toInt, text)
  }
}
