import axios from 'axios';
import type { Material } from '../model/material';
import { API_BASE_URL } from './constants';

const API_URL = `${API_BASE_URL}/materials`; // Replace with your actual base URL

// Fetch a Material by ID
export const getMaterial = async (id: number): Promise<Material> => {
  try {
    const response = await axios.get(`${API_URL}/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching material:', error);
    throw error;
  }
};

// Create or Update a Material (Upsert)
export const upsertMaterial = async (material: Partial<Material>): Promise<Material> => {
  try {
    const response = await axios.post(`${API_URL}/upsert/`, material);
    return response.data;
  } catch (error) {
    console.error('Error creating/updating material:', error);
    throw error;
  }
};

// Fetch all Materials
export const getAllMaterials = async (): Promise<Material[]> => {
  try {
    const response = await axios.get(`${API_URL}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching all materials:', error);
    throw error;
  }
};
