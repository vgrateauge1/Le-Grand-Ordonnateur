export interface Product {
  id?: number;
  name: string;
  description: string;
  retail_price: number;
  creation_date?: string; // DateTime field will be represented as a string in ISO format
  modification_date?: string; // Same as creation_date
  version: string;
  is_active: boolean;
}

interface SetActiveVersionData {
  version: string;
}