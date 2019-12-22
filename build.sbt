enablePlugins(DockerPlugin)

val Http4sVersion           = "0.20.8"
val CirceVersion            = "0.11.1"
val LogbackVersion          = "1.2.3"
val BetterFilesVersion      = "3.8.0"
val DirectoryWatcherVersion = "0.9.6"
val ScalaLoggingVersion     = "3.9.2"

organization := "name.orhideous"
name := "twicher"
version := "0.1.0-SNAPSHOT"
scalaVersion := "2.12.8"

dockerfile in docker := {
  val artifact: File     = assembly.value
  val artifactTargetPath = s"/app/${artifact.name}"

  new Dockerfile {
    from("openjdk:11-jre")
    add(artifact, artifactTargetPath)
    env("TWICHER_DIR", "/data")
    volume("/data")
    entryPoint("java", "-jar", artifactTargetPath)
  }
}

imageNames in docker := Seq(
  ImageName(s"${organization.value}/${name.value}:latest"),
  ImageName(
    namespace = Some(organization.value),
    repository = name.value,
    tag = Some("v" + version.value)
  )
)

libraryDependencies ++= Seq(
  "org.http4s"                 %% "http4s-blaze-server"            % Http4sVersion,
  "org.http4s"                 %% "http4s-circe"                   % Http4sVersion,
  "org.http4s"                 %% "http4s-dsl"                     % Http4sVersion,
  "io.circe"                   %% "circe-generic"                  % CirceVersion,
  "com.github.pathikrit"       %% "better-files"                   % BetterFilesVersion,
  "io.methvin"                 %% "directory-watcher-better-files" % DirectoryWatcherVersion,
  "com.typesafe.scala-logging" %% "scala-logging"                  % ScalaLoggingVersion,
  "ch.qos.logback"             % "logback-classic"                 % LogbackVersion,
  compilerPlugin("org.typelevel" %% "kind-projector"     % "0.10.3"),
  compilerPlugin("com.olegpy"    %% "better-monadic-for" % "0.3.0")
)

scalacOptions ++= Seq(
  "-deprecation",
  "-encoding",
  "UTF-8",
  "-language:higherKinds",
  "-language:postfixOps",
  "-feature",
  "-Ypartial-unification",
  "-Xfatal-warnings"
)
