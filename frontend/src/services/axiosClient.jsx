import axios from 'axios';

export const axiosClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL, // Lấy từ biến môi trường
    headers: {
        'Content-Type': 'application/json',
    },
});

export const axiosClientFile = axios.create({
    baseURL: import.meta.env.VITE_API_URL, // Lấy từ biến môi trường
    headers: {
        'Content-Type': 'multipart/form-data',
    },
});

// export default axiosClient;