import axios from 'axios';
import type {Product, Version} from "../model/products";

// Getting the API base URL from the environment variables
const API_BASE_URL = 'http://localhost:8000/api/products'; // Ensure the URL is a string

export const getAllProducts = async () : Promise<Product[]> => {
  try {
    const response = await axios.get(`${API_BASE_URL}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
    throw error;
  }
};

export const getProductById = async (id: string): Promise<Product> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching product with ID ${id}:`, error);
    throw error;
  }
};

export const upsertProduct = async (product: any) : Promise<Product> => {
  try {
    const response = await axios.post(API_BASE_URL + '/upsert/', product);
    return response.data;
  } catch (error) {
    console.error('Error creating/updating product:', error);
    throw error;
  }
};

export const deleteProduct = async (productId: number) : Promise<boolean> => {
  try {
    const response = await axios.delete(`${API_BASE_URL}/${productId}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting product:', error);
    throw error;
  }
};

export const getProductVersions = async (productId: String) : Promise<Version[]> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/versions/${productId}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting product:', error);
    throw error;
  }
};

export const upsertVersion = async (version: any) : Promise<Version> => {
  try {
    const response = await axios.post(API_BASE_URL + '/versions/upsert/', version);
    return response.data;
  } catch (error) {
    console.error('Error creating/updating product:', error);
    throw error;
  }
};