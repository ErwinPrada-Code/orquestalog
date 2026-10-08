export interface Centro {
  id: number;
  nombre: string;
  direccion: string;
}

export interface Flota {
  id: number;
  nombre: string;
  tipo: string;
  capacidad: number;
}

export type FlotaPayload = Omit<Flota, 'id'>;

export interface Ruta {
  id: number;
  origen: string;
  destino: string;
}
