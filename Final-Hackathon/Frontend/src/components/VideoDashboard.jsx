import React, { useState, useEffect } from "react";
import { analyzeVideo, getEvaluations, getFeedback } from "../api/api";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { Card, CardContent } from "./ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "./ui/tabs";
import { Loader } from "lucide-react";
import ReactMarkdown from "react-markdown";

export default function VideoDashboard() {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [evaluations, setEvaluations] = useState([]);
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeUrl, setActiveUrl] = useState(null);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      await analyzeVideo(youtubeUrl);
      setActiveUrl(youtubeUrl);
      fetchEvaluations();
      fetchFeedback(youtubeUrl);
    } catch (error) {
      console.error("Analysis failed", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchEvaluations = async () => {
    try {
      const res = await getEvaluations();
      setEvaluations(res?.data);
    } catch (error) {
      console.error("Error fetching evaluations", error);
    }
  };

  const fetchFeedback = async (url) => {
    try {
      const res = await getFeedback(url);
      setFeedback(res.data);
    } catch (error) {
      console.error("Error fetching feedback", error);
    }
  };

  useEffect(() => {
    fetchEvaluations();
  }, []);

  // Grouping evaluations by youtube_url
  const groupedEvaluations = evaluations.reduce((acc, curr) => {
    const url = curr.youtube_url;
    if (!acc[url]) acc[url] = [];
    acc[url].push(curr);
    return acc;
  }, {});

  // Extract only executive summary from markdown
  const extractExecutiveSummary = (markdown) => {
    const match = markdown.match(/\*\*1\. Executive Summary:\*\*\n([\s\S]*?)(\n\*\*|$)/);
    return match ? match[1].trim() : "No summary found.";
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold mb-4 text-center text-indigo-700">
        🎥 Video Submission Dashboard
      </h1>

      <div className="flex items-center space-x-4 mb-8">
        <Input
          type="text"
          placeholder="Paste YouTube video link..."
          value={youtubeUrl}
          onChange={(e) => setYoutubeUrl(e.target.value)}
        />
        <Button onClick={handleAnalyze} disabled={loading}>
          {loading ? <Loader className="animate-spin" /> : "Analyze"}
        </Button>
      </div>

      <Tabs defaultValue="evaluations">
        <TabsList>
          <TabsTrigger value="evaluations">Evaluations</TabsTrigger>
          <TabsTrigger value="feedback">Feedback & Tips</TabsTrigger>
        </TabsList>

        <TabsContent value="evaluations">
          {Object.entries(groupedEvaluations).map(([url, items], groupIdx) => (
            <div key={groupIdx} className="mb-6">
              <h2 className="text-xl font-bold text-indigo-800 mb-2">
                🎬 {items[0]?.metadata?.title || "Untitled Video"}
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {items.map((item, idx) => (
                  <Card key={idx} className="bg-white shadow-md rounded-2xl p-4">
                    <CardContent>
                      <p className="text-sm text-gray-600">
                        <strong>Channel:</strong> {item.metadata?.channel || "Unknown"}
                      </p>
                      <p className="text-sm text-gray-600">
                        <strong>Overall Score:</strong> {item.overall_score}/100
                      </p>

                      <div className="space-y-2 mt-2">
                        {["content", "clarity", "tone", "structure_flow"].map((key) => (
                          <div key={key}>
                            <p className="text-sm font-medium capitalize">{key}</p>
                            <div className="w-full h-2 bg-gray-200 rounded">
                              <div
                                className="h-2 rounded bg-indigo-500"
                                style={{ width: `${item.scores?.[key] || 0}%` }}
                              />
                            </div>
                          </div>
                        ))}
                      </div>

                      <a
                        href={url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="mt-3 inline-block text-indigo-600 hover:underline text-sm"
                      >
                        🔗 Watch Video
                      </a>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          ))}
        </TabsContent>

        <TabsContent value="feedback">
          <div className="mt-4">
            {feedback ? (
              <Card className="bg-emerald-50 p-4 shadow-md">
                <CardContent>
                  <h3 className="text-xl font-semibold text-emerald-800 mb-2">
                    Feedback for: <span className="underline">{activeUrl}</span>
                  </h3>
                  <div className="prose prose-sm max-w-none text-gray-800">
                    <ReactMarkdown>
                      {`### Executive Summary\n\n${extractExecutiveSummary(
                        feedback?.feedback || ""
                      )}`}
                    </ReactMarkdown>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <p className="text-gray-500 text-sm">No feedback selected.</p>
            )}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
