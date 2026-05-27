import { DropdownOption, SkillCategory } from './types';

// Phong cách học 
export const LEARNING_STYLES: DropdownOption[] = [
  { value: 'visual', label: 'Hình ảnh (Visual)' },
  { value: 'auditory', label: 'Thính giác (Auditory)' },
  { value: 'reading_writing', label: 'Đọc/Viết (Reading/Writing)' },
  { value: 'kinesthetic', label: 'Vận động (Kinesthetic)' },
];

// Bài học 
export const LESSON_TOPICS: DropdownOption[] = [
  { value: 'class_and_object', label: 'Bài 1: Giới thiệu về Đối tượng và Lớp' },
  { value: 'inheritance', label: 'Bài 2: Tính kế thừa (Inheritance)' },
  { value: 'polymorphism', label: 'Bài 3: Tính đa hình (Polymorphism)' }
];

const SYNTAX_OPTIONS: DropdownOption[] = [
  { value: 'level_1', label: 'Level 1: Cài đặt môi trường & Hello World' },
  { value: 'level_2', label: 'Level 2: Cú pháp cơ bản, biến, kiểu dữ liệu' },
  { value: 'level_3', label: 'Level 3: Cấu trúc điều khiển, hàm/method' },
  { value: 'level_4', label: 'Level 4: Luồng dữ liệu, file I/O' },
  { value: 'level_5', label: 'Level 5: Thành thạo & Tối ưu mã nguồn' },
];

const OOP_OPTIONS: DropdownOption[] = [
  { value: 'level_1', label: 'Level 1: Hiểu khái niệm cơ bản' },
  { value: 'level_2', label: 'Level 2: Cài đặt Class/Object cơ bản' },
  { value: 'level_3', label: 'Level 3: Overriding, đa hình, interface' },
  { value: 'level_4', label: 'Level 4: Ứng dụng OOP trong project nhỏ' },
  { value: 'level_5', label: 'Level 5: Thiết kế hệ thống hoàn chỉnh' },
];

const TESTING_OPTIONS: DropdownOption[] = [
  { value: 'level_1', label: 'Level 1: Tìm và sửa lỗi cú pháp' },
  { value: 'level_2', label: 'Level 2: Sửa lỗi logic, ngoại lệ' },
  { value: 'level_3', label: 'Level 3: Debugger & JUnit' },
  { value: 'level_4', label: 'Level 4: Integration test & Edge cases' },
];

const MODELING_OPTIONS: DropdownOption[] = [
  { value: 'level_1', label: 'Level 1: Đọc hiểu UML cơ bản' },
  { value: 'level_2', label: 'Level 2: Vẽ Use case, Class diagram' },
  { value: 'level_3', label: 'Level 3: Design Patterns & SOLID' },
  { value: 'level_4', label: 'Level 4: Thiết kế hệ thống phức tạp' },
];

const ABSTRACTION_OPTIONS: DropdownOption[] = [
  { value: 'level_1', label: 'Level 1: Generics & Collections cơ bản' },
  { value: 'level_2', label: 'Level 2: Wildcards và ràng buộc' },
  { value: 'level_3', label: 'Level 3: Wrapper & Container tổng quát' },
  { value: 'level_4', label: 'Level 4: Thành thạo Generics & Cấu trúc dữ liệu' },
];

export const SKILL_TREE_CONFIG: SkillCategory[] = [
  {
    id: 'syntax',
    title: 'Cú pháp và ngữ nghĩa Java',
    options: SYNTAX_OPTIONS, // 5 lựa chọn
  },
  {
    id: 'oopConcepts',
    title: 'Khái niệm và triển khai OOP',
    options: OOP_OPTIONS, // 5 lựa chọn
  },
  {
    id: 'testing',
    title: 'Gỡ lỗi và kiểm thử',
    options: TESTING_OPTIONS, // 4 lựa chọn
  },
  {
    id: 'modeling',
    title: 'Mô hình hóa và thiết kế',
    options: MODELING_OPTIONS, // 4 lựa chọn
  },
  {
    id: 'abstraction',
    title: 'Tổng quát hóa và cấu trúc dữ liệu',
    options: ABSTRACTION_OPTIONS, // 4 lựa chọn
  },
];