import axios from 'axios';
import type {Product} from "../model/products";

// Getting the API base URL from the environment variables
const API_BASE_URL = 'http://localhost:8000/api/products'; // Ensure the URL is a string

export const getAllProducts = async () : Promise<Product[]> => {
  try {
    const response = await axios.get(API_BASE_URL);
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

// Function to add ProductMaterial
export const addProductMaterial = async (
  productId: number,
  materialId: number,
  quantity: number,
  version: string
): Promise<ApiResponse> => {
  try {
    const response = await axios.post<ApiResponse>(`${API_BASE_URL}/${productId}/add_product_material/`, {
      material_id: materialId,
      quantity,
      version,
    });
    return response.data;
  } catch (error: any) {
    console.error('Error adding ProductMaterial:', error.response?.data || error.message);
    throw new Error(error.response?.data?.error || 'Unknown error');
  }
};



// Function to set the active version of the product
export const setActiveProductVersion = async (
  productId: number,
  version: string
): Promise<ApiResponse> => {
  try {
    const response = await axios.post<ApiResponse>(`${API_BASE_URL}/${productId}/set_active_version/`, {
      version,
    });
    return response.data;
  } catch (error: any) {
    console.error('Error setting active version:', error.response?.data || error.message);
    throw new Error(error.response?.data?.error || 'Unknown error');
  }
};
