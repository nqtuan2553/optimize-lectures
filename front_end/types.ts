export interface SkillLevels {
    syntax: string;
    oopConcepts: string;
    testing: string;
    modeling: string;
    abstraction: string;
  }
  
  export interface UserProfile {
    interests: string;
    learningStyle: string;
    skillLevels: SkillLevels;
    lessonTopic: string;
  }
  
  export interface DropdownOption {
    value: string;
    label: string;
  }
  
  export interface SkillCategory {
    id: keyof SkillLevels;
    title: string;
    subtitle?: string; // For the second line in the box (e.g. "và ngữ nghĩa Java")
    options: DropdownOption[];
  }