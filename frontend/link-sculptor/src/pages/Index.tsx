
import React, { useState, useImperativeHandle, forwardRef } from "react";
import { Button } from "../components/ui/button";
import { Card } from "../components/ui/card";
import { toast } from "sonner";
import FileUpload from "../components/FileUpload";
import SocialLinkInput from "../components/SocialLinkInput";
import ResultDisplay from "../components/ResultDisplay";
import ChatBox from "../components/ChatBox";

export interface IndexRef {
  generateCV: () => Promise<void>;
}

const Index = forwardRef<IndexRef>((_, ref) => {
  const [githubUsername, setGithubUsername] = useState("");
  const [linkedinLink, setLinkedinLink] = useState("");
  const [resume, setResume] = useState<File | null>(null);
  const [jobDescriptionLink, setJobDescriptionLink] = useState("");
  const [result, setResult] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    if (!githubUsername || !linkedinLink) {
      toast.error("Please provide both GitHub username and LinkedIn link");
      return;
    }

    if (!jobDescriptionLink) {
      toast.error("Please provide a job description link");
      return;
    }

    setIsLoading(true);
    setResult(""); // Clear previous result

    try {
      const formData = new FormData();
      formData.append('github_link', githubUsername);
      formData.append('linkedin_link', linkedinLink);
      formData.append('job_description', jobDescriptionLink);
      if (resume) {
        formData.append('resume', resume);
      }

      const response = await fetch('http://localhost:8000/user-profile', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to send data to server');
      }

      const data = await response.json();

      if (data.cv) {
        setResult(data.cv);
        toast.success("Your tailored CV has been generated!");
      } else {
        setResult("No CV content received from server");
        toast.error("Failed to generate CV");
      }
    } catch (error) {
      console.error('Error:', error);
      toast.error("Failed to generate CV");
      setResult("Error generating CV");
    } finally {
      setIsLoading(false);
    }
  };

  // Expose the generate function to parent components
  useImperativeHandle(ref, () => ({
    generateCV: handleSubmit
  }));

  return (
    <div className="min-h-screen py-8 px-4 max-w-2xl mx-auto">
      <Card className="p-6 glass-card">
        <h1 className="text-2xl font-semibold text-center mb-6">
          Resume Tailor
        </h1>

        <div className="space-y-6">
          <SocialLinkInput
            label="GitHub Username"
            value={githubUsername}
            onChange={setGithubUsername}
            placeholder="username"
            isGithub={true}
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

          <SocialLinkInput
            label="Job Description Link"
            value={jobDescriptionLink}
            onChange={setJobDescriptionLink}
            placeholder="https://example.com/job-posting"
          />

          <Button
            onClick={handleSubmit}
            className="w-full"
            disabled={isLoading}
          >
            {isLoading ? (
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-primary border-t-transparent"></div>
                <span>Generating CV...</span>
              </div>
            ) : (
              "Generate Tailored Resume"
            )}
          </Button>
        </div>
      </Card>

      {result && <ResultDisplay content={result} />}
      <ChatBox onGenerateCV={handleSubmit} />
    </div>
  );
});

Index.displayName = "Index";

export default Index;
