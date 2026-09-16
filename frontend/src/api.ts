const API=import.meta.env.VITE_API_URL||'http://localhost:8000/api/v1';
async function get<T>(path:string):Promise<T>{const r=await fetch(API+path);if(!r.ok)throw new Error(`API ${r.status}`);return r.json()}
export type Device={id:string;name:string;platform:string};export type Metric={timestamp:string;latency_ms:number|null;packet_loss_percent:number|null;health_score:number};export type Incident={id:number;status:string;classification:string;confidence:number;evidence:string};
export const api={devices:()=>get<Device[]>('/devices'),metrics:(id:string)=>get<Metric[]>(`/devices/${id}/metrics`),health:(id:string)=>get<{score:number}>(`/devices/${id}/health`),incidents:()=>get<Incident[]>('/incidents')};
