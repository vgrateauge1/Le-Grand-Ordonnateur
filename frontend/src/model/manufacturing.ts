export interface Step {
    id?: number;  // Optional for new steps
    name: string;
    manufacturing: number;  // Foreign key to Manufacturing
    order: number;
    estimated_time: string;  // We'll store this in minutes
}

export interface Manufacturing {
    id?: number;  // Optional for new records
    name: string;
    product: number;  // Foreign key to Product
    version: number;  // Foreign key to ProductVersion
    steps: Step[];   // Optional array of related steps
}

// For form handling, we might want a separate export interface without the IDs and relations
export interface ManufacturingFormData {
    name: string;
    steps: StepFormData[];
}

export interface StepFormData {
    name: string;
    order: number;
    estimated_time: number;
}
