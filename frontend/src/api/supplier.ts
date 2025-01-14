import axios from 'axios';
import type { Supplier } from '../model/supplier';
import { API_BASE_URL } from './constants';

const API_URL = `${API_BASE_URL}/suppliers`; // Replace with your actual base URL

// Fetch a Supplier by ID
export const getSupplier = async (id: number): Promise<Supplier> => {
  try {
    const response = await axios.get(`${API_URL}/${id}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching supplier:', error);
    throw error;
  }
};

// Create or Update a Supplier (Upsert)
export const upsertSupplier = async (supplier: Partial<Supplier>): Promise<Supplier> => {
  try {
    const response = await axios.post(`${API_URL}/upsert/`, supplier);
    return response.data;
  } catch (error) {
    console.error('Error creating/updating supplier:', error);
    throw error;
  }
};

// Fetch all Suppliers
export const getAllSuppliers = async (): Promise<Supplier[]> => {
  try {
    const response = await axios.get(`${API_URL}/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching all suppliers:', error);
    throw error;
  }
};
