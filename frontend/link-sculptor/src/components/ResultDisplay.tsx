
import React, { useEffect, useRef } from "react";
import { Card } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { toast } from "sonner";

interface ResultDisplayProps {
  content: string;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ content }) => {
  const resultRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (content && resultRef.current) {
      resultRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [content]);

  const handleDownload = () => {
    try {
      // Create a Blob with the CV content as text
      const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
      const url = window.URL.createObjectURL(blob);

      // Create a temporary link element
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'tailored-resume.txt');

      // Append link to body, click it, and remove it
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      // Clean up the URL
      window.URL.revokeObjectURL(url);

      toast.success("Resume downloaded successfully!");
    } catch (error) {
      console.error('Download error:', error);
      toast.error("Failed to download resume");
    }
  };

  if (!content) return null;

  return (
    <Card className="p-6 mt-8 animate-fadeIn glass-card" ref={resultRef}>
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-semibold">Your Tailored Resume</h3>
        <Button
          onClick={handleDownload}
          variant="outline"
          className="flex items-center gap-2"
        >
          <Download className="h-4 w-4" />
          Download Text
        </Button>
      </div>
      <Separator className="my-4" />
      <div className="prose max-w-none">
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
