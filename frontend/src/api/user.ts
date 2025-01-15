import axios from "axios";
import { API_BASE_URL } from "./constants";


export const connect = async (username: string, password: string, csrf:string): Promise<boolean> => {
    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        await axios.post(`${API_BASE_URL}/login/`,formData,{
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrf,  // Add CSRF token to headers
            },
            withCredentials: true,
        });
        return true;
    } catch (error) {
      console.error('Error connecting', error);
      return false;
    }
};

export const deconnect = async (csrf: string): Promise<boolean> => {
    try {
    //   await axios.post(`${API_BASE_URL}/logout/`,{
    //     headers: {
    //         'Content-Type': 'application/x-www-form-urlencoded',
    //         'X-CSRFToken': csrf,  // Add CSRF token to headers
    //     },
    //     withCredentials: true,
    //   });
      return true;
    } catch (error) {
      console.error('Error deconnecting:', error);
      return false;
    }
};

export const getCsrfToken = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/csrf-token/`);
        document.cookie = `csrftoken=${response.data.csrfToken}; path=/; secure; samesite=Lax`;
        return response.data.csrfToken;
    } catch (error) {
        console.error('Error getting csrf:', error);
        return false;
    }
}