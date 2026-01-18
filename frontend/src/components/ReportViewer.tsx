import React from 'react';
import Markdown from 'react-markdown';
import { Zap, Layout, FileText } from 'lucide-react';
import { ResearchResult } from '../App';

interface ReportViewerProps {
    result: ResearchResult;
}

const ReportViewer: React.FC<ReportViewerProps> = ({ result }) => {
    return (
        <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
            <div className="border-b border-slate-100 bg-slate-50/50 p-4 flex items-center justify-between">
                <div className="flex items-center gap-2 text-slate-700 font-medium">
                    <FileText className="w-5 h-5 text-blue-500" />
                    Research Report
                </div>
                {result.source === 'cache' && (
                    <div className="flex items-center gap-1.5 px-3 py-1 bg-amber-50 text-amber-600 rounded-full text-xs font-medium border border-amber-100">
                        <Zap className="w-3.5 h-3.5 fill-current" />
                        Cached Result
                    </div>
                )}
            </div>

            <div className="p-8 prose prose-slate max-w-none prose-headings:font-semibold prose-h1:text-2xl prose-h2:text-xl prose-a:text-blue-600 hover:prose-a:text-blue-700 bg-white">
                <Markdown>{result.report}</Markdown>
            </div>
        </div>
    );
};

export default ReportViewer;
