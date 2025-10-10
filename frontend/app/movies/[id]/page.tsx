// app/movies/[id]/page.tsx (server)
import MovieClient from "./MovieClient";
import { getMovieReviews } from "@/lib/tmdb";

export default async function MoviePage({
  params,
}: {
  params: { id: string };
}) {
  const reviews = await getMovieReviews(Number(params.id));
  return <MovieClient reviews={reviews.results} />;
}
