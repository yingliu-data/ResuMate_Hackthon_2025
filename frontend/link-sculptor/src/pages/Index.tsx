
import React, { useState } from "react";
import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";
import { toast } from "sonner";
import FileUpload from "../components/FileUpload";
import SocialLinkInput from "../components/SocialLinkInput";
import ResultDisplay from "../components/ResultDisplay";
import ChatBox from "../components/ChatBox";

const Index = () => {
  const [githubLink, setGithubLink] = useState("");
  const [linkedinLink, setLinkedinLink] = useState("");
  const [resume, setResume] = useState<File | null>(null);
  const [jobDescription, setJobDescription] = useState<File | null>(null);
  const [result, setResult] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    if (!githubLink || !linkedinLink) {
      toast.error("Please provide both GitHub and LinkedIn links");
      return;
    }

    if (!jobDescription) {
      toast.error("Please upload a job description");
      return;
    }

    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('githubLink', githubLink);
      formData.append('linkedinLink', linkedinLink);
      if (resume) {
        formData.append('resume', resume);
      }
      formData.append('jobDescription', jobDescription);

      const response = await fetch('http://localhost:3001/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to send data to server');
      }

      const data = await response.json();
      setResult(data.message || "Data successfully sent to server!");
      toast.success("Data successfully sent to server!");
    } catch (error) {
      console.error('Error:', error);
      toast.error("Failed to send data to server");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen py-8 px-4 max-w-2xl mx-auto">
      <Card className="p-6 glass-card">
        <h1 className="text-2xl font-semibold text-center mb-6">
          Resume Tailor
        </h1>
        
        <div className="space-y-6">
          <SocialLinkInput
            label="GitHub Profile"
            value={githubLink}
            onChange={setGithubLink}
            placeholder="https://github.com/username"
          />
          
          <SocialLinkInput
            label="LinkedIn Profile"
            value={linkedinLink}
            onChange={setLinkedinLink}
            placeholder="https://linkedin.com/in/username"
          />

          <div className="space-y-2">
            <p className="text-sm font-medium mb-2">Current Resume (Optional)</p>
            <FileUpload
              onFileSelect={(file) => {
                setResume(file);
                toast.success("Resume uploaded successfully");
              }}
              accept={{ "application/pdf": [".pdf"] }}
              label="Upload your current resume (PDF)"
            />
          </div>

          <div className="space-y-2">
            <p className="text-sm font-medium mb-2">Job Description</p>
            <FileUpload
              onFileSelect={(file) => {
                setJobDescription(file);
                toast.success("Job description uploaded successfully");
              }}
              accept={{
                "application/pdf": [".pdf"],
                "text/plain": [".txt"],
              }}
              label="Upload the job description (PDF or TXT)"
            />
          </div>

          <Button
            onClick={handleSubmit}
            className="w-full"
            disabled={isLoading}
          >
            {isLoading ? (
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-primary border-t-transparent"></div>
                <span>Processing...</span>
              </div>
            ) : (
              "Generate Tailored Resume"
            )}
          </Button>
        </div>
      </Card>

      {result && <ResultDisplay content={result} />}
      <ChatBox />
    </div>
  );
};

export default Index;
