import { useState, FC } from 'react';
import Markdown from 'react-markdown';
import { Zap, FileText, CheckCircle2, AlertTriangle, Play } from 'lucide-react';
import { ResearchResult } from '../App';
import { GlassCard } from './GlassCard';

interface ReportViewerProps {
    result: ResearchResult | null;
    onResume?: (feedback: string) => void;
}

const ReportViewer: FC<ReportViewerProps> = ({ result, onResume }) => {
    const [feedback, setFeedback] = useState('');

    if (!result) return null;

    const isCached = result.source === 'cache';
    const isPaused = result.status === 'paused';

    return (
        <div className="w-full max-w-4xl mx-auto space-y-6">
            <GlassCard className="border-t-4 border-t-purple-500">
                {/* Header */}
                <div className="px-8 py-6 border-b border-slate-700/50 flex items-center justify-between bg-slate-900/50">
                    <div className="flex items-center gap-3">
                        <FileText className="h-6 w-6 text-purple-400" />
                        <h2 className="text-xl font-semibold text-white">Research Intelligence</h2>
                    </div>
                    <div className="flex gap-2">
                        {isPaused && (
                            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20">
                                <AlertTriangle className="h-3.5 w-3.5" />
                                Awaiting Guidance
                            </span>
                        )}
                        {isCached && (
                            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                                <Zap className="h-3.5 w-3.5" />
                                Instant Semantic Match
                            </span>
                        )}
                        {!isCached && !isPaused && (
                            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-blue-500/10 text-blue-400 border border-blue-500/20">
                                <CheckCircle2 className="h-3.5 w-3.5" />
                                Live Verification
                            </span>
                        )}
                    </div>
                </div>

                {/* Content */}
                <div className="px-8 py-8">
                    {isPaused ? (
                        <div className="text-center py-12 space-y-6">
                            <div className="w-16 h-16 mx-auto bg-amber-500/10 rounded-full flex items-center justify-center">
                                <AlertTriangle className="h-8 w-8 text-amber-500" />
                            </div>
                            <div>
                                <h3 className="text-2xl font-bold text-white mb-2">Human Input Required</h3>
                                <p className="text-slate-400 max-w-lg mx-auto">
                                    The agent has paused execution at a breakpoint.
                                    Please provide guidance on how to proceed with the research.
                                </p>
                            </div>
                            <div className="flex max-w-lg mx-auto gap-2">
                                <input
                                    type="text"
                                    placeholder="E.g., Prioritize sources from 2024..."
                                    className="flex-1 px-4 py-3 bg-slate-900/50 border border-slate-700 rounded-lg text-white focus:border-purple-500 focus:outline-none"
                                    value={feedback}
                                    onChange={(e) => setFeedback(e.target.value)}
                                />
                                <button
                                    onClick={() => onResume && onResume(feedback || "Proceed")}
                                    className="px-6 py-3 bg-white text-slate-900 font-bold rounded-lg hover:bg-slate-200 transition-colors flex items-center gap-2"
                                >
                                    <Play className="h-4 w-4" />
                                    Resume
                                </button>
                            </div>
                        </div>
                    ) : (
                        <div className="prose prose-invert prose-lg max-w-none prose-headings:text-indigo-300 prose-a:text-purple-400 hover:prose-a:text-purple-300 prose-strong:text-white prose-blockquote:border-l-purple-500 prose-blockquote:bg-slate-800/30 prose-blockquote:py-1 prose-blockquote:px-4 prose-img:rounded-xl prose-img:shadow-2xl">
                            <Markdown>{result.report}</Markdown>
                        </div>
                    )}
                </div>
            </GlassCard>

            <div className="text-center text-slate-600 text-sm">
                Generated by AMRI Enterprise • {new Date().toLocaleDateString()}
            </div>
        </div>
    );
};

export default ReportViewer;
