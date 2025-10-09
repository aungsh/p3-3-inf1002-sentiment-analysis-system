"use client";

import { useState } from "react";
import Image from "next/image";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Search } from "lucide-react";
import { searchMovies } from "@/lib/tmdb";
import Link from "next/link";

// Type definition for a movie result
interface Movie {
  id: number;
  title: string;
  release_date?: string;
  poster_path?: string | null;
  overview?: string;
}

export default function SearchBar() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const res = await searchMovies(query);
      setResults(res.results || []);
    } catch (err) {
      console.error("Search failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-5xl mx-auto">
      {/* Search form */}
      <form
        onSubmit={handleSearch}
        className="mb-8 flex w-full items-center gap-2"
      >
        <Input
          type="text"
          placeholder="Search for a movie..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1"
        />
        <Button type="submit" variant="default" size="icon" disabled={loading}>
          <Search className="h-4 w-4" />
        </Button>
      </form>

      {/* Loading indicator */}
      {loading && (
        <p className="text-center text-muted-foreground m-10">Searching...</p>
      )}

      {/* Results grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
        {results.map((movie) => (
          <Link
            href={`/movies/${movie.id}`}
            key={movie.id}
            className="overflow-hidden"
          >
            <div key={movie.id} className="overflow-hidden">
              <div>
                <div className="relative w-full h-96">
                  {movie.poster_path ? (
                    <Image
                      src={`https://image.tmdb.org/t/p/w500${movie.poster_path}`}
                      alt={movie.title}
                      fill
                      className="object-cover rounded-md hover:shadow-md transition-shadow duration-200"
                      sizes="(max-width: 768px) 50vw, (max-width: 1200px) 25vw, 20vw"
                      priority={true}
                    />
                  ) : (
                    <div className="w-full h-full bg-gray-200 flex items-center justify-center rounded-md">
                      <span className="text-gray-500 text-sm">No Image</span>
                    </div>
                  )}
                </div>

                <div className="pt-3">
                  <h3 className="font-semibold text-sm line-clamp-1">
                    {movie.title}
                  </h3>
                  <p className="text-xs text-muted-foreground mb-1">
                    {movie.release_date?.slice(0, 4) || "N/A"}
                  </p>
                </div>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {/* No results */}
      {!loading && results.length === 0 && query && (
        <p className="text-center text-muted-foreground mt-4">
          No results found for “{query}”.
        </p>
      )}
    </div>
  );
}
