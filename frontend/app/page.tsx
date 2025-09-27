"use client";

import React, { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import {
  Loader2,
  Brain,
  BarChart3,
  TrendingUp,
  TrendingDown,
} from "lucide-react";

// Types
interface SentimentResult {
  sentiment: string;
  score: number;
}

interface GeminiResult {
  sentiment: string;
  score: number;
}

interface SentenceAnalysis {
  sentence: string;
  score: number;
}

interface ExtremesResult {
  most_positive: SentenceAnalysis;
  most_negative: SentenceAnalysis;
}

// API service
class SentimentAPI {
  private static baseUrl = "http://localhost:8000"; // Adjust based on your backend URL

  static async analyzeSentiment(text: string): Promise<SentimentResult> {
    const response = await fetch(`${this.baseUrl}/sentiment/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    return response.json();
  }

  static async analyzeWithGemini(text: string): Promise<GeminiResult> {
    const response = await fetch(`${this.baseUrl}/gemini`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    return response.json();
  }

  static async analyzePerSentence(text: string): Promise<SentenceAnalysis[]> {
    const response = await fetch(
      `${this.baseUrl}/sentiment/analyze_sentiment_per_sentence`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      }
    );
    return response.json();
  }

  static async analyzeExtremes(text: string): Promise<ExtremesResult> {
    const response = await fetch(`${this.baseUrl}/extremes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    return response.json();
  }
}

// Utility functions
const getSentimentColor = (sentiment: string, score?: number): string => {
  if (sentiment.toLowerCase() === "positive" || (score && score > 0))
    return "bg-green-100 text-green-800 border-green-200";
  if (sentiment.toLowerCase() === "negative" || (score && score < 0))
    return "bg-red-100 text-red-800 border-red-200";
  return "bg-gray-100 text-gray-800 border-gray-200";
};

const getSentimentIcon = (sentiment: string, score?: number) => {
  if (sentiment.toLowerCase() === "positive" || (score && score > 0))
    return <TrendingUp className="w-4 h-4" />;
  if (sentiment.toLowerCase() === "negative" || (score && score < 0))
    return <TrendingDown className="w-4 h-4" />;
  return <BarChart3 className="w-4 h-4" />;
};

// Components
const TextInput: React.FC<{
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
}> = ({ value, onChange, placeholder }) => (
  <Textarea
    value={value}
    onChange={(e) => onChange(e.target.value)}
    placeholder={placeholder}
    className="min-h-[120px] resize-none"
  />
);

const SentimentCard: React.FC<{
  title: string;
  sentiment: string;
  score: number;
  icon: React.ReactNode;
}> = ({ title, sentiment, score, icon }) => (
  <Card>
    <CardHeader className="pb-3">
      <CardTitle className="text-sm font-medium flex items-center gap-2">
        {icon}
        {title}
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div className="flex items-center justify-between">
        <Badge className={getSentimentColor(sentiment, score)}>
          {getSentimentIcon(sentiment, score)}
          <span className="ml-1 capitalize">{sentiment}</span>
        </Badge>
        <span className="text-2xl font-bold">
          {typeof score === "number" ? score.toFixed(1) : score}
        </span>
      </div>
    </CardContent>
  </Card>
);

const SentenceAnalysisCard: React.FC<{ sentences: SentenceAnalysis[] }> = ({
  sentences,
}) => (
  <Card>
    <CardHeader>
      <CardTitle className="text-sm font-medium flex items-center gap-2">
        <BarChart3 className="w-4 h-4" />
        Per-Sentence Analysis
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div className="space-y-3 max-h-60 overflow-y-auto">
        {sentences.map((item, index) => (
          <div
            key={index}
            className="flex items-start justify-between gap-3 p-3 rounded-lg bg-gray-50"
          >
            <p className="text-sm flex-1">{item.sentence}</p>
            <Badge className={getSentimentColor("", item.score)}>
              {getSentimentIcon("", item.score)}
              <span className="ml-1">{item.score}</span>
            </Badge>
          </div>
        ))}
      </div>
    </CardContent>
  </Card>
);

const ExtremesCard: React.FC<{ extremes: ExtremesResult }> = ({ extremes }) => (
  <Card>
    <CardHeader>
      <CardTitle className="text-sm font-medium flex items-center gap-2">
        <TrendingUp className="w-4 h-4" />
        Sentiment Extremes
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-4">
      <div className="p-3 rounded-lg bg-green-50 border border-green-200">
        <p className="text-xs font-medium text-green-800 mb-1">Most Positive</p>
        <p className="text-sm mb-2">{extremes.most_positive.sentence}</p>
        <Badge className="bg-green-100 text-green-800 border-green-200">
          <TrendingUp className="w-3 h-3 mr-1" />
          {extremes.most_positive.score}
        </Badge>
      </div>

      <div className="p-3 rounded-lg bg-red-50 border border-red-200">
        <p className="text-xs font-medium text-red-800 mb-1">Most Negative</p>
        <p className="text-sm mb-2">{extremes.most_negative.sentence}</p>
        <Badge className="bg-red-100 text-red-800 border-red-200">
          <TrendingDown className="w-3 h-3 mr-1" />
          {extremes.most_negative.score}
        </Badge>
      </div>
    </CardContent>
  </Card>
);

const LoadingButton: React.FC<{
  onClick: () => void;
  loading: boolean;
  children: React.ReactNode;
  variant?: "default" | "outline";
}> = ({ onClick, loading, children, variant = "default" }) => (
  <Button
    onClick={onClick}
    disabled={loading}
    variant={variant}
    className="flex-1"
  >
    {loading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
    {children}
  </Button>
);

// Main component
export default function Home() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState({
    sentiment: false,
    gemini: false,
    sentences: false,
    extremes: false,
  });

  const [results, setResults] = useState({
    sentiment: null as SentimentResult | null,
    gemini: null as GeminiResult | null,
    sentences: null as SentenceAnalysis[] | null,
    extremes: null as ExtremesResult | null,
  });

  const handleAnalysis = async (type: keyof typeof loading) => {
    if (!text.trim()) return;

    setLoading((prev) => ({ ...prev, [type]: true }));

    try {
      switch (type) {
        case "sentiment":
          const sentimentResult = await SentimentAPI.analyzeSentiment(text);
          setResults((prev) => ({ ...prev, sentiment: sentimentResult }));
          break;
        case "gemini":
          const geminiResult = await SentimentAPI.analyzeWithGemini(text);
          setResults((prev) => ({ ...prev, gemini: geminiResult }));
          break;
        case "sentences":
          const sentencesResult = await SentimentAPI.analyzePerSentence(text);
          setResults((prev) => ({ ...prev, sentences: sentencesResult }));
          break;
        case "extremes":
          const extremesResult = await SentimentAPI.analyzeExtremes(text);
          setResults((prev) => ({ ...prev, extremes: extremesResult }));
          break;
      }
    } catch (error) {
      console.error(`Error analyzing ${type}:`, error);
    } finally {
      setLoading((prev) => ({ ...prev, [type]: false }));
    }
  };

  const analyzeAll = async () => {
    if (!text.trim()) return;

    const types: (keyof typeof loading)[] = [
      "sentiment",
      "gemini",
      "sentences",
      "extremes",
    ];

    for (const type of types) {
      await handleAnalysis(type);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-gray-900">
            Sentiment Analysis Dashboard
          </h1>
          <p className="text-gray-600">
            Analyze text sentiment using multiple AI models and techniques
          </p>
        </div>

        {/* Input Section */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <Brain className="w-5 h-5" />
              Text Input
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <TextInput
              value={text}
              onChange={setText}
              placeholder="Enter your text here to analyze sentiment..."
            />

            <div className="flex gap-3 flex-wrap">
              <LoadingButton
                onClick={() => handleAnalysis("sentiment")}
                loading={loading.sentiment}
              >
                Basic Sentiment
              </LoadingButton>

              <LoadingButton
                onClick={() => handleAnalysis("gemini")}
                loading={loading.gemini}
                variant="outline"
              >
                Gemini Analysis
              </LoadingButton>

              <LoadingButton
                onClick={() => handleAnalysis("sentences")}
                loading={loading.sentences}
                variant="outline"
              >
                Per Sentence
              </LoadingButton>

              <LoadingButton
                onClick={() => handleAnalysis("extremes")}
                loading={loading.extremes}
                variant="outline"
              >
                Find Extremes
              </LoadingButton>

              <LoadingButton
                onClick={analyzeAll}
                loading={Object.values(loading).some(Boolean)}
              >
                Analyze All
              </LoadingButton>
            </div>
          </CardContent>
        </Card>

        {/* Results Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* Basic Sentiment */}
          {results.sentiment && (
            <SentimentCard
              title="Basic Analysis"
              sentiment={results.sentiment.sentiment}
              score={results.sentiment.score}
              icon={<BarChart3 className="w-4 h-4" />}
            />
          )}

          {/* Gemini Analysis */}
          {results.gemini && (
            <SentimentCard
              title="Gemini AI"
              sentiment={results.gemini.sentiment}
              score={results.gemini.score}
              icon={<Brain className="w-4 h-4" />}
            />
          )}
        </div>

        {/* Detailed Analysis */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Per-Sentence Analysis */}
          {results.sentences && (
            <SentenceAnalysisCard sentences={results.sentences} />
          )}

          {/* Extremes Analysis */}
          {results.extremes && <ExtremesCard extremes={results.extremes} />}
        </div>
      </div>
    </div>
  );
}
