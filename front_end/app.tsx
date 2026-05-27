import React, { useState } from 'react';
import { UserProfile, SkillLevels } from './types.ts';
import { LEARNING_STYLES, LESSON_TOPICS } from './constants.ts';
import { SkillTreeSection } from './components/skilltree.tsx';
import { Dropdown } from './components/dropdown.tsx';
import { generateLectureContent } from './services/geminiServices.ts';
import ReactMarkdown from 'react-markdown';

// Helper to initialize skill levels
const initialSkillLevels: SkillLevels = {
  syntax: '',
  oopConcepts: '',
  testing: '',
  modeling: '',
  abstraction: ''
};

const App: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  
  // Form State
  const [interests, setInterests] = useState('');
  const [learningStyle, setLearningStyle] = useState('');
  const [lessonTopic, setLessonTopic] = useState('');
  const [skillLevels, setSkillLevels] = useState<SkillLevels>(initialSkillLevels);

  const handleSkillChange = (key: keyof SkillLevels, value: string) => {
    setSkillLevels(prev => ({ ...prev, [key]: value }));
  };

  const handleGenerate = async () => {
    // Basic validation
    if (!lessonTopic || !learningStyle) {
      alert("Vui lòng chọn bài học và phong cách học.");
      return;
    }

    setLoading(true);
    setResult(null);

    const profile: UserProfile = {
      interests: interests || "Không có",
      learningStyle,
      lessonTopic,
      skillLevels
    };

    const content = await generateLectureContent(profile);
    setResult(content);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-white md:bg-gray-100 flex flex-col items-center py-4 md:py-10">
      
      {/* Header Container */}
      <div className="w-full max-w-5xl bg-white border border-gray-400 p-6 mb-0 md:mb-6 md:rounded-lg md:shadow-sm">
        <h1 className="text-xl md:text-2xl font-medium text-gray-800 text-center">
          Sinh bài giảng Lập trình hướng đối tượng với Java - GLOOPJ
        </h1>
      </div>

      {/* Main Form Container */}
      <div className="w-full max-w-5xl bg-white border border-gray-400 p-6 md:p-10 md:rounded-lg md:shadow-md relative">
        
        {/* Inner Border Box (Simulating the wireframe) */}
        <div className="border border-gray-400 rounded-lg p-6 md:p-8">
          
          {/* Interests */}
          <div className="mb-6">
            <label className="block text-gray-700 font-medium mb-2 ml-1">Sở thích</label>
            <input
              type="text"
              value={interests}
              onChange={(e) => setInterests(e.target.value)}
              placeholder="Ví dụ: bóng đá, âm nhạc, vẽ tranh..."
              className="w-full md:w-1/2 px-4 py-2 border border-gray-400 rounded focus:outline-none focus:border-gray-600 text-center"
            />
          </div>

          {/* Learning Style */}
          <div className="mb-6">
            <label className="block text-gray-700 font-medium mb-2 ml-1">Phong cách học</label>
            <div className="w-full md:w-1/2">
              <Dropdown
                value={learningStyle}
                onChange={setLearningStyle}
                options={LEARNING_STYLES}
                placeholder="Lựa chọn phong cách học"
              />
            </div>
          </div>

          {/* Skill Tree */}
          <div className="mb-6">
            <label className="block text-gray-700 font-medium ml-1">Đánh giá kỹ năng (Skill-tree)</label>
            <SkillTreeSection levels={skillLevels} onChange={handleSkillChange} />
          </div>

          {/* Lesson */}
          <div className="mb-2">
            <label className="block text-gray-700 font-medium mb-2 ml-1">Bài học</label>
            <div className="w-full md:w-1/2">
              <Dropdown
                value={lessonTopic}
                onChange={setLessonTopic}
                options={LESSON_TOPICS}
                placeholder="Lựa chọn bài học"
                className="text-left"
              />
            </div>
          </div>

        </div>

        {/* Action Button */}
        <div className="flex justify-end mt-6">
            <button
              onClick={handleGenerate}
              disabled={loading}
              className={`
                px-8 py-3 rounded border border-gray-400 font-medium transition-all
                ${loading 
                  ? 'bg-gray-200 text-gray-500 cursor-not-allowed' 
                  : 'bg-white text-gray-800 hover:bg-gray-50 shadow-sm active:shadow-inner'
                }
              `}
            >
              {loading ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-gray-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Đang tối ưu...
                </span>
              ) : (
                'Tối ưu bài giảng'
              )}
            </button>
        </div>
      </div>

      {/* Result Display */}
      {result && (
        <div className="w-full max-w-5xl mt-6 bg-white border border-gray-300 rounded-lg p-8 shadow-md">
          <h2 className="text-xl font-bold mb-4 text-gray-800 border-b pb-2">Nội dung bài giảng</h2>
          <div className="prose prose-slate max-w-none">
             <ReactMarkdown 
                components={{
                    h1: ({node, ...props}) => <h1 className="text-2xl font-bold mt-6 mb-4 text-blue-700" {...props} />,
                    h2: ({node, ...props}) => <h2 className="text-xl font-bold mt-5 mb-3 text-gray-800 border-l-4 border-blue-500 pl-3" {...props} />,
                    h3: ({node, ...props}) => <h3 className="text-lg font-semibold mt-4 mb-2 text-gray-700" {...props} />,
                    ul: ({node, ...props}) => <ul className="list-disc list-outside ml-6 mb-4 space-y-1" {...props} />,
                    ol: ({node, ...props}) => <ol className="list-decimal list-outside ml-6 mb-4 space-y-1" {...props} />,
                    li: ({node, ...props}) => <li className="text-gray-700" {...props} />,
                    p: ({node, ...props}) => <p className="mb-4 text-gray-700 leading-relaxed" {...props} />,
                    strong: ({node, ...props}) => <strong className="font-bold text-gray-900" {...props} />,
                    code: ({node, className, ...props}) => {
                        const match = /language-(\w+)/.exec(className || '')
                        const isInline = !match && !String(props.children).includes('\n');
                        return isInline 
                            ? <code className="bg-gray-100 text-red-500 px-1 py-0.5 rounded text-sm font-mono" {...props} />
                            : <div className="mockup-code bg-gray-800 text-gray-100 p-4 rounded-lg my-4 overflow-x-auto"><code className="font-mono text-sm" {...props} /></div>
                    },
                    blockquote: ({node, ...props}) => <blockquote className="border-l-4 border-gray-300 pl-4 italic text-gray-600 my-4" {...props} />,
                }}
             >
                {result}
             </ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  );
};

export default App;