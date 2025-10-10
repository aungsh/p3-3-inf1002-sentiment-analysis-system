"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import axios from "axios";
import { Switch } from "@/components/ui/switch";
import {
  Tooltip,
  TooltipTrigger,
  TooltipContent,
  TooltipProvider,
} from "@/components/ui/tooltip";

interface Review {
  id: string;
  author: string;
  content: string;
}

interface Extreme {
  text: string;
  sentiment: string;
  score: number;
}

interface SlidingWindow {
  text: string;
  score: number;
  indices: number[];
}

interface Analysis {
  overall: {
    sentiment: string;
    score: number;
  };
  extremes?: Extreme[];
  sliding_window?: SlidingWindow[];
}

async function fetchFullAnalysis(
  text: string,
  window_size = 3
): Promise<Analysis> {
  const response = await axios.post("http://localhost:8000/full_analysis", {
    text,
    window_size,
  });
  console.log("Text to analyze:", text);
  console.log("Analysis response:", response.data);
  return response.data;
}

export default function MovieClient({ reviews }: { reviews: Review[] }) {
  const [analysisMap, setAnalysisMap] = useState<Record<string, Analysis>>({});
  const [loading, setLoading] = useState(true);
  const [highlightSliding, setHighlightSliding] = useState(false);
  const [windowSize, setWindowSize] = useState(3);

  useEffect(() => {
    async function analyzeAll() {
      if (!reviews || reviews.length === 0) return setLoading(false);

      const analyses = await Promise.allSettled(
        reviews.map((r) => fetchFullAnalysis(r.content, windowSize))
      );

      const map: Record<string, Analysis> = {};
      reviews.forEach((r, i) => {
        if (analyses[i].status === "fulfilled") map[r.id] = analyses[i].value;
      });
      setAnalysisMap(map);
      setLoading(false);
    }

    analyzeAll();
  }, [reviews, windowSize]);

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto p-6 space-y-6">
        {[...Array(3)].map((_, i) => (
          <Card key={i} className="p-6">
            <Skeleton className="h-6 w-1/3 mb-3" />
            <Skeleton className="h-4 w-full mb-2" />
            <Skeleton className="h-4 w-5/6" />
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-8">
      <h1 className="text-3xl font-semibold text-center">Reviews</h1>

      <div className="flex justify-center items-center gap-3 mb-6">
        <span>Highlight Sliding Window</span>
        <Switch
          checked={highlightSliding}
          onCheckedChange={(val) => setHighlightSliding(!!val)}
        />
        {highlightSliding && (
          <div className="flex items-center gap-2">
            <span className="text-sm text-gray-600">Window Size:</span>
            <input
              type="number"
              min={1}
              max={10}
              value={windowSize}
              onChange={(e) => setWindowSize(Number(e.target.value))}
              className="w-16 border rounded px-2 py-1 text-sm dark:bg-gray-800 dark:border-gray-700"
            />
          </div>
        )}
      </div>

      {reviews.length === 0 ? (
        <p className="text-center text-gray-500">No reviews yet.</p>
      ) : (
        <div className="space-y-6">
          {reviews.map((review) => {
            const analysis = analysisMap[review.id];
            const sentiment = analysis?.overall.sentiment || "Loading...";
            const score = analysis?.overall.score ?? "–";
            const normalizedContent = review.content.replace(/[\r\n]+/g, " ");

            let highlightedParts: React.ReactNode[] = [normalizedContent];

            if (analysis) {
              const highlights = highlightSliding
                ? (
                    analysis.sliding_window?.filter(
                      (w): w is SlidingWindow => !!w && !!w.text
                    ) || []
                  ).map((w) => ({ text: w.text, score: w.score }))
                : (
                    analysis.extremes?.filter(
                      (e): e is Extreme => !!e && !!e.text
                    ) || []
                  ).map((e) => ({ text: e.text, score: e.score }));

              if (highlights.length > 0) {
                // Find min & max scores
                const minScore = Math.min(...highlights.map((h) => h.score));
                const maxScore = Math.max(...highlights.map((h) => h.score));

                highlights.forEach(({ text, score }) => {
                  // Choose color based on relative position
                  const color =
                    score === maxScore
                      ? "red"
                      : score === minScore
                      ? "blue"
                      : "yellow";

                  const newParts: React.ReactNode[] = [];

                  highlightedParts.forEach((part) => {
                    if (typeof part !== "string") return newParts.push(part);

                    const split = part.split(text);
                    for (let i = 0; i < split.length; i++) {
                      newParts.push(split[i]);
                      if (i < split.length - 1) {
                        newParts.push(
                          <TooltipProvider key={Math.random()}>
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <span
                                  className={`bg-${color}-100 dark:bg-${color}-900/40 text-${color}-800 dark:text-${color}-200 rounded px-1 cursor-help`}
                                >
                                  {text}
                                </span>
                              </TooltipTrigger>
                              <TooltipContent>
                                <p className="text-sm">
                                  Score: {score.toFixed(3)}
                                </p>
                              </TooltipContent>
                            </Tooltip>
                          </TooltipProvider>
                        );
                      }
                    }
                  });

                  highlightedParts = newParts;
                });
              }
            }

            let badgeColor = "bg-gray-200 text-gray-700";
            if (sentiment === "POSITIVE")
              badgeColor = "bg-green-500 text-white";
            else if (sentiment === "NEGATIVE")
              badgeColor = "bg-red-500 text-white";
            else if (sentiment === "NEUTRAL")
              badgeColor = "bg-blue-500 text-white";

            return (
              <Card
                key={review.id}
                className="border border-gray-200 dark:border-gray-700 hover:shadow-md transition"
              >
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span>{review.author}</span>
                    {analysis ? (
                      <Badge className={badgeColor}>
                        {sentiment} ({score})
                      </Badge>
                    ) : (
                      <Skeleton className="h-5 w-16" />
                    )}
                  </CardTitle>
                </CardHeader>

                <CardContent>
                  <p className="text-gray-700 dark:text-gray-300 whitespace-pre-line leading-relaxed mb-4">
                    {highlightedParts}
                  </p>

                  {/* Show analysis details */}
                  {analysis && (
                    <div className="border-t pt-3 mt-3 text-sm space-y-1">
                      <p className="font-medium text-gray-600 dark:text-gray-300">
                        {highlightSliding
                          ? "Sliding Window Segments"
                          : "Extreme Sentences"}
                        :
                      </p>

                      <ul className="list-disc list-inside space-y-1">
                        {(highlightSliding
                          ? analysis.sliding_window
                          : analysis.extremes
                        )?.map((item, idx) => (
                          <li
                            key={idx}
                            className="text-gray-600 dark:text-gray-400"
                          >
                            <span className="italic">{item.text}</span>{" "}
                            <span className="ml-1 text-xs text-gray-500">
                              (score: {item.score.toFixed(3)}
                              {highlightSliding
                                ? ""
                                : `, sentiment: ${
                                    (item as Extreme).sentiment || "N/A"
                                  }`}
                              )
                            </span>
                          </li>
                        )) || (
                          <p className="text-gray-400 italic text-sm">
                            No segments found.
                          </p>
                        )}
                      </ul>
                    </div>
                  )}
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
