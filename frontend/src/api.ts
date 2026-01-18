import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 120000,
});

export const conductResearch = async (topic: string, enableHitl: boolean = false) => {
    const response = await api.post('/research', { topic, enable_hitl: enableHitl });
    return response.data;
};

export const resumeResearch = async (threadId: string, feedback: string) => {
    const response = await api.post(`/research/resume/${threadId}`, null, {
        params: { feedback }
    });
    return response.data;
};

export const uploadPdf = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};
