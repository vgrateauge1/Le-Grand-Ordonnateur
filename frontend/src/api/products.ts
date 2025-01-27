import axios from 'axios';
import type {BomLine, Product, Version, Stock} from "../model/products";
import { API_BASE_URL } from './constants';

// Getting the API base URL from the environment variables
const API_URL = `${API_BASE_URL}/products`;// Ensure the URL is a string


export const getAllProducts = async () : Promise<Product[]> => {
  try {
    const response = await axios.get(`${API_URL}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
    throw error;
  }
};

// Fetch paginated products
export const getPaginatedProducts = async (page: number, size: number): Promise<{ data: Product[]; total: number }> => {
  try {
    const response = await axios.get(`${API_URL}/`, {
      params: { page, size },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching paginated products:', error);
    throw error;
  }
};

export const getActiveProducts = async (
  page: number,
  size: number,
  search?: string
): Promise<{ data: Product[]; total: number }> => {
  try {
    const response = await axios.get(`${API_URL}/active/`, {
      params: {
        page,
        size,
        search,  // <-- Pass the search parameter here
      },
    });
    return {
      data: response.data.results,
      total: response.data.count,
    };
  } catch (error) {
    console.error('Error fetching active products:', error);
    throw error;
  }
};

export const getProductById = async (id: string): Promise<Product> => {
  try {
    const response = await axios.get(`${API_URL}/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching product with ID ${id}:`, error);
    throw error;
  }
};

export const upsertProduct = async (product: any) : Promise<Product> => {
  try {
    const response = await axios.post(API_URL + '/upsert/', product);
    return response.data;
  } catch (error) {
    console.error('Error creating/updating product:', error);
    throw error;
  }
};

export const deleteProduct = async (productId: number) : Promise<boolean> => {
  try {
    const response = await axios.delete(`${API_URL}/${productId}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting product:', error);
    throw error;
  }
};

export const getProductVersions = async (productId: String) : Promise<Version[]> => {
  try {
    const response = await axios.get(`${API_URL}/versions/${productId}`);
    return response.data;
  } catch (error) {
    console.error('Error getting versions:', error);
    throw error;
  }
};

export const getStockByProductId = async (productId: number): Promise<Stock> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/product-stock/${productId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching stock for product ID ${productId}:`, error);
    throw error;
  }
};

export const updateStock = async (productId: number, quantity: number): Promise<Stock> => {
  try {
    const response = await axios.post(`${API_BASE_URL}/product-stock/`, { product: productId, quantity });
    return response.data;
  } catch (error) {
    console.error(`Error updating stock for product ID ${productId}:`, error);
    throw error;
  }
};

export const upsertVersion = async (version: Version) : Promise<Version> => {
  try {
    const response = await axios.post(API_URL + '/versions/upsert/', version);
    return response.data;
  } catch (error) {
    console.error('Error creating/updating product:', error);
    throw error;
  }
};

export const getBOM = async (productId: String) => {
  try {
    const response = await axios.get(`${API_URL}/materials/bom/${productId}/`);
    return response.data; // Return the BOM data
  } catch (error) {
    console.error('Error fetching BOM:', error);
    return []
  }
};

export const upsertBOM = async (productId: String, bomLines: BomLine[]) => {
  try {
    const response = await axios.post(`${API_URL}/materials/bom/${productId}/upsert/`, bomLines);
    return response.data; // Return the BOM data
  } catch (error) {
    console.error('Error fetching BOM:', error);
    throw error;
  }
};
