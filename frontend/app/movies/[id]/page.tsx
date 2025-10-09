import { getMovieReviews } from "@/lib/tmdb";

interface Review {
  id: string;
  author: string;
  content: string;
}

export default async function MoviePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const reviews = await getMovieReviews(Number(id));

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-8">
      <h1 className="text-3xl font-semibold text-center">Reviews</h1>

      {reviews.results.length === 0 ? (
        <p className="text-center text-gray-500">No reviews yet.</p>
      ) : (
        <div className="space-y-6">
          {reviews.results.map((review: Review) => (
            <div
              key={review.id}
              className="rounded-2xl bg-gray-50 dark:bg-gray-800 p-6 shadow-sm border border-gray-200 dark:border-gray-700 transition hover:shadow-md"
            >
              <h2 className="text-lg font-semibold mb-2 text-gray-800 dark:text-gray-100">
                {review.author}
              </h2>
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed whitespace-pre-line">
                {review.content}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
