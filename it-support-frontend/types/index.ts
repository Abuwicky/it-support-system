export interface User {
  id: number;
  username: string;
  email: string;
  role: "employee" | "it_staff" | "admin";
  full_name: string;
  department?: string;
}

export interface Ticket {
  id: number;
  title: string;
  description: string;
  category: string;
  priority: "low" | "medium" | "high" | "urgent";
  status:
    | "open"
    | "assigned"
    | "in_progress"
    | "pending_onsite"
    | "resolved"
    | "closed";
  created_by: User;
  assigned_to?: User;
  created_at: string;
  updated_at: string;
  attachments: any[];
  comments: any[];
  video_url?: string;
}
