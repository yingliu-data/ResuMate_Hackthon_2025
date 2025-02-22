
import React from "react";
import { Card } from "@/components/ui/card";

interface ResultDisplayProps {
  content: string;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ content }) => {
  if (!content) return null;

  return (
    <Card className="p-6 mt-8 animate-fadeIn glass-card">
      <h3 className="text-lg font-semibold mb-4">Tailored Resume</h3>
      <div className="prose max-w-none">
        <pre className="whitespace-pre-wrap text-sm">{content}</pre>
      </div>
    </Card>
  );
};

export default ResultDisplay;
