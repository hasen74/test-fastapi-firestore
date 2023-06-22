export interface Snippet {
  id: string;
  title: string;
  description: string;
  content: string;
  language_id: string;
  user_email: string;
  tags_id: string[];
  createdAt: Date;
  updatedAt: Date;
}