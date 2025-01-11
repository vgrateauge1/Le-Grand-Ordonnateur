export interface Product {
  id?: number;
  name: string;
  description: string;
  creation_date: string; // ISO 8601 datetime string
  modification_date?: string; // ISO 8601 datetime string
  is_active: boolean;
}

export interface Version {
  product: number;
  version: string; // e.g., "1.0"
  retail_price: number;
  is_active: boolean;
  creation_date: string; // ISO 8601 datetime string
  modification_date: string; // ISO 8601 datetime string
}

export interface BomLine {
  material: number;
  supplier: number;
  unit_price: number;
  quantity: number;
  total?: number;
}