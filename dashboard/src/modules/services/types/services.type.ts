
export interface ServiceType {
    id: number;
    name: string;
    is_public: boolean;
    user_ids: number[];
    inbound_ids: number[];
}
