import { useState } from 'react';
import ResearchForm from './components/ResearchForm';
import ReportViewer from './components/ReportViewer';
import { conductResearch, uploadPdf, resumeResearch } from './api';
import { Toaster, toast } from 'react-hot-toast';
import { BrainCircuit } from 'lucide-react';

export interface ResearchResult {
    report: string;
    source: string;
    thread_id?: string;
    status?: string; // 'completed' | 'paused'
}

function App() {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<ResearchResult | null>(null);

    const handleSearch = async (topic: string, enableHitl: boolean) => {
        setLoading(true);
        setResult(null);
        try {
            const data = await conductResearch(topic, enableHitl);
            setResult(data);
            if (data.status === 'paused') {
                toast("Research paused for your input!", { icon: '✋' });
            } else {
                toast.success("Research completed successfully!");
            }
        } catch (error) {
            console.error(error);
            toast.error("Failed to conduct research.");
        } finally {
            setLoading(false);
        }
    };

    const handleResume = async (feedback: string) => {
        if (!result?.thread_id) return;
        setLoading(true);
        try {
            const data = await resumeResearch(result.thread_id, feedback);
            setResult(data);
            toast.success("Research completed successfully!");
        } catch (error) {
            console.error(error);
            toast.error("Failed to resume research.");
        } finally {
            setLoading(false);
        }
    };

    const handleUpload = async (file: File) => {
        try {
            await uploadPdf(file);
            toast.success("PDF uploaded and indexed!");
        } catch (error) {
            console.error(error);
            toast.error("Failed to upload PDF.");
        }
    };

    return (
        <div className="min-h-screen pb-20">
            <Toaster position="top-right" toastOptions={{
                style: {
                    background: '#1e293b',
                    color: '#fff',
                }
            }} />

            {/* Header / Hero */}
            <div className="w-full pt-12 pb-12 px-4 flex flex-col items-center justify-center text-center space-y-4">
                <div className="flex items-center gap-3 mb-2">
                    <div className="p-3 bg-purple-600/20 rounded-xl">
                        <BrainCircuit className="h-8 w-8 text-purple-400" />
                    </div>
                    <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-indigo-400">
                        AMRI Enterprise
                    </h1>
                </div>
                <p className="text-slate-400 max-w-lg">
                    Agentic Multi-Source Research Intelligence.
                    <br />
                    <span className="text-slate-500 text-sm">Powered by Hybrid RAG, Semantic Caching & Vision Models.</span>
                </p>
            </div>

            <div className="container mx-auto px-4 space-y-12">
                <ResearchForm
                    onSearch={handleSearch}
                    onUpload={handleUpload}
                    loading={loading}
                />

                <ReportViewer
                    result={result}
                    onResume={handleResume}
                />
            </div>
        </div>
    );
}

export default App;
