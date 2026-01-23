export interface Citation {
    id: string;
    page: number | string;
    source: string;
    snippet: string;
}

export interface QAResponse {
    answer: string;
    context: string;
    citations: Record<string, Citation> | null;
}
