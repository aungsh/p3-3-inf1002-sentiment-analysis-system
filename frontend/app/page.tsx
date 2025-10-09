"use client";
import SearchBar from "@/components/sentiment/search";

// Main component
export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-gray-900">
            Movie Sentiment Analysis Dashboard
          </h1>
          <p className="text-gray-600">Analyze movie sentiment from TMDB</p>
        </div>

        <SearchBar />
      </div>
    </div>
  );
}
