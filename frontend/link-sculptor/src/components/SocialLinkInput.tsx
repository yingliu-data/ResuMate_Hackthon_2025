
import React from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface SocialLinkInputProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
}

const SocialLinkInput: React.FC<SocialLinkInputProps> = ({
  label,
  value,
  onChange,
  placeholder,
}) => {
  return (
    <div className="space-y-2">
      <Label htmlFor={label.toLowerCase()}>{label}</Label>
      <Input
        id={label.toLowerCase()}
        type="url"
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="transition-all duration-200 focus:ring-2 focus:ring-primary/20"
      />
    </div>
  );
};

export default SocialLinkInput;
