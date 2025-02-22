
import React from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface SocialLinkInputProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
  isGithub?: boolean;
}

const SocialLinkInput: React.FC<SocialLinkInputProps> = ({
  label,
  value,
  onChange,
  placeholder,
  isGithub = false,
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const inputValue = e.target.value;
    if (isGithub) {
      // Remove any GitHub URL prefix if user pastes a full URL
      const username = inputValue.replace(/^https?:\/\/github\.com\//, '');
      onChange(username);
    } else {
      onChange(inputValue);
    }
  };

  return (
    <div className="space-y-2">
      <Label htmlFor={label.toLowerCase()}>{label}</Label>
      <div className="relative">
        {isGithub && (
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground text-sm">
            github.com/
          </span>
        )}
        <Input
          id={label.toLowerCase()}
          type={isGithub ? "text" : "url"}
          placeholder={placeholder}
          value={value}
          onChange={handleChange}
          className={`transition-all duration-200 focus:ring-2 focus:ring-primary/20 ${
            isGithub ? "pl-24" : ""
          }`}
        />
      </div>
    </div>
  );
};

export default SocialLinkInput;
