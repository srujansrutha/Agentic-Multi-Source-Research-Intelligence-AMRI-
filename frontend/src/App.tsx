import { useState } from 'react';
import ResearchForm from './components/ResearchForm';
import ReportViewer from './components/ReportViewer';
import { researchService } from './api';

export interface ResearchResult {
    report: string;
    source: string;
}

function App() {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<ResearchResult | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleResearch = async (topic: string) => {
        setLoading(true);
        setError(null);
        setResult(null);
        try {
            const data = await researchService.conductResearch(topic);
            setResult(data);
        } catch (err) {
            setError('Research failed. Please try again.');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleUpload = async (file: File) => {
        try {
            await researchService.uploadPdf(file);
            alert('PDF uploaded and indexed successfully!');
        } catch (err) {
            alert('Upload failed.');
            console.error(err);
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 flex flex-col">
            <header className="bg-white border-b border-slate-200 py-4 px-6 shadow-sm sticky top-0 z-10">
                <div className="max-w-4xl mx-auto flex items-center gap-3">
                    <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">
                        A
                    </div>
                    <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                        AMRI <span className="text-slate-400 font-normal text-sm ml-2">Agentic Multi-Source Research Intelligence</span>
                    </h1>
                </div>
            </header>

            <main className="flex-1 max-w-4xl mx-auto w-full p-6 flex flex-col gap-8">
                <div className="bg-white rounded-xl shadow-sm border border-slate-100 overflow-hidden">
                    <div className="p-1 bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 opacity-20"></div>
                    <div className="p-6">
                        <h2 className="text-lg font-semibold text-slate-800 mb-4">Start New Research</h2>
                        <ResearchForm
                            onSearch={handleResearch}
                            onUpload={handleUpload}
                            loading={loading}
                        />
                    </div>
                </div>

                {error && (
                    <div className="bg-red-50 text-red-600 p-4 rounded-lg border border-red-100 flex items-center gap-3">
                        <span className="font-medium">Error:</span> {error}
                    </div>
                )}

                {result && (
                    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <ReportViewer result={result} />
                    </div>
                )}
            </main>

            <footer className="text-center py-6 text-slate-400 text-sm">
                &copy; {new Date().getFullYear()} AMRI Research Agent
            </footer>
        </div>
    );
}

export default App;
