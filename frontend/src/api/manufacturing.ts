import type {Manufacturing, ManufacturingFormData} from "../model/manufacturing";
import axios from "axios";
import {API_BASE_URL} from "./constants";

const API_URL = `${API_BASE_URL}/manufacturing`; // Replace with your actual base URL

export const getManufacturing = async (productId: String) => {
    try {
        const response = await axios.get(`${API_URL}/${productId}/`);
        if (!response.data || response.data.length === 0) {
            return null;  // Return null when no records found
        }
        return response.data;
    } catch (error) {
        console.error('Error fetching BOM:', error);
        return null
    }
};


export const upsertManufacturing = async (productId:String, data: ManufacturingFormData): Promise<Manufacturing> => {
    try {
        const response = await axios.post(`${API_URL}/${productId}/upsert/`, data);
        return response.data;
    } catch (error) {
        console.error('Error creating/updating material:', error);
        throw error;
    }
}