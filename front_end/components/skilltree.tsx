import React from 'react';
import { SkillLevels } from '../types.ts';
import { SKILL_TREE_CONFIG } from '../constants.ts';
import { Dropdown } from './dropdown.tsx';

interface SkillTreeSectionProps {
  levels: SkillLevels;
  onChange: (key: keyof SkillLevels, value: string) => void;
}

export const SkillTreeSection: React.FC<SkillTreeSectionProps> = ({ levels, onChange }) => {
  return (
    <div className="border border-gray-400 rounded-lg p-4 mt-6">
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        {SKILL_TREE_CONFIG.map((skill) => (
          <div key={skill.id} className="flex flex-col items-center">
            <div className="border border-gray-400 rounded-lg px-2 py-3 w-full h-full flex flex-col justify-between items-center bg-white">
              <div className="text-center mb-3 min-h-[48px] flex flex-col justify-center">
                <span className="font-semibold text-gray-700 block text-sm">{skill.title}</span>
                {skill.subtitle && (
                  <span className="text-gray-600 text-xs block">{skill.subtitle}</span>
                )}
              </div>
              <Dropdown
                value={levels[skill.id]}
                onChange={(val) => onChange(skill.id, val)}
                options={skill.options}
                placeholder="Lựa chọn trình độ"
                className="w-full"
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};