import axios from 'axios';

// Create axios instance
const api = axios.create({
    baseURL: 'http://localhost:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const researchService = {
    conductResearch: async (topic: string) => {
        const response = await api.post('/research', { topic });
        return response.data;
    },

    uploadPdf: async (file: File) => {
        const formData = new FormData();
        formData.append('file', file);

        // Allow long timeout for large files/indexing
        const response = await api.post('/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
            timeout: 120000,
        });
        return response.data;
    },
};

export default api;
