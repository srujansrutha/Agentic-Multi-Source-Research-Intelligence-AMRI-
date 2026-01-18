import { useState, useCallback, FC, FormEvent } from 'react';
import { useDropzone } from 'react-dropzone';
import { Search, Upload, Loader2, Sparkles, FileType } from 'lucide-react';
import { GlassCard } from './GlassCard';

interface ResearchFormProps {
    onSearch: (topic: string, enableHitl: boolean) => void;
    onUpload: (file: File) => void;
    loading: boolean;
}

const ResearchForm: FC<ResearchFormProps> = ({ onSearch, onUpload, loading }) => {
    const [topic, setTopic] = useState('');
    const [enableHitl, setEnableHitl] = useState(false);
    const [uploading, setUploading] = useState(false);

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        const file = acceptedFiles[0];
        if (file) {
            setUploading(true);
            try {
                await onUpload(file);
            } finally {
                setUploading(false);
            }
        }
    }, [onUpload]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: { 'application/pdf': ['.pdf'] },
        multiple: false
    });

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        if (topic.trim()) {
            onSearch(topic, enableHitl);
        }
    };

    return (
        <div className="w-full max-w-2xl mx-auto space-y-8">
            <GlassCard className="p-1">
                <form onSubmit={handleSubmit} className="relative group">
                    <div className="absolute inset-y-0 left-0 pl-6 flex items-center pointer-events-none">
                        <Search className="h-6 w-6 text-slate-400 group-focus-within:text-purple-400 transition-colors" />
                    </div>
                    <input
                        type="text"
                        value={topic}
                        onChange={(e) => setTopic(e.target.value)}
                        placeholder="What do you want to research today?"
                        className="w-full pl-16 pr-36 py-6 bg-transparent text-lg text-white placeholder-slate-400 focus:outline-none rounded-xl"
                        disabled={loading}
                    />
                    <div className="absolute right-2 top-2 bottom-2">
                        <button
                            type="submit"
                            disabled={loading || !topic.trim()}
                            className="h-full px-8 bg-purple-600 hover:bg-purple-500 disabled:bg-slate-700 text-white font-medium rounded-lg transition-all duration-200 shadow-lg shadow-purple-500/20 flex items-center gap-2"
                        >
                            {loading ? (
                                <Loader2 className="h-5 w-5 animate-spin" />
                            ) : (
                                <>
                                    <span>Research</span>
                                    <Sparkles className="h-4 w-4" />
                                </>
                            )}
                        </button>
                    </div>
                </form>
            </GlassCard>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* PDF Upload Card */}
                <GlassCard delay={0.1} className="relative group cursor-pointer border-dashed border-2 border-slate-700 hover:border-purple-500/50 transition-colors bg-slate-900/20">
                    <div {...getRootProps()} className="p-6 flex flex-col items-center justify-center text-center h-full min-h-[160px]">
                        <input {...getInputProps()} />
                        <div className="w-12 h-12 mb-4 rounded-full bg-slate-800 group-hover:bg-slate-700 flex items-center justify-center transition-colors">
                            {uploading ? (
                                <Loader2 className="h-6 w-6 text-purple-400 animate-spin" />
                            ) : (
                                <Upload className="h-6 w-6 text-slate-300 group-hover:text-white transition-colors" />
                            )}
                        </div>
                        {isDragActive ? (
                            <p className="text-purple-400 font-medium">Drop the intelligence here...</p>
                        ) : (
                            <>
                                <p className="text-slate-200 font-medium mb-1">Upload Internal Context</p>
                                <p className="text-sm text-slate-500">Drag & drop PDF files</p>
                            </>
                        )}
                    </div>
                </GlassCard>

                {/* Settings Card */}
                <GlassCard delay={0.2} className="p-6 flex flex-col justify-center bg-slate-900/20">
                    <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-indigo-500/10 rounded-lg">
                                <FileType className="h-5 w-5 text-indigo-400" />
                            </div>
                            <div>
                                <h3 className="text-slate-200 font-medium">Human Guidance</h3>
                                <p className="text-xs text-slate-500">Pause for approval</p>
                            </div>
                        </div>
                        <label className="relative inline-flex items-center cursor-pointer">
                            <input
                                type="checkbox"
                                checked={enableHitl}
                                onChange={(e) => setEnableHitl(e.target.checked)}
                                className="sr-only peer"
                            />
                            <div className="w-11 h-6 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-500"></div>
                        </label>
                    </div>
                    <div className="mt-3 p-3 bg-slate-800/50 rounded-lg border border-slate-700/50">
                        <div className="flex items-center justify-between text-xs text-slate-400">
                            <span>Mode</span>
                            <span className="text-purple-400 font-mono">Enterprise</span>
                        </div>
                    </div>
                </GlassCard>
            </div>
        </div>
    );
};

export default ResearchForm;
