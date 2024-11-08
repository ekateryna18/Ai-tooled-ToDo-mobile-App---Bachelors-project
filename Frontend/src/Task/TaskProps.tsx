export interface TaskProps{
    _id?: string;
    label: string;
    duration?: number;
    start_time?: number;
    end_time?: number;
    date?: string;
    completed?: boolean;
}