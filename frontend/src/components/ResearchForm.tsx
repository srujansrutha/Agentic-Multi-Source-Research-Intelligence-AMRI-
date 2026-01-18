import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Search, Upload, FileText, Loader2 } from 'lucide-react';

interface ResearchFormProps {
    onSearch: (topic: string) => void;
    onUpload: (file: File) => void;
    loading: boolean;
}

const ResearchForm: React.FC<ResearchFormProps> = ({ onSearch, onUpload, loading }) => {
    const [topic, setTopic] = useState('');

    const onDrop = useCallback((acceptedFiles: File[]) => {
        if (acceptedFiles.length > 0) {
            onUpload(acceptedFiles[0]);
        }
    }, [onUpload]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        maxFiles: 1,
        accept: { 'application/pdf': ['.pdf'] }
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (topic.trim()) {
            onSearch(topic);
        }
    };

    return (
        <div className="space-y-6">
            <form onSubmit={handleSubmit} className="flex gap-2">
                <input
                    type="text"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    placeholder="Enter research topic..."
                    className="flex-1 px-4 py-3 rounded-lg border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                />
                <button
                    type="submit"
                    disabled={loading || !topic.trim()}
                    className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 transition-colors"
                >
                    {loading ? (
                        <Loader2 className="w-5 h-5 animate-spin" />
                    ) : (
                        <Search className="w-5 h-5" />
                    )}
                    Research
                </button>
            </form>

            <div className="relative group">
                <div className="absolute inset-0 bg-blue-500 rounded-xl opacity-0 group-hover:opacity-5 transition-opacity pointer-events-none"></div>
                <div
                    {...getRootProps()}
                    className={`
            border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all
            ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-slate-200 hover:border-blue-400'}
          `}
                >
                    <input {...getInputProps()} />
                    <div className="flex flex-col items-center gap-3 text-slate-500">
                        <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center group-hover:bg-blue-100 group-hover:text-blue-600 transition-colors">
                            <Upload className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="font-medium text-slate-700">Upload PDF documents</p>
                            <p className="text-sm">Drag and drop or click to select</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ResearchForm;
