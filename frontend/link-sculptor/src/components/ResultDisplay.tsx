
import React from "react";
import { Card } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";

interface ResultDisplayProps {
  content: string;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ content }) => {
  if (!content) return null;

  return (
    <Card className="p-6 mt-8 animate-fadeIn glass-card">
      <h3 className="text-xl font-semibold mb-4">Your Tailored Resume</h3>
      <Separator className="my-4" />
      <div className="prose max-w-none">
        {/* Split the content by newlines and render each section */}
        {content.split('\n').map((line, index) => (
          <div key={index} className="mb-2">
            {line.trim() ? (
              <p className="text-base leading-relaxed">{line}</p>
            ) : (
              <br />
            )}
          </div>
        ))}
      </div>
    </Card>
  );
};

export default ResultDisplay;
